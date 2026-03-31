# #----------VERSION-1.9.0 (SNAP FALSE-TRIGGER FIXED | CLEAN KILL | BROCODE VIBE)-----------

# 1. INITIALIZATION & CONFIGURATION
import time
import datetime
import pyttsx3
import pyaudio
import numpy as np
import speech_recognition as sr
import os
import requests
import subprocess
import pyautogui
import pygame
import json
import feedparser
from groq import Groq

PROJECT_DIR = r"C:\Users\ASUS\Documents\Wakeup_Jarvis"

# ── API KEYS ─────────────────────────────────────────────────
NEWS_API_KEY   = ""
GROQ_API_KEY   = ""
# ─────────────────────────────────────────────────────────────

if not NEWS_API_KEY or NEWS_API_KEY == "PASTE_YOUR_NEW_NEWSAPI_KEY_HERE":
    print("\nWARNING: NEWS_API_KEY not set. NewsAPI features will be skipped.\n")
else:
    print("\n--> API Keys Loaded Successfully.")

# ── USER NAME ─────────────────────────────────────────────────
USER_NAME = input("What's your name?: ").strip().capitalize()
if not USER_NAME:
    USER_NAME = "Sir"
print(f"\n--> Welcome, {USER_NAME}. Jarvis is initializing...\n")
# ─────────────────────────────────────────────────────────────

client = Groq(api_key=GROQ_API_KEY)

CHROME_EXE_PATH       = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_WORK_PROFILE   = "Default"
CHROME_KUSHAL_PROFILE = "Profile 10"
CHROME_ALT_PROFILE    = "Profile 1"

pygame.mixer.init()


# 2. VOICE ENGINE
def get_engine():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 178)
    return engine

def speak(audio):
    print(f"\nJarvis: {audio}\n")
    for attempt in range(2):   # retry once if first attempt produces no audio
        try:
            engine = get_engine()
            engine.say(audio)
            engine.runAndWait()
            engine.stop()
            break   # success
        except Exception as e:
            if attempt == 0:
                # SAPI5 COM session may be dirty after a snap interruption
                # Short sleep lets Windows audio pipeline fully reset
                time.sleep(0.3)
            # second attempt failure is silent — don't crash

def user_say(text):
    print(f"\n{USER_NAME}: {text}\n")

def greet_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:    greeting = "good morning"
    elif 12 <= hour < 18: greeting = "good afternoon"
    else:                 greeting = "good evening"
    speak(f"Greetings Mr. {USER_NAME} sir, {greeting}. Welcome back.")
    speak("All systems are online. Daddy's home.")

def launch_chrome(url, profile_dir):
    try:
        subprocess.Popen([CHROME_EXE_PATH, f"--profile-directory={profile_dir}", url])
    except Exception:
        pass


# 3. NEWS SOURCES
def get_newsapi_dump():
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': (
            "AI OR Robotics OR Nvidia OR GPU OR AMD OR Intel OR TPU OR "
            "Bitcoin OR Stocks OR Crypto OR Cybersecurity OR Hacker OR "
            "Space OR NASA OR ISRO OR SpaceX OR Cosmos OR Universe OR "
            "Biotech OR Neuralink OR BCI OR Biology OR Science OR Invention OR "
            "Anthropic OR OpenAI OR Gemini OR Deepmind OR Groq OR Perplexity OR "
            "AWS OR Azure OR GCP OR Oracle OR Cloud"
        ),
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': 30
    }
    headers = {'X-Api-Key': NEWS_API_KEY}
    try:
        res  = requests.get(url, headers=headers, params=params, timeout=10)
        data = res.json()
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            raw = ""
            for i, a in enumerate(articles):
                raw += f"[{i+1}] Title: {a['title']} | URL: {a['url']} | Summary: {a.get('description','')}\n"
            return raw
        else:
            print(f"--> NEWSAPI ERROR: {data.get('code')} - {data.get('message')}")
            return None
    except Exception as e:
        print(f"--> NETWORK ERROR: {e}")
        return None

RSS_FEEDS = {
    "Tech & AI": [
        "https://feeds.feedburner.com/TechCrunch",
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "https://www.theverge.com/rss/index.xml",
        "https://venturebeat.com/feed/",
        "https://techcrunch.com/feed/",
    ],
    "AI Companies": [
        "https://www.anthropic.com/news/rss.xml",
        "https://openai.com/blog/rss.xml",
        "https://blog.google/technology/ai/rss/",
        "https://deepmind.google/blog/rss/",
    ],
    "Space & Science": [
        "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "https://www.spacex.com/updates/index.xml",
        "https://feeds.feedburner.com/spacecom",
        "https://www.isro.gov.in/rss.xml",
    ],
    "Stocks & Crypto": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=NVDA,AMD,INTC&region=US&lang=en-US",
        "https://feeds.feedburner.com/coindesk/rss",
        "https://decrypt.co/feed",
    ],
    "Newsletters (Insta Pages)": [
        "https://artificial-intelligencee.beehiiv.com/feed",
        "https://theaifield.beehiiv.com/feed",
        "https://theroboticsnewsletter.beehiiv.com/feed",
        "https://evolvingai.io/feed",
        "https://uncoverai.co/feed",
        "https://aibusinesssummary.com/feed",
    ],
}

