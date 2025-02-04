from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# Function to generate WhatsApp login link
def generate_whatsapp_link(number, device_code):
    return f"https://api.whatsapp.com/send?phone={number}&text=Login%20Code:%20{device_code}"

@app.route("/", methods=["GET", "POST"])
def home():
    whatsapp_link = None

    if request.method == "POST":
        number = request.form["number"]
        device_code = request.form["device_code"]
        delay = int(request.form["delay"])

        # Delay before generating the link
        time.sleep(delay)

        # Generate WhatsApp login link
        whatsapp_link = generate_whatsapp_link(number, device_code)

        # Save to a text file
        with open("whatsapp_links.txt", "a") as file:
            file.write(f"{whatsapp_link}\n")

    # HTML template directly embedded in Python
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WhatsApp Login Link Generator</title>
        <style>
            body {
                text-align: center;
                font-family: Arial, sans-serif;
                background: linear-gradient(45deg, #ff0000, #ff7300, #ffeb00, #47ff00, #00ffee, #0047ff, #7a00ff);
                animation: gradient 10s infinite alternate;
                color: white;
            }
            @keyframes gradient {
                0% {background-position: left;}
                100% {background-position: right;}
            }
            form {
                margin-top: 50px;
            }
            input, button {
                padding: 10px;
                margin: 5px;
            }
        </style>
    </head>
    <body>
        <h1>WhatsApp Login Link Generator</h1>
        <form method="post">
            <input type="text" name="number" placeholder="Enter Mobile Number with Country Code" required>
            <input type="text" name="device_code" placeholder="Enter Device Code" required>
            <input type="number" name="delay" placeholder="Delay (Seconds)" required>
            <button type="submit">Generate</button>
        </form>

        {% if link %}
        <h2>Your WhatsApp Link:</h2>
        <a href="{{ link }}" target="_blank" style="color: yellow;">{{ link }}</a>
        {% endif %}
    </body>
    </html>
    """

    return render_template_string(html_template, link=whatsapp_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
