# ACARE: Autonomous Clinical Assistance Robot (Voice Module)

ACARE is a robotic assistant designed for clinical environments, specializing in fetching surgical tools via voice commands. This repository contains the **Voice Module**, which handles the complete audio-to-intent pipeline.

---

## 🛠️ Project Structure & File Map

All core logic is located in the `voice/` package:

| File | Purpose | Key Technology |
| :--- | :--- | :--- |
| **`main.py`** | **Entry Point** | Standalone Orchestration |
| `voice/voice_node.py` | **Master Controller** | Audio State Machine & Pipeline Logic |
| `voice/asr.py` | Real-time Transcription | Deepgram Nova-2 (Streaming) |
| `voice/tts.py` | Dual-Engine Speech | **edge-tts** (Neural) & **pyttsx3** (Safety) |
| `voice/vad.py` | Human Speech Detection | Silero VAD (v5) |
| `voice/intent_parser.py`| Command Understanding | Groq (Llama 3 8B) |
| `voice/normaliser.py` | Text Cleaning | Regex-based sanitization |
| `voice/alias_expansion.py`| Tool Mapping | Alias matching (e.g., "blade" → "scalpel") |
| `voice/keyword_monitor.py`| Emergency Monitoring | 100ms Collision Window Listener |
| `voice/assistant_agent.py`| Conversational AI | LOGGED_OUT mode (Assistant guidance) |

---

## ✨ Features Implemented (Done)

- [x] **Dual TTS Architecture**: 
  - **Normal**: Premium Azure Neural via `edge-tts` (completely free, no key needed).
  - **Emergency**: Instant `pyttsx3` offline speech for ESTOP/URGENT alerts.
- [x] **High-Speed ASR**: Real-time streaming from Deepgram with partial transcript handling.
- [x] **Safety First**: Dedicated emergency keyword thread that triggers `<200ms` ESTOP.
- [x] **Intelligent Parsing**: Validates intents with JSON schema enforcement via Groq.
- [x] **Clinical Logic**:
  - Alias expansion for surgical tools.
  - Multi-tool detection (prevents robot from grabbing two things at once).
  - Logged-out assistant mode for auth guidance.

---

## 🚀 How to Run

### 1. Setup Environment
Ensure your `.env` file contains:
* `DEEPGRAM_API_KEY`
* `GROQ_API_KEY`

Sync dependencies using `uv`:
```powershell
uv sync
```

### 2. Execute System
Launch the full standalone voice pipeline:
```powershell
python main.py
```

### 3. Interactive Commands
Once running, type these into the terminal to simulate robot states:
* `login`: Starts the surgical command session.
* `logout`: Returns to assistant guidance.
* `estop`: Forces an emergency stop.
* `resume`: Resets to standby.
* `quit`: Clean shutdown.

---

## 🎙️ Changing the Voice

We use **edge-tts** for natural speech. You can change the robot's personality in `voice/tts.py` on **Line 116**.

| Feature | Voice Name | Description |
| :--- | :--- | :--- |
| **Neutral Robotic** | `en-US-AvaNeural` | **(Current)** Clean, standard AI tone. |
| **Sophisticated** | `en-GB-SoniaNeural` | Crisp British tone, very clear. |
| **Friendly Male** | `en-US-AndrewNeural` | Calm, helpful assistant. |
| **Regional (IN)** | `en-IN-NeerjaNeural` | Natural Indian-English female tone. |

**To change:** Edit `voice/tts.py`:
```python
# Line 116
voice = "en-US-AvaNeural" 
```
You can also use `edge-tts --list-voices`  command in the terminal to list all other available voices.

---

## 🧪 Testing Sub-Modules
You can test components individually:
* **TTS Test**: `python -m voice.tts`
* **Normaliser Test**: `python -m voice.normaliser`
* **Alias Test**: `python -m voice.alias_expansion`
