from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import time
import subprocess
import threading

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

# Serve HTML directly from Python
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Web Sender</title>
</head>
<body>
    <h2>Send WhatsApp Message</h2>
    <input type="text" id="number" placeholder="Enter Mobile Number">
    <textarea id="message" placeholder="Enter Message"></textarea>
    <input type="number" id="delay" placeholder="Delay in seconds">
    <button onclick="sendMessage()">Send</button>

    <script>
        async function sendMessage() {
            const number = document.getElementById('number').value;
            const message = document.getElementById('message').value;
            const delay = document.getElementById('delay').value || 1;

            const response = await fetch('/send-message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ number, message, delay })
            });

            const result = await response.json();
            alert(result.status);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)  # Serve the HTML directly

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    number = data.get('number')
    message = data.get('message')
    delay = int(data.get('delay', 1))

    if not number or not message:
        return jsonify({'error': 'Missing number or message'}), 400

    def run_whatsapp_script():
        script = f"""
const {{ Client, LocalAuth }} = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({{
    authStrategy: new LocalAuth()
}});

client.on('qr', qr => {{
    console.log('Scan this QR code to authenticate:');
    qrcode.generate(qr, {{ small: true }});
}});

client.on('ready', async () => {{
    console.log('WhatsApp Web is ready!');
    let chatId = "{number}@c.us";
    await new Promise(r => setTimeout(r, {delay} * 1000));
    client.sendMessage(chatId, "{message}");
    console.log(`Message sent to {number}: {message}`);
}});

client.initialize();
"""
        with open("send_message.js", "w") as f:
            f.write(script)

        subprocess.run(["node", "send_message.js"])

    threading.Thread(target=run_whatsapp_script).start()
    
    return jsonify({'status': 'Message Sent'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
