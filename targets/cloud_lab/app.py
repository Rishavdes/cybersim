import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

S3_BUCKETS = {
    "public-assets": {"logo.png": "binary data", "styles.css": "body { color: red; }"},
    "company-confidential": {"passwords.txt": "admin:Sup3rS3cr3t", "flag.txt": "FLAG_PLACEHOLDER"}
}

HTML_INDEX = """
<!DOCTYPE html>
<html>
<head><title>Cloud Image Fetcher</title></head>
<body>
    <h2>Fetch External Image</h2>
    <form action="/fetch" method="GET">
        URL: <input type="text" name="url" placeholder="http://example.com/image.png" size="50">
        <input type="submit" value="Fetch">
    </form>
    <hr>
    <h3>Company Cloud Storage</h3>
    <p>Browse our public assets at /s3/public-assets/</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return "Please provide a URL.", 400
    try:
        r = requests.get(url, timeout=3)
        return f"<pre>Fetched content from {url}:\n\n{r.text}</pre>"
    except Exception as e:
        return f"Error fetching URL: {str(e)}", 500

@app.route('/s3/<bucket>/', defaults={'key': ''})
@app.route('/s3/<bucket>/<path:key>')
def s3_access(bucket, key):
    if bucket not in S3_BUCKETS:
        return jsonify({"error": "NoSuchBucket"}), 404
    if not key:
        return jsonify({"Name": bucket, "Contents": [{"Key": k} for k in S3_BUCKETS[bucket].keys()]})
    if key in S3_BUCKETS[bucket]:
        content = S3_BUCKETS[bucket][key]
        if content == "FLAG_PLACEHOLDER":
            content = os.environ.get("CYBERSIM_FLAG", "FLAG{cloud_s3_default}")
        return content, 200, {'Content-Type': 'text/plain'}
    return jsonify({"error": "NoSuchKey"}), 404

@app.route('/latest/meta-data/')
def imds_root():
    return "iam/\nhostname\npublic-keys/"

@app.route('/latest/meta-data/iam/security-credentials/')
def imds_iam():
    return "s3-admin-role"

@app.route('/latest/meta-data/iam/security-credentials/s3-admin-role')
def imds_creds():
    flag = os.environ.get("CYBERSIM_FLAG", "FLAG{cloud_imds_default}")
    return jsonify({
        "Code": "Success",
        "Type": "AWS-HMAC",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "Token": flag,
        "Expiration": "2026-12-31T23:59:59Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
