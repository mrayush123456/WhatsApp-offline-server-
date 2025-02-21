from flask import Flask, render_template_string, request, jsonify
import random
import time

app = Flask(__name__)

# Store OTPs temporarily
otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/')
def index():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP Verification & WhatsApp Messaging</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 50px;
                }
                .frame {
                    display: none;
                }
                .active {
                    display: block;
                }
            </style>
            <script>
                function showFrame(frameId) {
                    document.querySelectorAll('.frame').forEach(frame => frame.classList.remove('active'));
                    document.getElementById(frameId).classList.add('active');
                }

                function sendOTP(event) {
                    event.preventDefault();
                    let phone = document.querySelector('input[name="phone"]').value;
                    fetch('/send_otp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: 'phone=' + encodeURIComponent(phone)
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        showFrame('otpFrame');
                    });
                }

                function verifyOTP(event) {
                    event.preventDefault();
                    let phone = document.querySelector('input[name="phone"]').value;
                    let otp = document.querySelector('input[name="otp"]').value;
                    fetch('/verify_otp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: 'phone=' + encodeURIComponent(phone) + '&otp=' + encodeURIComponent(otp)
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        if (data.message === "OTP Verified Successfully!") {
                            showFrame('whatsappFrame');
                        }
                    });
                }

                function sendMessage(event) {
                    event.preventDefault();
                    let target_number = document.querySelector('input[name="target_number"]').value;
                    let message = document.querySelector('textarea[name="message"]').value;
                    let delay = document.querySelector('input[name="delay"]').value;
                    fetch('/send_whatsapp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: 'target_number=' + encodeURIComponent(target_number) + '&message=' + encodeURIComponent(message) + '&delay=' + encodeURIComponent(delay)
                    })
                    .then(response => response.json())
                    .then(data => alert(data.message));
                }
            </script>
        </head>
        <body>

            <!-- OTP Request Frame -->
            <div id="phoneFrame" class="frame active">
                <h2>Enter Your Phone Number</h2>
                <form onsubmit="sendOTP(event)">
                    <label>Phone Number (WhatsApp):</label>
                    <input type="text" name="phone" required>
                    <button type="submit">Send OTP</button>
                </form>
            </div>

            <!-- OTP Verification Frame -->
            <div id="otpFrame" class="frame">
                <h2>Verify Your OTP</h2>
                <form onsubmit="verifyOTP(event)">
                    <label>Enter OTP:</label>
                    <input type="text" name="otp" required>
                    <button type="submit">Verify</button>
                </form>
            </div>

            <!-- WhatsApp Message Sending Frame -->
            <div id="whatsappFrame" class="frame">
                <h2>Send a WhatsApp Message</h2>
                <form onsubmit="sendMessage(event)">
                    <label>Recipient Number:</label>
                    <input type="text" name="target_number" required><br><br>
                    <label>Message:</label>
                    <textarea name="message" required></textarea><br><br>
                    <label>Delay (seconds):</label>
                    <input type="number" name="delay" required><br><br>
                    <button type="submit">Send Message</button>
                </form>
            </div>

        </body>
        </html>
    """)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone = request.form.get('phone')
    otp = generate_otp()
    otp_storage[phone] = otp  # Store OTP temporarily
    print(f"OTP for {phone}: {otp}")  # Simulating OTP sending
    return jsonify({"message": "OTP sent successfully!"})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    phone = request.form.get('phone')
    otp = request.form.get('otp')
    if otp_storage.get(phone) == otp:
        return jsonify({"message": "OTP Verified Successfully!"})
    return jsonify({"message": "Invalid OTP!"}), 400

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    target_number = request.form.get('target_number')
    message = request.form.get('message')
    delay = int(request.form.get('delay', 0))
    
    print(f"Sending WhatsApp message to {target_number}: {message} (after {delay} sec)")
    time.sleep(delay)  # Simulating delay
    return jsonify({"message": "WhatsApp Message Sent Successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
