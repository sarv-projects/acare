from silero_vad import load_silero_vad,get_speech_timestamps 
import sounddevice as sd
import numpy as np
import threading
import torch

SAMPLE_RATE = 16000
CHUNK_DURATION = 0.032
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)  # 480 samples

MIN_SPEECH_DURATION = 0.5  # Ignore very short noises
SILENCE_TIMEOUT = 0.8      # Much faster response time

model = load_silero_vad()

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
            prob = model(torch.FloatTensor(audio_tensor), SAMPLE_RATE).item()
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

        # If the incoming buffer contains multiple CHUNK_SIZE frames,
        # split it into fixed-size subchunks so VAD processing stays aligned.
        n = len(chunk)
        if n == CHUNK_SIZE:
            self.process_chunk(chunk)
            if self.asr_client and not self.streaming_paused:
                self.asr_client.send_chunk(chunk)
            return

        if n % CHUNK_SIZE == 0:
            # Process each subchunk sequentially
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
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype='float32',
                # Use a slightly larger block to reduce input-overflow risk
                # while still processing fixed-size VAD chunks below.
                blocksize=CHUNK_SIZE * 2,
                callback=self._sd_callback
            ):
                while self.is_listening:
                    sd.sleep(100)
        except Exception as e:
            print(f"[VAD] Fatal Error: {e}")

    def stop(self):
        self.is_listening = False