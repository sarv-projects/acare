from silero_vad import load_silero_vad,get_speech_timestamps 
import sounddevice as sd
import numpy as np
import threading
import torch

SAMPLE_RATE = 16000
CHUNK_DURATION = 0.032
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)

MIN_SPEECH_DURATION = 0.5
SILENCE_TIMEOUT = 0.8
MAX_UTTERANCE_DURATION = 8.0

_model = None

def _get_vad_model():
    global _model
    if _model is None:
        _model = load_silero_vad()
    return _model

class VADListener:
    def __init__(self, asr_client=None):
        self.model = _get_vad_model()
        self.speech_buffer = []
        self.asr_client = asr_client
        self.silence_duration = 0.0
        self.speech_duration = 0.0
        self.is_listening = False
        self.callback = None
        self.streaming_paused = False
        self._chunk_count = 0
        self._speech_detected = False

    def process_chunk(self, chunk):
        audio_tensor = np.array(chunk, dtype=np.float32)
        audio_tensor = audio_tensor - np.mean(audio_tensor)
        peak = abs(audio_tensor).max() if len(audio_tensor) else 0.0
        if peak > 1.0:
            audio_tensor = audio_tensor / peak

        if len(audio_tensor) != CHUNK_SIZE or not np.isfinite(audio_tensor).all():
            if self.speech_duration > 0:
                self.speech_buffer.append(chunk)
                self.speech_duration += CHUNK_DURATION
            else:
                self.silence_duration += CHUNK_DURATION
            return

        try:
            prob = self.model(torch.FloatTensor(audio_tensor), SAMPLE_RATE).item()
            speech = prob > 0.5
        except Exception:
            speech = False

        if speech:
            if not self._speech_detected:
                self._speech_detected = True
                print(f"[VAD] Speech detected (prob={prob:.3f})")
            self.silence_duration = 0.0
            self.speech_duration += CHUNK_DURATION
            self.speech_buffer.append(chunk)
            if self.speech_duration >= MAX_UTTERANCE_DURATION:
                self._flush()
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
        if self.speech_buffer and self.callback:
            print(f"[VAD] Utterance complete — {self.speech_duration:.2f}s, flushing to ASR")
            audio = np.concatenate(self.speech_buffer)
            self.callback(audio)
        self._reset()
        self._speech_detected = False

    def _reset(self):
        self.speech_buffer = []
        self.silence_duration = 0.0
        self.speech_duration = 0.0

    def _sd_callback(self, indata, frames, time, status):
        if status:
            print(f"[VAD] SoundDevice Status: {status}")
        chunk = indata[:, 0]

        self._chunk_count += 1
        if self._chunk_count % 94 == 0:
            state = "PAUSED" if self.streaming_paused else "STREAMING"
            centered = chunk - np.mean(chunk)
            rms = np.sqrt(np.mean(centered.astype(np.float64)**2))
            print(f"[VAD] Mic active ({state}) — {self._chunk_count} chunks, RMS={rms:.6f}")

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

        self.process_chunk(chunk)
        if self.asr_client and not self.streaming_paused:
            self.asr_client.send_chunk(chunk)

    def pause_streaming(self):
        self.streaming_paused = True
        if self.asr_client:
            self.asr_client.start_keepalive()

    def resume_streaming(self):
        self.streaming_paused = False
        self._reset()
        self._speech_detected = False
        if self.asr_client:
            self.asr_client.stop_keepalive()

    def start(self, callback):
        self.callback = callback
        self.is_listening = True
        try:
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype='float32',
                blocksize=CHUNK_SIZE,
                callback=self._sd_callback
            ):
                while self.is_listening:
                    sd.sleep(100)
        except Exception as e:
            print(f"[VAD] Fatal Error: {e}")

    def stop(self):
        self.is_listening = False
        try:
            sd.stop()
        except Exception:
            pass
