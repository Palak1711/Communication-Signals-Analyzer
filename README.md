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

## Known Limitations
- Speech-to-text uses Whisper's "base" model — accuracy decreases for
  proper nouns (names) and fast speech. A larger model would improve
  this at the cost of processing speed.
- Eye contact is measured via eyelid landmark position, not true
  iris/gaze tracking — it cannot distinguish "head tilted down" from
  "eyes cast down while head stays still."
- Blink detection tracks only the left eye as a simplification.
- Body language research this scoring is based on carries a Western
  cultural bias — eye contact and pacing norms vary across cultures.
- The overall scoring weights are transparent design decisions
  grounded in research, not a peer-reviewed formula — see project
  documentation for full reasoning.
- No hand-occlusion detection yet — a hand covering the face during
  gestures can temporarily affect eye contact/head stability accuracy.

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