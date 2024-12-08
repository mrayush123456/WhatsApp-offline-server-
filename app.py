from flask import Flask, request, render_template_string, flash, redirect, url_for
import time
import requests

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #555;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
        .message {
            text-align: center;
            color: red;
            font-size: 14px;
        }
        .success {
            text-align: center;
            color: green;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>WhatsApp Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="mobile_number">Your Mobile Number:</label>
            <input type="text" id="mobile_number" name="mobile_number" placeholder="Enter your mobile number" required>

            <label for="target_number">Target Mobile Number:</label>
            <input type="text" id="target_number" name="target_number" placeholder="Enter target mobile number" required>

            <label for="haters_name">Hater's Name:</label>
            <input type="text" id="haters_name" name="haters_name" placeholder="Enter hater's name" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a text file containing messages, one message per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay between messages" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Endpoint to render form and process requests
@app.route("/", methods=["GET", "POST"])
def send_whatsapp_messages():
    if request.method == "POST":
        try:
            # Get form data
            mobile_number = request.form["mobile_number"]
            target_number = request.form["target_number"]
            haters_name = request.form["haters_name"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Validate message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "message")
                return redirect(url_for("send_whatsapp_messages"))

            # Mock login process (replace with actual API)
            print(f"[INFO] Logging in with mobile number: {mobile_number}")
            time.sleep(2)  # Simulate login delay
            print("[SUCCESS] Login successful!")

            # Simulate sending messages
            for message in messages:
                custom_message = f"{message} - {haters_name}"
                print(f"[INFO] Sending to {target_number}: {custom_message}")
                
                # Replace with actual API call
                # Example:
                # response = requests.post(api_url, data={"message": custom_message, "number": target_number})
                # Check response status
                print(f"[SUCCESS] Message sent: {custom_message}")
                time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect(url_for("send_whatsapp_messages"))

        except Exception as e:
            flash(f"An error occurred: {e}", "message")
            return redirect(url_for("send_whatsapp_messages"))

    # Render form
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
                        
