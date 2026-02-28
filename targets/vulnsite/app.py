"""
CyberSim VulnSite — A realistic vulnerable web application for OWASP training.
Difficulty-based security: EASY (no filters), NORMAL (light sanitization),
HARD (WAF active), ULTRA_HARD (WAF + rate limiting + IP blocking).
"""
import os, sqlite3, hashlib, time, json, re, secrets, base64
from functools import wraps
from flask import (Flask, request, render_template, redirect, url_for,
                   session, jsonify, flash, make_response, g, abort)

app = Flask(__name__)
app.secret_key = "cybersim-vuln-secret-key-12345"
DB_PATH = "/app/vulnsite.db"
DIFFICULTY = os.environ.get("DIFFICULTY", "easy").lower()
UPLOAD_DIR = "/app/uploads"

# ─── CTF FLAGS (random hashes generated on startup) ──────────────────────────
import uuid
CTF_FLAGS = {
    "sqli_login":   "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "sqli_search":  "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "xss":          "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "idor":         "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "admin_access": "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "ssrf":         "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "cmd_injection":"FLAG{" + uuid.uuid4().hex[:16] + "}",
    "crypto":       "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "file_upload":  "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "misconfig":    "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "insecure_design": "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "auth_failure": "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "logging":      "FLAG{" + uuid.uuid4().hex[:16] + "}",
    "exceptions":   "FLAG{" + uuid.uuid4().hex[:16] + "}",
}

# Rate limiting storage
rate_limits = {}
blocked_ips = {}

# ─────────────────────────────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            security_question TEXT,
            security_answer TEXT,
            reset_token TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            image_url TEXT
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total REAL,
            status TEXT DEFAULT 'pending',
            coupon_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            author TEXT,
            content TEXT,
            rating INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            ip TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Create flags table
    db.execute("CREATE TABLE IF NOT EXISTS ctf_flags (id TEXT PRIMARY KEY, flag TEXT)")
    # Store flags in DB so they can be found via SQLi
    for fid, fval in CTF_FLAGS.items():
        try:
            db.execute("INSERT INTO ctf_flags (id, flag) VALUES (?,?)", (fid, fval))
        except sqlite3.IntegrityError:
            pass
    # Seed data
    try:
        pw_admin = hashlib.md5("admin123".encode()).hexdigest()
        pw_john  = hashlib.md5("password".encode()).hexdigest()
        pw_jane  = hashlib.md5("qwerty".encode()).hexdigest()
        db.execute("INSERT INTO users (username,email,password,role,security_question,security_answer) VALUES (?,?,?,?,?,?)",
                   ("admin","admin@shopsim.com",pw_admin,"admin","What is your pet's name?","fluffy"))
        db.execute("INSERT INTO users (username,email,password,role,security_question,security_answer) VALUES (?,?,?,?,?,?)",
                   ("john","john@shopsim.com",pw_john,"user","What city were you born in?","new york"))
        db.execute("INSERT INTO users (username,email,password,role,security_question,security_answer) VALUES (?,?,?,?,?,?)",
                   ("jane","jane@shopsim.com",pw_jane,"user","What is your mother's maiden name?","smith"))
        db.execute("INSERT INTO products (name,description,price,category) VALUES (?,?,?,?)",
                   ("Wireless Mouse","High-precision wireless mouse with ergonomic design",29.99,"Electronics"))
        db.execute("INSERT INTO products (name,description,price,category) VALUES (?,?,?,?)",
                   ("USB-C Hub","7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader",49.99,"Electronics"))
        db.execute("INSERT INTO products (name,description,price,category) VALUES (?,?,?,?)",
                   ("Mechanical Keyboard","Cherry MX Blue switches, RGB backlit",89.99,"Electronics"))
        db.execute("INSERT INTO products (name,description,price,category) VALUES (?,?,?,?)",
                   ("Security Camera","1080p WiFi security camera with night vision",39.99,"Security"))
        db.execute("INSERT INTO products (name,description,price,category) VALUES (?,?,?,?)",
                   ("VPN Router","Pre-configured VPN router for secure browsing",129.99,"Networking"))
        db.execute("INSERT INTO reviews (product_id,user_id,author,content,rating) VALUES (?,?,?,?,?)",
                   (1,2,"john","Great mouse! My pet fluffy loves sitting on it.",5))
        db.execute("INSERT INTO reviews (product_id,user_id,author,content,rating) VALUES (?,?,?,?,?)",
                   (2,3,"jane","Perfect hub for my MacBook. Born in New York, shipped fast!",4))
        db.commit()
    except sqlite3.IntegrityError:
        pass
    db.close()

