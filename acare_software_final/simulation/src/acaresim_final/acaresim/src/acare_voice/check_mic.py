"""Diagnostic: capture 3s of audio and analyze it."""
import sounddevice as sd
import numpy as np

sr = 16000
duration = 3
print(f"Recording {duration}s of audio... (don't speak)")
rec = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
sd.wait()

audio = rec[:, 0]
rms = np.sqrt(np.mean(audio**2))
peak = abs(audio).max()
print(f"\nRMS = {rms:.6f}")
print(f"Peak = {peak:.6f}")
print(f"Min = {audio.min():.6f}")
print(f"Max = {audio.max():.6f}")

# Frequency analysis
fft = np.fft.rfft(audio * np.hanning(len(audio)))
freq = np.fft.rfftfreq(len(audio), 1/sr)
mag = np.abs(fft)
dominant_freq = freq[np.argmax(mag)]
print(f"\nDominant frequency: {dominant_freq:.1f} Hz")

# If dominant freq is 50/60/100/120 Hz = electrical hum
# If dominant freq is 200-500 Hz = fan noise
# If dominant freq is 300-3000 Hz = speech/voice
if dominant_freq < 80:
    print(">>> Likely: Electrical hum (50/60Hz) or DC offset")
elif dominant_freq < 200:
    print(">>> Likely: Fan noise or mechanical vibration")
elif dominant_freq < 1000:
    print(">>> Likely: Ambient noise/rumble")
else:
    print(">>> Could be: Voice/speech or high-frequency noise")

print("\nSilence check:")
if rms < 0.01:
    print(f"  RMS={rms:.6f} → Normal silence (good)")
elif rms < 0.05:
    print(f"  RMS={rms:.6f} → Slightly noisy (could work)")
else:
    print(f"  RMS={rms:.6f} → VERY NOISY! Mic gain too high or feedback loop!")
    print("  Fix: pavucontrol → Input Devices → reduce Internal Mic volume to ~10%")
