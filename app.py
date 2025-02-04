from flask import Flask, render_template_string, request
import random
import string
import socket

app = Flask(__name__)

def get_available_port():
    """Finds an available port dynamically."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def generate_random_rdp():
    """Generates random RDP credentials."""
    ip_address = ".".join(str(random.randint(1, 255)) for _ in range(4))
    hostname = f"host-{random.randint(1000, 9999)}"
    username = "user" + "".join(random.choices(string.ascii_letters, k=5))
    password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    port = random.choice([3389, 3390, 3391])  # Common RDP ports
    return {"hostname": hostname, "ip": ip_address, "username": username, "password": password, "port": port}

@app.route("/", methods=["GET", "POST"])
def home():
    rdp_details = None
    trial_option = None
    
    if request.method == "POST":
        trial_option = request.form.get("trial_option")
        rdp_details = generate_random_rdp()

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RDP Generator</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(45deg, #2c3e50, #3498db);
                    background-size: 400% 400%;
                    animation: gradient 10s ease infinite;
                    text-align: center;
                    color: white;
                }
                @keyframes gradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                .container {
                    margin-top: 50px;
                    padding: 20px;
                    border-radius: 10px;
                    background: rgba(255, 255, 255, 0.1);
                    display: inline-block;
                }
                button {
                    padding: 10px 20px;
                    font-size: 18px;
                    background-color: #27ae60;
                    border: none;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #2ecc71;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Random RDP Generator</h2>
                <form method="post">
                    <label>Select Trial Option:</label><br>
                    <input type="radio" name="trial_option" value="30 Days"> 30 Days<br>
                    <input type="radio" name="trial_option" value="24 Hours"> 24 Hours<br>
                    <br>
                    <button type="submit">Generate RDP</button>
                </form>

                {% if rdp %}
                <h3>Generated RDP Details:</h3>
                <p><strong>Trial Duration:</strong> {{ trial }}</p>
                <p><strong>Hostname:</strong> {{ rdp.hostname }}</p>
                <p><strong>IP Address:</strong> {{ rdp.ip }}</p>
                <p><strong>Username:</strong> {{ rdp.username }}</p>
                <p><strong>Password:</strong> {{ rdp.password }}</p>
                <p><strong>Port:</strong> {{ rdp.port }}</p>
                {% endif %}
            </div>
        </body>
        </html>
    """, rdp=rdp_details, trial=trial_option)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
