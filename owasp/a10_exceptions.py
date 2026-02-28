"""A10:2025 — Mishandling Exceptions — VulnSite Challenges"""
SECTION = {
    "id": "a10", "name": "A10:2025 — Mishandling Exceptions (NEW)",
    "theory": "NEW for 2025! Verbose errors, unhandled exceptions, fail-open behavior,\nstack traces leaking internals.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Verbose Error Messages", "min_difficulty": "easy", "techniques": [
            {"id": "ex_1", "description": "Trigger a 404 error that leaks internal file paths.", "target_page": "/",
             "payload": "/nonexistent_page", "hint": "Visit a URL that doesn't exist and read the error carefully.",
             "steps_easy": ["Navigate to /nonexistent_page", "The error reveals: server name, db_path, internal paths"]},
            {"id": "ex_2", "description": "Trigger a database error with malformed input.", "target_page": "/search",
             "payload": "' (single quote)", "hint": "Send a single quote to trigger an SQL error with full trace.",
             "steps_easy": ["Go to /search", "Search for just a single quote: '", "The error reveals the full SQL query structure"]},
        ]},
        {"name": "Fail-Open Behavior", "min_difficulty": "hard", "techniques": [
            {"id": "ex_3", "description": "Send unexpected content to API endpoints to see fail behavior.", "target_page": "/",
             "payload": "curl -X POST http://localhost:8080/login -d 'email=&password='",
             "hint": "What happens when required fields are empty?",
             "steps_easy": ["Run: curl -X POST http://localhost:8080/login -d 'email=&password='",
                 "Check if empty fields cause an unhandled exception"]},
        ]},
    ],
    "external_labs": {"free": [("PortSwigger — Info Disclosure", "https://portswigger.net/web-security/information-disclosure")], "paid": []},
}
