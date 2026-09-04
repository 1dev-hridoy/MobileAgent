"""
Unified command executor for Termux API calls.
On Termux: runs real commands with timeout.
Off Termux: returns simulated responses for desktop testing.
"""

import json
import subprocess
from harness.config import CMD_TIMEOUT, IS_TERMUX


def run_cmd(args: list[str], timeout: int = CMD_TIMEOUT) -> str:
    """Execute a command and return its output. Falls back to simulation on desktop."""
    try:
        res = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            return res.stdout.strip() if res.stdout.strip() else "Success"
        if IS_TERMUX:
            err = res.stderr.strip() or res.stdout.strip() or f"Exit code {res.returncode}"
            return f"Error ({args[0]}): {err}"
        raise FileNotFoundError
    except subprocess.TimeoutExpired:
        if IS_TERMUX:
            return f"Error ({args[0]}): Timed out after {timeout}s. Check Termux:API permissions."
        raise FileNotFoundError
    except (FileNotFoundError, PermissionError, subprocess.SubprocessError):
        if IS_TERMUX:
            return f"Error ({args[0]}): Execution failed in Termux."
        return _simulate(args)


def run_cmd_json(args: list[str], timeout: int = CMD_TIMEOUT):
    """Execute command and parse JSON output. Returns dict/list or raw string."""
    res = run_cmd(args, timeout)
    try:
        return json.loads(res)
    except (json.JSONDecodeError, TypeError):
        return res


# ─── Simulation layer (desktop testing) ───────────────────────────────

def _get_arg(args: list[str], idx: int, default: str = "") -> str:
    return args[idx] if 0 < idx < len(args) else default


def _get_flag(args: list[str], flag: str, default: str = "") -> str:
    """Get value after a flag like --title or -d."""
    if flag in args:
        idx = args.index(flag) + 1
        return args[idx] if idx < len(args) else default
    return default


def _simulate(args: list[str]) -> str:
    """Return simulated responses for each known Termux command."""
    cmd = args[0]
    sims = {
        "termux-battery-status": lambda: json.dumps({
            "health": "GOOD", "percentage": 87, "plugged": "UNPLUGGED",
            "status": "DISCHARGING", "temperature": 29.5, "current": -240
        }),
        "termux-toast": lambda: f"[Sim] Toast: '{_get_arg(args, 1)}'",
        "termux-notification": lambda: f"[Sim] Notification: {_get_flag(args, '--title', 'System')} — {_get_flag(args, '--content', 'Alert')}",
        "termux-tts-speak": lambda: f"[Sim] TTS spoke: '{_get_arg(args, 1)}'",
        "termux-clipboard-set": lambda: f"[Sim] Clipboard set: '{_get_arg(args, 1)}'",
        "termux-clipboard-get": lambda: "Simulated clipboard content",
        "termux-vibrate": lambda: f"[Sim] Vibrated for {_get_flag(args, '-d', '500')}ms",
        "termux-torch": lambda: f"[Sim] Flashlight {_get_arg(args, 1).upper()}",
        "termux-location": lambda: json.dumps({
            "latitude": 37.7749, "longitude": -122.4194,
            "altitude": 18.2, "accuracy": 15.0, "provider": "gps"
        }),
        "termux-sms-send": lambda: f"[Sim] SMS to {_get_flag(args, '-n', '?')}: '{_get_arg(args, 3) if len(args) > 3 else ''}'",
        "termux-telephony-call": lambda: f"[Sim] Calling {_get_arg(args, 1)}",
        "termux-wifi-connectioninfo": lambda: json.dumps({
            "ssid": "Home_5G", "ip": "192.168.1.108",
            "link_speed_mbps": 866, "rssi": -48, "supplicant_state": "COMPLETED"
        }),
        "termux-camera-photo": lambda: f"[Sim] Photo saved",
        "termux-sms-list": lambda: json.dumps([
            {"address": "+1234567890", "body": "Hey!", "date": "2026-08-30 12:00:00", "read": True, "type": "inbox"},
            {"address": "OTP-BANK", "body": "Your OTP is 582103", "date": "2026-08-30 11:45:00", "read": False, "type": "inbox"}
        ]),
        "termux-contact-list": lambda: json.dumps([
            {"name": "Alice", "number": "+1987654321"},
            {"name": "Bob", "number": "+15550199"}
        ]),
        "termux-download": lambda: f"[Sim] Downloading from URL",
        "termux-brightness": lambda: f"[Sim] Brightness set to {_get_arg(args, 1)}",
        "termux-volume": lambda: (
            json.dumps([
                {"stream": "music", "volume": 11, "max_volume": 15},
                {"stream": "ring", "volume": 5, "max_volume": 7}
            ]) if len(args) <= 2
            else f"[Sim] Volume {_get_arg(args, 1)} set to {_get_arg(args, 2)}"
        ),
        "termux-share": lambda: f"[Sim] Shared content via share sheet",
        "termux-call-log": lambda: json.dumps([
            {"name": "Alice", "number": "+1987654321", "duration": "2m 14s", "date": "2026-08-31 10:15:22", "type": "incoming"},
            {"name": "Bob", "number": "+15550199", "duration": "0s", "date": "2026-08-30 18:44:10", "type": "missed"}
        ]),
        "termux-fingerprint": lambda: json.dumps({"auth_result": "AUTH_SUCCESS", "errors": None}),
        "termux-microphone-record": lambda: (
            "[Sim] Recording stopped" if "-q" in args
            else f"[Sim] Recording started"
        ),
        "termux-telephony-deviceinfo": lambda: json.dumps({
            "data_state": "DATA_CONNECTED", "device_id": "864209753197531",
            "network_operator": "Google Fi", "network_type": "LTE",
            "sim_state": "SIM_STATE_READY"
        }),
        "termux-wifi-scaninfo": lambda: json.dumps([
            {"bssid": "aa:bb:cc:dd:ee:ff", "ssid": "Home_5G", "rssi": -55},
            {"bssid": "11:22:33:44:55:66", "ssid": "Cafe_Free", "rssi": -72}
        ]),
    }

    handler = sims.get(cmd)
    if handler:
        return handler()
    if cmd in ("monkey", "am"):
        pkg = args[args.index("-p") + 1] if "-p" in args else "app"
        return f"[Sim] Launched: {pkg}"
    return f"[Sim] Executed: {' '.join(args)}"
