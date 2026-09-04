"""
Media tools: camera capture, audio recording, text-to-speech.
"""

import os
import subprocess
import needle
from harness.runner import run_cmd
from harness.config import PHOTO_PATHS


@needle.tool
def take_camera_photo():
    """Capture a photo with the back camera and save to Downloads."""
    print("[Tool] take_camera_photo()")
    for target in PHOTO_PATHS:
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            res = run_cmd(["termux-camera-photo", "-c", "0", target])
            if os.path.exists(target) and os.path.getsize(target) > 0:
                return f"Photo saved to: {target}"
        except Exception:
            continue
    return "Camera failed. Check Termux:API has Camera + Storage permissions."


@needle.tool
def text_to_speech(text: str):
    """Speak text aloud using the device TTS engine."""
    print(f"[Tool] text_to_speech('{text}')")
    try:
        res = subprocess.run(
            ["termux-tts-speak"],
            input=text, capture_output=True, text=True, timeout=10
        )
        if res.returncode != 0:
            return f"Error: {res.stderr.strip()}"
        return "Speech triggered."
    except (FileNotFoundError, PermissionError):
        return f"[Sim] TTS spoke: '{text}'"
    except Exception as e:
        return f"Error: {e}"


@needle.tool
def record_audio_start(file_path: str = "recording.3gp", limit_seconds: int = 0):
    """Start recording audio from the microphone."""
    print(f"[Tool] record_audio_start('{file_path}')")
    cmd = ["termux-microphone-record", "-f", file_path]
    if limit_seconds > 0:
        cmd.extend(["-l", str(limit_seconds)])
    return run_cmd(cmd)


@needle.tool
def record_audio_stop():
    """Stop the current audio recording."""
    print("[Tool] record_audio_stop()")
    return run_cmd(["termux-microphone-record", "-q"])