def get_rss_dump():
    raw   = ""
    count = 1
    for category, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:
                    title   = entry.get('title', 'No title')
                    link    = entry.get('link', '')
                    summary = entry.get('summary', entry.get('description', ''))[:200]
                    raw    += f"[{count}] Category: {category} | Title: {title} | URL: {link} | Summary: {summary}\n"
                    count  += 1
            except Exception as e:
                print(f"--> RSS error ({feed_url}): {e}")
                continue
    return raw if raw else None


# 4. CATEGORIZED NEWS ENGINE


CATEGORIES = [
    "AI and Machine Learning",
    "Chips and Hardware, GPU, TPU, XPU",
    "Space, Cosmos and Science",
    "Stocks, Crypto and Trading",
    "Cybersecurity and Hacking",
    "Biotech, Neuralink and BCI",
    "Cloud and Infrastructure",
    "Newsletter Picks from your insta feeds",
    "General and Trending",
]

# ── Global news session — tracks position for snap + CONTINUE ──
NEWS_SESSION = {
    "categories_data": None,
    "left_cat_idx":    None,
    "left_item_idx":   None,
    "mode":            None,
    "all_urls":        [],
    "yt_queries":      [],
    "full_text_dump":  "",
}

# ── Last completed briefing — stored in RAM for snap + READ replay ──
LAST_COMPLETED_SESSION = {
    "categories_data": None,
    "all_urls":        [],
    "yt_queries":      [],
    "full_text_dump":  "",
    "mode":            None,
}

def get_ist_hour():
    """Returns current hour in IST (UTC+5:30) using only stdlib."""
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    return ist_now.hour

def get_time_of_day():
    """
    Returns (label, news_mode) based on IST hour.
    morning   5am-12pm  -> newsapi
    afternoon 12pm-5pm  -> rss
    evening   5pm-9pm   -> rss
    night     9pm-12am  -> rss
    midnight  12am-5am  -> rss
    """
    hour = get_ist_hour()
    if 5  <= hour < 12: return "morning",   "morning"
    if 12 <= hour < 17: return "afternoon", "evening"
    if 17 <= hour < 21: return "evening",   "evening"
    if 21 <= hour < 24: return "night",     "evening"
    return "midnight", "evening"

BROCODE_SYSTEM_PROMPT = """
You are Jarvis — but not the boring butler kind. You're that one friend who's insanely smart, always up on everything, and somehow makes even boring news sound interesting.

YOUR VIBE: Think BroCode YouTube channel. Casual, confident, hype when something's actually hype, real when something's serious. You talk like a bro who just read everything on the internet and is now catching his friend up over a call.

YOUR PERSONALITY RULES:
- Talk directly TO the person. Always "you" or "sir" — never their name mid-briefing
- Use natural filler transitions like — "Okay, so", "Real quick", "And get this", "Here's the wild part", "No cap", "Lowkey", "Bro", "Okay, moving on", "This one's actually big"
- React genuinely — if something is wild, say it's wild. If something's bad news, acknowledge it
- Keep it punchy — headline then 2 sentences max per news item. Don't lecture
- Occasionally throw in a quick hot take or prediction — just one line, keep it short
- End each category with a one-liner like "That's the AI corner for you sir" or "Crypto's doing its thing as usual"
- Never say "As an AI" or anything robotic like that
- No asterisks. No markdown. No bullet points. Pure spoken word energy
- Sound like you actually care about this stuff — because Jarvis does
"""

def build_news_prompt(raw_news, mode):
    time_context = "past 24 hours" if mode == "morning" else "today so far"
    return f"""
{BROCODE_SYSTEM_PROMPT}

You have news from the {time_context}. Categorize into these groups:
{chr(10).join(CATEGORIES)}

For each category with relevant news, pick TOP 2-3 stories max.
Skip categories with nothing relevant.

Return ONLY a valid JSON array. Zero explanation. Zero markdown. Just raw JSON:
[
  {{
    "category": "AI and Machine Learning",
    "intro": "One casual bro-style intro line for this category. Like: Okay, so the AI world has been busy sir.",
    "items": [
      {{
        "headline": "Punchy rewritten headline in your own words — not a copy of the original title",
        "briefing": "2 sentences max. React to it. Talk directly to the listener. No URLs. Throw in a hot take if it deserves one.",
        "url": "original article URL"
      }}
    ],
    "outro": "One casual closing line for this category. Like: And that is the AI corner for you sir."
  }}
]

STRICT RULES:
- Valid JSON only. No code fences. No markdown
- No URLs inside headline or briefing
- Address listener as you or sir only — never by name
- Max 3 items per category
- Only include categories with actual relevant news
- Keep intros and outros short — one line each

News Data:
{raw_news}
"""


