"""
Unified entry point for the Harness Mobile Agent.

Usage:
  python -m harness                 # Interactive CLI
  python -m harness web             # Web UI (browser)
  python -m harness web --port 8080 # Custom port
  python -m harness telegram        # Telegram bot
  python -m harness all             # Web + Telegram
"""

import sys
import os

# Ensure harness package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harness.config import TELEGRAM_TOKEN, WEB_PORT


def main():
    args = sys.argv[1:]
    mode = args[0].lower() if args else "cli"

    if mode == "web":
        from harness.web import start_web
        port = int(args[1]) if len(args) > 1 and args[1].isdigit() else WEB_PORT
        # Optionally start Telegram alongside web
        if "--telegram" in args:
            tidx = args.index("--telegram") + 1
            token = args[tidx] if tidx < len(args) else TELEGRAM_TOKEN
            if token:
                from harness.telegram_bot import start_telegram
                start_telegram(token)
        start_web(port=port)

    elif mode == "telegram":
        token = args[1] if len(args) > 1 else TELEGRAM_TOKEN
        if not token:
            print("Error: Provide Telegram bot token.")
            print("Usage: python -m harness telegram YOUR_BOT_TOKEN")
            sys.exit(1)
        from harness.telegram_bot import start_telegram
        start_telegram(token)
        # Keep main thread alive
        import time
        while True:
            time.sleep(60)

    elif mode == "all":
        from harness.web import start_web
        from harness.telegram_bot import start_telegram
        token = args[1] if len(args) > 1 else TELEGRAM_TOKEN
        if token:
            start_telegram(token)
        start_web()

    else:
        from harness.cli import start_cli
        start_cli()


if __name__ == "__main__":
    main()
