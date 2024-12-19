from flask import Flask, request, render_template_string
import time
import threading
import requests

app = Flask(__name__)

# HTML Template for the Flask Web Page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WhatsApp Automation</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(to right, rgb(0, 123, 255), rgb(0, 230, 118));
      color: #fff;
      text-align: center;
      padding-top: 20px;
    }
    .container {
      background: rgba(0, 0, 0, 0.5);
      padding: 20px;
      border-radius: 10px;
    }
    .btn-primary {
      background-color: #4caf50;
      border-color: #4caf50;
    }
    .btn-primary:hover {
      background-color: #3e8e41;
      border-color: #3e8e41;
    }
    .stop-button {
      background-color: #f44336;
      border-color: #f44336;
    }
    .stop-button:hover {
      background-color: #d32f2f;
      border-color: #d32f2f;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>WhatsApp Automation Tool</h1>
    <form action="/" method="POST" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="mobile" class="form-label">Your Mobile Number:</label>
        <input type="text" class="form-control" id="mobile" name="mobile" required>
      </div>
      <div class="mb-3">
        <label for="otp" class="form-label">OTP Code:</label>
        <input type="text" class="form-control" id="otp" name="otp" required>
      </div>
      <div class="mb-3">
        <label for="target" class="form-label">Target Mobile Number:</label>
        <input type="text" class="form-control" id="target" name="target" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Select Message File (TXT):</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3">
        <label for="delay" class="form-label">Delay Between Messages (seconds):</label>
        <input type="number" class="form-control" id="delay" name="delay" required>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
      <button type="button" class="btn stop-button" onclick="stopSending()">Stop</button>
    </form>
  </div>
  <script>
    function stopSending() {
      fetch('/stop', { method: 'POST' }).then(() => alert("Stopped!"));
    }
  </script>
</body>
</html>
'''

# Global Flag for Stopping Message Sending
STOP_FLAG = False

@app.route("/", methods=["GET", "POST"])
def whatsapp_automation():
    global STOP_FLAG
    if request.method == "POST":
        mobile = request.form.get("mobile")
        otp = request.form.get("otp")
        target = request.form.get("target")
        delay = int(request.form.get("delay"))
        txt_file = request.files["txtFile"]

        # Read the message file
        try:
            messages = txt_file.read().decode("utf-8").splitlines()
        except Exception as e:
            return f"<h3>Error reading file: {e}</h3>"

        # Simulate OTP Login (Replace with actual API or automation)
        if otp != "123456":  # Placeholder for OTP validation
            return "<h3>Invalid OTP. Please try again.</h3>"

        # Start Sending Messages in a Separate Thread
        def send_messages():
            global STOP_FLAG
            for message in messages:
                if STOP_FLAG:
                    print("Message sending stopped.")
                    break
                try:
                    # Simulate WhatsApp API Call
                    print(f"Sending to {target}: {message}")
                    time.sleep(delay)  # Simulate delay
                except Exception as e:
                    print(f"Error sending message: {e}")

        threading.Thread(target=send_messages).start()
        return "<h3>Messages are being sent in the background. Check logs for updates.</h3>"

    return render_template_string(HTML_TEMPLATE)

@app.route("/stop", methods=["POST"])
def stop():
    global STOP_FLAG
    STOP_FLAG = True
    return "Message sending stopped."

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
