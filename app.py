import time
import pyautogui
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import os

app = Flask(__name__)

# Set up Chrome options for headless mode (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Set up WebDriver
def initialize_driver():
    service = Service(executable_path='/path/to/chromedriver')  # Path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://web.whatsapp.com')
    return driver

# Function to verify OTP
def verify_otp(driver, otp_code):
    # You need to inspect WhatsApp Web's elements for the OTP input field
    otp_input = driver.find_element(By.XPATH, "//input[@type='text']")
    otp_input.send_keys(otp_code)
    otp_input.send_keys(Keys.RETURN)

# Function to send a message
def send_message(driver, target_number, message):
    # You need to set up the element to search for the contact in WhatsApp Web
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.send_keys(target_number)
    time.sleep(2)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    
    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    message_box.send_keys(message)
    message_box.send_keys(Keys.RETURN)

@app.route('/')
def home():
    return '''
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>WhatsApp Automation</title>
                <style>
                    body {
                        background-image: url('background.jpg');
                        background-size: cover;
                    }
                    button {
                        padding: 10px 20px;
                        font-size: 16px;
                        margin: 10px;
                        border: none;
                        cursor: pointer;
                        transition: transform 0.3s ease;
                    }
                    button:hover {
                        transform: scale(1.1);
                    }
                    .file-input {
                        margin-top: 10px;
                    }
                </style>
            </head>
            <body>
                <h1>WhatsApp Automation</h1>
                <form id="otp-form">
                    <label for="otp_code">Enter OTP Code:</label>
                    <input type="text" id="otp_code" name="otp_code" required>
                    <button type="submit">Verify OTP</button>
                </form>

                <form id="message-form">
                    <label for="target_number">Target WhatsApp Number:</label>
                    <input type="text" id="target_number" name="target_number" required><br><br>
                    <label for="message_file">Select Message File:</label>
                    <input type="file" id="message_file" class="file-input" accept=".txt" required><br><br>
                    <button type="submit">Send Message</button>
                </form>

                <button id="stop-button" onclick="stopAutomation()">Stop Automation</button>

                <script>
                    document.getElementById('otp-form').addEventListener('submit', function(event) {
                        event.preventDefault();
                        const otp_code = document.getElementById('otp_code').value;
                        fetch('/login', {
                            method: 'POST',
                            body: new URLSearchParams({
                                otp_code: otp_code
                            })
                        }).then(response => response.json())
                          .then(data => alert(data.message));
                    });

                    document.getElementById('message-form').addEventListener('submit', function(event) {
                        event.preventDefault();
                        const target_number = document.getElementById('target_number').value;
                        const message_file = document.getElementById('message_file').files[0];
                        
                        const formData = new FormData();
                        formData.append('target_number', target_number);
                        formData.append('message_file', message_file);

                        fetch('/send_message', {
                            method: 'POST',
                            body: formData
                        }).then(response => response.json())
                          .then(data => alert(data.message));
                    });

                    function stopAutomation() {
                        fetch('/stop', {
                            method: 'POST'
                        }).then(response => response.json())
                          .then(data => alert(data.message));
                    }
                </script>
            </body>
        </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    otp_code = request.form.get('otp_code')
    driver = initialize_driver()
    verify_otp(driver, otp_code)
    return jsonify({"message": "Login successful!"})

@app.route('/send_message', methods=['POST'])
def send_whatsapp_message():
    target_number = request.form.get('target_number')
    message_file = request.files['message_file']
    message = message_file.read().decode('utf-8')
    
    driver = initialize_driver()
    send_message(driver, target_number, message)
    return jsonify({"message": "Message sent!"})

@app.route('/stop', methods=['POST'])
def stop():
    # Logic to stop the automation or close the WebDriver
    driver.quit()
    return jsonify({"message": "Automation stopped!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    