# 5. SNAP DETECTION DURING NEWS
# ARCHITECTURE: Listen ONLY in silence gaps between sentences.
# Mic is completely OFF while Jarvis is speaking.
# This eliminates all loopback false triggers — Jarvis cannot
# hear its own speaker because the mic is not open during TTS.
#
# Flow per news sentence:
#   speak_news(text) → pyttsx3 speaks fully → mic opens → 1.5s snap window
#   → snap detected → _handle_snap_during_news → SKIP or continue
#   → no snap → next sentence immediately


def check_for_snap_in_silence(listen_seconds=1.5):
    """
    Listens for a snap ONLY after TTS has fully finished.
    Mic is OFF during TTS — only active in the silence gap between sentences.
    This completely eliminates Jarvis hearing its own speaker output.

    listen_seconds: how long to listen after each sentence (default 1.5s).
    Returns True if snap detected, False if silence.
    """
    CHUNK           = 512
    RATE            = 44100
    THRESHOLD       = 1500
    RATIO_THRESHOLD = 3.5
    CONFIRM_CHUNKS  = 2
    # Small flush at start to clear any last echo of TTS from the room
    FLUSH_SECONDS   = 0.15

    try:
        p      = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"--> [Snap check] Mic open failed: {e}")
        return False

    total_chunks = int(RATE / CHUNK * listen_seconds)
    flush_chunks = int(RATE / CHUNK * FLUSH_SECONDS)
    chunks_read  = 0
    consecutive  = 0
    snap_found   = False

    for _ in range(total_chunks):
        try:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            chunks_read += 1

            if chunks_read <= flush_chunks:
                continue   # discard tail echo of TTS

            peak = np.max(np.abs(data))

            if peak > THRESHOLD:
                fft_data  = np.abs(np.fft.rfft(data))
                fft_freqs = np.fft.rfftfreq(CHUNK, 1.0 / RATE)

                speech_energy = np.sum(fft_data[(fft_freqs > 300)  & (fft_freqs < 3000)])
                snap_energy   = np.sum(fft_data[(fft_freqs > 3500) & (fft_freqs < 8000)])
                low_energy    = np.sum(fft_data[(fft_freqs > 500)  & (fft_freqs < 2500)]) + 1
                ratio         = snap_energy / low_energy

                is_candidate = (
                    ratio > RATIO_THRESHOLD
                    and snap_energy > speech_energy * 0.8
                )

                if is_candidate:
                    consecutive += 1
                    if consecutive >= CONFIRM_CHUNKS:
                        print(f"--> [Snap confirmed in silence] ratio={ratio:.2f}")
                        snap_found = True
                        break
                else:
                    consecutive = 0
            else:
                consecutive = 0

        except Exception:
            consecutive = 0
            continue

    try:
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception:
        pass

    return snap_found


def speak_news(text):
    """
    Speaks a news sentence fully via blocking pyttsx3.
    After finishing, checks for snap in silence window.
    Returns True if completed with no snap, False if snap detected after.
    Mic is NEVER active while TTS is playing — eliminates all loopback issues.
    """
    print(f"\nJarvis: {text}\n")
    try:
        engine = get_engine()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"--> [TTS error] {e}")

    # Now TTS is done — check for snap in the silence after
    snap = check_for_snap_in_silence(listen_seconds=1.5)
    return not snap   # True = no snap (completed), False = snap detected


def _handle_snap_during_news(r_recognizer):
    """
    Called after snap confirmed during news.
    Switches to Google STT, asks SKIP or continue.
    Returns True if skipped, False if continuing.
    """
    speak("Snap detected sir. Say SKIP to stop, or stay quiet to keep going.")

    r_snap = sr.Recognizer()
    with sr.Microphone() as src:
        r_snap.adjust_for_ambient_noise(src, duration=0.5)
        r_snap.energy_threshold = 300
        try:
            audio   = r_snap.listen(src, timeout=5, phrase_time_limit=3)
            keyword = r_snap.recognize_google(audio, language='en-in').lower()
            user_say(keyword)

            if "skip" in keyword:
                speak("Got it sir. Dumping full report to terminal. Opening all tabs now.")
                print(NEWS_SESSION["full_text_dump"])
                urls = NEWS_SESSION["all_urls"]
                speak(f"Opening {len(urls)} source tabs and {len(NEWS_SESSION['yt_queries'])} YouTube tabs sir.")
                for i, u in enumerate(urls):
                    launch_chrome(u.strip(), CHROME_WORK_PROFILE)
                    if (i + 1) % 3 == 0:
                        time.sleep(2.0)
                    else:
                        time.sleep(0.6)
                for q in NEWS_SESSION["yt_queries"]:
                    launch_chrome(
                        f"https://www.youtube.com/results?search_query={q.replace(' ','+')}",
                        CHROME_WORK_PROFILE
                    )
                    time.sleep(0.8)
                speak("All tabs open sir. Snap and say CONTINUE when you are free to resume the news.")
                return True

            else:
                speak("Alright, continuing the news sir.")
                return False

        except (sr.WaitTimeoutError, sr.UnknownValueError):
            speak("No command heard. Continuing the news sir.")
            return False
        except (sr.RequestError, OSError) as e:
            print(f"--> [Network error in snap handler] {e}")
            speak("Network hiccup sir. Continuing the news.")
            return False
        except Exception as e:
            print(f"--> [Snap handler error] {e}")
            return False


