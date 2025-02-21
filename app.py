from flask import Flask, request, redirect, url_for, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import os

app = Flask(__name__)

# Global variables
driver = None
stop_flag = False

def start_whatsapp():
    global driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./chrome_data")  # Save login session
    options.add_argument("--disable-blink-features=AutomationControlled")  
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://web.whatsapp.com")
    time.sleep(15)  # Wait for QR Code Scan

def send_message(phone_number, message, delay=3):
    global driver, stop_flag

    if driver is None:
        start_whatsapp()

    # Open chat
    driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}")
    time.sleep(delay)

    # Click send button
    try:
        send_button = driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
        send_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error sending message: {e}")

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('https://source.unsplash.com/random/1600x900');
            background-size: cover;
            text-align: center;
            padding: 50px;
        }
        form {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            display: inline-block;
            border-radius: 10px;
        }
        input, textarea, button {
            margin: 10px;
            padding: 10px;
            width: 90%;
        }
    </style>
</head>
<body>
    <h1>WhatsApp Message Sender</h1>
    <form action="/send" method="post">
        <input type="text" name="phone" placeholder="Enter WhatsApp number or TXT file" required><br>
        <textarea name="message" placeholder="Enter your message" required></textarea><br>
        <input type="number" name="delay" placeholder="Delay (seconds)" value="3"><br>
        <button type="submit">Send Message</button>
    </form>
    <form action="/stop" method="post">
        <button type="submit" style="background:red; color:white;">Stop</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/send", methods=["POST"])
def send():
    global stop_flag
    phone_number = request.form["phone"]
    message = request.form["message"]
    delay = int(request.form["delay"])

    stop_flag = False  # Reset stop flag

    def send_process():
        if phone_number.endswith(".txt"):  # If a text file is provided
            with open(phone_number, "r") as file:
                for line in file:
                    if stop_flag:
                        break
                    num = line.strip()
                    send_message(num, message, delay)
                    time.sleep(delay)
        else:
            send_message(phone_number, message, delay)

    thread = threading.Thread(target=send_process)
    thread.start()

    return redirect(url_for("index"))

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True
    return redirect(url_for("index"))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
