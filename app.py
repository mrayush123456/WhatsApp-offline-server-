from flask import Flask, request, render_template_string

app = Flask(__name__)

html_content = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>WhatsApp Automation</title>
    <script src=\"https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js\"></script>
</head>
<body>
    <h2>WhatsApp Automation</h2>
    
    <label for=\"deviceNumber\">WhatsApp Number:</label>
    <input type=\"text\" id=\"deviceNumber\" placeholder=\"Enter your WhatsApp number\"><br>
    
    <label for=\"targetNumber\">Target Number/Thread ID:</label>
    <input type=\"text\" id=\"targetNumber\" placeholder=\"Enter target number or thread ID\"><br>
    
    <label for=\"message\">Message:</label>
    <textarea id=\"message\" placeholder=\"Enter your message\"></textarea><br>
    
    <label for=\"speed\">Speed (seconds):</label>
    <input type=\"number\" id=\"speed\" min=\"1\" value=\"5\"><br>
    
    <label for=\"fileInput\">Upload TXT File:</label>
    <input type=\"file\" id=\"fileInput\" accept=\".txt\"><br>
    
    <label for=\"mentionName\">Mention Name:</label>
    <input type=\"text\" id=\"mentionName\" placeholder=\"Enter name to mention\"><br>
    
    <button onclick=\"generateQRCode()\">Generate QR Code</button>
    <div id=\"qrcode\"></div>
    
    <button onclick=\"sendMessage()\">Send Message</button>
    
    <script>
        function generateQRCode() {
            let number = document.getElementById('deviceNumber').value;
            if (number) {
                document.getElementById('qrcode').innerHTML = '';
                new QRCode(document.getElementById(\"qrcode\"), `https://wa.me/${number}`);
            } else {
                alert(\"Enter your WhatsApp number\");
            }
        }

        function sendMessage() {
            let deviceNumber = document.getElementById('deviceNumber').value;
            let targetNumber = document.getElementById('targetNumber').value;
            let message = document.getElementById('message').value;
            let speed = document.getElementById('speed').value * 1000;
            let mention = document.getElementById('mentionName').value;
            
            if (!deviceNumber || !targetNumber || !message) {
                alert(\"Please fill in all fields.\");
                return;
            }
            
            let finalMessage = mention ? `@${mention} ${message}` : message;
            
            setTimeout(() => {
                let whatsappLink = `https://api.whatsapp.com/send?phone=${targetNumber}&text=${encodeURIComponent(finalMessage)}`;
                window.open(whatsappLink, '_blank');
            }, speed);
        }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
