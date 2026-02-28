import os
import hashlib
import hmac
from flask import Flask, render_template_string, Response, request

app = Flask(__name__)

SSID = b"CyberSim_Corporate_WiFi"
BSSID = b"\x11\x22\x33\x44\x55\x66"
CLIENT_MAC = b"\xAA\xBB\xCC\xDD\xEE\xFF"
PASSWORD = b"P@ssw0rd2024"

pmk = hashlib.pbkdf2_hmac('sha1', PASSWORD, SSID, 4096, 32)
pmk_name = b"PMK Name"
message = pmk_name + BSSID + CLIENT_MAC
pmkid = hmac.new(pmk, message, hashlib.sha1).digest()[:16]
hashcat_line = f"{pmkid.hex()}*{BSSID.hex()}*{CLIENT_MAC.hex()}*{SSID.hex()}"

HTML_INDEX = """
<!DOCTYPE html>
<html>
<head><title>CyberSim Wireless Lab</title></head>
<body>
    <h2>Wireless Reconnaissance Simulation</h2>
    <p>Target SSID: <strong>CyberSim_Corporate_WiFi</strong></p>
    <h3>Captured PMKID Hash</h3>
    <pre style="background:#222;color:#0f0;padding:10px;">{{ hash }}</pre>
    <h3>Instructions</h3>
    <ol>
        <li>Save the hash to hash.txt</li>
        <li>Download the <a href="/wordlist">wordlist</a></li>
        <li>Run: <code>hashcat -m 16800 hash.txt wordlist.txt</code></li>
    </ol>
    <hr>
    <p><a href="/verify">Submit cracked password</a> to get the flag.</p>
</body>
</html>
"""

HTML_VERIFY = """
<!DOCTYPE html>
<html>
<head><title>Verify WiFi Password</title></head>
<body>
    <h2>Submit Cracked Password</h2>
    <form action="/verify" method="POST">
        Password: <input type="text" name="password">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INDEX, hash=hashcat_line)

@app.route('/wordlist')
def wordlist():
    words = ["password123", "admin", "admin123", "CyberSim2024",
             "P@ssw0rd2024", "Welcome123", "companywifi", "guest"]
    return Response("\n".join(words), mimetype='text/plain')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        return render_template_string(HTML_VERIFY)
    submitted = request.form.get('password')
    if submitted == PASSWORD.decode('utf-8'):
        flag = os.environ.get('CYBERSIM_FLAG', 'FLAG{wifi_cracked_default}')
        return f"<h2>Success!</h2><p>WiFi password cracked.</p><p>{flag}</p>"
    return "<h2>Failed</h2><p>Incorrect password.</p><a href='/verify'>Try again</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
