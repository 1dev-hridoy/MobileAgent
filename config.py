"""
Centralized configuration for the Harness Mobile Agent.
All settings in one place — no magic strings scattered across files.
"""

import os

# ── Paths ──────────────────────────────────────────────────────────────
TERMUX_BIN_PATH = "/data/data/com.termux/files/usr/bin"
TERMUX_ROOT = "/data/data/com.termux"
STORAGE_DIR = os.path.expanduser("~/storage")
DOWNLOAD_DIR = "/sdcard/Download"
PHOTO_SAVE_DIR = os.path.join(DOWNLOAD_DIR, "harness_photos")

# ── Runtime detection ──────────────────────────────────────────────────
IS_TERMUX = os.path.exists(TERMUX_ROOT)

# ── Command execution ──────────────────────────────────────────────────
CMD_TIMEOUT = 15  # seconds

# ── Web server ─────────────────────────────────────────────────────────
WEB_HOST = "0.0.0.0"
WEB_PORT = int(os.environ.get("HARNESS_PORT", 5000))

# ── Telegram (set via env or CLI flag) ─────────────────────────────────
TELEGRAM_TOKEN = os.environ.get("HARNESS_TELEGRAM_TOKEN", "")

# ── Photo capture paths (tried in order) ───────────────────────────────
PHOTO_PATHS = [
    os.path.join(DOWNLOAD_DIR, "harness_photo.jpg"),
    os.path.join(STORAGE_DIR, "downloads", "harness_photo.jpg"),
    os.path.join(os.path.expanduser("~"), "harness_photo.jpg"),
]

# ── App launch database ────────────────────────────────────────────────
APP_URLS = {
    "youtube": "https://www.youtube.com",
    "yt": "https://www.youtube.com",
    "whatsapp": "https://api.whatsapp.com",
    "wa": "https://api.whatsapp.com",
    "chrome": "http://google.com",
    "google": "http://google.com",
    "browser": "http://google.com",
    "instagram": "https://instagram.com",
    "insta": "https://instagram.com",
    "spotify": "https://open.spotify.com",
    "telegram": "https://t.me",
    "facebook": "https://facebook.com",
    "fb": "https://facebook.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "gmail": "mailto:",
    "maps": "https://maps.google.com",
    "google maps": "https://maps.google.com",
}

APP_PACKAGES = {
    "youtube": "com.google.android.youtube",
    "whatsapp": "com.whatsapp",
    "chrome": "com.android.chrome",
    "instagram": "com.instagram.android",
    "spotify": "com.spotify.music",
    "telegram": "org.telegram.messenger",
    "facebook": "com.facebook.katana",
    "gmail": "com.google.android.gm",
    "maps": "com.google.android.apps.maps",
    "settings": "com.android.settings",
    "calculator": "com.google.android.calculator",
    "camera": "com.android.camera",
}

APP_ACTIVITIES = {
    "settings": "com.android.settings/.Settings",
    "calculator": "com.google.android.calculator/com.android.calculator2.Calculator",
    "camera": "com.android.camera/com.android.camera.Camera",
}
