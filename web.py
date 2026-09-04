"""
Flask web server — provides the glassmorphic chat UI and REST API.
"""

import os
import sys
import json

# Make the harness package importable when run as a plain script (python web.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, render_template_string
from harness.agent import agent
from harness.config import WEB_HOST, WEB_PORT

app = Flask(__name__)


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = agent.run(user_msg)
        return jsonify({"response": str(response)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tools")
def list_tools():
    """Return the list of registered tool names."""
    names = [t.__name__ for t in agent.tools] if hasattr(agent, "tools") else []
    return jsonify({"tools": names})


def start_web(host: str = WEB_HOST, port: int = WEB_PORT):
    """Start the web server."""
    print(f"Web UI: http://{host}:{port}")
    try:
        from waitress import serve
        serve(app, host=host, port=port)
    except ImportError:
        app.run(host=host, port=port, debug=False)


# ─── HTML Template ────────────────────────────────────────────────────

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Harness Agent</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090a0f; --panel: #11131e; --border: rgba(255,255,255,0.06);
      --primary: #4f46e5; --primary-light: #6366f1;
      --accent: #10b981; --text: #f1f5f9; --muted: #64748b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; }
    header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid var(--border); background: rgba(9,10,15,0.85); backdrop-filter: blur(12px); position: sticky; top: 0; z-index: 10; }
    .logo { display: flex; align-items: center; gap: 0.6rem; }
    .logo-mark { width: 1.6rem; height: 1.6rem; border-radius: 6px; background: linear-gradient(135deg, var(--primary), var(--primary-light)); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem; color: #fff; }
    .logo h1 { font-size: 1rem; font-weight: 600; }
    .logo span { font-size: 0.65rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
    .status { display: flex; align-items: center; gap: 0.4rem; font-size: 0.7rem; color: var(--accent); }
    .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 8px var(--accent); animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
    main { display: grid; grid-template-columns: 1.3fr 0.7fr; gap: 1rem; padding: 1rem; flex: 1; max-width: 1400px; margin: 0 auto; width: 100%; }
    @media (max-width: 1024px) { main { grid-template-columns: 1fr; } }
    .card { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; height: calc(100vh - 100px); }
    .chat-header { padding: 0.8rem 1.2rem; border-bottom: 1px solid var(--border); font-size: 0.85rem; font-weight: 600; }
    .messages { flex: 1; padding: 1.2rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem; }
    .msg { max-width: 85%; animation: fadeIn 0.2s ease-out; }
    .msg.user { align-self: flex-end; }
    .msg.agent { align-self: flex-start; width: 100%; }
    .bubble { padding: 0.75rem 1rem; border-radius: 10px; font-size: 0.88rem; line-height: 1.45; }
    .msg.user .bubble { background: var(--primary); color: #fff; border-bottom-right-radius: 2px; }
    .msg.agent .bubble { background: #161824; border: 1px solid var(--border); border-bottom-left-radius: 2px; }
    .meta { font-size: 0.68rem; color: var(--muted); margin-top: 0.2rem; }
    .input-area { padding: 1rem 1.2rem; border-top: 1px solid var(--border); display: flex; gap: 0.6rem; }
    .input-area input { flex: 1; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 0.65rem 0.9rem; color: var(--text); font-family: inherit; font-size: 0.85rem; outline: none; }
    .input-area input:focus { border-color: var(--primary-light); }
    .btn { background: var(--primary); color: #fff; border: none; border-radius: 8px; padding: 0 1.1rem; font-weight: 500; font-size: 0.8rem; cursor: pointer; }
    .btn:hover { background: var(--primary-light); }
    .tools-panel { padding: 1.2rem; overflow-y: auto; height: 100%; }
    .section-title { font-size: 0.75rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 0.6rem; }
    .triggers { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; }
    .trigger { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 8px; padding: 0.6rem; font-family: inherit; color: var(--text); font-size: 0.75rem; text-align: left; cursor: pointer; }
    .trigger:hover { background: rgba(255,255,255,0.05); border-color: var(--primary-light); }
    .tag { font-size: 0.6rem; color: var(--muted); text-transform: uppercase; display: block; margin-bottom: 0.15rem; }
    @keyframes fadeIn { from { transform: translateY(6px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @media (max-width: 768px) { main { padding: 0.5rem; } .card { height: calc(100vh - 80px); } .triggers { grid-template-columns: 1fr 1fr; } }
  </style>
</head>
<body>
  <header>
    <div class="logo">
      <div class="logo-mark">⬡</div>
      <div>
        <h1>Harness</h1>
        <span>Mobile Agent</span>
      </div>
    </div>
    <div class="status"><div class="dot"></div><span>Online</span></div>
  </header>
  <main>
    <div class="card">
      <div class="chat-header">Agent Console</div>
      <div class="messages" id="msgs">
        <div class="msg agent">
          <div class="bubble">Ready. Tell me what to do on your phone — I understand natural language.</div>
          <div class="meta">System</div>
        </div>
      </div>
      <div class="input-area">
        <input id="input" placeholder="e.g. turn on flashlight, read my messages..." autocomplete="off">
        <button class="btn" id="send">Execute</button>
      </div>
    </div>
    <div class="card" style="height:auto;">
      <div class="tools-panel">
        <div class="section-title">⚡ Quick Actions</div>
        <div class="triggers">
          <button class="trigger" onclick="sendCmd('Check battery status')"><span class="tag">System</span>Battery</button>
          <button class="trigger" onclick="sendCmd('Turn on flashlight')"><span class="tag">Hardware</span>Torch ON</button>
          <button class="trigger" onclick="sendCmd('Turn off flashlight')"><span class="tag">Hardware</span>Torch OFF</button>
          <button class="trigger" onclick="sendCmd('Vibrate for 500ms')"><span class="tag">Hardware</span>Vibrate</button>
          <button class="trigger" onclick="sendCmd('Where am I?')"><span class="tag">Location</span>GPS</button>
          <button class="trigger" onclick="sendCmd('WiFi info')"><span class="tag">Network</span>WiFi Info</button>
          <button class="trigger" onclick="sendCmd('Scan WiFi networks')"><span class="tag">Network</span>WiFi Scan</button>
          <button class="trigger" onclick="sendCmd('List contacts')"><span class="tag">Data</span>Contacts</button>
          <button class="trigger" onclick="sendCmd('Last 5 messages')"><span class="tag">Messages</span>SMS Inbox</button>
          <button class="trigger" onclick="sendCmd('Recent call log')"><span class="tag">Calls</span>Call Log</button>
          <button class="trigger" onclick="sendCmd('Take a photo')"><span class="tag">Camera</span>Photo</button>
          <button class="trigger" onclick="sendCmd('Say hello')"><span class="tag">Audio</span>TTS</button>
          <button class="trigger" onclick="sendCmd('Set brightness to 128')"><span class="tag">Display</span>Brightness</button>
          <button class="trigger" onclick="sendCmd('Get volume levels')"><span class="tag">Audio</span>Volume</button>
          <button class="trigger" onclick="sendCmd('Copy hello to clipboard')"><span class="tag">System</span>Clipboard</button>
          <button class="trigger" onclick="sendCmd('Open YouTube')"><span class="tag">Apps</span>YouTube</button>
          <button class="trigger" onclick="sendCmd('Open WhatsApp')"><span class="tag">Apps</span>WhatsApp</button>
          <button class="trigger" onclick="sendCmd('Open Chrome')"><span class="tag">Apps</span>Chrome</button>
          <button class="trigger" onclick="sendCmd('Show device info')"><span class="tag">Device</span>Telephony</button>
          <button class="trigger" onclick="sendCmd('Authenticate fingerprint')"><span class="tag">Security</span>Fingerprint</button>
        </div>
      </div>
    </div>
  </main>
  <script>
    const msgs = document.getElementById('msgs');
    const input = document.getElementById('input');
    const sendBtn = document.getElementById('send');

    function addMsg(text, cls) {
      const d = document.createElement('div');
      d.className = 'msg ' + cls;
      d.innerHTML = '<div class="bubble">' + text + '</div><div class="meta">' + (cls === 'user' ? 'You' : 'Agent') + ' • ' + new Date().toLocaleTimeString() + '</div>';
      msgs.appendChild(d);
      msgs.scrollTop = msgs.scrollHeight;
    }

    async function sendCmd(text) {
      input.value = text;
      sendBtn.click();
    }

    sendBtn.addEventListener('click', async () => {
      const text = input.value.trim();
      if (!text) return;
      addMsg(text, 'user');
      input.value = '';
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message: text})
        });
        const data = await res.json();
        addMsg(data.response || data.error || 'No response', 'agent');
      } catch (e) {
        addMsg('Error: ' + e.message, 'agent');
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') sendBtn.click();
    });
  </script>
</body>
</html>
"""
