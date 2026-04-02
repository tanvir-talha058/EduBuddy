"""
EduBuddy — AI Learning Assistant
A modern, professional GUI application for students.
"""

import customtkinter as ctk
import threading
import datetime
import sys
import os
import webbrowser
import random

# Optional dependencies with graceful fallback
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

# ── Theme ─────────────────────────────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DARK = {
    "bg_primary":    "#0f172a",
    "bg_secondary":  "#1e293b",
    "bg_tertiary":   "#334155",
    "accent":        "#3b82f6",
    "accent_hover":  "#2563eb",
    "success":       "#22c55e",
    "warning":       "#f59e0b",
    "error":         "#ef4444",
    "text_primary":  "#f1f5f9",
    "text_secondary":"#94a3b8",
    "user_bubble":   "#1d4ed8",
    "bot_bubble":    "#1e293b",
    "bubble_border": "#334155",
}

LIGHT = {
    "bg_primary":    "#f8fafc",
    "bg_secondary":  "#e2e8f0",
    "bg_tertiary":   "#cbd5e1",
    "accent":        "#2563eb",
    "accent_hover":  "#1d4ed8",
    "success":       "#16a34a",
    "warning":       "#d97706",
    "error":         "#dc2626",
    "text_primary":  "#0f172a",
    "text_secondary":"#475569",
    "user_bubble":   "#2563eb",
    "bot_bubble":    "#ffffff",
    "bubble_border": "#cbd5e1",
}

C = DARK  # active colour palette (mutable reference)


# ── TTS Engine ────────────────────────────────────────────────────────────────

class TTSEngine:
    """Thread-safe Text-to-Speech wrapper."""

    def __init__(self):
        self._engine = None
        self._lock = threading.Lock()
        if TTS_AVAILABLE:
            try:
                self._engine = pyttsx3.init()
                voices = self._engine.getProperty("voices")
                if len(voices) > 1:
                    self._engine.setProperty("voice", voices[1].id)
                self._engine.setProperty("rate", 170)
            except Exception:
                self._engine = None

    def speak(self, text: str):
        if self._engine is None:
            return
        with self._lock:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception:
                pass


# ── Message Bubble ────────────────────────────────────────────────────────────

