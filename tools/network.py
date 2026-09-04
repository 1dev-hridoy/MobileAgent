"""
Network & connectivity tools: WiFi, downloads, device telephony info.
"""

import needle
from harness.runner import run_cmd, run_cmd_json


@needle.tool
def get_wifi_info():
    """Get details of the active WiFi connection (SSID, IP, speed, signal)."""
    print("[Tool] get_wifi_info()")
    return run_cmd_json(["termux-wifi-connectioninfo"])


@needle.tool
def scan_wifi_networks():
    """Scan for nearby WiFi networks and their signal strengths."""
    print("[Tool] scan_wifi_networks()")
    return run_cmd_json(["termux-wifi-scaninfo"])


@needle.tool
def download_file(url: str, title: str = "Download"):
    """Download a file from a URL using the system download manager."""
    print(f"[Tool] download_file('{url}', '{title}')")
    return run_cmd(["termux-download", "-t", title, url])


@needle.tool
def get_telephony_info():
    """Get device telephony info: network operator, SIM state, network type, IMEI."""
    print("[Tool] get_telephony_info()")
    return run_cmd_json(["termux-telephony-deviceinfo"])
