import numpy as np
import sounddevice as sd
import threading
import time

SAMPLE_RATE = 16000

def _generate_beep(freq=880, duration=0.15, volume=0.3, fade=True):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(2 * np.pi * freq * t) * volume
    if fade:
        fade_len = int(SAMPLE_RATE * 0.02)
        wave[:fade_len] *= np.linspace(0, 1, fade_len)
        wave[-fade_len:] *= np.linspace(1, 0, fade_len)
    return wave.astype(np.float32)

def _generate_ding(freq=1200, duration=0.3, volume=0.25):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = (np.sin(2 * np.pi * freq * t) * 0.6 +
            np.sin(2 * np.pi * freq * 1.5 * t) * 0.3 +
            np.sin(2 * np.pi * freq * 2 * t) * 0.1) * volume
    decay = np.exp(-t * 8)
    wave *= decay
    return wave.astype(np.float32)

def _generate_chime(freqs=[523, 659, 784], duration=0.4, volume=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.zeros_like(t)
    for i, freq in enumerate(freqs):
        offset = i * 0.08
        mask = t >= offset
        partial = np.zeros_like(t)
        partial[mask] = np.sin(2 * np.pi * freq * (t[mask] - offset)) * volume * 0.4
        decay = np.exp(-(t - offset) * 6)
        decay[t < offset] = 0
        partial *= decay
        wave += partial
    return wave.astype(np.float32)

def _generate_error_buzz(freq=200, duration=0.4, volume=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(2 * np.pi * freq * t) * volume
    wave += np.random.normal(0, 0.05, len(t))
    wave *= (0.5 + 0.5 * np.sin(2 * np.pi * 8 * t))
    return wave.astype(np.float32)

_EARCONS = {
    "listen_start": _generate_beep(freq=1200, duration=0.1, volume=0.2),
    "listen_end": _generate_beep(freq=600, duration=0.1, volume=0.2),
    "turn_ready": _generate_ding(freq=1000, duration=0.25, volume=0.2),
    "confirm": _generate_chime(volume=0.2),
    "error": _generate_error_buzz(),
    "estop": _generate_beep(freq=440, duration=0.5, volume=0.4),
    "barge_in": _generate_beep(freq=1500, duration=0.08, volume=0.15),
}

_lock = threading.Lock()

def play_earcon(name: str, blocking: bool = False):
    with _lock:
        if name not in _EARCONS:
            print(f"[Earcons] Unknown earcon: {name}")
            return
        wave = _EARCONS[name]
        try:
            if blocking:
                sd.play(wave, SAMPLE_RATE)
                sd.wait()
            else:
                sd.play(wave, SAMPLE_RATE)
        except Exception as e:
            print(f"[Earcons] Play error: {e}")

def play_listen_start():
    play_earcon("listen_start")

def play_turn_ready():
    play_earcon("turn_ready")

def play_confirm():
    play_earcon("confirm")

def play_error():
    play_earcon("error")

def play_estop():
    play_earcon("estop", blocking=True)

def play_barge_in():
    play_earcon("barge_in")