# 6. NEWS DELIVERY
def deliver_news_briefing(raw_news, mode, r_recognizer, resume=False):
    """
    resume=False : fresh briefing
    resume=True  : continues from NEWS_SESSION left-off position
    """
    global NEWS_SESSION

    # ── RESUME MODE ───────────────────────────────────────────
    if resume and NEWS_SESSION["categories_data"]:
        categories_data = NEWS_SESSION["categories_data"]
        all_urls        = NEWS_SESSION["all_urls"]
        yt_queries      = NEWS_SESSION["yt_queries"]
        raw_start_cat   = NEWS_SESSION["left_cat_idx"] or 0
        raw_start_item  = NEWS_SESSION["left_item_idx"] or 0

        cat_items = categories_data[raw_start_cat].get("items", []) if raw_start_cat < len(categories_data) else []
        if raw_start_item >= len(cat_items):
            start_cat_idx  = raw_start_cat + 1
            start_item_idx = 0
        else:
            start_cat_idx  = raw_start_cat
            start_item_idx = raw_start_item

        if start_cat_idx >= len(categories_data):
            speak("That was the last news item sir. Full briefing is complete. Snap and say READ to replay or NEW for fresh news.")
            NEWS_SESSION["left_cat_idx"]  = None
            NEWS_SESSION["left_item_idx"] = None
            return

        prev_item_text = None
        if start_item_idx > 0:
            prev           = categories_data[start_cat_idx]["items"][start_item_idx - 1]
            prev_cat       = categories_data[start_cat_idx].get("category", "")
            prev_item_text = f"{prev_cat}, News {start_item_idx}. {prev.get('headline','')}. {prev.get('briefing','')}"
        elif start_cat_idx > 0:
            prev_cat_data  = categories_data[start_cat_idx - 1]
            prev_items     = prev_cat_data.get("items", [])
            if prev_items:
                prev           = prev_items[-1]
                prev_cat       = prev_cat_data.get("category", "")
                prev_item_text = f"{prev_cat}, News {len(prev_items)}. {prev.get('headline','')}. {prev.get('briefing','')}"

        left_cat  = categories_data[start_cat_idx].get("category", "")
        left_news = start_item_idx + 1

        speak(f"Alright sir, previously we left off at {left_cat}, News {left_news}.")
        if prev_item_text:
            speak("But first let me recall the last news we discussed.")
            speak(f"Previously: {prev_item_text}")
        speak(f"Continuing now from {left_cat}, News {left_news}.")

    # ── FRESH MODE ────────────────────────────────────────────
    else:
        start_cat_idx  = 0
        start_item_idx = 0

        prompt = build_news_prompt(raw_news, mode)
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
            )
            raw_response    = response.choices[0].message.content.strip()
            raw_response    = raw_response.replace('```json', '').replace('```', '').strip()
            categories_data = json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"--> JSON PARSE ERROR: {e}")
            speak("The AI fumbled the formatting sir. Check the terminal.")
            return
        except Exception as e:
            print(f"--> GROQ ERROR: {e}")
            speak("Something went sideways sir. Check the terminal.")
            return

        full_text_dump  = "\n" + "="*60 + "\n"
        full_text_dump += "   JARVIS NEWS BRIEFING — FULL REPORT\n"
        full_text_dump += "="*60 + "\n"
        all_urls = []

        for cat_data in categories_data:
            category = cat_data.get('category', '').strip()
            items    = cat_data.get('items', [])
            if not items: continue
            full_text_dump += f"\n[ {category.upper()} ]\n"
            for i, item in enumerate(items):
                full_text_dump += f"  News {i+1}: {item.get('headline','')}\n"
                full_text_dump += f"  {item.get('briefing','')}\n"
                full_text_dump += f"  Source: {item.get('url','')}\n\n"
                if item.get('url'): all_urls.append(item['url'])

        curr_year  = datetime.datetime.now().strftime('%Y')
        yt_queries = [
            f"latest AI breakthroughs {curr_year}",
            "Nvidia AMD GPU news today",
            f"space discovery news {curr_year}",
            "bitcoin crypto market today",
            "cybersecurity news today",
        ]
        full_text_dump += "\n[ YOUTUBE DEEP DIVES ]\n"
        for q in yt_queries:
            full_text_dump += f"  https://www.youtube.com/results?search_query={q.replace(' ','+')}\n"
        full_text_dump += "="*60 + "\n"

        NEWS_SESSION["categories_data"] = categories_data
        NEWS_SESSION["full_text_dump"]  = full_text_dump
        NEWS_SESSION["all_urls"]        = all_urls
        NEWS_SESSION["yt_queries"]      = yt_queries
        NEWS_SESSION["mode"]            = mode
        NEWS_SESSION["left_cat_idx"]    = 0
        NEWS_SESSION["left_item_idx"]   = 0

        speak("Alright sir, here is your briefing. Snap anytime to pause and say SKIP.")

    # ── News reading loop ─────────────────────────────────────
    skipped = False

    for cat_idx, cat_data in enumerate(categories_data):
        if cat_idx < start_cat_idx:
            continue
        if skipped: break

        category = cat_data.get('category', '').strip()
        intro    = cat_data.get('intro', '')
        outro    = cat_data.get('outro', '')
        items    = cat_data.get('items', [])
        if not items: continue

        # Category intro — retry from start if snap+continue
        if (cat_idx == start_cat_idx and start_item_idx == 0) or cat_idx > start_cat_idx:
            while True:
                completed = speak_news(f"{category}. {intro}")
                if completed: break
                skipped = _handle_snap_during_news(r_recognizer)
                if skipped: break
                # Not skipped → re-read intro from beginning
            if skipped: break

        for item_idx, item in enumerate(items):
            if cat_idx == start_cat_idx and item_idx < start_item_idx:
                continue
            if skipped: break

            headline = item.get('headline', '')
            briefing = item.get('briefing', '')
            url      = item.get('url', '')

            # Read news item — retry from start if snap+continue
            while True:
                completed = speak_news(f"News {item_idx + 1}. {headline}. {briefing}")
                if completed: break
                skipped = _handle_snap_during_news(r_recognizer)
                if skipped: break
                # Not skipped → re-read this item from beginning

            if skipped: break

            # Save position only after item fully completed
            NEWS_SESSION["left_cat_idx"]  = cat_idx
            NEWS_SESSION["left_item_idx"] = item_idx + 1

            if url:
                print(f"--> Opening: {url}")
                launch_chrome(url.strip(), CHROME_WORK_PROFILE)

        if skipped: break

        # Category outro — retry from start if snap+continue
        if outro and not skipped:
            while True:
                completed = speak_news(outro)
                if completed: break
                skipped = _handle_snap_during_news(r_recognizer)
                if skipped: break

    # ── Fully completed ───────────────────────────────────────
    if not skipped:
        LAST_COMPLETED_SESSION["categories_data"] = NEWS_SESSION["categories_data"]
        LAST_COMPLETED_SESSION["all_urls"]        = NEWS_SESSION["all_urls"]
        LAST_COMPLETED_SESSION["yt_queries"]      = NEWS_SESSION["yt_queries"]
        LAST_COMPLETED_SESSION["full_text_dump"]  = NEWS_SESSION["full_text_dump"]
        LAST_COMPLETED_SESSION["mode"]            = NEWS_SESSION["mode"]

        speak("That is your full briefing sir. Opening deep dive research tabs now.")
        for q in NEWS_SESSION["yt_queries"]:
            launch_chrome(
                f"https://www.youtube.com/results?search_query={q.replace(' ','+')}",
                CHROME_WORK_PROFILE
            )
            time.sleep(0.8)
        speak(f"Done. {len(NEWS_SESSION['all_urls'])} source tabs and {len(NEWS_SESSION['yt_queries'])} YouTube tabs ready sir.")
        NEWS_SESSION["left_cat_idx"]  = None
        NEWS_SESSION["left_item_idx"] = None