# ─────────────────────────────────────────────────────────────────────
# WAF MIDDLEWARE (only active in hard/ultra_hard)
# ─────────────────────────────────────────────────────────────────────
WAF_PATTERNS = [
    r"(\bunion\b.*\bselect\b)", r"(--\s*$)", r"(;\s*drop\b)",
    r"(<script)", r"(javascript:)", r"(onerror\s*=)", r"(onload\s*=)",
    r"(\bexec\b.*\()", r"(\bsystem\b.*\()", r"(file:///)",
    r"(\.\.\/)", r"(%2e%2e)", r"(127\.0\.0\.1)", r"(localhost)",
]

def waf_check(value):
    """Check a value against WAF patterns. Returns True if blocked."""
    if DIFFICULTY not in ("hard", "ultra_hard"):
        return False
    if not value:
        return False
    for pattern in WAF_PATTERNS:
        if re.search(pattern, str(value), re.IGNORECASE):
            return True
    return False

def check_rate_limit(ip, limit=20, window=60):
    """Rate limiting for ultra_hard mode."""
    if DIFFICULTY != "ultra_hard":
        return False
    now = time.time()
    if ip not in rate_limits:
        rate_limits[ip] = []
    rate_limits[ip] = [t for t in rate_limits[ip] if now - t < window]
    if len(rate_limits[ip]) >= limit:
        blocked_ips[ip] = now + 120
        return True
    rate_limits[ip].append(now)
    return False

@app.before_request
def before_request_checks():
    ip = request.remote_addr
    # IP block check
    if ip in blocked_ips:
        if time.time() < blocked_ips[ip]:
            return jsonify({"error": "IP blocked. Try again later."}), 403
        else:
            del blocked_ips[ip]
    # Rate limiting
    if check_rate_limit(ip):
        return jsonify({"error": "Rate limit exceeded. Blocked for 2 minutes."}), 429

def light_sanitize(value):
    """Light sanitization for normal mode."""
    if DIFFICULTY == "normal":
        value = value.replace("'", "''").replace('"', '\\"')
    return value

# ─────────────────────────────────────────────────────────────────────
# SECURITY HEADERS (only in hard/ultra_hard)
# ─────────────────────────────────────────────────────────────────────
@app.after_request
def security_headers(response):
    if DIFFICULTY in ("hard", "ultra_hard"):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
    if DIFFICULTY == "ultra_hard":
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response

