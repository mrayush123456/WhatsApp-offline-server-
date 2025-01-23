from flask import Flask, request, redirect, url_for, render_template, flash
import pywhatkit as kit
import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Allowed file extensions for message upload
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WhatsApp Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f3f4f6;
                    padding: 20px;
                    text-align: center;
                }
                form {
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                }
                label {
                    display: block;
                    margin: 10px 0 5px;
                    font-weight: bold;
                }
                input, button {
                    padding: 10px;
                    width: 100%;
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                .alert {
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>WhatsApp Message Sender</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="phone">Target Mobile Number (with country code):</label>
                <input type="text" id="phone" name="phone" placeholder="+1234567890" required>

                <label for="message">Message:</label>
                <textarea id="message" name="message" placeholder="Type your message here..." rows="4"></textarea>

                <label for="file">Or Upload a .txt File (optional):</label>
                <input type="file" id="file" name="file" accept=".txt">

                <label for="delay">Delay (in seconds):</label>
                <input type="number" id="delay" name="delay" min="0" value="10" required>

                <button type="submit">Send Message</button>
            </form>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def send_message():
    try:
        # Get phone number and delay
        phone = request.form['phone']
        delay = int(request.form['delay'])

        # Get the message from text input or file
        message = request.form.get('message', '').strip()
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            # Read the message from the uploaded file
            message = file.read().decode('utf-8').strip()

        if not message:
            flash("Error: You must provide a message (either type or upload a file).", "error")
            return redirect(url_for('index'))

        # Calculate time for the message to be sent
        now = datetime.datetime.now()
        send_time = now + datetime.timedelta(seconds=delay)
        hours, minutes = send_time.hour, send_time.minute

        # Send the message using pywhatkit
        kit.sendwhatmsg(phone, message, hours, minutes)
        flash(f"Message scheduled successfully to {phone} at {hours}:{minutes}!", "success")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
      
