"""
Application launcher tools: open apps and URLs on the device.
"""

import needle
from harness.runner import run_cmd
from harness.config import APP_URLS, APP_PACKAGES, APP_ACTIVITIES


@needle.tool
def open_app(app_name: str):
    """
    Open an app or URL on the phone.
    Supports: whatsapp, youtube, chrome, instagram, spotify, telegram,
    facebook, twitter/x, gmail, maps, calculator, settings, camera,
    or any URL starting with http/https.
    """
    print(f"[Tool] open_app('{app_name}')")
    raw = app_name.strip().lower()
    clean = raw.replace("open", "").replace("the", "").replace("app", "").strip()

    # Direct URL
    if raw.startswith("http://") or raw.startswith("https://"):
        run_cmd(["termux-open-url", raw])
        return f"Opened URL: {raw}"

    # Find matching key
    target = None
    for key in (clean, raw):
        if key in APP_URLS or key in APP_PACKAGES or key in APP_ACTIVITIES:
            target = key
            break
    if not target:
        for key in APP_URLS:
            if key in clean or clean in key:
                target = key
                break

    if target:
        if target in APP_URLS:
            run_cmd(["termux-open-url", APP_URLS[target]])
        if target in APP_PACKAGES:
            run_cmd(["monkey", "-p", APP_PACKAGES[target], "--user", "0",
                      "-c", "android.intent.category.LAUNCHER", "1"])
        if target in APP_ACTIVITIES:
            run_cmd(["am", "start", "--user", "0", "-n", APP_ACTIVITIES[target]])
        return f"Opened: {app_name}"

    # Fallback: try as package name
    pkg = raw if "." in raw else f"com.{raw}"
    run_cmd(["monkey", "-p", pkg, "--user", "0",
              "-c", "android.intent.category.LAUNCHER", "1"])
    return f"Attempted to open: {app_name}"