class MessageBubble(ctk.CTkFrame):
    """A single chat message bubble."""

    def __init__(self, parent, text: str, sender: str = "assistant", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        is_user = sender == "user"
        timestamp = datetime.datetime.now().strftime("%I:%M %p")

        self.grid_columnconfigure(0, weight=1)

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="ew", padx=8, pady=4)
        wrapper.grid_columnconfigure(0, weight=1)

        bubble = ctk.CTkFrame(
            wrapper,
            corner_radius=16,
            fg_color=C["user_bubble"] if is_user else C["bot_bubble"],
            border_width=0 if is_user else 1,
            border_color=C["bubble_border"],
        )

        if is_user:
            bubble.grid(row=0, column=0, sticky="e", padx=(100, 0))
        else:
            bubble.grid(row=0, column=0, sticky="w", padx=(0, 100))

        # Header row (name + timestamp)
        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.grid(row=0, column=0, padx=14, pady=(10, 2), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        name = "You" if is_user else "🎓 EduBuddy"
        ctk.CTkLabel(
            header,
            text=name,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#93c5fd" if is_user else C["accent"],
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text=timestamp,
            font=ctk.CTkFont(size=10),
            text_color=C["text_secondary"],
        ).grid(row=0, column=1, sticky="e")

        # Message body
        ctk.CTkLabel(
            bubble,
            text=text,
            wraplength=520,
            justify="left",
            font=ctk.CTkFont(size=13),
            text_color=C["text_primary"],
        ).grid(row=1, column=0, padx=14, pady=(0, 12), sticky="w")


# ── Main Application ──────────────────────────────────────────────────────────

QUICK_ACTIONS = [
    ("🔍  Google Search",    "open google"),
    ("▶️  YouTube",          "open youtube"),
    ("🐍  Learn Python",     "learn python"),
    ("☕  Learn Java",       "learn java"),
    ("🌐  Learn HTML/CSS",   "learn html"),
    ("⚡  Learn JavaScript", "learn javascript"),
    ("🔷  Learn C / C++",    "learn c"),
    ("🐘  Learn PHP",        "learn php"),
    ("🦄  Learn Django",     "learn django"),
    ("⚛️  Learn React",      "learn react"),
    ("🛡️  Ethical Hacking",  "ethical hacking"),
    ("⏰  Set Reminder",     "set reminder"),
    ("😄  Tell a Joke",      "tell me a joke"),
    ("🎬  Suggest Movie",    "suggest a movie"),
    ("📅  Today's Date",     "what is the date"),
    ("❓  Help",             "help"),
]


class EduBuddyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("EduBuddy — AI Learning Assistant")
        self.geometry("1150x730")
        self.minsize(920, 620)
        self.configure(fg_color=C["bg_primary"])

        self._is_listening = False
        self._theme_mode = "dark"
        self._tts = TTSEngine()

        self._build_ui()
        self.after(700, self._welcome)

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()

    def _build_sidebar(self):
        sb = ctk.CTkFrame(
            self, width=256, corner_radius=0, fg_color=C["bg_secondary"]
        )
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_rowconfigure(3, weight=1)
        sb.grid_columnconfigure(0, weight=1)

        # Brand
        brand = ctk.CTkFrame(sb, fg_color="transparent")
        brand.grid(row=0, column=0, padx=22, pady=(28, 10), sticky="ew")

        ctk.CTkLabel(brand, text="🎓", font=ctk.CTkFont(size=40)).grid(
            row=0, column=0, sticky="w"
        )
        ctk.CTkLabel(
            brand,
            text="EduBuddy",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=C["text_primary"],
        ).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(
            brand,
            text="AI Learning Assistant",
            font=ctk.CTkFont(size=11),
            text_color=C["text_secondary"],
        ).grid(row=2, column=0, sticky="w", pady=(2, 0))

        # Divider
        ctk.CTkFrame(sb, height=1, fg_color=C["bg_tertiary"]).grid(
            row=1, column=0, sticky="ew", padx=16, pady=(4, 10)
        )

        # Section label
        ctk.CTkLabel(
            sb,
            text="  QUICK ACTIONS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=C["text_secondary"],
        ).grid(row=2, column=0, padx=16, sticky="w")

        # Scrollable actions list
        actions_scroll = ctk.CTkScrollableFrame(
            sb,
            fg_color="transparent",
            scrollbar_button_color=C["bg_tertiary"],
            scrollbar_button_hover_color="#475569",
        )
        actions_scroll.grid(row=3, column=0, sticky="nsew", padx=8, pady=(4, 0))
        actions_scroll.grid_columnconfigure(0, weight=1)

        for label, cmd in QUICK_ACTIONS:
            ctk.CTkButton(
                actions_scroll,
                text=label,
                anchor="w",
                fg_color="transparent",
                text_color=C["text_primary"],
                hover_color=C["bg_tertiary"],
                height=38,
                corner_radius=8,
                font=ctk.CTkFont(size=13),
                command=lambda c=cmd: self._quick_action(c),
            ).grid(sticky="ew", padx=4, pady=2)

        # Bottom controls
        bottom = ctk.CTkFrame(sb, fg_color="transparent")
        bottom.grid(row=4, column=0, sticky="ew", padx=14, pady=(8, 20))
        bottom.grid_columnconfigure(0, weight=1)

        self._theme_btn = ctk.CTkButton(
            bottom,
            text="☀️  Light Mode",
            height=34,
            corner_radius=8,
            fg_color=C["bg_tertiary"],
            hover_color="#475569",
            font=ctk.CTkFont(size=12),
            command=self._toggle_theme,
        )
        self._theme_btn.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        status_card = ctk.CTkFrame(
            bottom, fg_color=C["bg_primary"], corner_radius=8
        )
        status_card.grid(row=1, column=0, sticky="ew")
        status_card.grid_columnconfigure(1, weight=1)

        self._status_dot = ctk.CTkLabel(
            status_card,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color=C["success"],
        )
        self._status_dot.grid(row=0, column=0, padx=(12, 6), pady=10)

        self._status_label = ctk.CTkLabel(
            status_card,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=C["text_primary"],
        )
        self._status_label.grid(row=0, column=1, sticky="w", pady=10)

    def _build_main(self):
        main = ctk.CTkFrame(self, corner_radius=0, fg_color=C["bg_primary"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(
            main, height=64, corner_radius=0, fg_color=C["bg_secondary"]
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)

        ctk.CTkLabel(
            header,
            text="💬  Conversation",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=C["text_primary"],
        ).grid(row=0, column=0, padx=22, pady=16, sticky="w")

        btn_group = ctk.CTkFrame(header, fg_color="transparent")
        btn_group.grid(row=0, column=2, padx=16, pady=12)

        ctk.CTkButton(
            btn_group,
            text="🗑  Clear",
            width=90,
            height=36,
            corner_radius=8,
            fg_color=C["bg_tertiary"],
            hover_color="#475569",
            font=ctk.CTkFont(size=12),
            command=self._clear_chat,
        ).grid(row=0, column=0, padx=(0, 6))

        ctk.CTkButton(
            btn_group,
            text="❓  Help",
            width=80,
            height=36,
            corner_radius=8,
            fg_color=C["bg_tertiary"],
            hover_color="#475569",
            font=ctk.CTkFont(size=12),
            command=lambda: self._quick_action("help"),
        ).grid(row=0, column=1)

        # Chat area
        self._chat = ctk.CTkScrollableFrame(
            main,
            corner_radius=0,
            fg_color=C["bg_primary"],
            scrollbar_button_color=C["bg_tertiary"],
            scrollbar_button_hover_color="#475569",
        )
        self._chat.grid(row=1, column=0, sticky="nsew")
        self._chat.grid_columnconfigure(0, weight=1)

        # Input bar
        input_bar = ctk.CTkFrame(
            main, height=76, corner_radius=0, fg_color=C["bg_secondary"]
        )
        input_bar.grid(row=2, column=0, sticky="ew")
        input_bar.grid_columnconfigure(0, weight=1)
        input_bar.grid_propagate(False)

        self._entry = ctk.CTkEntry(
            input_bar,
            placeholder_text="Type a command or click 🎤 to speak…",
            height=46,
            corner_radius=23,
            font=ctk.CTkFont(size=13),
            fg_color=C["bg_primary"],
            border_color=C["bg_tertiary"],
            text_color=C["text_primary"],
            placeholder_text_color=C["text_secondary"],
        )
        self._entry.grid(row=0, column=0, padx=(16, 8), pady=15, sticky="ew")
        self._entry.bind("<Return>", self._on_send)

        self._send_btn = ctk.CTkButton(
            input_bar,
            text="Send",
            width=80,
            height=46,
            corner_radius=23,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=C["accent"],
            hover_color=C["accent_hover"],
            command=self._on_send,
        )
        self._send_btn.grid(row=0, column=1, padx=(0, 8), pady=15)

        self._mic_btn = ctk.CTkButton(
            input_bar,
            text="🎤",
            width=46,
            height=46,
            corner_radius=23,
            font=ctk.CTkFont(size=18),
            fg_color=C["bg_tertiary"],
            hover_color="#475569",
            command=self._toggle_mic,
        )
        self._mic_btn.grid(row=0, column=2, padx=(0, 16), pady=15)

    # ── Core Helpers ──────────────────────────────────────────────────────────

    def _add_message(self, text: str, sender: str = "assistant"):
        bubble = MessageBubble(self._chat, text=text, sender=sender)
        bubble.grid(sticky="ew", padx=0, pady=0)
        self.after(80, lambda: self._chat._parent_canvas.yview_moveto(1.0))

    def _speak(self, text: str):
        self._add_message(text, "assistant")
        threading.Thread(target=self._tts.speak, args=(text,), daemon=True).start()

    def _set_status(self, label: str, level: str = "success"):
        colour_map = {
            "success": C["success"],
            "warning": C["warning"],
            "error":   C["error"],
            "info":    C["accent"],
        }
        self._status_dot.configure(text_color=colour_map.get(level, C["success"]))
        self._status_label.configure(text=label)

    # ── Event Handlers ────────────────────────────────────────────────────────

    def _on_send(self, _event=None):
        text = self._entry.get().strip()
        if text:
            self._entry.delete(0, "end")
            self._add_message(text, "user")
            threading.Thread(
                target=self._process, args=(text.lower(),), daemon=True
            ).start()

    def _quick_action(self, cmd: str):
        self._add_message(cmd.title(), "user")
        threading.Thread(
            target=self._process, args=(cmd.lower(),), daemon=True
        ).start()

    def _toggle_mic(self):
        if not self._is_listening:
            if not SPEECH_AVAILABLE:
                self._speak(
                    "Speech recognition is unavailable. "
                    "Please install the 'speechrecognition' and 'pyaudio' packages."
                )
                return
            threading.Thread(target=self._listen, daemon=True).start()

    def _listen(self):
        self._is_listening = True
        self._set_status("Listening…", "warning")
        self.after(0, lambda: self._mic_btn.configure(
            fg_color=C["error"], text="⏹"
        ))

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)

            self._set_status("Recognising…", "info")
            query = recognizer.recognize_google(audio, language="en-in")
            self._add_message(query, "user")
            self._process(query.lower())

        except sr.WaitTimeoutError:
            self._speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            self._speak("Sorry, I couldn't understand that. Please speak clearly.")
        except sr.RequestError as exc:
            self._speak(f"Speech service error: {exc}. Check your connection.")
        except Exception:
            self._speak("Something went wrong with the microphone. Please try again.")
        finally:
            self._is_listening = False
            self.after(0, lambda: self._mic_btn.configure(
                fg_color=C["bg_tertiary"], text="🎤"
            ))
            self._set_status("Ready", "success")

    def _toggle_theme(self):
        global C
        if self._theme_mode == "dark":
            ctk.set_appearance_mode("light")
            self._theme_mode = "light"
            C = LIGHT
            self._theme_btn.configure(text="🌙  Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self._theme_mode = "dark"
            C = DARK
            self._theme_btn.configure(text="☀️  Light Mode")

    def _clear_chat(self):
        for widget in self._chat.winfo_children():
            widget.destroy()

    # ── Command Processor ─────────────────────────────────────────────────────

    def _process(self, query: str):
        self._set_status("Processing…", "info")
        try:
            self._dispatch(query)
        finally:
            self._set_status("Ready", "success")

    def _dispatch(self, query: str):  # noqa: C901
        # Greetings
        if any(w in query for w in ("hello", "hi", "hey", "greetings")):
            self._speak(random.choice([
                "Hello! How can I help you learn today? 👋",
                "Hi there! Ready to explore something new?",
                "Hey! I'm here to help. What would you like to know?",
            ]))

        # Time
        elif "time" in query and "reminder" not in query:
            t = datetime.datetime.now().strftime("%I:%M %p")
            self._speak(f"The current time is {t}.")

        # Date
        elif "date" in query or ("today" in query and "reminder" not in query):
            d = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self._speak(f"Today is {d}.")

        # Wikipedia search
        elif any(p in query for p in ("tell me about", "what is", "who is", "search wikipedia")):
            term = (query
                    .replace("tell me about", "")
                    .replace("what is", "")
                    .replace("who is", "")
                    .replace("search wikipedia", "")
                    .strip())
            self._wiki(term)

        # Open Notepad / editor
        elif "open notepad" in query:
            self._speak("Opening Notepad…")
            if sys.platform == "win32":
                os.system("notepad.exe")
            else:
                self._speak("Notepad is only available on Windows.")

        # Terminal
        elif "open terminal" in query or "open command prompt" in query:
            self._speak("Opening terminal…")
            if sys.platform == "win32":
                os.system("start cmd")
            elif sys.platform == "darwin":
                os.system("open -a Terminal")
            else:
                os.system("x-terminal-emulator &")

        # Websites
        elif "open youtube" in query:
            self._speak("Opening YouTube…")
            webbrowser.open("https://www.youtube.com")

        elif "open facebook" in query:
            self._speak("Opening Facebook…")
            webbrowser.open("https://www.facebook.com")

        elif "open chatgpt" in query or "open chat gpt" in query:
            self._speak("Opening ChatGPT…")
            webbrowser.open("https://chat.openai.com")

        elif "open github" in query:
            self._speak("Opening GitHub…")
            webbrowser.open("https://www.github.com")

        elif "open google" in query:
            self._speak("Opening Google…")
            webbrowser.open("https://www.google.com")

        # Google search
        elif "search" in query:
            term = (query
                    .replace("search", "")
                    .replace("on google", "")
                    .replace("google", "")
                    .replace("for", "", 1)
                    .strip())
            if term:
                self._speak(f"Searching Google for: {term}")
                webbrowser.open(
                    f"https://www.google.com/search?q={term.replace(' ', '+')}"
                )
            else:
                webbrowser.open("https://www.google.com")
                self._speak("Opening Google Search.")

        # Learning resources
        elif "learn python" in query:
            self._open_resource("Python", "https://www.w3schools.com/python/")
        elif "learn java" in query:
            self._open_resource("Java", "https://www.w3schools.com/java/")
        elif "learn html" in query:
            self._open_resource("HTML", "https://www.w3schools.com/html/")
        elif "learn css" in query:
            self._open_resource("CSS", "https://www.w3schools.com/css/")
        elif "learn javascript" in query or "learn js" in query:
            self._open_resource("JavaScript", "https://www.w3schools.com/js/")
        elif "learn c++" in query or "learn cpp" in query:
            self._open_resource("C++", "https://www.w3schools.com/cpp/")
        elif "learn c" in query:
            self._open_resource("C", "https://www.w3schools.com/c/")
        elif "learn php" in query:
            self._open_resource("PHP", "https://www.w3schools.com/php/")
        elif "learn django" in query:
            self._open_resource("Django", "https://www.w3schools.com/django/")
        elif "learn react" in query:
            self._open_resource("React", "https://www.w3schools.com/react/")
        elif "learn web development" in query:
            self._open_resource(
                "Web Development", "https://www.w3schools.com/whatis/"
            )
        elif "ethical hacking" in query:
            self._speak("Opening the Ethical Hacking course on YouTube…")
            webbrowser.open(
                "https://youtube.com/playlist?list="
                "PL82D6HIBQ199l1XGskGj-_H9c8Fr-5hr4"
            )

        # Reminder
        elif "set reminder" in query or "remind me" in query:
            self._speak("Opening an online reminder tool for you.")
            webbrowser.open("https://vclock.com/")

        # Movie suggestion
        elif "movie" in query or "suggest" in query or "recommend" in query:
            picks = [
                ("The Pursuit of Happyness",
                 "An inspiring story about perseverance and chasing your dreams."),
                ("The Social Network",
                 "The story of Facebook's founding — great for tech enthusiasts."),
                ("Good Will Hunting",
                 "A brilliant mind overcomes personal barriers — very motivating."),
                ("October Sky",
                 "A young man pursues his dream of becoming a rocket scientist."),
                ("The Imitation Game",
                 "Alan Turing's incredible story of cracking the Enigma code."),
            ]
            title, desc = random.choice(picks)
            self._speak(f"I recommend '{title}'. {desc}")

        # Jokes
        elif "joke" in query:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "Why did the programmer quit? They didn't get arrays! 😄",
                "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡",
                "Why do Java developers wear glasses? Because they can't C#! 😂",
                "A SQL query walks into a bar and asks two tables: 'Can I join you?' 😄",
                "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings. 😢",
            ]
            self._speak(random.choice(jokes))

        # Help
        elif "help" in query:
            self._speak(
                "Here's what I can do:\n"
                "• Check the time or date\n"
                "• Search Wikipedia — e.g. 'tell me about Python'\n"
                "• Open YouTube, Google, Facebook, GitHub, ChatGPT\n"
                "• Google search — e.g. 'search machine learning'\n"
                "• Programming tutorials: Python, Java, HTML, CSS, JS, C, PHP, Django, React\n"
                "• Ethical Hacking course\n"
                "• Set reminders\n"
                "• Tell jokes or suggest movies\n"
                "• Open Notepad or Terminal\n"
                "• Just ask naturally — I'll try my best!"
            )

        # Exit
        elif any(w in query for w in ("exit", "quit", "bye", "goodbye", "close")):
            self._speak("Goodbye! Keep learning and growing! 🎓")
            self.after(2500, self.destroy)

        # Fallback — try Wikipedia
        else:
            self._wiki(query)

    def _open_resource(self, name: str, url: str):
        self._speak(f"Opening the {name} tutorial on W3Schools…")
        webbrowser.open(url)

    def _wiki(self, term: str):
        if not term:
            self._speak(
                "Please tell me what you'd like to know about. "
                "For example: 'tell me about artificial intelligence'."
            )
            return
        if not WIKIPEDIA_AVAILABLE:
            self._speak(
                "Wikipedia search is unavailable. "
                "Please install the 'wikipedia' package."
            )
            return
        try:
            result = wikipedia.summary(term, sentences=2)
            self._speak(result)
        except wikipedia.exceptions.DisambiguationError as exc:
            suggestion = exc.options[0] if exc.options else "something else"
            self._speak(
                f"There are multiple results for '{term}'. "
                f"Did you mean '{suggestion}'? Please be more specific."
            )
        except wikipedia.exceptions.PageError:
            self._speak(
                f"I couldn't find a Wikipedia page for '{term}'. "
                "Please try a different query."
            )
        except Exception:
            self._speak(
                "I'm not sure about that. "
                "Try asking differently or say 'help' to see what I can do."
            )

    # ── Welcome ───────────────────────────────────────────────────────────────

    def _welcome(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        self._speak(
            f"{greeting}! 👋 I'm EduBuddy, your AI learning assistant. "
            "I can help you learn programming, search Wikipedia, open apps, and much more. "
            "Use the quick actions on the left, type a command, or click 🎤 to speak!"
        )


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = EduBuddyApp()
    app.mainloop()
