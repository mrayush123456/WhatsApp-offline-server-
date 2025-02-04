from flask import Flask, render_template_string, request
import random
import string
import socket

app = Flask(__name__)

def get_free_port():
    """Finds a free port dynamically."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def generate_random_rdp():
    """Generates random RDP credentials."""
    ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))
    hostname = f"host-{random.randint(1000, 9999)}"
    username = "user" + "".join(random.choices(string.ascii_letters, k=5))
    password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    port = random.choice([3389, 3390, 3391])  # Common RDP ports
    return {"hostname": hostname, "ip": ip_address, "username": username, "password": password, "port": port}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Random RDP Generator</title>
    <style>
        body {
            background-image: url('https://source.unsplash.com/1920x1080/?technology');
            background-size: cover;
            text-align: center;
            color: white;
            font-family: Arial, sans-serif;
        }
        .container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        button {
            padding: 15px 30px;
            font-size: 20px;
            background-color: #ff9800;
            border: none;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background-color: #e68900;
        }
        .output {
            margin-top: 20px;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            display: inline-block;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Random RDP Generator</h1>
        <form method="POST">
            <select name="trial_option">
                <option value="30 Days">30 Days Trial</option>
                <option value="24 Hours">24 Hours Trial</option>
            </select>
            <br><br>
            <button type="submit">Generate RDP</button>
        </form>

        {% if rdp %}
        <div class="output">
            <h3>Generated RDP:</h3>
            <p><b>Trial Duration:</b> {{ trial }}</p>
            <p><b>Hostname:</b> {{ rdp.hostname }}</p>
            <p><b>IP Address:</b> {{ rdp.ip }}</p>
            <p><b>Username:</b> {{ rdp.username }}</p>
            <p><b>Password:</b> {{ rdp.password }}</p>
            <p><b>Port:</b> {{ rdp.port }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    rdp_details = None
    trial_option = None

    if request.method == "POST":
        trial_option = request.form.get("trial_option")
        rdp_details = generate_random_rdp()

    return render_template_string(HTML_TEMPLATE, rdp=rdp_details, trial=trial_option)

if __name__ == "__main__":
    port = get_free_port()  # Dynamically find an available port
    print(f"Running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
    
