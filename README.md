# 🎓 EduBuddy — AI Learning Assistant

EduBuddy is a modern, voice-activated AI assistant designed specifically for students.
It features a professional dark/light-theme GUI, chat-style conversation interface, voice
input/output, and quick access to learning resources — all from a single desktop application.

---

## ✨ Features

- **Modern GUI** — Clean dark/light theme powered by CustomTkinter with chat bubbles, sidebar, and status bar
- **Voice Input** — Click the 🎤 button to speak your command
- **Text Input** — Type commands directly in the input bar
- **Text-to-Speech** — Responses are spoken aloud via pyttsx3
- **Wikipedia Search** — Ask "tell me about …" or "what is …"
- **Programming Tutorials** — Instant links to W3Schools for Python, Java, HTML, CSS, JavaScript, C, PHP, Django, React
- **Web Shortcuts** — Open Google, YouTube, Facebook, GitHub, ChatGPT
- **Google Search** — "search machine learning" opens a Google results page
- **Reminders** — Opens an online timer/reminder tool
- **Jokes & Movie Suggestions** — For a quick break
- **Time & Date** — Always at your fingertips
- **Dark / Light Theme Toggle** — Switch with one click

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `pyaudio` may require additional system libraries.
> - **Windows:** `pip install pyaudio` usually works directly.
> - **macOS:** `brew install portaudio && pip install pyaudio`
> - **Linux:** `sudo apt-get install portaudio19-dev && pip install pyaudio`

### 2. Run the app

```bash
python app.py
```

---

## 🗂 Project Structure

| File | Description |
|------|-------------|
| `app.py` | **Main application** — modern GUI entry point |
| `requirements.txt` | Python dependency list |
| `final.py` | Original CLI voice assistant |
| `reminder.py` | Original reminder module |
| `main.py` | Original prototype |

---

## 💬 Example Commands

| You say / type | EduBuddy does |
|---|---|
| `tell me about machine learning` | Wikipedia summary |
| `learn python` | Opens W3Schools Python tutorial |
| `open youtube` | Opens YouTube in browser |
| `search deep learning` | Google search |
| `what is the time` | Speaks current time |
| `set reminder` | Opens vclock.com |
| `tell me a joke` | Tells a programming joke |
| `suggest a movie` | Recommends an inspiring film |
| `help` | Lists all available commands |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `customtkinter` | Modern GUI widgets |
| `pyttsx3` | Text-to-speech |
| `SpeechRecognition` | Voice input |
| `pyaudio` | Microphone access |
| `wikipedia` | Wikipedia search |

---

*EduBuddy aims to create an easy and user-friendly environment for students to make their academic life more productive and convenient.*
