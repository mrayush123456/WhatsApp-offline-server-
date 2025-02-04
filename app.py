from flask import Flask, request, render_template_string
import requests
import datetime

app = Flask(__name__)

# Facebook App Credentials (Replace with your actual App ID & Secret)
FACEBOOK_APP_ID = "YOUR_FACEBOOK_APP_ID"
FACEBOOK_APP_SECRET = "YOUR_FACEBOOK_APP_SECRET"

# HTML template for the web page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Token Validator</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        input, button { padding: 10px; margin: 5px; }
        .valid { color: green; font-weight: bold; }
        .invalid { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Facebook Token Validator</h2>
    <form method="post">
        <label>Enter Access Token:</label><br>
        <input type="text" name="token" required size="50"><br>
        <button type="submit">Check Token</button>
    </form>
    
    {% if token_info %}
        <h3>Token Details:</h3>
        <p><strong>Token Status:</strong> 
            {% if token_info['valid'] %}
                <span class="valid">Valid</span>
            {% else %}
                <span class="invalid">Expired/Invalid</span>
            {% endif %}
        </p>
        <p><strong>Expires At:</strong> {{ token_info['expires_at'] }}</p>
        <p><strong>Issued At:</strong> {{ token_info['issued_at'] }}</p>
    {% endif %}
</body>
</html>
"""

def check_facebook_token(access_token):
    """
    Checks if a Facebook token is valid and retrieves expiration details.
    """
    debug_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={FACEBOOK_APP_ID}|{FACEBOOK_APP_SECRET}"
    
    response = requests.get(debug_url)
    data = response.json()

    if "data" in data and data["data"].get("is_valid"):
        expires_at = data["data"].get("expires_at", 0)
        issued_at = data["data"].get("issued_at", 0)

        expires_at = datetime.datetime.utcfromtimestamp(expires_at).strftime('%Y-%m-%d %H:%M:%S') if expires_at else "Unknown"
        issued_at = datetime.datetime.utcfromtimestamp(issued_at).strftime('%Y-%m-%d %H:%M:%S') if issued_at else "Unknown"

        return {"valid": True, "expires_at": expires_at, "issued_at": issued_at}
    else:
        return {"valid": False, "expires_at": "N/A", "issued_at": "N/A"}

@app.route("/", methods=["GET", "POST"])
def home():
    token_info = None
    if request.method == "POST":
        access_token = request.form["token"]
        token_info = check_facebook_token(access_token)

    return render_template_string(HTML_TEMPLATE, token_info=token_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
