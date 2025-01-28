from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import os

app = Flask(__name__)

driver = None  # To hold the Selenium WebDriver instance
stop_flag = False  # Global flag to stop sending messages


@app.route('/')
def index():
    return '''
        <html>
        <head>
            <title>WhatsApp Automation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f3f4f6;
                    text-align: center;
                    padding: 20px;
                }
                .container {
                    max-width: 500px;
                    margin: auto;
                    padding: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input, button, select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #45a049;
                }
                .stop-button {
                    background-color: red;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>WhatsApp Automation</h1>
                <form action="/start" method="post" enctype="multipart/form-data">
                    <label>Target Number (Single Number):</label>
                    <input type="text" name="target_number" placeholder="e.g., +1234567890">
                    
                    <label>Upload .txt File (Numbers and Messages):</label>
                    <input type="file" name="file" accept=".txt">
                    
                    <label>Delay (in seconds):</label>
                    <input type="number" name="delay" value="5" min="1">
                    
                    <button type="submit">Start Automation</button>
                </form>
                <form action="/stop" method="post">
                    <button type="submit" class="stop-button">Stop Automation</button>
                </form>
            </div>
        </body>
        </html>
    '''


@app.route('/start', methods=['POST'])
def start():
    global driver, stop_flag

    # Get form data
    target_number = request.form.get('target_number')
    file = request.files.get('file')
    delay = int(request.form.get('delay', 5))

    # Create a list of numbers and messages
    numbers_and_messages = []
    if target_number:
        numbers_and_messages.append((target_number, ""))
    if file:
        content = file.read().decode('utf-8')
        for line in content.splitlines():
            parts = line.split(',', 1)
            if len(parts) == 2:
                numbers_and_messages.append((parts[0].strip(), parts[1].strip()))

    # Start a new thread to handle WhatsApp automation
    stop_flag = False
    threading.Thread(target=send_messages, args=(numbers_and_messages, delay)).start()

    return redirect(url_for('index'))


@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return redirect(url_for('index'))


def send_messages(numbers_and_messages, delay):
    global driver, stop_flag

    # Initialize WebDriver if not already started
    if driver is None:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://web.whatsapp.com/")
        print("[INFO] Please scan the QR code on WhatsApp Web.")
        time.sleep(15)  # Wait for QR code scanning

    for number, message in numbers_and_messages:
        if stop_flag:
            print("[INFO] Automation stopped.")
            break

        try:
            # Open chat with the target number
            url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
            driver.get(url)
            time.sleep(5)  # Allow page to load

            # Click the send button
            send_button = driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
            send_button.click()
            print(f"[INFO] Message sent to {number}")

            time.sleep(delay)  # Delay between messages

        except Exception as e:
            print(f"[ERROR] Failed to send message to {number}: {str(e)}")
            continue


@app.route('/shutdown', methods=['POST'])
def shutdown():
    global driver
    if driver:
        driver.quit()
    driver = None
    return "[INFO] WebDriver shut down."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
