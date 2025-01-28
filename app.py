from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import time
import os

app = Flask(__name__)

# Global variables to control the process
driver = None
stop_sending = False

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WhatsApp Automation</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f2f2f2; margin: 0; padding: 0; }
                .container { max-width: 600px; margin: 50px auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                h1 { text-align: center; }
                label { display: block; margin-bottom: 10px; }
                input, button { width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 5px; }
                button { background: #4CAF50; color: white; border: none; cursor: pointer; }
                button:hover { background: #45a049; }
                .stop-btn { background: red; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>WhatsApp Automation</h1>
                <form action="/start" method="post" enctype="multipart/form-data">
                    <label for="mobile">Target Mobile Number:</label>
                    <input type="text" id="mobile" name="mobile" placeholder="e.g., +1234567890" required>
                    
                    <label for="txtFile">Select Text File of Messages:</label>
                    <input type="file" id="txtFile" name="txtFile" accept=".txt" required>
                    
                    <label for="delay">Delay Between Messages (in seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" min="1" required>
                    
                    <button type="submit">Start Sending Messages</button>
                </form>
                <form action="/stop" method="post">
                    <button type="submit" class="stop-btn">Stop</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/start', methods=['POST'])
def start():
    global driver, stop_sending

    # Get form data
    mobile = request.form['mobile']
    txt_file = request.files['txtFile']
    delay = int(request.form['delay'])

    # Read messages from the uploaded text file
    messages = txt_file.read().decode('utf-8').splitlines()

    # Start Selenium WebDriver
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
    driver.get('https://web.whatsapp.com')
    stop_sending = False

    # Start a new thread to send messages
    thread = threading.Thread(target=send_messages, args=(mobile, messages, delay))
    thread.start()

    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    global stop_sending
    stop_sending = True
    return redirect(url_for('index'))

def send_messages(mobile, messages, delay):
    global driver, stop_sending

    try:
        # Wait for the user to scan the QR code
        print("Please scan the QR code on WhatsApp Web.")
        input("Press Enter after scanning the QR code...")

        # Open chat with the target number
        driver.get(f'https://web.whatsapp.com/send?phone={mobile}')
        time.sleep(10)  # Allow time for the chat to load

        # Send messages
        for message in messages:
            if stop_sending:
                print("Message sending stopped by the user.")
                break

            # Find the message input box and send the message
            message_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
            message_box.click()
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            print(f"Message sent: {message}")
            time.sleep(delay)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Quit the driver after completion
        if driver:
            driver.quit()
            driver = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
