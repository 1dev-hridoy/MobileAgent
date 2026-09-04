"""
Tool registry — imports all tool modules and exports a flat list of tools.
This is the single source of truth for what the agent can do.
"""

from harness.tools.system import (
    show_toast, show_notification, get_battery_status,
    set_clipboard, get_clipboard, set_screen_brightness,
    get_volume_info, set_volume, share_content,
)
from harness.tools.hardware import (
    set_torch, vibrate_device, authenticate_fingerprint, get_location,
)
from harness.tools.communication import (
    send_sms, make_phone_call, get_sms_messages,
    get_contacts, get_call_log,
)
from harness.tools.media import (
    take_camera_photo, text_to_speech,
    record_audio_start, record_audio_stop,
)
from harness.tools.network import (
    get_wifi_info, scan_wifi_networks, download_file,
    get_telephony_info,
)
from harness.tools.apps import open_app

ALL_TOOLS = [
    # System
    show_toast, show_notification, get_battery_status,
    set_clipboard, get_clipboard, set_screen_brightness,
    get_volume_info, set_volume, share_content,
    # Hardware
    set_torch, vibrate_device, authenticate_fingerprint, get_location,
    # Communication
    send_sms, make_phone_call, get_sms_messages,
    get_contacts, get_call_log,
    # Media
    take_camera_photo, text_to_speech,
    record_audio_start, record_audio_stop,
    # Network
    get_wifi_info, scan_wifi_networks, download_file,
    get_telephony_info,
    # Apps
    open_app,
]
