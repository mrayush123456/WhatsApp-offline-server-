from flask import Flask, request, jsonify
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

driver = None

def start_whatsapp():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=whatsapp_session")
    options.add_argument("--headless")  # Optional: Run in the background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")
    
    time.sleep(10)
    return "Scan the QR Code in the WhatsApp Web tab"

def send_message(target, message, delay=2):
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.clear()
    search_box.send_keys(target)
    time.sleep(3)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    
    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='6']")
    message_box.send_keys(message)
    time.sleep(delay)
    message_box.send_keys(Keys.ENTER)

@app.route("/")
def index():
    return """
    <html>
    <head>
        <title>WhatsApp Automation</title>
        <script>
            function startWhatsApp() {
                fetch('/start')
                .then(response => response.json())
                .then(data => alert(data.status));
            }
            function sendMessage() {
                let target = document.getElementById("target").value;
                let message = document.getElementById("message").value;
                let delay = document.getElementById("delay").value;

                fetch('/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ target: target, message: message, delay: delay })
                })
                .then(response => response.json())
                .then(data => alert(data.status));
            }
        </script>
    </head>
    <body>
        <h1>WhatsApp Web Automation</h1>
        <button onclick="startWhatsApp()">Start WhatsApp</button>
        <h2>Send Message</h2>
        <label>Target:</label>
        <input type="text" id="target" placeholder="+1234567890"><br>
        <label>Message:</label>
        <input type="text" id="message" placeholder="Hello!"><br>
        <label>Delay:</label>
        <input type="number" id="delay" value="2"><br>
        <button onclick="sendMessage()">Send Message</button>
    </body>
    </html>
    """

@app.route("/start", methods=["GET"])
def start():
    return jsonify({"status": start_whatsapp()})

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    target = data.get("target")
    message = data.get("message")
    delay = int(data.get("delay", 2))
    
    try:
        send_message(target, message, delay)
        return jsonify({"status": "Message Sent Successfully"})
    except Exception as e:
        return jsonify({"status": "Failed", "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        
