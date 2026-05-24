# Tech Stack

## Runtime
- Python 3.11+ (both sub-projects)
- Package manager: `uv` (lockfile-based, `uv.lock` present in each sub-project)

## acarevoice — Voice Pipeline

### AI / ML
- **Deepgram Nova-2** — streaming STT via WebSocket (`deepgram-sdk==3.10.1`), language `en-IN`
- **Groq (Llama 3.1 8B Instant)** — intent parsing and assistant agent (`groq>=1.0.0`)
- **Silero VAD v5** — client-side voice activity detection (`silero-vad>=6.2.1`)

### Audio
- `sounddevice` — mic input / audio I/O
- `soundfile` — audio file handling
- `pygame` — MP3 playback for edge-tts output
- `edge-tts` — primary TTS (Azure Neural voices, free, no key)
- `pyttsx3` — fallback/emergency TTS (offline, instant)

### Other Dependencies
- `numpy` — audio buffer manipulation
- `torch` / `torchaudio` — Silero VAD inference
- `python-dotenv` — `.env` loading for API keys

### Required Environment Variables (`.env`)
```
DEEPGRAM_API_KEY=...
GROQ_API_KEY=...
```

## acare_camera_test — Camera SDK Tests
- `opencv-python` — image processing
- `numpy` — array ops
- Native DLLs: `AngstrongCameraSdk.dll`, `alg_kunlun.dll`, etc. (Windows-only)

## Future Stack (ROS2 — not yet in repo)
- ROS2 (target: Humble or Iron) on Raspberry Pi 5
- `acare_msgs` custom message package
- YOLOv11 TFLite INT8 — vision inference
- SpeechBrain — speaker verification
- LangGraph — dialogue node
- SQLite — audit logging
- C++ — `embedded_interface_node` (CAN/UART bridge)

---

## Common Commands

### Setup
```bash
# Install dependencies (run inside acarevoice/ or acare_camera_test/)
uv sync
```

### Run Voice Pipeline
```bash
cd acarevoice
python main.py
```

### Test Individual Modules
```bash
cd acarevoice
python -m voice.tts
python -m voice.normaliser
python -m voice.alias_expansion
```

### Run Diagnostics
```bash
cd acarevoice
python -m pytest tests/test_pipeline.py -v
# or directly:
python tests/test_pipeline.py
```

### List Available TTS Voices
```bash
edge-tts --list-voices
```
