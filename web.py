# web.py
from flask import Flask, request, jsonify, render_template_string
import random
import os

app = Flask(__name__)

# Mixed nonsense, light sense, gentle slang, and brief existential zingers
DUMB_RESPONSES = [
    # Pure nonsense
    "fup", "moss", "tib", "zib", "glom", "pof", "yef", "soj", "wox", "nib",

    # Whimsical fun
    "fiddle‑faddle", "blip blop", "womp womp", "zoink", "quonk", "snorf",

    # Everyday reactions
    "nice try", "good one", "no way", "oh snap", "right on",

    # Low‑key slang
    "bet", "no cap", "mid", "vibe check", "mood",

    # Existential one‑liners
    "why bother", "nothing matters", "embrace the void", "what is real",
    "were all dust", "existence precedes", "question everything",
    "plot hole life", "authentic self", "cold universe",

    # Emoji‑style extras
    "💀", "🥲", "🔥"
]

# Inline HTML template with dark grey background & mid grey chatbox
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ChatPGT</title>
  <style>
    body {
      margin: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 100vh;
      background: #1e1e1e;
      font-family: sans-serif;
    }
    header {
      background: #121212;
      color: #fff;
      padding: 1rem;
      width: 100%;
      text-align: center;
      font-size: 1.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    #chat {
      flex: 1;
      width: 90%;
      max-width: 600px;
      margin: 1rem 0;
      padding: 1rem;
      background: #4a4a4a;
      color: #f0f0f0;
      overflow-y: auto;
      border-radius: 8px;
    }
    .user { text-align: right; margin: .5rem 0; color: #9cdcfe; }
    .bot  { text-align: left;  margin: .5rem 0; color: #c586c0; }
    #input-box {
      display: flex;
      width: 90%;
      max-width: 600px;
      margin-bottom: 1rem;
    }
    #input-box input {
      flex: 1;
      padding: .75rem;
      border: none;
      border-radius: 4px 0 0 4px;
      font-size: 1rem;
    }
    #input-box button {
      padding: .75rem 1rem;
      border: none;
      background: #007acc;
      color: #fff;
      cursor: pointer;
      border-radius: 0 4px 4px 0;
      font-size: 1rem;
    }
    @media (max-width: 600px) {
      #chat, #input-box { width: 95%; }
      #input-box input, #input-box button { font-size: .9rem; }
    }
  </style>
</head>
<body>
  <header>ChatPGT</header>
  <div id="chat"></div>
  <div id="input-box">
    <input id="message" placeholder="Say something..." autofocus onkeydown="if(event.key==='Enter'){send()}" />
    <button onclick="send()">Send</button>
  </div>
  <script>
    function appendMessage(role, text) {
      const d = document.createElement('div');
      d.className = role;
      d.textContent = text;
      document.getElementById('chat').appendChild(d);
      d.scrollIntoView();
    }
    function send() {
      const input = document.getElementById('message');
      const msg = input.value.trim();
      if (!msg) {
        appendMessage('bot', 'can you repeat the question?');
        return;
      }
      appendMessage('user', msg);
      fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      })
      .then(r => r.json())
      .then(data => appendMessage('bot', data.response))
      .catch(() => appendMessage('bot', 'huh?'));
      input.value = '';
      input.focus();
    }
  </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    msg = data.get('message', '').strip()
    if not msg:
        return jsonify({'response': 'can you repeat the question?'})
    # Choose a random reply from the static list
    return jsonify({'response': random.choice(DUMB_RESPONSES)})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)