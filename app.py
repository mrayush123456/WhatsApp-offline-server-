from flask import Flask, render_template_string, request, redirect, url_for, session
import pywhatkit as kit
import time
import os
from threading import Thread

app = Flask(__name__)
app.secret_key = "whatsapp_automation"

# Simulated OTP Storage
OTP_STORE = {}

# Function to send WhatsApp message
def send_whatsapp_message(phone, message, delay):
    time.sleep(delay)  # Apply delay
    kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10)

# Route: Home Page
@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head>
            <title>WhatsApp Login</title>
        </head>
        <body>
            <h2>Enter Your WhatsApp Number</h2>
            <form action="/login" method="post">
                <input type="text" name="phone" placeholder="Enter phone number" required>
                <button type="submit">Send OTP</button>
            </form>
        </body>
        </html>
    ''')

# Route: Login (Enter Phone Number)
@app.route('/login', methods=['POST'])
def login():
    phone = request.form['phone']
    otp = "123456"  # Simulated OTP (Replace with an actual OTP method)
    OTP_STORE[phone] = otp
    session['phone'] = phone
    return render_template_string('''
        <html>
        <head>
            <title>Enter OTP</title>
        </head>
        <body>
            <h2>Enter OTP sent to {{ phone }}</h2>
            <form action="/verify" method="post">
                <input type="text" name="otp" placeholder="Enter OTP" required>
                <button type="submit">Verify</button>
            </form>
        </body>
        </html>
    ''', phone=phone)

# Route: Submit OTP Verification
@app.route('/verify', methods=['POST'])
def verify():
    phone = session.get('phone')
    entered_otp = request.form['otp']
    
    if OTP_STORE.get(phone) == entered_otp:
        return redirect(url_for('dashboard'))
    else:
        return "Invalid OTP! Try Again."

# Route: Dashboard (Send Messages)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        target_phone = request.form['target_phone']
        message = request.form['message']
        delay = int(request.form['delay'])
        
        thread = Thread(target=send_whatsapp_message, args=(target_phone, message, delay))
        thread.start()
        
        return "Message Sent Successfully!"
    
    return render_template_string('''
        <html>
        <head>
            <title>Send WhatsApp Message</title>
            <style>
                body {
                    background-image: url('/static/bg.jpg');
                    background-size: cover;
                }
            </style>
        </head>
        <body>
            <h2>Send a WhatsApp Message</h2>
            <form action="/dashboard" method="post">
                <input type="text" name="target_phone" placeholder="Target Phone Number" required>
                <textarea name="message" placeholder="Enter message" required></textarea>
                <input type="number" name="delay" placeholder="Delay in seconds" required>
                <button type="submit">Send</button>
            </form>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".txt">
                <button type="submit">Upload File</button>
            </form>
        </body>
        </html>
    ''')

# Route: Upload Text File for Messages
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)
        return f"File uploaded successfully: {file.filename}"
    return "No file selected."

# Start Flask Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
