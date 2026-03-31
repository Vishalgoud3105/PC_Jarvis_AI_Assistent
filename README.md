# 🧠PC Jarvis AI Assistant🤖

> **Version 1.9.0** · Windows · Python 3.11 · SAPI5 TTS · Groq LLM · NewsAPI + RSS

A fully offline-capable, voice-controlled personal assistant built for Windows. Jarvis wakes on a double clap, greets you, reads a categorized AI-curated news briefing, and lets you control your PC workflow with finger snaps and voice keywords — all hands-free.

---

## Demo Flow

```
Double clap  →  Boot sequence + rock guitar intro
Say "wake up"  →  Greeting + auto news briefing (morning/night aware)
Snap + keyword  →  Task groups: WORK | CHILL | MESSAGES | BREAK | TODAY
Snap + "SKIP"  →  Pause news mid-briefing, dump full report + open all tabs
Snap + "CONTINUE"  →  Resume from exact left-off point with recall
Snap + "READ"  →  Replay last completed briefing
Snap + "NEW"  →  Fetch fresh news anytime, N times a day
Triple clap  →  Exit chill mode
Say "that's all for today"  →  Kill all apps and close everything
```

---

## Features

### Acoustic Wake System
- **Double clap** to boot — detected via PyAudio FFT analysis, no hotword cloud service needed
- **Finger snap** to trigger task commands in snapby mode
- **Triple clap** to exit chill mode while watching anime/movies without touching the keyboard
- All acoustic detection is purely local — no audio sent anywhere

### Smart News Briefing
- **Morning (5am–12pm):** Pulls last 24hrs from NewsAPI across 30 articles
- **Afternoon/Evening/Night:** Pulls live RSS feeds from TechCrunch, Ars Technica, The Verge, VentureBeat, NASA, SpaceX, CoinDesk, Anthropic, OpenAI, DeepMind and more
- Groq LLM (`llama-4-scout-17b-16e-instruct`) categorizes and rewrites news in BroCode personality — casual, punchy, opinionated
- **9 categories:** AI & ML · Chips & Hardware · Space & Science · Stocks & Crypto · Cybersecurity · Biotech & BCI · Cloud · Newsletter Picks · General & Trending
- Each category has an AI-generated bro-style intro and outro
- Opens source tabs and YouTube deep-dive searches automatically on completion

### News Interruption System
- **Snap during 1.5s silence gap** between sentences to pause news
- Say **SKIP** → saves position, dumps full report to terminal, opens all source + YouTube tabs
- Say **CONTINUE** (snap + keyword) → recalls the last news heard, resumes from exact left-off item
- Say **READ** (snap + keyword) → replays the last completed briefing from the beginning
- Say **NEW** (snap + keyword) → fetches a completely fresh briefing at any time of day

### Task Groups (Snap + Keyword)
| Keyword | Action |
|---|---|
| **WORK** | Opens VSCode, Claude desktop, WhatsApp, Gemini, Gmail, new Chrome tab |
| **CHILL** | Opens YouTube (personal profile), AnimeSuge, ToonStream, FlixerSH |
| **MESSAGES** | Opens Instagram, WhatsApp |
| **BREAK** | Minimizes all windows (Win+D) |
| **TODAY** / "that's all for today" | Kills Chrome, WhatsApp, Claude; protects VSCode; says goodbye |

### Evening Briefing
- Automatically offers an RSS-based evening briefing once per session between 9–11pm IST
- Fires exactly once — won't repeat on every snap cycle

### False Trigger Prevention
- Mic is **completely OFF** while Jarvis is speaking — eliminates Windows audio loopback false snaps
- Snap detection only runs in the **silence gap after each sentence**
- FFT ratio filter: snap energy (3500–8000Hz) must exceed ratio threshold of 3.5 — speech/music tops out at ~2.5
- 2-consecutive-chunk confirmation required — filters single-frame plosive spikes

---

## Project Structure

```
Wakeup_Jarvis/
├── jarvis.py              # Main script — all logic in one file
├── requirements.txt       # Python dependencies
├── assets/
│   └── rock_guiter.mp3   # Boot intro audio
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/Wakeup_Jarvis.git
cd Wakeup_Jarvis
```

### 2. Create and activate a virtual environment

