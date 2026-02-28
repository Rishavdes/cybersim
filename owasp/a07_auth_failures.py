"""A07:2025 — Authentication Failures — VulnSite Challenges"""
SECTION = {
    "id": "a07", "name": "A07:2025 — Authentication Failures",
    "theory": "Authentication Failures: weak passwords, no rate limiting, credential stuffing,\nweak session management.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Weak Credentials", "min_difficulty": "easy", "techniques": [
            {"id": "au_1", "description": "Login with the admin's weak password.", "target_page": "/login",
             "payload": "admin@shopsim.com / admin123", "hint": "Try the most common passwords.",
             "steps_easy": ["Go to /login", "Email: admin@shopsim.com", "Password: admin123"]},
            {"id": "au_2", "description": "Register with an extremely weak password (no policy).", "target_page": "/register",
             "payload": "password: 1", "hint": "Does the app enforce any password complexity?",
             "steps_easy": ["Go to /register", "Use password: 1", "It accepts it — no password policy!"]},
        ]},
        {"name": "No Rate Limiting", "min_difficulty": "normal", "techniques": [
            {"id": "au_3", "description": "Brute-force the login — no lockout exists.", "target_page": "/login",
             "payload": "hydra -l admin@shopsim.com -P rockyou.txt localhost http-post-form '/login:email=^USER^&password=^PASS^:Invalid'",
             "hint": "Try 20 wrong passwords rapidly. Do you get locked out?",
             "steps_easy": ["Try 20 wrong passwords on /login", "No lockout, no CAPTCHA, no delay",
                 "Use Hydra for automated brute-force"]},
        ]},
    ],
    "external_labs": {"free": [("PortSwigger — Authentication", "https://portswigger.net/web-security/authentication")], "paid": []},
}
