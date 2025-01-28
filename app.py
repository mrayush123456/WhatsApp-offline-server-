from flask import Flask, request, render_template, redirect, url_for
import pywhatkit as kit
import os
import time

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WhatsApp Automation</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                width: 400px;
                padding: 20px;
                background: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }
            h2 {
                text-align: center;
                color: #333;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            label {
                font-weight: bold;
                color: #333;
            }
            input[type="text"], input[type="number"], input[type="file"], button {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>WhatsApp Automation</h2>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="mobile_number">Your Mobile Number:</label>
                <input type="text" id="mobile_number" name="mobile_number" placeholder="Enter your number" required>

                <label for="target_file">Target Numbers and Messages (.txt file):</label>
                <input type="file" id="target_file" name="target_file" accept=".txt" required>

                <label for="interval">Time Interval (Seconds):</label>
                <input type="number" id="interval" name="interval" min="1" value="5" required>

                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route('/', methods=['POST'])
def automate_whatsapp():
    try:
        # Get form data
        mobile_number = request.form.get('mobile_number')
        interval = int(request.form.get('interval'))
        file = request.files['target_file']

        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Read target numbers and messages from file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # Parse each line as "number:message"
            number, message = line.strip().split(':', 1)
            number = number.strip()
            message = message.strip()

            # Send WhatsApp message
            kit.sendwhatmsg_instantly(
                phone_no=f"+{number}",
                message=message,
                wait_time=interval,
                tab_close=True,
                close_time=2,
            )
            time.sleep(interval)  # Delay between messages

        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Success</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
            </style>
        </head>
        <body>
            <h1>Messages Sent Successfully!</h1>
            <a href="/">Go Back</a>
        </body>
        </html>
        '''
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
