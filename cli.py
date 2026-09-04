"""
Interactive CLI mode — chat with the agent in your terminal.

Run from anywhere:
  python -m harness            # from MobileAgent/ (project root)
  python cli.py                # from inside harness/
"""

import os
import sys

# Make the harness package importable when run as a plain script (python cli.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harness.agent import agent


def start_cli():
    """Start an interactive chat loop in the terminal."""
    print("╔══════════════════════════════════════╗")
    print("║   Harness Agent — Interactive CLI    ║")
    print("║   Type 'exit' or 'quit' to stop.    ║")
    print("╚══════════════════════════════════════╝")
    print()

    while True:
        try:
            user_input = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye.")
            break

        try:
            response = agent.run(user_input)
            print(f"Agent > {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    start_cli()