# 7. EVENING BRIEFING CHECK
_evening_briefing_done = False   # fires only once per session

def check_evening_briefing(r):
    global _evening_briefing_done
    if _evening_briefing_done:
        return
    ist_hour = get_ist_hour()
    if 21 <= ist_hour <= 23:
        _evening_briefing_done = True   # mark immediately so it never repeats
        speak("Hey sir, it's end of the day. You've been grinding hard. Want me to catch you up on everything that happened today? Just say sure or skip.")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.energy_threshold = 250
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
                reply = r.recognize_google(audio).lower()
                print(f"Heard: {reply}")
                user_say(reply)
                if any(w in reply for w in ["sure", "ok", "okay", "yes", "yeah", "go ahead", "do it"]):
                    speak("Bet. Let me pull today's feed for you sir.")
                    raw = get_rss_dump()
                    if raw:
                        deliver_news_briefing(raw, mode="evening", r_recognizer=r)
                    else:
                        speak("Couldn't pull the feeds sir. Check your connection.")
                else:
                    speak("No worries, skipping the evening briefing. Snap when you need me.")
            except (sr.RequestError, OSError) as e:
                print(f"--> [Network error in evening briefing] {e}")
                speak("Network hiccup sir. Skipping evening briefing.")
            except Exception:
                speak("Didn't catch that. Skipping evening briefing.")


