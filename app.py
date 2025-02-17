from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import threading
import os
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Global variables
driver = None
stop_flag = False

def start_whatsapp():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./whatsapp_session")  # Save session
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")
    time.sleep(15)  # Wait for manual QR code scan

def send_message(phone, message, delay):
    global stop_flag
    try:
        url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
        driver.get(url)
        time.sleep(5)
        
        # Press send button
        send_button = driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
        send_button.click()
        time.sleep(delay)
    except Exception as e:
        print(f"Error sending message: {e}")

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Automation</title>
        <style>
            body {
                background-image: url('/static/bg.jpg');
                background-size: cover;
                font-family: Arial, sans-serif;
                text-align: center;
                color: white;
            }
            .container {
                margin-top: 50px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WhatsApp Bulk Message Sender</h1>
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" accept=".txt" required><br><br>
                <label>Delay (Seconds):</label>
                <input type="number" name="delay" value="5"><br><br>
                <button type="button" onclick="startSending()">Start</button>
                <button type="button" onclick="stopSending()">Stop</button>
            </form>
        </div>
        <script>
            function startSending() {
                var formData = new FormData(document.getElementById("uploadForm"));
                fetch("/start", { method: "POST", body: formData })
                    .then(response => response.json())
                    .then(data => alert(data.status));
            }
            
            function stopSending() {
                fetch("/stop", { method: "POST" })
                    .then(response => response.json())
                    .then(data => alert(data.status));
            }
        </script>
    </body>
    </html>
    '''

@app.route('/start', methods=['POST'])
def start():
    global stop_flag
    stop_flag = False
    file = request.files['file']
    delay = int(request.form['delay'])
    
    if file:
        file_path = "messages.txt"
        file.save(file_path)
        
        # Read numbers and messages
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        # Start sending messages in a new thread
        def send_messages():
            for line in lines:
                if stop_flag:
                    break
                phone, message = line.strip().split(",", 1)
                send_message(phone, message, delay)
        
        threading.Thread(target=send_messages).start()
    
    return jsonify({"status": "Started sending messages"})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return jsonify({"status": "Stopped sending messages"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
        
