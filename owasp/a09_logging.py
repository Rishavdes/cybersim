"""A09:2025 — Logging & Alerting Failures — VulnSite Challenges"""
SECTION = {
    "id": "a09", "name": "A09:2025 — Logging & Alerting Failures",
    "theory": "Logging failures: no alerts on brute-force, missing audit logs,\nunmonitored sensitive actions.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Missing Brute-Force Detection", "min_difficulty": "easy", "techniques": [
            {"id": "lg_1", "description": "Perform 10 failed logins and check if you get locked out.", "target_page": "/login",
             "payload": "No lockout after 10 failed attempts", "hint": "Try many wrong passwords. Any lockout?",
             "steps_easy": ["Go to /login", "Enter wrong passwords 10 times rapidly", "No lockout, no CAPTCHA, no alert = logging failure"]},
        ]},
        {"name": "Check Logs API", "min_difficulty": "normal", "techniques": [
            {"id": "lg_2", "description": "Access the logs API to see what events are (or aren't) recorded.", "target_page": "/",
             "payload": "/api/logs", "hint": "Check if there's a logging endpoint.",
             "steps_easy": ["Navigate to /api/logs", "Check what events are logged", "Notice: failed logins may not be recorded"]},
        ]},
    ],
    "external_labs": {"free": [("TryHackMe — SIEM", "https://tryhackme.com/room/introtosiem")], "paid": []},
}
