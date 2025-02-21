from flask import Flask, request, render_template_string, redirect, url_for
from twilio.rest import Client
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Twilio Credentials
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Selenium WebDriver Setup
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login_whatsapp():
    driver.get("https://web.whatsapp.com")
    time.sleep(10)
    qr_path = "static/qr.png"
    driver.save_screenshot(qr_path)
    return qr_path

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        phone = request.form.get("phone")
        message = request.form.get("message")
        file = request.files.get("file")
        delay = int(request.form.get("delay", 1))

        if file:
            file_path = "uploads/" + file.filename
            file.save(file_path)
            with open(file_path, "r") as f:
                numbers = f.readlines()
            
            for num in numbers:
                send_whatsapp_message(num.strip(), message)
                time.sleep(delay)
        else:
            send_whatsapp_message(phone, message)

        return redirect(url_for("home"))

    qr_code = login_whatsapp()
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Automation</title>
        <style>
            body {{
                background-image: url('/static/bg.jpg');
                background-size: cover;
                font-family: Arial, sans-serif;
                text-align: center;
                color: white;
            }}
            form {{
                margin: 20px auto;
                padding: 20px;
                background: rgba(0, 0, 0, 0.7);
                display: inline-block;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <h2>WhatsApp Automation</h2>
        <img src="{qr_code}" width="200"><br><br>

        <form method="POST" enctype="multipart/form-data">
            <label>Target WhatsApp Number:</label>
            <input type="text" name="phone" required><br><br>
            
            <label>Message:</label>
            <textarea name="message" required></textarea><br><br>

            <label>Upload TXT File (optional):</label>
            <input type="file" name="file"><br><br>

            <label>Delay (seconds):</label>
            <input type="number" name="delay" value="1"><br><br>

            <button type="submit">Send Message</button>
        </form>

        <br>
        <a href="/stop"><button>Stop</button></a>
    </body>
    </html>
    """
    return render_template_string(html_template)

def send_whatsapp_message(to, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:+{to}"
        )
    except Exception as e:
        print("Error:", e)

@app.route("/stop")
def stop():
    driver.quit()
    return "WhatsApp Automation Stopped"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