# 8. ACOUSTIC STATE MACHINE
def listen_for_acoustic_events(target_sound):
    CHUNK            = 512
    RATE             = 44100
    VOLUME_THRESHOLD = 1200

    p      = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    claps_detected = 0
    last_clap_time = 0
    cooldown       = False
    cooldown_until = 0

    while True:
        data         = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        peak         = np.max(np.abs(data))
        current_time = time.time()

        if cooldown and current_time < cooldown_until:
            continue
        cooldown = False

        if peak > VOLUME_THRESHOLD:
            fft_data  = np.abs(np.fft.rfft(data))
            fft_freqs = np.fft.rfftfreq(CHUNK, 1.0 / RATE)

            low_energy  = np.sum(fft_data[(fft_freqs > 500)  & (fft_freqs < 2500)]) + 1
            high_energy = np.sum(fft_data[(fft_freqs > 3500) & (fft_freqs < 8000)])
            ratio       = high_energy / low_energy

            if target_sound == "clap" and 0.08 < ratio <= 2.5:
                if claps_detected == 0:
                    claps_detected = 1
                    last_clap_time = current_time
                    print("--> [1st Clap] Waiting for 2nd...")
                    cooldown       = True
                    cooldown_until = current_time + 0.08
                elif claps_detected == 1:
                    time_passed = current_time - last_clap_time
                    if 0.08 < time_passed <= 0.9:
                        print("--> [2nd Clap Confirmed!] Initializing...")
                        stream.stop_stream(); stream.close(); p.terminate()
                        return "clap"
                    elif time_passed > 0.9:
                        print("--> [Reset] New 1st clap detected.")
                        claps_detected = 1
                        last_clap_time = current_time
                        cooldown       = True
                        cooldown_until = current_time + 0.08

            elif target_sound == "snap" and ratio > 1.5:
                stream.stop_stream(); stream.close(); p.terminate()
                return "snap"

        if claps_detected == 1 and (current_time - last_clap_time) > 0.9:
            claps_detected = 0


# 9. CHILL MODE — TRIPLE CLAP EXIT
def chill_mode_acoustic_guard():
    """
    Mic stays ON but ignores everything except triple clap.
    Filters all speech, music, room noise via FFT.
    3 claps within 3 seconds triggers exit.
    """
    CHUNK      = 512
    RATE       = 44100
    THRESHOLD  = 1200
    clap_times = []

    print("\n--> [CHILL MODE] Acoustic filter active. Triple clap to exit.")

    p      = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    while True:
        try:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            peak = np.max(np.abs(data))

            if peak > THRESHOLD:
                fft_data  = np.abs(np.fft.rfft(data))
                fft_freqs = np.fft.rfftfreq(CHUNK, 1.0 / RATE)

                speech_energy = np.sum(fft_data[(fft_freqs > 300)  & (fft_freqs < 3000)])
                snap_energy   = np.sum(fft_data[(fft_freqs > 3500) & (fft_freqs < 8000)])
                low_energy    = np.sum(fft_data[(fft_freqs > 500)  & (fft_freqs < 2500)]) + 1
                ratio         = snap_energy / low_energy

                is_clap = ratio > 1.5 and snap_energy > speech_energy * 0.8

                if is_clap:
                    now = time.time()
                    clap_times.append(now)
                    clap_times[:] = [t for t in clap_times if now - t <= 3.0]
                    print(f"--> [Clap {len(clap_times)}/3]")
                    if len(clap_times) >= 3:
                        print("--> [Triple Clap] Exiting chill mode.")
                        break

        except Exception:
            continue

    stream.stop_stream()
    stream.close()
    p.terminate()


