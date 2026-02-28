"""
Vulnerable Web App - CyberSim Level 10 Target
Intentionally vulnerable Flask application for training purposes.
"""
from flask import Flask, request, render_template_string, session
import sqlite3
import os
import logging

app = Flask(__name__)
app.secret_key = "supersecretkey123"

logging.basicConfig(
    filename='/var/log/web_victim.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

# ─── Database Setup ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('/tmp/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'supersecret123', 'admin')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password', 'user')")
    conn.commit()
    conn.close()

init_db()

# ─── Templates ────────────────────────────────────────────────────────────────
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>CyberSim Corp - Login</title>
    <style>
        body { background: #1a1a2e; color: #eee; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #16213e; padding: 40px; border: 1px solid #0f3460; border-radius: 8px; width: 350px; }
        h2 { color: #e94560; text-align: center; }
        input { width: 100%; padding: 10px; margin: 8px 0; background: #0f3460; border: none; color: #eee; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #e94560; border: none; color: white; cursor: pointer; border-radius: 4px; font-size: 16px; }
        .msg { color: #e94560; text-align: center; margin-top: 10px; }
        .flag { color: #00ff88; background: #0a2a1a; padding: 10px; border-radius: 4px; margin-top: 15px; font-size: 12px; word-break: break-all; }
    </style>
</head>
<body>
<div class="box">
    <h2>🔒 CORP LOGIN</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">LOGIN</button>
    </form>
    {% if error %}<p class="msg">{{ error }}</p>{% endif %}
    {% if flag %}<div class="flag">{{ flag }}</div>{% endif %}
</div>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>CyberSim Corp - Dashboard</title>
    <style>
        body { background: #1a1a2e; color: #eee; font-family: monospace; padding: 40px; }
        h1 { color: #00ff88; }
        .comment-box { background: #16213e; padding: 20px; border-radius: 8px; margin: 20px 0; }
        input[type=text] { width: 70%; padding: 10px; background: #0f3460; border: none; color: #eee; border-radius: 4px; }
        button { padding: 10px 20px; background: #e94560; border: none; color: white; cursor: pointer; border-radius: 4px; }
        .comments { margin-top: 20px; }
        .comment { background: #0f3460; padding: 10px; margin: 5px 0; border-radius: 4px; }
        .flag { color: #00ff88; background: #0a2a1a; padding: 10px; border-radius: 4px; margin-top: 15px; }
    </style>
</head>
<body>
<h1>Welcome, {{ username }}!</h1>
<div class="comment-box">
    <h3>💬 Leave a Comment (XSS Challenge)</h3>
    <form method="POST" action="/comment">
        <input type="text" name="comment" placeholder="Enter your comment...">
        <button type="submit">Post</button>
    </form>
    <div class="comments">
        {% for c in comments %}
        <div class="comment">{{ c | safe }}</div>
        {% endfor %}
    </div>
    {% if xss_flag %}
    <div class="flag">XSS Detected! {{ xss_flag }}</div>
    {% endif %}
</div>
</body>
</html>
"""

# ─── In-memory comment store ───────────────────────────────────────────────────
comments = []
xss_triggered = False

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    flag = None

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Log the attempt (Defender monitors this)
        logging.info(f"Login attempt: username='{username}' password='{password}' ip={request.remote_addr}")

        # INTENTIONALLY VULNERABLE: SQL Injection
        try:
            conn = sqlite3.connect('/tmp/users.db')
            c = conn.cursor()
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            logging.info(f"Query: {query}")
            c.execute(query)
            user = c.fetchone()
            conn.close()

            if user:
                session['user'] = user[1]
                flag = "FLAG{sql_1nj3ct10n_byp4ss} - You bypassed the login!"
                return render_template_string(LOGIN_PAGE, error=None, flag=flag)
            else:
                error = "Invalid credentials."
        except Exception as e:
            error = f"DB Error: {e}"

    return render_template_string(LOGIN_PAGE, error=error, flag=flag)


@app.route('/dashboard')
def dashboard():
    global xss_triggered
    user = session.get('user', 'Guest')
    xss_flag = "FLAG{xss_st0r3d_4tt4ck}" if xss_triggered else None
    return render_template_string(DASHBOARD_PAGE, username=user, comments=comments, xss_flag=xss_flag)


@app.route('/comment', methods=['POST'])
def comment():
    global xss_triggered
    c = request.form.get('comment', '')
    logging.info(f"Comment posted: {c} from {request.remote_addr}")

    # INTENTIONALLY VULNERABLE: Stored XSS (no sanitization)
    if '<script>' in c.lower():
        xss_triggered = True
    comments.append(c)
    return dashboard()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
