"""A02:2025 — Security Misconfiguration — VulnSite Challenges"""
SECTION = {
    "id": "a02", "name": "A02:2025 — Security Misconfiguration",
    "theory": "Security Misconfiguration is #2 in 2025. Includes exposed debug info, default creds,\ndirectory listing, verbose errors, missing security headers.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Debug & Info Disclosure", "min_difficulty": "easy", "techniques": [
            {"id": "mc_debug", "description": "Find the debug endpoint leaking server internals.", "target_page": "/", "payload": "/debug",
             "hint": "Developers sometimes leave /debug endpoints exposed.", "steps_easy": ["Navigate to /debug", "You'll see secret_key, db_path, user counts, and environment variables"]},
            {"id": "mc_robots", "description": "Read robots.txt to discover hidden paths.", "target_page": "/", "payload": "/robots.txt",
             "hint": "robots.txt tells search engines what NOT to index — which reveals secrets.", "steps_easy": ["Navigate to /robots.txt", "It reveals /admin, /debug, /api/users, /backup/"]},
            {"id": "mc_backup", "description": "Find the exposed database backup file.", "target_page": "/", "payload": "/backup/db.sql",
             "hint": "Try common backup file paths.", "steps_easy": ["Navigate to /backup/db.sql", "It contains the admin password hash!"]},
        ]},
        {"name": "Default Credentials", "min_difficulty": "normal", "techniques": [
            {"id": "mc_default", "description": "Login using default admin credentials.", "target_page": "/login", "payload": "admin@shopsim.com / admin123",
             "hint": "Try the most common admin email and password combinations.", "steps_easy": ["Go to /login", "Email: admin@shopsim.com", "Password: admin123"]},
        ]},
        {"name": "Exposed API Data", "min_difficulty": "normal", "techniques": [
            {"id": "mc_api", "description": "Access the user API that leaks password hashes.", "target_page": "/", "payload": "/api/users",
             "hint": "REST APIs sometimes expose too much data.", "steps_easy": ["Navigate to /api/users", "In easy mode, you see password hashes for ALL users"]},
        ]},
    ],
    "external_labs": {"free": [("PortSwigger — Info Disclosure", "https://portswigger.net/web-security/information-disclosure")], "paid": []},
}
