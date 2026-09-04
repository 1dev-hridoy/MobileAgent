"""
Hardware control tools: torch, vibration, fingerprint, GPS location.
"""

import json
import needle
from harness.runner import run_cmd, run_cmd_json


@needle.tool
def set_torch(on: bool):
    """Turn the camera flash/torch ON (True) or OFF (False)."""
    print(f"[Tool] set_torch({on})")
    return run_cmd(["termux-torch", "on" if on else "off"])


@needle.tool
def vibrate_device(duration_ms: int = 500):
    """Vibrate the phone for a given number of milliseconds."""
    print(f"[Tool] vibrate_device({duration_ms}ms)")
    return run_cmd(["termux-vibrate", "-d", str(duration_ms)])


@needle.tool
def authenticate_fingerprint():
    """Prompt for fingerprint authentication to verify user identity."""
    print("[Tool] authenticate_fingerprint()")
    return run_cmd_json(["termux-fingerprint"])


@needle.tool
def get_location():
    """Get the device's GPS coordinates (latitude, longitude, altitude)."""
    print("[Tool] get_location()")
    return run_cmd_json(["termux-location", "-p", "network", "-r", "last"])
