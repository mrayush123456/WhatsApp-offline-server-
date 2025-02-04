from flask import Flask, render_template_string, request
import random
import string
import socket

app = Flask(__name__)

def generate_random_rdp():
    ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))
    hostname = f"host-{random.randint(1000, 9999)}"
    username = "user" + "".join(random.choices(string.ascii_letters, k=5))
    password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    port = random.choice([3389, 3390, 3391])  # Common RDP ports
    return {"hostname": hostname, "ip": ip_address, "username": username, "password": password, "port": port}

@app.route("/", methods=["GET", "POST"])
def home():
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
                        font-size: 20px;
                        background: linear-gradient(45deg, #ff6b6b, #f9d423);
                        background-size: 400% 400%;
                        animation: gradientAnimation 10s ease infinite;
                        color: #333;
                        font-family: Arial, sans-serif;
                    }
                    h2 {
                        text-align: center;
                    }
                    button {
                        padding: 10px 20px;
                        background-color: #008CBA;
                        border: none;
                        color: white;
                        font-size: 18px;
                        cursor: pointer;
                    }
                    button:hover {
                        background-color: #005f73;
                    }
                    p {
                        font-size: 18px;
                    }
                    label {
                        font-size: 18px;
                    }
                    @keyframes gradientAnimation {
                        0% {
                            background-position: 0% 50%;
                        }
                        50% {
                            background-position: 100% 50%;
                        }
                        100% {
                            background-position: 0% 50%;
                        }
                    }
                </style>
            </head>
            <body>
                <h2>Random RDP Generator</h2>
                <form method="post">
                    <label>Select Trial Option:</label><br>
                    <input type="radio" name="trial_option" value="30 Days"> 30 Days<br>
                    <input type="radio" name="trial_option" value="24 Hours"> 24 Hours<br>
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
            </body>
            </html>
        """, rdp=rdp_details, trial=trial_option)
    
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RDP Generator</title>
            <style>
                body {
                    font-size: 20px;
                    background: linear-gradient(45deg, #ff6b6b, #f9d423);
                    background-size: 400% 400%;
                    animation: gradientAnimation 10s ease infinite;
                    color: #333;
                    font-family: Arial, sans-serif;
                }
                h2 {
                    text-align: center;
                }
                button {
                    padding: 10px 20px;
                    background-color: #008CBA;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #005f73;
                }
                label {
                    font-size: 18px;
                }
                @keyframes gradientAnimation {
                    0% {
                        background-position: 0% 50%;
                    }
                    50% {
                        background-position: 100% 50%;
                    }
                    100% {
                        background-position: 0% 50%;
                    }
                }
            </style>
        </head>
        <body>
            <h2>Random RDP Generator</h2>
            <form method="post">
                <label>Select Trial Option:</label><br>
                <input type="radio" name="trial_option" value="30 Days"> 30 Days<br>
                <input type="radio" name="trial_option" value="24 Hours"> 24 Hours<br>
                <button type="submit">Generate RDP</button>
            </form>
        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
