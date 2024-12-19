from flask import Flask, request, render_template_string
import time
import threading
import pywhatkit as kit

app = Flask(__name__)

# HTML Template
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
            background-color: #282c34;
            color: white;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background: rgb(50, 60, 80);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
        }
        .btn {
            width: 100%;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">WhatsApp Automation</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="mobile" class="form-label">Your WhatsApp Number:</label>
                <input type="text" class="form-control" id="mobile" name="mobile" placeholder="Enter your number (with country code)" required>
            </div>
            <div class="mb-3">
                <label for="otp" class="form-label">Enter OTP:</label>
                <input type="text" class="form-control" id="otp" name="otp" placeholder="Enter the OTP received" required>
            </div>
            <div class="mb-3">
                <label for="target" class="form-label">Target WhatsApp Number:</label>
                <input type="text" class="form-control" id="target" name="target" placeholder="Enter target number (with country code)" required>
            </div>
            <div class="mb-3">
                <label for="txtFile" class="form-label">Upload Message File (.txt):</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="hatersName" class="form-label">Hater's Name:</label>
                <input type="text" class="form-control" id="hatersName" name="hatersName" placeholder="Enter Hater's Name" required>
            </div>
            <div class="mb-3">
                <label for="delay" class="form-label">Delay Between Messages (seconds):</label>
                <input type="number" class="form-control" id="delay" name="delay" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <button class="btn btn-danger" onclick="stopAutomation()">Stop Automation</button>
    </div>
    <script>
        function stopAutomation() {
            fetch('/stop', { method: 'POST' }).then(response => alert('Automation Stopped!'));
        }
    </script>
</body>
</html>
'''

# Global flag to stop the automation
stop_flag = False

# Function to send WhatsApp messages
def send_messages(target, messages, delay, hater_name):
    global stop_flag
    for msg in messages:
        if stop_flag:
            break
        full_msg = f"Hello {hater_name}, {msg}"
        print(f"[INFO] Sending: {full_msg} to {target}")
        try:
            # Send message using pywhatkit
            kit.sendwhatmsg_instantly(phone_no=target, message=full_msg, wait_time=10)
            time.sleep(delay)
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
            time.sleep(5)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        global stop_flag
        stop_flag = False

        # Retrieve form data
        mobile = request.form["mobile"]
        otp = request.form["otp"]
        target = request.form["target"]
        txt_file = request.files["txtFile"]
        hater_name = request.form["hatersName"]
        delay = int(request.form["delay"])

        # Verify OTP (simulation, requires integration with WhatsApp APIs)
        if otp != "123456":  # Dummy OTP check
            return "<h3>Invalid OTP</h3>"

        # Read message file
        try:
            messages = txt_file.read().decode("utf-8").splitlines()
        except Exception as e:
            return f"<h3>Error reading file: {e}</h3>"

        # Start sending messages in a separate thread
        threading.Thread(target=send_messages, args=(target, messages, delay, hater_name)).start()
        return "<h3>Messages are being sent in the background!</h3>"

    return render_template_string(HTML_TEMPLATE)

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True
    return "Automation stopped!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    