# 10. TASK GROUPS
def open_task_group(mode):
    if mode == "break":
        pyautogui.hotkey('win', 'd')
        speak("Alright sir, let me take a break. Everything is minimized.")
        return

    elif mode == "today":
        speak("Alright, shutting down everything. Good work today, see you tomorrow sir.")

        os.system("taskkill /f /im chrome.exe /T")

        import subprocess as sp

        VSCODE_PATH    = r"C:\Users\ASUS\AppData\Local\Programs\Microsoft VS Code\Code.exe".lower()
        protected_pids = {str(os.getpid())}

        wmic_result = sp.run(
            'wmic process get ProcessId,ExecutablePath /format:csv',
            shell=True, capture_output=True, text=True
        )
        for line in wmic_result.stdout.strip().splitlines():
            if VSCODE_PATH in line.lower():
                parts = line.split(',')
                pid   = parts[-1].strip()
                if pid.isdigit():
                    protected_pids.add(pid)
                    print(f"--> Protected VSCode PID: {pid}")

        killed_pids = set()

        def kill_by_keyword(keyword):
            result = sp.run(
                'tasklist /fo csv /nh',
                shell=True, capture_output=True, text=True
            )
            for line in result.stdout.strip().splitlines():
                if keyword.lower() not in line.lower():
                    continue
                proc_name = line.split(',')[0].strip('"')
                pid       = line.split(',')[1].strip('"')

                if pid in protected_pids:
                    print(f"--> Skipping protected: {proc_name} (PID {pid})")
                    continue
                if pid in killed_pids:
                    continue

                result2 = sp.run(
                    f"taskkill /f /pid {pid} /T",
                    shell=True, capture_output=True, text=True
                )
                killed_pids.add(pid)

                stdout = result2.stdout.strip()
                if stdout and "SUCCESS" in stdout:
                    import re
                    child_pids = re.findall(r'PID (\d+)', stdout)
                    killed_pids.update(child_pids)
                    print(f"--> Killed: {proc_name} (PID {pid}) + {len(child_pids)-1} children")

        kill_by_keyword("whatsapp")
        kill_by_keyword("claude")

        time.sleep(1)
        verify     = sp.run('tasklist /fo csv /nh', shell=True, capture_output=True, text=True)
        proc_names = [
            line.split(',')[0].strip('"').lower()
            for line in verify.stdout.strip().splitlines()
            if line.strip()
        ]
        wa_still_running     = any("whatsapp" in p for p in proc_names)
        claude_still_running = any(
            "claude" in p for p in proc_names
            if p not in ("python.exe", "python3.exe", "")
        )

        if wa_still_running:
            print("--> WARNING: WhatsApp still running.")
            speak("WhatsApp is resisting sir, it may need manual close.")
        if claude_still_running:
            print("--> WARNING: Claude still running.")
            speak("Claude is still up sir, it may need manual close.")

        speak("All systems closed. Later sir.")
        return

    pyautogui.hotkey('win', 'd')
    time.sleep(0.5)

    if mode == "work":
        speak("Alright, let's get back to work sir.")
        vscode = r"C:\Users\ASUS\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        claude = r"C:\Users\ASUS\AppData\Local\AnthropicClaude\claude.exe"
        if os.path.exists(vscode): subprocess.Popen([vscode])
        if os.path.exists(claude): subprocess.Popen([claude])
        os.system("start whatsapp:")
        launch_chrome("https://gemini.google.com/app", CHROME_WORK_PROFILE)
        launch_chrome("https://mail.google.com/mail/u/0/", CHROME_WORK_PROFILE)
        launch_chrome("chrome://newtab", CHROME_WORK_PROFILE)

    elif mode == "chill":
        speak("Yeah sir, let's chill.")
        launch_chrome("https://www.youtube.com/", CHROME_KUSHAL_PROFILE)
        sites = [
            "https://animesuge.cz/",
            "https://toonstream.dad/home/",
            "https://animesalt.top/",
            "https://flixer.sh/"
        ]
        for site in sites:
            launch_chrome(site, CHROME_ALT_PROFILE)

        speak("Enjoy sir. Triple clap anytime to exit chill mode and minimize everything.")
        chill_mode_acoustic_guard()
        pyautogui.hotkey('win', 'd')
        speak("Triple clap detected sir. Minimizing everything. Back to snapby mode.")
        print("--> [CHILL MODE] Exited. Acoustic filter off.")

    elif mode == "messages":
        speak("Okay, here are your messages sir.")
        launch_chrome("https://www.instagram.com/", CHROME_WORK_PROFILE)
        os.system("start whatsapp:")


