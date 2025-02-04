from flask import Flask, render_template_string, jsonify
import random
import string
import socket
import datetime

app = Flask(__name__)

# Function to generate random username and password
def generate_credentials():
    username = "user" + str(random.randint(1000, 9999))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

# Function to get the local IP address
def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

# Generate RDP details
def generate_rdp():
    hostname, ip_address = get_ip()
    username, password = generate_credentials()
    port = random.choice([3389, 3390, 3391])  # Standard RDP ports
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
    
    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "username": username,
        "password": password,
        "port": port,
        "valid_until": expiry_date.strftime("%Y-%m-%d %H:%M:%S")
    }

# HTML template as a string
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated RDP Credentials</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .container { margin-top: 50px; }
        table { margin: 0 auto; border-collapse: collapse; width: 50%; }
        th, td { padding: 10px; border: 1px solid black; text-align: left; }
    </style>
</head>
<body>
    <div class="container">
        <h2>RDP Credentials</h2>
        <table>
            <tr><th>Hostname</th><td>{{ rdp_data.hostname }}</td></tr>
            <tr><th>IP Address</th><td>{{ rdp_data.ip_address }}</td></tr>
            <tr><th>Username</th><td>{{ rdp_data.username }}</td></tr>
            <tr><th>Password</th><td>{{ rdp_data.password }}</td></tr>
            <tr><th>Port</th><td>{{ rdp_data.port }}</td></tr>
            <tr><th>Valid Until</th><td>{{ rdp_data.valid_until }}</td></tr>
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    rdp_data = generate_rdp()
    return render_template_string(html_template, rdp_data=rdp_data)

@app.route('/api/rdp')
def api_rdp():
    return jsonify(generate_rdp())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
