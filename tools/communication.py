"""
Communication tools: SMS, phone calls, call logs, contacts.
"""

import json
import needle
from harness.runner import run_cmd, run_cmd_json


@needle.tool
def send_sms(recipient: str, message: str):
    """Send an SMS text message to a phone number."""
    print(f"[Tool] send_sms('{recipient}', '{message}')")
    return run_cmd(["termux-sms-send", "-n", recipient, message])


@needle.tool
def make_phone_call(phone_number: str):
    """Initiate a voice call to a phone number."""
    print(f"[Tool] make_phone_call('{phone_number}')")
    return run_cmd(["termux-telephony-call", phone_number])


@needle.tool
def get_sms_messages(limit: int = 5):
    """Retrieve recent incoming SMS messages."""
    print(f"[Tool] get_sms_messages(limit={limit})")
    return run_cmd_json(["termux-sms-list", "-l", str(limit)])


@needle.tool
def get_contacts():
    """Retrieve the phone's contact list (names and numbers)."""
    print("[Tool] get_contacts()")
    return run_cmd_json(["termux-contact-list"])


@needle.tool
def get_call_log(limit: int = 5):
    """Retrieve recent call history."""
    print(f"[Tool] get_call_log(limit={limit})")
    return run_cmd_json(["termux-call-log", "-l", str(limit)])