# 11. MAIN JARVIS LOOP
def run_jarvis():
    r = sr.Recognizer()

    print("\n" + "="*50)
    print("PHASE 1: SYSTEM BOOT")
    print("Double-clap to wake Jarvis...")
    print("="*50)

    listen_for_acoustic_events(target_sound="clap")

    speak("Boot sequence initiated.")
    music_path = os.path.join(PROJECT_DIR, "assets", "rock_guiter.mp3")

    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Audio engine error: {e}")
    else:
        print(f"Music file missing: {music_path}")

    print("\n[LISTENING] Say 'wake up' to continue, or 'skip' to go straight to snapby...")

    wake_word_heard = False
    skip_word_heard = False

    while not wake_word_heard and not skip_word_heard:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.8)
            r.energy_threshold = 200
            try:
                audio   = r.listen(source, timeout=None, phrase_time_limit=6)
                command = r.recognize_google(audio, language='en-in').lower()
                print(f"Heard: {command}")

                if "wake up" in command:
                    wake_word_heard = True
                elif "skip" in command:
                    skip_word_heard = True
                    user_say(command)
                    print("--> Skip detected. Jumping to snapby.")
                else:
                    user_say(command)
                    print("--> Waiting for 'wake up' or 'skip'...")

            except sr.UnknownValueError:
                print("--> Couldn't understand. Still listening...")
                continue
            except sr.RequestError as e:
                print(f"--> Google Speech API error: {e}. Retrying...")
                time.sleep(1)
                continue
            except OSError as e:
                print(f"--> [Socket error in wake loop] {e}. Retrying...")
                time.sleep(1)
                continue

    pygame.mixer.music.fadeout(1500)

    if skip_word_heard:
        speak("Alright, standing by sir.")
    else:
        user_say("wake up")
        greet_me()

    print("\n" + "="*50)
    print("PHASE 3: SNAP MODE")
    print("Commands: WORK | CHILL | MESSAGES | BREAK | TODAY | NEW | READ | CONTINUE")
    print("NEW = fetch fresh news anytime | READ = replay last news | CONTINUE = resume at left off news with recall news")
    print("="*50)

    if wake_word_heard:
        time_label, news_mode = get_time_of_day()
        speak(f"It's {time_label} sir. Let me get today's global news for you.")
        if news_mode == "morning":
            raw_news = get_newsapi_dump()
        else:
            raw_news = get_rss_dump()
        if raw_news:
            speak("Got the news sir. Based on your interests, categorizing and prioritizing news for you now.")
            deliver_news_briefing(raw_news, mode=news_mode, r_recognizer=r)
        else:
            speak("Could not fetch the news sir. Check your connection or API key.")

    while True:
        listen_for_acoustic_events(target_sound="snap")
        print("\n--> Jarvis: Awaiting command...")

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.energy_threshold = 250
            try:
                audio = r.listen(source, timeout=8, phrase_time_limit=5)
                mode  = r.recognize_google(audio, language='en-in').lower()
                print(f"Heard Task: {mode}")
                user_say(mode)

                if "work" in mode:
                    open_task_group("work")

                elif "chill" in mode:
                    open_task_group("chill")

                elif "message" in mode:
                    open_task_group("messages")

                elif "break" in mode:
                    open_task_group("break")

                elif "today" in mode:
                    open_task_group("today")

                elif "continue" in mode:
                    if NEWS_SESSION["categories_data"] and NEWS_SESSION["left_cat_idx"] is not None:
                        speak("Welcome back sir. Let me pick up right where we left off.")
                        deliver_news_briefing(None, mode=NEWS_SESSION["mode"], r_recognizer=r, resume=True)
                    else:
                        speak("No interrupted news to resume sir. Snap and say READ to replay last briefing, or NEW to fetch fresh news.")

                elif "read" in mode:
                    if LAST_COMPLETED_SESSION["categories_data"]:
                        speak("Replaying the last briefing from the top sir.")
                        NEWS_SESSION["categories_data"] = LAST_COMPLETED_SESSION["categories_data"]
                        NEWS_SESSION["all_urls"]        = LAST_COMPLETED_SESSION["all_urls"]
                        NEWS_SESSION["yt_queries"]      = LAST_COMPLETED_SESSION["yt_queries"]
                        NEWS_SESSION["full_text_dump"]  = LAST_COMPLETED_SESSION["full_text_dump"]
                        NEWS_SESSION["mode"]            = LAST_COMPLETED_SESSION["mode"]
                        NEWS_SESSION["left_cat_idx"]    = 0
                        NEWS_SESSION["left_item_idx"]   = 0
                        deliver_news_briefing(None, mode=NEWS_SESSION["mode"], r_recognizer=r, resume=True)
                    else:
                        speak("No previous briefing to replay sir. Snap and say NEW to fetch news.")

                elif "new" in mode:
                    time_label, news_mode = get_time_of_day()
                    speak(f"Got it sir. Fetching the latest {time_label} news for you right now.")
                    if news_mode == "morning":
                        raw = get_newsapi_dump()
                    else:
                        raw = get_rss_dump()
                    if raw:
                        deliver_news_briefing(raw, mode=news_mode, r_recognizer=r)
                    else:
                        speak("Could not fetch news sir. Check your connection.")

                else:
                    print(f"--> Command '{mode}' not recognized.")
                    speak("Didn't catch that sir. Try again.")

            except sr.WaitTimeoutError:
                print("Timed out. Snap to try again.")
            except sr.UnknownValueError:
                print("--> Couldn't understand. Snap to try again.")
            except sr.RequestError as e:
                print(f"--> [Network error in snapby] {e}. Snap to try again.")
            except OSError as e:
                print(f"--> [Socket error in snapby] {e}. Snap to try again.")
            except Exception as e:
                print(f"--> [Snapby error] {e}. Snap to try again.")

        check_evening_briefing(r)


# 12. ENTRY POINT
if __name__ == "__main__":
    run_jarvis()