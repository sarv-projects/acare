# Project Structure

## Top-Level Layout
```
/
├── acarevoice/          # Standalone voice pipeline (primary active codebase)
├── acare_camera_test/   # Camera SDK integration tests (Windows-only, DLL-dependent)
├── dia/                 # Architecture/state machine diagrams (PNG reference images)
└── acare.txt            # Project notes
```

## acarevoice/
```
acarevoice/
├── main.py              # Entry point — instantiates VoiceNode and runs standalone loop
├── voice/               # Core pipeline package
│   ├── voice_node.py    # Master controller: audio state machine, pipeline orchestration
│   ├── asr.py           # Deepgram Nova-2 streaming WebSocket client
│   ├── vad.py           # Silero VAD — 32ms chunks, speech/silence detection
│   ├── tts.py           # Dual TTS: edge-tts (normal) + pyttsx3 (urgent/fallback)
│   ├── intent_parser.py # Groq LLM intent extraction → structured JSON
│   ├── normaliser.py    # Text cleaning: lowercase, filler strip, punctuation removal
│   ├── alias_expansion.py # Alias → canonical tool mapping (e.g. "blade" → "scalpel")
│   ├── keyword_monitor.py # Always-on ESTOP keyword thread, 100ms collision window
│   └── assistant_agent.py # Groq conversational agent for LOGGED_OUT state
├── tests/
│   ├── test_pipeline.py    # Component diagnostics (imports, env vars, audio, APIs)
│   ├── test_camera.py
│   ├── test_live_app.py
│   └── test_runtime_issues.py
├── .env                 # API keys (DEEPGRAM_API_KEY, GROQ_API_KEY) — not committed
├── pyproject.toml       # uv project config + dependencies
└── acare_spec.md        # Full system specification (2000+ lines, authoritative reference)
```

## acare_camera_test/
```
acare_camera_test/
├── main.py              # Camera test entry point
├── camera_test.py       # SDK integration tests
├── hp60c_test.py        # HP60C-specific tests
├── configurationfiles/  # Per-camera JSON config files (encrypted)
├── *.dll / *.lib        # Native Windows camera SDK binaries
└── pyproject.toml
```

---

## Architecture Patterns

### Voice Pipeline Data Flow
```
Mic → VAD (Silero) → ASR chunks → Deepgram WebSocket
                                        ↓
                              Final transcript
                                        ↓
                         normalise → alias_expand → parse_intent (Groq)
                                        ↓
                              on_intent_resolved callback
```

### State Machines
- `AudioState` (in `voice_node.py`): `IDLE → LISTENING → TRANSCRIBING → SPEAKING → ESTOP_LISTEN`
- `RobotState` (in `voice_node.py`): `LOGGED_OUT → STANDBY → LISTENING → PROCESSING → EXECUTING → HOLDING → HANDOVER → ESTOP`
- Full global state machine (ROS2 `state_manager`) is defined in `acare_spec.md` Section VI

### Module Responsibilities — One Concern Per File
Each file in `voice/` owns exactly one concern. Do not add cross-cutting logic to a module that doesn't own it. Route new concerns to the appropriate existing module or create a new one.

### Spec References
Every module that maps to a spec section includes a `Spec Reference: Section X` comment at the top. When modifying a module, check `acare_spec.md` for the corresponding section to understand constraints and requirements.

### Safety Rules (Non-Negotiable)
- ESTOP keyword detection runs on a dedicated always-on thread — never block or slow this path
- `speak_urgent()` uses `pyttsx3` (offline, instant) — never `edge-tts` for emergency speech
- Logout must be rejected when `RobotState` is `EXECUTING`, `HOLDING`, or `HANDOVER`
- All API calls (Deepgram, Groq) must have `try/except` with graceful fallback

### Valid Tool Names
The canonical tool list is defined in `intent_parser.py` and mirrored in `normaliser.py`:
`scalpel, scissors, forceps, bandage, gauze, thermometer, oximeter, plaster`
Any new tool must be added to both files and the Groq system prompt.
