from flask import Flask, request, render_template_string, flash
from twilio.rest import Client
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Twilio Credentials (Replace with your actual credentials)
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Official Twilio sandbox number

def send_whatsapp_message(target_number, message, delay):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    time.sleep(delay)
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=f"whatsapp:{target_number}"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    background_image = ""  # Default empty background image URL
    if request.method == 'POST':
        account_sid = request.form['account_sid']
        auth_token = request.form['auth_token']
        target_number = request.form['target_number']
        delay = int(request.form['delay'])
        background_image = request.form['background_image']
        
        if account_sid and auth_token:
            global TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
            TWILIO_ACCOUNT_SID = account_sid
            TWILIO_AUTH_TOKEN = auth_token
        
        if 'txt_file' in request.files:
            txt_file = request.files['txt_file']
            if txt_file.filename.endswith('.txt'):
                messages = txt_file.read().decode('utf-8').split('\n')
                for msg in messages:
                    send_whatsapp_message(target_number, msg, delay)
                flash("Messages sent successfully!", "success")
            else:
                flash("Invalid file format. Please upload a .txt file.", "danger")
        else:
            message = request.form['message']
            send_whatsapp_message(target_number, message, delay)
            flash("Message sent successfully!", "success")
    
    html_template = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WhatsApp Automation</title>
        <style>
            body {{
                background-image: url('{background_image}');
                background-size: cover;
                text-align: center;
                font-family: Arial, sans-serif;
            }}
            .container {{
                width: 50%;
                margin: auto;
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>WhatsApp Automation</h2>
            <form method="POST" enctype="multipart/form-data">
                <label>Account SID:</label>
                <input type="text" name="account_sid" required><br><br>
                
                <label>Auth Token:</label>
                <input type="text" name="auth_token" required><br><br>
                
                <label>Target Number:</label>
                <input type="text" name="target_number" required><br><br>
                
                <label>Message:</label>
                <textarea name="message"></textarea><br><br>
                
                <label>Upload TXT file:</label>
                <input type="file" name="txt_file"><br><br>
                
                <label>Delay (seconds):</label>
                <input type="number" name="delay" min="0" required><br><br>
                
                <label>Background Image URL:</label>
                <input type="text" name="background_image"><br><br>
                
                <button type="submit">Send Message</button>
            </form>
            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endif %}
            {% endwith %}
        </div>
    </body>
    </html>'''
    
    return render_template_string(html_template)
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
