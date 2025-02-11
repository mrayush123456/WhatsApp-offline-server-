from flask import Flask, request, render_template_string
import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>WhatsApp Auto Messenger</title>
    <style>
        body {
            background: url('https://source.unsplash.com/random/1920x1080') no-repeat center center fixed;
            background-size: cover;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .animated-text {
            font-size: 24px;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }
    </style>
</head>
<body>
    <h1 class="animated-text">WhatsApp Auto Messenger</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required><br><br>
        <input type="text" name="message" placeholder="Enter message" required><br><br>
        <input type="number" name="delay" placeholder="Delay in seconds" required><br><br>
        <button type="submit">Send Messages</button>
    </form>
</body>
</html>
"""

def send_whatsapp_message(target_number, message):
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get("https://web.whatsapp.com/")
    time.sleep(20)  # Wait for user login manually

    try:
        url = f"https://web.whatsapp.com/send?phone={target_number}&text={message}"
        driver.get(url)
        time.sleep(10)  # Wait for the chat to load

        send_button = driver.find_element(By.XPATH, "//button[@data-testid='send']")
        send_button.click()
        time.sleep(5)  # Allow message to send
    except Exception as e:
        print(f"Failed to send message to {target_number}: {e}")
    
    driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        delay = int(request.form["delay"])
        message = request.form["message"]

        numbers = file.read().decode("utf-8").splitlines()
        for number in numbers:
            send_whatsapp_message(number.strip(), message)
            time.sleep(delay)

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
