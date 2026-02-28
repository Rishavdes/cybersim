"""
CyberSim Knowledge Base — Pre-built answers for every vulnerability.
Fast, offline answers. Optional AI fallback via Ollama.
"""
import json, urllib.request

CYAN = "\033[96m"; GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"
BOLD = "\033[1m"; DIM = "\033[2m"; RESET = "\033[0m"; MAGENTA = "\033[95m"

KNOWLEDGE = {
    # ─── A01: Broken Access Control ───────────────────────────────
    "idor_1": {"title": "IDOR (Insecure Direct Object Reference)",
        "explain": "IDOR occurs when an app uses user-supplied input to access objects (e.g. /profile/1) without checking if the user owns that object.",
        "fix": "Always verify the logged-in user owns the resource. Use session-based ownership checks.",
        "tools": ["Burp Suite Intruder (iterate IDs)", "curl (change params)", "OWASP ZAP"],
        "example": "Change /profile/1 → /profile/2 in the URL bar. If you see another user's data, it's IDOR."},
    "idor_2": {"title": "API IDOR — Order Access",
        "explain": "REST APIs that return data based on sequential IDs without auth checks allow anyone to enumerate all records.",
        "fix": "Check session.user_id == order.user_id before returning data. Use UUIDs instead of sequential IDs.",
        "tools": ["curl", "Postman", "Burp Repeater"],
        "example": "GET /api/order/1, /api/order/2, ... — you can read all orders."},
    "admin_1": {"title": "Forced Browsing — Admin Panel",
        "explain": "Admin panels accessible without authentication. Attackers guess common paths like /admin, /dashboard, /manager.",
        "fix": "Always check role and auth before serving admin pages. Use middleware/decorators.",
        "tools": ["DirBuster", "Gobuster", "ffuf", "dirb"],
        "example": "Navigate to /admin without logging in — full admin access."},
    "admin_2": {"title": "Exposed .env File",
        "explain": ".env files contain secrets (DB passwords, API keys). If web server serves them, all secrets are leaked.",
        "fix": "Configure web server to block dotfiles. Never put .env in web root.",
        "tools": ["curl /.env", "dirsearch", "ffuf"],
        "example": "Visit /.env — you'll see DB_PASS, SECRET_KEY, etc."},
    "ssrf_1": {"title": "SSRF — Server-Side Request Forgery",
        "explain": "SSRF makes the server fetch URLs on your behalf. You can access internal services (127.0.0.1, metadata APIs).",
        "fix": "Whitelist allowed URLs/domains. Block private IP ranges. Validate URL schemes.",
        "tools": ["Burp Collaborator", "curl", "SSRFmap"],
        "example": "URL Checker: enter http://localhost:5000/debug — the server fetches its own debug page."},
    # ─── A02: Security Misconfiguration ───────────────────────────
    "mc_debug": {"title": "Exposed Debug Endpoint",
        "explain": "Debug endpoints leak server internals: secret keys, DB paths, environment variables, user counts.",
        "fix": "Remove or disable debug endpoints in production. Use environment-based toggles.",
        "tools": ["Browser", "curl", "dirsearch"],
        "example": "/debug returns the Flask secret_key and full environment."},
    "mc_robots": {"title": "robots.txt Info Leak",
        "explain": "robots.txt tells search engines what NOT to index — but it also tells attackers what's hidden.",
        "fix": "Don't put sensitive paths in robots.txt. Use authentication instead.",
        "tools": ["Browser", "curl"],
        "example": "/robots.txt reveals /admin, /debug, /api/users, /backup/."},
    "mc_backup": {"title": "Exposed Database Backup",
        "explain": "Backup files left in web root contain full database dumps including password hashes.",
        "fix": "Never store backups in web-accessible directories. Use separate backup storage.",
        "tools": ["dirsearch", "ffuf", "curl"],
        "example": "/backup/db.sql contains the admin password hash."},
    "mc_default": {"title": "Default Credentials",
        "explain": "Applications ship with default admin passwords that are never changed.",
        "fix": "Force password change on first login. Use strong random initial passwords.",
        "tools": ["Hydra", "Burp Intruder", "SecLists default creds"],
        "example": "admin@shopsim.com / admin123 — the default admin password works."},
    "mc_api": {"title": "Exposed User API",
        "explain": "API endpoints that return too much data, including password hashes, to unauthenticated users.",
        "fix": "Restrict API access with authentication. Only return necessary fields.",
        "tools": ["curl", "Postman", "Browser DevTools"],
        "example": "/api/users returns password hashes for all users in easy mode."},
    # ─── A05: Injection ───────────────────────────────────────────
    "sqli_1": {"title": "SQL Injection — Login Bypass (OR 1=1)",
        "explain": "When login queries use string concatenation, injecting ' OR '1'='1'-- makes the WHERE clause always true.",
        "fix": "Use parameterized queries / prepared statements. Never concat user input into SQL.",
        "tools": ["sqlmap", "Burp Repeater", "manual testing"],
        "example": "Email: ' OR '1'='1'-- | Password: anything → logged in as first user (admin)."},
    "sqli_2": {"title": "SQL Injection — Comment Bypass",
        "explain": "Adding -- at the end comments out the rest of the query, bypassing the password check.",
        "fix": "Parameterized queries. Input validation.",
        "tools": ["sqlmap", "manual"],
        "example": "Email: admin@shopsim.com'-- → the password check is commented out."},
    "sqli_5": {"title": "SQL Injection — UNION SELECT",
        "explain": "UNION SELECT appends a second query's results to the first. You can extract data from any table.",
        "fix": "Parameterized queries. WAF rules.",
        "tools": ["sqlmap --technique=U", "manual UNION testing"],
        "example": "Search: ' UNION SELECT 1,username,password,email,role FROM users--"},
    "xss_1": {"title": "Reflected XSS",
        "explain": "User input is reflected back in the page without escaping. Attackers inject <script> tags.",
        "fix": "Escape all output. Use Content-Security-Policy headers. Template auto-escaping.",
        "tools": ["XSStrike", "Burp Scanner", "manual"],
        "example": "Search: <script>alert('XSS')</script> → executes in browser."},
    "xss_2": {"title": "Stored XSS",
        "explain": "XSS payload is stored in the database (e.g. in a review) and executes for every visitor.",
        "fix": "Sanitize input on storage AND escape on output. CSP headers.",
        "tools": ["XSStrike", "BeEF", "manual"],
        "example": "Review: <img src=x onerror=alert('XSS')> → executes for all users viewing the product."},
    "cmdi_1": {"title": "Command Injection",
        "explain": "When user input is passed to os.popen() or system(), attackers chain commands with ; or |.",
        "fix": "Never pass user input to shell commands. Use subprocess with argument lists.",
        "tools": ["Commix", "Burp Repeater", "manual"],
        "example": "Email: test@test.com; id → server executes 'id' command."},
    # ─── A04: Cryptographic Failures ──────────────────────────────
    "cr_1": {"title": "Exposed Password Hashes",
        "explain": "API returns MD5 password hashes. MD5 is fast to crack — rainbow tables exist for billions of hashes.",
        "fix": "Use bcrypt/argon2. Never expose hashes via API.",
        "tools": ["hashcat", "john", "CrackStation", "rainbow tables"],
        "example": "/api/users shows password field with MD5 hashes."},
    "cr_3": {"title": "Cracking MD5 Hashes",
        "explain": "MD5 is a broken algorithm. Use online databases or tools to reverse the hash.",
        "fix": "Migrate to bcrypt (cost factor 12+) or argon2id.",
        "tools": ["crackstation.net", "hashcat -m 0", "john --format=raw-md5"],
        "example": "Paste MD5 hash into crackstation.net → instant result: admin123."},
    # ─── A06: Insecure Design ─────────────────────────────────────
    "id_1": {"title": "Security Question Exploit",
        "explain": "Security questions can be answered by reading public info (reviews, social media).",
        "fix": "Don't use security questions. Use email/SMS verification or TOTP.",
        "tools": ["OSINT", "social engineering", "manual"],
        "example": "John's review says 'Born in New York' — that's his security answer."},
    "id_2": {"title": "Negative Quantity Business Logic",
        "explain": "Setting quantity to -5 reverses the charge, giving you a refund/credit.",
        "fix": "Validate quantity > 0 server-side. Never trust client-side validation alone.",
        "tools": ["Burp Repeater", "DevTools", "curl"],
        "example": "Buy product with quantity=-5 → negative total = refund."},
    # ─── A07: Auth Failures ───────────────────────────────────────
    "au_1": {"title": "Weak Admin Password",
        "explain": "Admin uses 'admin123' — one of the top 10 most common passwords.",
        "fix": "Enforce password complexity requirements. Use password managers.",
        "tools": ["Hydra", "Burp Intruder", "common password lists"],
        "example": "Login: admin@shopsim.com / admin123 → admin access."},
    "au_3": {"title": "No Rate Limiting",
        "explain": "No lockout after failed attempts. Attackers can try millions of passwords.",
        "fix": "Implement rate limiting (5 failed attempts → 15 min lockout). Add CAPTCHA.",
        "tools": ["Hydra", "wfuzz", "Burp Intruder"],
        "example": "Try 100 wrong passwords rapidly — no lockout, no CAPTCHA."},
    # ─── A08: Data Integrity ──────────────────────────────────────
    "di_1": {"title": "Unrestricted File Upload",
        "explain": "No file type validation. Upload .php/.py shells to get remote code execution.",
        "fix": "Whitelist allowed extensions AND content types. Rename files. Store outside web root.",
        "tools": ["Burp Suite", "curl", "weevely"],
        "example": "Upload shell.php → access /uploads/shell.php?cmd=id."},
    # ─── A09: Logging ─────────────────────────────────────────────
    "lg_1": {"title": "Missing Brute-Force Logging",
        "explain": "Application doesn't log or alert on repeated failed login attempts.",
        "fix": "Log all auth events. Alert on: >5 failures from same IP in 60s.",
        "tools": ["docker logs", "Splunk", "ELK Stack"],
        "example": "10 failed logins — no alert, no lockout, possibly not even logged."},
    # ─── A10: Exceptions ──────────────────────────────────────────
    "ex_1": {"title": "Verbose 404 Error",
        "explain": "404 errors return internal paths, server info, and database locations.",
        "fix": "Use generic error pages. Log details server-side only.",
        "tools": ["Browser", "curl"],
        "example": "/nonexistent → returns server name, db_path, internal paths."},
    "ex_2": {"title": "SQL Error Information Leak",
        "explain": "Malformed SQL input causes unhandled exceptions that leak query structure.",
        "fix": "Catch all DB exceptions. Return generic errors. Log details internally.",
        "tools": ["manual", "sqlmap"],
        "example": "Search for single quote ' → error reveals full SQL query."},
}


