# Communication Signals Analyzer

An AI-powered **communication signals analyzer** that records
your speech and provides a structured score based on voice
delivery, body language, and communication quality.

## What it does
- Records audio + webcam for a set duration
- Analyzes: speaking speed, pauses, filler words, voice energy
- Analyzes: eye contact, head movement, facial expressions
- Transcribes speech and gives structured NLP feedback
- Outputs an overall Communication Signals Score (0-100)

## Research Foundation
Scoring is grounded in peer-reviewed research:
- Aucouturier et al. (2015) — vocal confidence cues
- Brennan & Williams (1995) — filler words and credibility
- PMC (2024) — amplitude and speaking rate as confidence signals
- Compton et al. (2018) — nonverbal communication scoring

## Tech Stack
Python · OpenCV · MediaPipe · Whisper (OpenAI) ·
librosa · sounddevice · soundfile · Flask · OpenAI API 

## Project Status
| Phase | Status |
|-------|--------|
| Phase 1: Python core + recording | ✅ complete |
| Phase 2: Audio analysis | ✅ complete  |
| Phase 3: Computer vision | 🔧 In progress |
| Phase 4: NLP + scoring | ⏳ Not started |
| Phase 5: Web interface | ⏳ Not started |

## Setup
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

## Built by
Palak — learning and building simultaneously.

Started: June 26, 2026