"""
Agent initialization — loads the Needle LLM and registers all tools.
"""

import needle
from harness.tools import ALL_TOOLS

print("Loading local Needle model...")
agent = needle.Needle(tools=ALL_TOOLS)
print(f"Agent ready — {len(ALL_TOOLS)} tools registered.")
