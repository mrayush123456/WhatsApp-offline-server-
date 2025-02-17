from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the Chrome driver
driver = webdriver.Chrome()

def send_otp_and_login(phone_number):
    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    time.sleep(15)  # Wait for user to scan QR code

    # Navigate to the target phone number
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Send OTP (This is a placeholder, replace with actual OTP sending logic)
    otp = "123456"  # Replace with actual OTP
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    message_box.send_keys(f"Your OTP is: {otp}")
    message_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Enter OTP (This is a placeholder, replace with actual OTP entry logic)
    otp_input = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    otp_input.send_keys(otp)
    otp_input.send_keys(Keys.ENTER)
    time.sleep(2)

def send_message(target_number, message):
    # Navigate to the target phone number
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(target_number)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Send the message
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)
    time.sleep(2)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    phone_number = data.get('phone_number')
    send_otp_and_login(phone_number)
    return jsonify({"status": "OTP sent and login successful"})

@app.route('/send_message', methods=['POST'])
def send_msg():
    data = request.json
    target_number = data.get('target_number')
    message = data.get('message')
    send_message(target_number, message)
    return jsonify({"status": "Message sent successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
