"""
System-level tools: battery, toast, notification, clipboard, brightness, volume, share.
"""

import json
import needle
from harness.runner import run_cmd, run_cmd_json


@needle.tool
def show_toast(message: str):
    """Display a brief toast notification popup on the phone screen."""
    print(f"[Tool] show_toast('{message}')")
    return run_cmd(["termux-toast", message])


@needle.tool
def show_notification(title: str, content: str):
    """Display a system notification with a title and message content."""
    print(f"[Tool] show_notification('{title}', '{content}')")
    return run_cmd(["termux-notification", "--title", title, "--content", content])


@needle.tool
def get_battery_status():
    """Get battery details: percentage, status, health, temperature."""
    print("[Tool] get_battery_status()")
    return run_cmd_json(["termux-battery-status"])


@needle.tool
def set_clipboard(text: str):
    """Copy text to the device clipboard."""
    print(f"[Tool] set_clipboard('{text}')")
    return run_cmd(["termux-clipboard-set", text])


@needle.tool
def get_clipboard():
    """Read the current text from the device clipboard."""
    print("[Tool] get_clipboard()")
    return run_cmd(["termux-clipboard-get"])


@needle.tool
def set_screen_brightness(level: str):
    """Set screen brightness. Use 0-255 or 'auto'."""
    print(f"[Tool] set_screen_brightness('{level}')")
    return run_cmd(["termux-brightness", str(level)])


@needle.tool
def get_volume_info():
    """Get current volume levels for all audio streams."""
    print("[Tool] get_volume_info()")
    return run_cmd_json(["termux-volume"])


@needle.tool
def set_volume(stream: str, volume: int):
    """Set volume for an audio stream (alarm, music, notification, ring, system, call)."""
    print(f"[Tool] set_volume('{stream}', {volume})")
    return run_cmd(["termux-volume", stream, str(volume)])


@needle.tool
def share_content(text: str = "", file_path: str = ""):
    """Share text or a file via the Android share sheet."""
    print(f"[Tool] share_content(text='{text}', file='{file_path}')")
    import subprocess
    if file_path:
        return run_cmd(["termux-share", "-a", "send", file_path])
    elif text:
        try:
            res = subprocess.run(
                ["termux-share", "-a", "send"],
                input=text, capture_output=True, text=True, timeout=10
            )
            return res.stdout.strip() if res.returncode == 0 else f"Error: {res.stderr.strip()}"
        except Exception as e:
            return f"Error: {e}"
    return "Error: Provide text or file_path."
