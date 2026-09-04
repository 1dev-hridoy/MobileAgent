# ⬡ Harness — Mobile Agent

A lightweight, modular AI agent for Android/Termux that controls your phone via natural language. Powered by **Needle (14MB)** local LLM.

## Features

- **Natural Language Control** — talk to your phone in plain English
- **Web UI** — sleek glassmorphic dashboard for interaction
- **Telegram Bot** — control your phone remotely via Telegram
- **CLI Mode** — interactive terminal chat
- **Desktop Simulation** — test on any OS without Termux
- **27+ Tools** — system, hardware, communication, media, network, apps

## Quick Install (Single Command)

**On Android/Termux:**

```bash
curl -sL https://raw.githubusercontent.com/1dev-hridoy/MobileAgent/main/install.sh | bash
```

**On Desktop (Linux/macOS):**

```bash
curl -sL https://raw.githubusercontent.com/1dev-hridoy/MobileAgent/main/install.sh | bash
```

Or clone manually:

```bash
git clone https://github.com/1dev-hridoy/MobileAgent.git
cd MobileAgent/harness
pip install -r requirements.txt
```

## Usage

After the one-line install, it lands in `~/harness`. Activate and run:

```bash
cd ~/harness/harness   # or: cd ~/harness  (if package is at repo root)
source ../venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null || true
python -m harness                # Interactive CLI
python -m harness web            # Web UI (http://localhost:5000)
python -m harness web 8080       # Custom port
python -m harness telegram TOKEN # Telegram bot
python -m harness all            # Web + Telegram together
```

> Tip: The installer prints the exact `cd` + activate + run commands at the end — just copy them.

**Manual setup from GitHub (no installer):**

```bash
git clone https://github.com/1dev-hridoy/MobileAgent.git
cd MobileAgent/harness
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m harness
```

## Available Tools (27)

### System

| Tool                    | Description                      |
| ----------------------- | -------------------------------- |
| `show_toast`            | Display toast notification       |
| `show_notification`     | System notification drawer       |
| `get_battery_status`    | Battery percentage, health, temp |
| `set_clipboard`         | Copy text to clipboard           |
| `get_clipboard`         | Read clipboard content           |
| `set_screen_brightness` | Adjust screen brightness (0-255) |
| `get_volume_info`       | Get all volume levels            |
| `set_volume`            | Set volume for a stream          |
| `share_content`         | Share text/file via share sheet  |

### Hardware

| Tool                       | Description                |
| -------------------------- | -------------------------- |
| `set_torch`                | Turn flashlight ON/OFF     |
| `vibrate_device`           | Vibrate for N milliseconds |
| `authenticate_fingerprint` | Fingerprint auth prompt    |
| `get_location`             | GPS coordinates            |

### Communication

| Tool               | Description           |
| ------------------ | --------------------- |
| `send_sms`         | Send text message     |
| `make_phone_call`  | Dial a phone number   |
| `get_sms_messages` | Read recent SMS inbox |
| `get_contacts`     | List phone contacts   |
| `get_call_log`     | Recent call history   |

### Media

| Tool                 | Description                 |
| -------------------- | --------------------------- |
| `take_camera_photo`  | Capture photo (back camera) |
| `text_to_speech`     | Speak text aloud            |
| `record_audio_start` | Start mic recording         |
| `record_audio_stop`  | Stop mic recording          |

### Network

| Tool                 | Description                      |
| -------------------- | -------------------------------- |
| `get_wifi_info`      | Current WiFi connection details  |
| `scan_wifi_networks` | Scan nearby WiFi networks        |
| `download_file`      | Download file via system manager |
| `get_telephony_info` | SIM, network, IMEI info          |

### Apps

| Tool       | Description           |
| ---------- | --------------------- |
| `open_app` | Launch any app or URL |

## Project Structure

```
harness/
├── install.sh          # Single-command installer
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── main.py             # Entry point (for direct execution)
├── __init__.py         # Package init
├── __main__.py         # python -m harness support
├── config.py           # Centralized configuration
├── runner.py           # Command executor + simulation layer
├── agent.py            # Needle LLM initialization
├── web.py              # Flask web UI + REST API
├── telegram_bot.py     # Telegram remote control
├── cli.py              # Interactive CLI
└── tools/              # Modular tool definitions
    ├── __init__.py     # Tool registry (exports ALL_TOOLS)
    ├── system.py       # System tools
    ├── hardware.py     # Hardware tools
    ├── communication.py # Communication tools
    ├── media.py        # Media tools
    ├── network.py      # Network tools
    └── apps.py         # App launcher tools
```

## Prerequisites (Android)

1. Install [Termux](https://f-droid.org/en/packages/com.termux/) from F-Droid
2. Install [Termux:API](https://f-droid.org/en/packages/com.termux.api/) from F-Droid
3. Grant necessary permissions to Termux:API in Android Settings

## Adding Custom Tools

Create a new file in `tools/` and use the `@needle.tool` decorator:

```python
import needle
from harness.runner import run_cmd

@needle.tool
def my_custom_tool(param: str):
    """Description of what this tool does."""
    return run_cmd(["termux-some-command", param])
```

Then add it to `tools/__init__.py`:

```python
from harness.tools.my_module import my_custom_tool

ALL_TOOLS = [
    ...,
    my_custom_tool,
]
```

## License

MIT
