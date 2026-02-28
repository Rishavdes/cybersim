"""A01:2025 — Broken Access Control + SSRF — VulnSite Challenges"""

SECTION = {
    "id": "a01",
    "name": "A01:2025 — Broken Access Control + SSRF",
    "theory": (
        "Broken Access Control means users can act outside their intended permissions.\n"
        "This includes IDOR (changing ?id=1 to ?id=2), forced browsing (/admin),\n"
        "privilege escalation, and SSRF (making the server request internal resources).\n\n"
        "🎯 TARGET: ShopSim VulnSite at http://localhost:8080"
    ),
    "stages": [
        {
            "name": "IDOR — View Other Users' Profiles",
            "min_difficulty": "easy",
            "techniques": [
                {"id": "idor_1", "description": "Access another user's profile by changing the ID in the URL.",
                 "target_page": "/profile/1", "payload": "/profile/2",
                 "hint": "Change the number in /profile/1 to /profile/2 or /profile/3.",
                 "steps_easy": ["Login to ShopSim", "Go to your profile page", "Look at the URL: /profile/1",
                     "Change it to /profile/2 — you can see another user's data!"]},
                {"id": "idor_2", "description": "Access another user's order via the API.",
                 "target_page": "/", "payload": "/api/order/1",
                 "hint": "Try accessing /api/order/1 or /api/order/2 directly.",
                 "steps_easy": ["Open a new tab", "Go to http://localhost:8080/api/order/1",
                     "You can see order details that don't belong to you"]},
            ],
        },
        {
            "name": "Forced Browsing — Admin Panel",
            "min_difficulty": "easy",
            "techniques": [
                {"id": "admin_1", "description": "Find the hidden admin panel that anyone can access.",
                 "target_page": "/", "payload": "/admin",
                 "hint": "Try common admin paths like /admin.",
                 "steps_easy": ["Navigate to http://localhost:8080/admin",
                     "You see the admin panel with ALL user data — without being logged in!"]},
                {"id": "admin_2", "description": "Find the exposed .env file with database credentials.",
                 "target_page": "/", "payload": "/.env",
                 "hint": "Dotfiles like .env often contain secrets.",
                 "steps_easy": ["Navigate to http://localhost:8080/.env",
                     "You'll see DB_PASS, SECRET_KEY, and ADMIN_EMAIL"]},
            ],
        },
        {
            "name": "SSRF — Server-Side Request Forgery",
            "min_difficulty": "hard",
            "techniques": [
                {"id": "ssrf_1", "description": "Use the URL Checker to make the server request its own debug page.",
                 "target_page": "/fetch", "payload": "http://localhost:5000/debug",
                 "hint": "Enter a URL pointing to the server's own internal endpoints.",
                 "steps_easy": ["Go to the URL Checker page (/fetch)",
                     "Enter: http://localhost:5000/debug",
                     "The server fetches its OWN debug endpoint, leaking secrets"]},
            ],
        },
    ],
    "external_labs": {
        "free": [("PortSwigger — Access Control", "https://portswigger.net/web-security/access-control")],
        "paid": [("HTB Academy — Broken Access Control", "https://academy.hackthebox.com")],
    },
}