def show_knowledge(tech_id: str):
    """Display pre-built knowledge for a vulnerability."""
    kb = KNOWLEDGE.get(tech_id)
    if not kb:
        print(f"  {YELLOW}[!] No pre-built knowledge for this challenge.{RESET}")
        return

    print(f"\n  {GREEN}{'═'*56}{RESET}")
    print(f"  {GREEN}{BOLD}📚 KNOWLEDGE BASE: {kb['title']}{RESET}")
    print(f"  {GREEN}{'═'*56}{RESET}")
    print(f"\n  {CYAN}[What is it?]{RESET}")
    print(f"  {kb['explain']}")
    print(f"\n  {CYAN}[How to fix?]{RESET}")
    print(f"  {kb['fix']}")
    print(f"\n  {CYAN}[Example]{RESET}")
    print(f"  {kb['example']}")
    print(f"\n  {CYAN}[Tools]{RESET}")
    print(f"  {', '.join(kb['tools'])}")
    print(f"  {GREEN}{'═'*56}{RESET}")

    # Offer AI follow-up
    more = input(f"\n  {YELLOW}Want more detail from AI Mentor? (y/n): {RESET}").strip().lower()
    if more == "y":
        ask_ai_about(kb["title"], kb["explain"])


def ask_ai_about(title: str, context: str):
    """Ask Ollama AI for more detail about a vulnerability."""
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "llama3.2:1b"

    prompt = f"""You are a cybersecurity expert. The student is learning about this vulnerability:

VULNERABILITY: {title}
CONTEXT: {context}

Give a detailed, practical explanation with:
1. Real-world attack scenario
2. Step-by-step exploitation
3. Proper remediation
4. Why it matters in 2026

Keep it under 300 words."""

    print(f"\n  {DIM}Asking AI Mentor...{RESET}")
    try:
        payload = json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(OLLAMA_URL, data=payload,
                                     headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        answer = data.get("response", "No response from AI.")
        print(f"\n  {MAGENTA}[🤖 AI MENTOR]{RESET}")
        for line in answer.split("\n"):
            print(f"  {line}")
    except Exception as e:
        print(f"  {RED}[!] AI unavailable: {e}{RESET}")
        print(f"  {DIM}Make sure Ollama is running: ollama serve{RESET}")