```bash
python -m venv Jarvis
Jarvis\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API keys

Open `jarvis.py` and fill in your keys at the top:

```python
NEWS_API_KEY = "your_newsapi_key_here"
GROQ_API_KEY = "your_groq_key_here"
```

- **NewsAPI** — free tier at [newsapi.org](https://newsapi.org) (100 requests/day)
- **Groq** — free tier at [console.groq.com](https://console.groq.com) (generous daily token limit)

> **Security note:** Never commit your API keys to a public repo. Use environment variables or a `.env` file with `python-dotenv` for production use.

### 5. Add boot audio

Place your boot sound file at `assets/rock_guiter.mp3` (any MP3 works — the filename is intentional).

### 6. Run

```bash
python jarvis.py
```

---

## Requirements

```
pyttsx3
pyaudio
numpy
SpeechRecognition
requests
feedparser
groq
pyautogui
pygame
```

**System requirements:**
- Windows 10/11 (SAPI5 TTS is Windows-only)
- Python 3.11
- A microphone
- Google Chrome installed at the default path
- Internet connection for news fetch and Google STT

---

## Hardware Tested On

| Component | Spec |
|---|---|
| Laptop | ASUS VivoBook 14 Flip |
| CPU | Intel Core Ultra 5 226V (Lunar Lake) |
| GPU | Intel Arc 130V iGPU |
| RAM | 16GB |
| OS | Windows 11 |

---

## How Snap Detection Works

Jarvis uses PyAudio to read raw microphone input and NumPy FFT to analyze frequency content in real time. A finger snap produces a short percussive burst with most energy above 3500Hz. Human speech and music have their energy concentrated in 300–3000Hz. The detector computes the ratio of high-frequency energy to low-frequency energy. Values above 3.5 with 2 consecutive confirming chunks are classified as a snap.

The mic only opens **after** each TTS sentence finishes and stays open for 1.5 seconds. This completely prevents the assistant from detecting its own speaker output as a snap — which was the primary false-trigger issue on laptop hardware with close mic-speaker proximity.

---

## Snap Command Reference

| Command | Trigger | What it does |
|---|---|---|
| Boot | Double clap | Starts Jarvis |
| Wake | Say "wake up" | Greeting + auto news |
| Skip boot | Say "skip" | Jump straight to snapby |
| WORK | Snap + "work" | Opens work apps |
| CHILL | Snap + "chill" | Opens entertainment sites |
| MESSAGES | Snap + "messages" | Opens chat apps |
| BREAK | Snap + "break" | Minimizes everything |
| TODAY | Snap + "today" | Kills all apps, goodbye |
| NEW | Snap + "new" | Fetches fresh news now |
| READ | Snap + "read" | Replays last briefing |
| CONTINUE | Snap + "continue" | Resumes interrupted news |
| SKIP | Snap during news + "skip" | Stops news, opens all tabs |
| Exit chill | Triple clap | Minimizes chill windows |

---

## Roadmap

- [ ] Send WhatsApp/Gmail messages via voice
- [ ] Full PC control handover to AI (open apps, manage files)
- [ ] Calendar and reminder integration
- [ ] Multi-language support for commands
- [ ] Custom wake word training
- [ ] Mobile companion app

---

## License

MIT License — do whatever you want with it, just don't sell it as-is.

---

## Acknowledgements

- [Groq](https://groq.com) for blazing fast LLM inference
- [NewsAPI](https://newsapi.org) for the morning news feed
- [BroCode](https://www.youtube.com/@BroCodez) for the personality inspiration
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for offline TTS on Windows

---

<div align="center">

**Built with 💻 and ☕ by Vishal Goud**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](http://www.linkedin.com/in/vishalgoud3105)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/Vishalgoud3105)
[![Portfolio](https://img.shields.io/badge/Portfolio-orange?style=flat)](https://vishalgoud3105.github.io/Portfolio/)

---

### 📬 Contact

This repository is **private**. For collaboration inquiries, demo requests, or questions:

📧 **Email**: [vishalgoud3105@gmail.com](mailto:vishalgoud3105@gmail.com)  
💼 **LinkedIn**: [vishalgoud](http://www.linkedin.com/in/vishalgoud3105)  
🌐 **Portfolio**: [vishalgoud3105.github.io](https://vishalgoud3105.github.io/Portfolio/)

⭐ **Interested in this project? Reach out!** ⭐
