from flask import Flask, request, render_template_string, flash
from twilio.rest import Client
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Automation</title>
    <style>
        body {
            background-image: url('{{ background_image }}');
            background-size: cover;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .container {
            width: 50%;
            margin: auto;
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
        }
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
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    background_image = request.form.get('background_image', '')
    
    if request.method == 'POST':
        account_sid = request.form['account_sid']
        auth_token = request.form['auth_token']
        target_number = request.form['target_number']
        message = request.form['message']
        delay = int(request.form['delay'])
        
        if 'txt_file' in request.files:
            txt_file = request.files['txt_file']
            if txt_file.filename:
                message = txt_file.read().decode('utf-8')
        
        time.sleep(delay)
        
        try:
            client = Client(account_sid, auth_token)
            client.messages.create(
                from_='whatsapp:+14155238886',
                body=message,
                to=f'whatsapp:{target_number}'
            )
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template_string(HTML_TEMPLATE, background_image=background_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
