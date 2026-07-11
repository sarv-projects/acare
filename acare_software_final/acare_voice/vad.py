from silero_vad import load_silero_vad,get_speech_timestamps 
import sounddevice as sd
import numpy as np
import threading
import torch

# Pipeline sample rate — Silero VAD, Deepgram ASR, ECAPA-TDNN all expect 16kHz.
# Some USB mics (e.g. TI PCM2902 in the MI-305) only support 44100/48000 Hz
# natively. When PortAudio can't open the device at 16kHz we record at the
# device's default rate and downsample in the callback.
TARGET_RATE = 16000
CHUNK_DURATION = 0.032
CHUNK_SIZE = int(TARGET_RATE * CHUNK_DURATION)  # 480 samples at 16kHz

MIN_SPEECH_DURATION = 0.5
SILENCE_TIMEOUT = 0.8

model = load_silero_vad()


def _probe_device_rate():
    """Return a sample rate PortAudio can actually open for the default input device."""
    try:
        dev_info = sd.query_devices(kind='input')
        default_rate = int(dev_info['default_samplerate'])
        # Quick test: can we open a stream at 16 kHz?
        test_stream = sd.InputStream(samplerate=TARGET_RATE, channels=1, dtype='float32')
        test_stream.close()
        return TARGET_RATE, 1.0
    except Exception:
        # 16 kHz failed — fall back to the device's native rate
        pass
    try:
        dev_info = sd.query_devices(kind='input')
        native_rate = int(dev_info['default_samplerate'])
        if native_rate <= 0:
            native_rate = 44100
    except Exception:
        native_rate = 44100
    ratio = native_rate / TARGET_RATE
    print(f"[VAD] Device doesn't support {TARGET_RATE}Hz — recording at {native_rate}Hz "
          f"(resample ratio {ratio:.2f}x)")
    return native_rate, ratio


def _resample_chunk(chunk_1d: np.ndarray, src_rate: int, tgt_rate: int) -> np.ndarray:
    """Downsample float32 mono audio using scipy's Fourier method if available,
    otherwise a lightweight polyphase approximation."""
    if src_rate == tgt_rate:
        return chunk_1d.astype(np.float32).copy()
    try:
        from scipy.signal import resample
        target_len = max(1, int(len(chunk_1d) * tgt_rate / src_rate))
        return resample(chunk_1d.astype(np.float64), target_len).astype(np.float32)
    except ImportError:
        pass
    # Fallback: simple decimation with linear interpolation for non-integer ratios
    factor = tgt_rate / src_rate
    src_n = len(chunk_1d)
    tgt_n = max(1, int(src_n * factor))
    src_indices = np.linspace(0, src_n - 1, tgt_n)
    lo = np.floor(src_indices).astype(int)
    hi = np.minimum(lo + 1, src_n - 1)
    frac = src_indices - lo.astype(float)
    return ((1.0 - frac) * chunk_1d[lo] + frac * chunk_1d[hi]).astype(np.float32)


class VADListener:
    def __init__(self, asr_client=None):
        self.speech_buffer = []
        self.asr_client = asr_client
        self.silence_duration = 0.0
        self.speech_duration = 0.0
        self.is_listening = False
        self.callback = None
        self.streaming_paused = False
        self._flushing = False

        # Device rate detection
        self._hw_rate, self._rate_ratio = _probe_device_rate()
        # blocksize at hw rate that yields ~32 ms worth of samples
        self._hw_blocksize = max(
            int(self._hw_rate * CHUNK_DURATION),
            CHUNK_SIZE,
        )

    def process_chunk(self, chunk):
        audio_tensor = np.array(chunk, dtype=np.float32)
        
        if len(audio_tensor) != CHUNK_SIZE or not np.isfinite(audio_tensor).all():
            if self.speech_duration > 0:
                self.speech_buffer.append(chunk)
                self.speech_duration += CHUNK_DURATION
            else:
                self.silence_duration += CHUNK_DURATION
            return
        
        try:
            prob = model(torch.FloatTensor(audio_tensor), TARGET_RATE).item()
            speech = prob > 0.5
        except Exception:
            speech = False

        if speech:
            self.silence_duration = 0.0
            self.speech_duration += CHUNK_DURATION
            self.speech_buffer.append(chunk)
        else:
            self.silence_duration += CHUNK_DURATION
            if self.speech_duration > 0:
                self.speech_buffer.append(chunk)

            if self.silence_duration >= SILENCE_TIMEOUT:
                if self.speech_duration >= MIN_SPEECH_DURATION:
                    self._flush()
                else:
                    self._reset()

    def _flush(self):
        if self._flushing:
            return
        self._flushing = True
        try:
            if self.speech_buffer and self.callback:
                audio = np.concatenate(self.speech_buffer)
                self.callback(audio)
        finally:
            self._reset()
            self._flushing = False

    def _reset(self):
        self.speech_buffer = []
        self.silence_duration = 0.0
        self.speech_duration = 0.0

    def _sd_callback(self, indata, frames, time, status):
        if status:
            print(f"[VAD] SoundDevice Status: {status}")
        chunk = indata[:, 0]

        # Resample from hardware rate -> 16 kHz if needed
        if self._hw_rate != TARGET_RATE:
            chunk = _resample_chunk(chunk, self._hw_rate, TARGET_RATE)

        # Split into fixed-size VAD chunks
        n = len(chunk)
        if n == CHUNK_SIZE:
            self.process_chunk(chunk)
            if self.asr_client and not self.streaming_paused:
                self.asr_client.send_chunk(chunk)
            return

        if n % CHUNK_SIZE == 0:
            for i in range(0, n, CHUNK_SIZE):
                sub = chunk[i:i+CHUNK_SIZE]
                self.process_chunk(sub)
                if self.asr_client and not self.streaming_paused:
                    self.asr_client.send_chunk(sub)
            return

        # Fallback for non-aligned sizes
        self.process_chunk(chunk)
        if self.asr_client and not self.streaming_paused:
            self.asr_client.send_chunk(chunk)
    
    def pause_streaming(self):
        self.streaming_paused = True
    
    def resume_streaming(self):
        self.streaming_paused = False

    def start(self, callback):
        self.callback = callback
        self.is_listening = True
        try:
            with sd.InputStream(
                samplerate=self._hw_rate,
                channels=1,
                dtype='float32',
                blocksize=self._hw_blocksize,
                callback=self._sd_callback
            ):
                while self.is_listening:
                    sd.sleep(100)
        except Exception as e:
            print(f"[VAD] Fatal Error: {e}")

    def stop(self):
        self.is_listening = False