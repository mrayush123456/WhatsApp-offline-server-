from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
import time
import os
import threading

app = Flask(__name__)

# Twilio Credentials (Replace with yours)
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox Number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to send WhatsApp message
def send_whatsapp_message(number, message, delay, repeat):
    for _ in range(repeat):
        try:
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=message,
                to=f"whatsapp:{number}"
            )
            print(f"Message sent to {number}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error sending message: {e}")

# API for Uploading Text File & Sending Messages
@app.route('/send', methods=['POST'])
def send_messages():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    delay = int(request.form.get("delay", 5))
    repeat = int(request.form.get("repeat", 1))
    sender_name = request.form.get("sender_name", "User")
    message_text = request.form.get("message", "Hello from WhatsApp Automation!")

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read numbers from file
    numbers = [line.strip() for line in file.readlines()]
    
    # Start messaging in a separate thread
    for number in numbers:
        msg = f"{sender_name}: {message_text}"
        threading.Thread(target=send_whatsapp_message, args=(number, msg, delay, repeat)).start()

    return jsonify({"status": "Messages are being sent"}), 200

# Flask Background Wallpaper & Animation
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>WhatsApp Automation</title>
        <style>
            body { background-image: url('https://source.unsplash.com/random/1600x900'); color: white; text-align: center; }
            h1 { font-size: 50px; animation: fadeIn 2s ease-in-out; }
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        </style>
    </head>
    <body>
        <h1>WhatsApp Automation</h1>
        <form action="/send" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <input type="text" name="message" placeholder="Enter Message" required><br>
            <input type="number" name="delay" placeholder="Delay (sec)" required><br>
            <input type="number" name="repeat" placeholder="Repeat Count" required><br>
            <input type="text" name="sender_name" placeholder="Sender Name"><br>
            <button type="submit">Send Messages</button>
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
