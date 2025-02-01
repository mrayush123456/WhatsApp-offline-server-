from flask import Flask, render_template_string, request, redirect, url_for, send_file
import qrcode
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

QR_CODE_PATH = os.path.join(UPLOAD_FOLDER, "whatsapp_qr.png")

# Generate WhatsApp Web QR Code
def generate_qr_code():
    whatsapp_web_url = "https://web.whatsapp.com"
    qr = qrcode.make(whatsapp_web_url)
    qr.save(QR_CODE_PATH)

generate_qr_code()  # Generate QR at startup

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WhatsApp Message Sender</title>
  <script>
    function toggleFields() {
      const targetOption = document.getElementById('targetOption').value;
      document.getElementById('numbersField').style.display = targetOption === '1' ? 'block' : 'none';
      document.getElementById('groupUIDsField').style.display = targetOption === '2' ? 'block' : 'none';
    }

    function animateTitle() {
      let colors = ["#FF5733", "#33FF57", "#3357FF", "#FFFF33", "#FF33FF"];
      let index = 0;
      setInterval(() => {
        document.getElementById('title').style.color = colors[index];
        index = (index + 1) % colors.length;
      }, 500);
    }

    function blinkText() {
      let isVisible = true;
      setInterval(() => {
        document.getElementById('blinking-text').style.visibility = isVisible ? 'hidden' : 'visible';
        isVisible = !isVisible;
      }, 500);
    }

    window.onload = function() {
      animateTitle();
      blinkText();
    };
  </script>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: black;
      color: white;
      text-align: center;
      padding: 20px;
    }
    .form-container { margin-top: 30px; }
    .form-group { margin: 15px 0; }
    label { display: block; margin-bottom: 5px; }
    input, select, button {
      width: 100%; padding: 10px; margin: 5px 0; font-size: 16px;
    }
    #qrCode {
      margin: 20px auto; border: 2px solid #00FF00; padding: 10px;
      width: 250px; height: 250px;
      display: flex; justify-content: center; align-items: center;
      background-color: white;
    }
    img { max-width: 100%; max-height: 100%; }
    button {
      background-color: green; color: white; border: none; cursor: pointer;
    }
    button:hover {
      background-color: limegreen;
    }
  </style>
</head>
<body>
  <h1 id="title">WhatsApp Message Sender</h1>
  <p id="blinking-text">Scan this QR Code</p>
  <div id="qrCode">
    <img src="/qr-code" alt="QR Code">
  </div>
  <p>Open WhatsApp on your phone, go to Settings > Linked Devices, and scan this QR code.</p>
  <p><a href="https://wa.me/?text=Hello" style="color: limegreen;">Link with phone number instead</a></p>

  <div class="form-container">
    <form action="/send-messages" method="POST" enctype="multipart/form-data">
      <div class="form-group">
        <label for="targetOption">Target Option:</label>
        <select name="targetOption" id="targetOption" onchange="toggleFields()">
          <option value="1">Send to Numbers</option>
          <option value="2">Send to Groups</option>
        </select>
      </div>
      <div class="form-group" id="numbersField">
        <label for="numbers">Target Numbers (comma-separated):</label>
        <input type="text" name="numbers" id="numbers" placeholder="e.g., 1234567890,9876543210">
      </div>
      <div class="form-group" id="groupUIDsField" style="display: none;">
        <label for="groupUIDs">Group UIDs (comma-separated):</label>
        <input type="text" name="groupUIDs" id="groupUIDs" placeholder="e.g., group1@g.us,group2@g.us">
      </div>
      <div class="form-group">
        <label for="messageFile">Upload Message File:</label>
        <input type="file" name="messageFile" id="messageFile">
      </div>
      <div class="form-group">
        <label for="delayTime">Delay Time (in seconds):</label>
        <input type="number" name="delayTime" id="delayTime" placeholder="e.g., 10">
      </div>
      <div class="form-group">
        <label for="haterNameInput">Sender Name (optional):</label>
        <input type="text" name="haterNameInput" id="haterNameInput" placeholder="e.g., Your Name">
      </div>
      <button type="submit">Start Sending Messages</button>
    </form>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/qr-code')
def qr_code():
    return send_file(QR_CODE_PATH, mimetype='image/png')

@app.route('/send-messages', methods=['POST'])
def send_messages():
    target_option = request.form.get("targetOption")
    numbers = request.form.get("numbers")
    group_uids = request.form.get("groupUIDs")
    delay_time = request.form.get("delayTime")
    sender_name = request.form.get("haterNameInput")

    message_file = request.files.get("messageFile")
    if message_file:
        file_path = os.path.join(UPLOAD_FOLDER, message_file.filename)
        message_file.save(file_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
