from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Selenium WebDriver setup
driver = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    global driver
    try:
        driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and in PATH
        driver.get("https://web.whatsapp.com")
        flash("WhatsApp Web is now open. Scan the QR code.")
    except Exception as e:
        flash(f"Error starting WhatsApp Web: {e}")
    return redirect(url_for("index"))

@app.route("/send_message", methods=["POST"])
def send_message():
    global driver
    if not driver:
        flash("WhatsApp Web is not open. Please login first.")
        return redirect(url_for("index"))

    mobile_number = request.form.get("mobile_number")
    message = request.form.get("message")
    delay = int(request.form.get("delay", 0))

    try:
        driver.get(f"https://web.whatsapp.com/send?phone={mobile_number}&text={message}")
        time.sleep(delay)
        send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
        send_button.click()
        flash("Message sent successfully!")
    except Exception as e:
        flash(f"Error sending message: {e}")

    return redirect(url_for("index"))

@app.route("/send_bulk", methods=["POST"])
def send_bulk():
    global driver
    if not driver:
        flash("WhatsApp Web is not open. Please login first.")
        return redirect(url_for("index"))

    file = request.files.get("file")
    delay = int(request.form.get("delay", 0))

    if not file or not file.filename.endswith(".txt"):
        flash("Please upload a valid .txt file.")
        return redirect(url_for("index"))

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
    file.save(file_path)

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            mobile_number, message = line.strip().split(",")
            driver.get(f"https://web.whatsapp.com/send?phone={mobile_number}&text={message}")
            time.sleep(delay)
            send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_button.click()
            time.sleep(2)  # Extra delay between messages

        flash("Bulk messages sent successfully!")
    except Exception as e:
        flash(f"Error sending bulk messages: {e}")

    return redirect(url_for("index"))

@app.route("/logout", methods=["POST"])
def logout():
    global driver
    if driver:
        driver.quit()
        driver = None
        flash("Logged out from WhatsApp Web.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
        