# ─────────────────────────────────────────────────────────────────────
# ROUTES — HOME
# ─────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("index.html", products=products, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A07: AUTH — LOGIN (SQL Injection vulnerable in easy mode)
# ─────────────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        if waf_check(email) or waf_check(password):
            error = "Request blocked by security filter."
            return render_template("login.html", error=error, difficulty=DIFFICULTY)

        if DIFFICULTY in ("easy",):
            # VULNERABLE: Raw SQL injection
            query = f"SELECT * FROM users WHERE email='{email}' AND password='{hashlib.md5(password.encode()).hexdigest()}'"
            try:
                db = get_db()
                user = db.execute(query).fetchone()
                if user:
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["role"] = user["role"]
                    session["email"] = user["email"]
                    flash(f"🚩 SQLi Login Flag: {CTF_FLAGS['sqli_login']}")
                    return redirect(url_for("home"))
                error = "Invalid email or password."
            except Exception as e:
                error = f"Database error: {e}" if DIFFICULTY == "easy" else "Login failed."
        elif DIFFICULTY == "normal":
            # Slightly vulnerable: simple sanitization but still bypassable
            email = light_sanitize(email)
            query = f"SELECT * FROM users WHERE email='{email}' AND password='{hashlib.md5(password.encode()).hexdigest()}'"
            try:
                db = get_db()
                user = db.execute(query).fetchone()
                if user:
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["role"] = user["role"]
                    session["email"] = user["email"]
                    return redirect(url_for("home"))
                error = "Invalid credentials."
            except Exception:
                error = "Login failed."
        else:
            # SECURE: Parameterized queries
            db = get_db()
            pw_hash = hashlib.md5(password.encode()).hexdigest()
            user = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, pw_hash)).fetchone()
            if user:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                session["email"] = user["email"]
                return redirect(url_for("home"))
            error = "Invalid credentials."

    return render_template("login.html", error=error, difficulty=DIFFICULTY)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        security_q = request.form.get("security_question", "What is your pet's name?")
        security_a = request.form.get("security_answer", "")

        if DIFFICULTY == "ultra_hard" and len(password) < 8:
            error = "Password must be at least 8 characters."
            return render_template("register.html", error=error, difficulty=DIFFICULTY)

        try:
            db = get_db()
            pw_hash = hashlib.md5(password.encode()).hexdigest()
            db.execute("INSERT INTO users (username,email,password,security_question,security_answer) VALUES (?,?,?,?,?)",
                       (username, email, pw_hash, security_q, security_a))
            db.commit()
            return redirect(url_for("login"))
        except Exception as e:
            error = f"Registration failed: {e}" if DIFFICULTY == "easy" else "Registration failed."

    return render_template("register.html", error=error, difficulty=DIFFICULTY)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ─────────────────────────────────────────────────────────────────────
