"""
Telegram bot — remote phone control via text messages.
"""

import sys
import os
import threading

# Make the harness package importable when run as a plain script (python telegram_bot.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harness.agent import agent


def start_telegram(token: str):
    """Start a Telegram bot listener in a background thread."""
    try:
        import telebot
    except ImportError:
        print("Error: pyTelegramBotAPI not installed. Run: pip install pyTelegramBotAPI")
        return

    bot = telebot.TeleBot(token)
    print(f"Telegram bot active. Send messages to control your phone remotely.")

    @bot.message_handler(func=lambda m: True)
    def handle(message):
        user_text = message.text.strip()
        if not user_text:
            return

        print(f"[Telegram] {message.from_user.first_name}: {user_text}")
        try:
            response = agent.run(user_text)
            bot.reply_to(message, str(response))
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    # Run bot polling in a background thread
    thread = threading.Thread(target=bot.infinity_polling, daemon=True)
    thread.start()
    print("Telegram listener running in background.")
