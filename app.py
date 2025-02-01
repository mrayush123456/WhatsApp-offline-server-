from flask import Flask, render_template_string, request, redirect, url_for
import qrcode
import os
from io import BytesIO
import base64
from flask import send_file

app = Flask(__name__)

# Function to generate a QR code
def generate_qr_code(data):
    qr = qrcode.make(data)
    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode()

# Simulating a WhatsApp authentication URL (Replace with dynamic data from whatsapp-web.js)
WHATSAPP_AUTH_URL = "https://wa.me/qr/SAMPLEQRDATA"

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
      width: 250px; height: 250px; display: flex; justify-content: center; align-items: center;
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
  <h1>WhatsApp Message Sender</h1>
  <p>Scan this QR Code to authenticate with WhatsApp</p>
  <div id="qrCode">
    <img src="{{ qr_code }}" alt="QR Code">
  </div>
  <p>Open WhatsApp on your phone, go to Settings > Linked Devices, and scan this QR code.</p>

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
      <button type="submit">Start Sending Messages</button>
    </form>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    qr_code = generate_qr_code(WHATSAPP_AUTH_URL)
    return render_template_string(HTML_PAGE, qr_code=f"data:image/png;base64,{qr_code}")

@app.route('/send-messages', methods=['POST'])
def send_messages():
    target_option = request.form.get("targetOption")
    numbers = request.form.get("numbers")
    group_uids = request.form.get("groupUIDs")
    delay_time = request.form.get("delayTime")
    
    # Handle file upload
    message_file = request.files.get("messageFile")
    if message_file:
        file_path = "uploaded_messages.txt"
        message_file.save(file_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