# A05: INJECTION — SEARCH (SQL Injection + XSS)
# ─────────────────────────────────────────────────────────────────────
@app.route("/search")
def search():
    q = request.args.get("q", "")

    if waf_check(q):
        return render_template("search.html", query=q, products=[], error="Blocked by WAF.", difficulty=DIFFICULTY)

    db = get_db()
    if DIFFICULTY in ("easy",):
        # VULNERABLE: Raw SQL
        query = f"SELECT * FROM products WHERE name LIKE '%{q}%' OR description LIKE '%{q}%'"
        try:
            products = db.execute(query).fetchall()
        except Exception as e:
            return render_template("search.html", query=q, products=[], error=str(e), difficulty=DIFFICULTY)
    elif DIFFICULTY == "normal":
        q_san = light_sanitize(q)
        query = f"SELECT * FROM products WHERE name LIKE '%{q_san}%' OR description LIKE '%{q_san}%'"
        try:
            products = db.execute(query).fetchall()
        except Exception:
            products = []
    else:
        # SECURE
        products = db.execute("SELECT * FROM products WHERE name LIKE ? OR description LIKE ?",
                              (f"%{q}%", f"%{q}%")).fetchall()

    # XSS: In easy/normal mode, query is reflected unescaped in template
    return render_template("search.html", query=q, products=products, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A01: BROKEN ACCESS CONTROL — USER PROFILES (IDOR)
# ─────────────────────────────────────────────────────────────────────
@app.route("/profile/<int:user_id>")
def profile(user_id):
    db = get_db()

    if DIFFICULTY in ("hard", "ultra_hard"):
        # SECURE: Only allow viewing own profile
        if "user_id" not in session or session["user_id"] != user_id:
            abort(403)

    user = db.execute("SELECT id,username,email,role,created_at FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        abort(404)

    orders = db.execute("SELECT o.*,p.name as product_name FROM orders o JOIN products p ON o.product_id=p.id WHERE o.user_id=?", (user_id,)).fetchall()
    return render_template("profile.html", user=user, orders=orders, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A01: BROKEN ACCESS CONTROL — ADMIN PANEL
# ─────────────────────────────────────────────────────────────────────
@app.route("/admin")
def admin():
    if DIFFICULTY in ("hard", "ultra_hard"):
        if "role" not in session or session["role"] != "admin":
            abort(403)

    db = get_db()
    users = db.execute("SELECT id,username,email,role,created_at FROM users").fetchall()
    # Flag hidden in admin page
    return render_template("admin.html", users=users, difficulty=DIFFICULTY, flag=CTF_FLAGS['admin_access'])

# ─────────────────────────────────────────────────────────────────────
# A06: INSECURE DESIGN — PASSWORD RESET
# ─────────────────────────────────────────────────────────────────────
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    error = None
    success = None
    question = None
    email_val = request.form.get("email", request.args.get("email", ""))

    if request.method == "POST":
        action = request.form.get("action", "")
        email = request.form.get("email", "")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        if action == "get_question":
            if user:
                question = user["security_question"]
                email_val = email
            else:
                error = "Email not found."

        elif action == "reset":
            answer = request.form.get("answer", "")
            new_password = request.form.get("new_password", "")
            if user:
                if DIFFICULTY in ("easy", "normal"):
                    # VULNERABLE: Case-insensitive comparison, no rate limiting
                    if answer.lower() == user["security_answer"].lower():
                        pw_hash = hashlib.md5(new_password.encode()).hexdigest()
                        db.execute("UPDATE users SET password=? WHERE id=?", (pw_hash, user["id"]))
                        db.commit()
                        success = "Password reset successfully!"
                    else:
                        error = "Wrong answer."
                        question = user["security_question"]
                else:
                    # SECURE: Exact match + rate limiting on attempts
                    if answer == user["security_answer"]:
                        pw_hash = hashlib.md5(new_password.encode()).hexdigest()
                        db.execute("UPDATE users SET password=? WHERE id=?", (pw_hash, user["id"]))
                        db.commit()
                        success = "Password reset successfully!"
                    else:
                        error = "Incorrect."
                        question = user["security_question"]

    return render_template("forgot_password.html", error=error, success=success,
                           question=question, email=email_val, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A05: COMMAND INJECTION — CONTACT FORM
# ─────────────────────────────────────────────────────────────────────
@app.route("/contact", methods=["GET", "POST"])
def contact():
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        message = request.form.get("message", "")

        if waf_check(message) or waf_check(name):
            return render_template("contact.html", result="Blocked by WAF.", difficulty=DIFFICULTY)

        # Store feedback
        db = get_db()
        if DIFFICULTY in ("easy",):
            # VULNERABLE: Command injection via os.popen in email validation
            check = os.popen(f"echo {email} | grep -c '@'").read()
            db.execute("INSERT INTO feedback (name,email,message) VALUES (?,?,?)", (name, email, message))
            db.commit()
            result = f"Thank you {name}! Your message has been received."
        else:
            db.execute("INSERT INTO feedback (name,email,message) VALUES (?,?,?)", (name, email, message))
            db.commit()
            result = f"Thank you! Your message has been received."

    return render_template("contact.html", result=result, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A01/A10: SSRF — URL FETCH
# ─────────────────────────────────────────────────────────────────────
@app.route("/fetch", methods=["GET", "POST"])
def fetch_url():
    result = None
    if request.method == "POST":
        url = request.form.get("url", "")

        if waf_check(url):
            return render_template("fetch.html", result="Blocked by WAF.", difficulty=DIFFICULTY)

        if DIFFICULTY in ("easy", "normal"):
            # VULNERABLE: No URL validation — SSRF possible
            try:
                import urllib.request
                resp = urllib.request.urlopen(url, timeout=5)
                result = resp.read().decode("utf-8", errors="replace")[:2000]
            except Exception as e:
                result = f"Error: {e}" if DIFFICULTY == "easy" else "Could not fetch URL."
        else:
            # SECURE: Whitelist check
            if url.startswith("https://"):
                try:
                    import urllib.request
                    resp = urllib.request.urlopen(url, timeout=5)
                    result = resp.read().decode("utf-8", errors="replace")[:2000]
                except Exception:
                    result = "Could not fetch URL."
            else:
                result = "Only HTTPS URLs are allowed."

    return render_template("fetch.html", result=result, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A08: DATA INTEGRITY — FILE UPLOAD
# ─────────────────────────────────────────────────────────────────────
@app.route("/upload", methods=["GET", "POST"])
def upload():
    result = None
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            if DIFFICULTY in ("easy",):
                # VULNERABLE: No extension check, no content type check
                filepath = os.path.join(UPLOAD_DIR, file.filename)
                file.save(filepath)
                result = f"File uploaded: {file.filename}"
            elif DIFFICULTY == "normal":
                # Basic extension check (easy to bypass)
                if file.filename.endswith((".jpg", ".png", ".pdf")):
                    filepath = os.path.join(UPLOAD_DIR, file.filename)
                    file.save(filepath)
                    result = f"File uploaded: {file.filename}"
                else:
                    result = "Only .jpg, .png, .pdf files allowed."
            else:
                # SECURE: Whitelist + content type + random name
                allowed = {"image/jpeg", "image/png", "application/pdf"}
                if file.content_type in allowed:
                    safe_name = secrets.token_hex(8) + os.path.splitext(file.filename)[1]
                    filepath = os.path.join(UPLOAD_DIR, safe_name)
                    file.save(filepath)
                    result = f"File uploaded: {safe_name}"
                else:
                    result = "Invalid file type."

    return render_template("upload.html", result=result, difficulty=DIFFICULTY)

# ─────────────────────────────────────────────────────────────────────
# A04: CRYPTO — EXPOSED DATA
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/users")
def api_users():
    db = get_db()
    if DIFFICULTY in ("easy",):
        # VULNERABLE: Exposes password hashes
        users = db.execute("SELECT id,username,email,password,role FROM users").fetchall()
        return jsonify([dict(u) for u in users])
    elif DIFFICULTY == "normal":
        # Leaks some data
        users = db.execute("SELECT id,username,email,role FROM users").fetchall()
        return jsonify([dict(u) for u in users])
    else:
        if "role" not in session or session["role"] != "admin":
            return jsonify({"error": "Unauthorized"}), 403
        users = db.execute("SELECT id,username,role FROM users").fetchall()
        return jsonify([dict(u) for u in users])

# ─────────────────────────────────────────────────────────────────────
# A01: IDOR — ORDER API
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/order/<int:order_id>")
def api_order(order_id):
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    if DIFFICULTY in ("hard", "ultra_hard"):
        if "user_id" not in session or session["user_id"] != order["user_id"]:
            return jsonify({"error": "Unauthorized"}), 403

    return jsonify(dict(order))

# ─────────────────────────────────────────────────────────────────────
# A02: MISCONFIG — DEBUG ENDPOINT
# ─────────────────────────────────────────────────────────────────────
@app.route("/debug")
def debug_page():
    if DIFFICULTY in ("hard", "ultra_hard"):
        abort(404)
    return jsonify({
        "app": "CyberSim VulnSite",
        "version": "1.0.0",
        "db_path": DB_PATH,
        "secret_key": app.secret_key,
        "difficulty": DIFFICULTY,
        "users_count": get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "env": dict(os.environ),
        "flag_misconfig": CTF_FLAGS["misconfig"],
    })

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /admin\nDisallow: /debug\nDisallow: /api/users\nDisallow: /backup/\n"

@app.route("/backup/db.sql")
def backup():
    if DIFFICULTY in ("hard", "ultra_hard"):
        abort(404)
    return "-- Database backup\n-- admin password hash: " + hashlib.md5("admin123".encode()).hexdigest()

# ─────────────────────────────────────────────────────────────────────
# A09: LOGGING — Check if events are logged
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/logs")
def api_logs():
    if DIFFICULTY in ("hard", "ultra_hard"):
        if "role" not in session or session["role"] != "admin":
            return jsonify({"error": "Unauthorized"}), 403
    db = get_db()
    logs = db.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50").fetchall()
    return jsonify([dict(l) for l in logs])

# ─────────────────────────────────────────────────────────────────────
# A10: EXCEPTION — ERROR HANDLER
# ─────────────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    if DIFFICULTY in ("easy",):
        return jsonify({"error": "Not found", "path": request.path,
                        "server": "CyberSim VulnSite/Flask",
                        "db": DB_PATH,
                        "flag_exceptions": CTF_FLAGS["exceptions"]}), 404
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    if DIFFICULTY in ("easy", "normal"):
        return jsonify({"error": str(e), "trace": repr(e)}), 500
    return jsonify({"error": "Internal server error"}), 500

@app.route("/product/<int:product_id>")
def product(product_id):
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not product:
        abort(404)
    reviews = db.execute("SELECT * FROM reviews WHERE product_id=?", (product_id,)).fetchall()
    return render_template("product.html", product=product, reviews=reviews, difficulty=DIFFICULTY)

@app.route("/product/<int:product_id>/review", methods=["POST"])
def add_review(product_id):
    content = request.form.get("content", "")
    rating = request.form.get("rating", 5)
    author = request.form.get("author", session.get("username", "Anonymous"))

    if waf_check(content):
        flash("Review blocked by security filter.")
        return redirect(url_for("product", product_id=product_id))

    db = get_db()
    if DIFFICULTY in ("easy", "normal"):
        # VULNERABLE: author field can be forged + XSS in content
        db.execute("INSERT INTO reviews (product_id,user_id,author,content,rating) VALUES (?,?,?,?,?)",
                   (product_id, session.get("user_id", 0), author, content, rating))
    else:
        # SECURE: Author from session only
        if "user_id" not in session:
            abort(403)
        db.execute("INSERT INTO reviews (product_id,user_id,author,content,rating) VALUES (?,?,?,?,?)",
                   (product_id, session["user_id"], session["username"], content, rating))
    db.commit()
    return redirect(url_for("product", product_id=product_id))

@app.route("/buy/<int:product_id>", methods=["POST"])
def buy(product_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    quantity = int(request.form.get("quantity", 1))
    coupon = request.form.get("coupon", "")
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not product:
        abort(404)

    total = product["price"] * quantity

    if DIFFICULTY in ("easy", "normal"):
        # VULNERABLE: Negative quantity, reusable coupons
        if coupon == "DISCOUNT50":
            total = total * 0.5
    else:
        if quantity < 1:
            flash("Invalid quantity.")
            return redirect(url_for("product", product_id=product_id))
        if coupon == "DISCOUNT50":
            total = total * 0.5

    db.execute("INSERT INTO orders (user_id,product_id,quantity,total,coupon_code) VALUES (?,?,?,?,?)",
               (session["user_id"], product_id, quantity, total, coupon))
    db.commit()
    flash(f"Order placed! Total: ${total:.2f}")
    return redirect(url_for("profile", user_id=session["user_id"]))

# ─────────────────────────────────────────────────────────────────────
# A02: .env EXPOSURE
# ─────────────────────────────────────────────────────────────────────
@app.route("/.env")
def env_file():
    if DIFFICULTY in ("hard", "ultra_hard"):
        abort(404)
    return "DB_HOST=localhost\nDB_USER=root\nDB_PASS=cybersim123\nSECRET_KEY=cybersim-vuln-secret-key-12345\nADMIN_EMAIL=admin@shopsim.com\n"

# ─────────────────────────────────────────────────────────────────────
# FLAG VERIFICATION API (used by CyberSim terminal)
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/verify-flag", methods=["POST"])
def verify_flag():
    data = request.get_json() or {}
    submitted = data.get("flag", "")
    for fid, fval in CTF_FLAGS.items():
        if submitted.strip() == fval:
            return jsonify({"valid": True, "vuln_id": fid, "message": f"Correct! You captured the {fid} flag."})
    return jsonify({"valid": False, "message": "Invalid flag. Keep hacking!"}), 400

@app.route("/api/flags-status")
def flags_status():
    """Show which flags exist (not their values) for progress tracking."""
    return jsonify({"total_flags": len(CTF_FLAGS), "flag_ids": list(CTF_FLAGS.keys())})

# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print(f"[CyberSim VulnSite] Running on http://0.0.0.0:5000 | Difficulty: {DIFFICULTY}")
    print(f"[FLAGS] {len(CTF_FLAGS)} CTF flags active (random hashes, regenerated each restart)")
    app.run(host="0.0.0.0", port=5000, debug=(DIFFICULTY == "easy"))
