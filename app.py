import time
import pywhatkit as kit
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to initiate WhatsApp pairing (QR code)
@app.route('/whatsapp-pair', methods=['GET'])
def whatsapp_pair():
    # You will need to scan the QR code manually using your WhatsApp mobile app
    try:
        # Initiate WhatsApp Web pairing by displaying the QR code
        kit.info('WhatsApp web QR code will be generated.')
        return jsonify({"message": "Scan the QR code on WhatsApp web to pair your phone."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to send a message via WhatsApp
@app.route('/send-message', methods=['POST'])
def send_message():
    # Extracting data from the request
    target_number = request.json.get("target_number")
    message = request.json.get("message")
    delay = request.json.get("delay", 5)  # Delay in seconds before sending the message

    if not target_number or not message:
        return jsonify({"error": "Missing target_number or message"}), 400

    try:
        # Sending the message via WhatsApp
        kit.sendwhatmsg(target_number, message, time.localtime().tm_hour, time.localtime().tm_min + delay)
        return jsonify({"message": f"Message sent to {target_number} after {delay} seconds."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle file upload
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": f"File uploaded successfully: {filename}"})
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
