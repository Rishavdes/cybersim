"""A04:2025 — Cryptographic Failures — VulnSite Challenges"""
SECTION = {
    "id": "a04", "name": "A04:2025 — Cryptographic Failures",
    "theory": "Cryptographic Failures: passwords in weak hashes (MD5), exposed credentials,\ndata over HTTP, no encryption at rest.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Exposed Credentials", "min_difficulty": "easy", "techniques": [
            {"id": "cr_1", "description": "Find exposed password hashes via the API.", "target_page": "/",
             "payload": "/api/users", "hint": "Check if the user API exposes more data than it should.",
             "steps_easy": ["Navigate to /api/users", "In Easy mode, password hashes (MD5) are visible!", "Copy the admin hash"]},
            {"id": "cr_2", "description": "Find the admin password hash in the database backup.", "target_page": "/",
             "payload": "/backup/db.sql", "hint": "Check for backup files.", "steps_easy": ["Navigate to /backup/db.sql", "The admin MD5 hash is right there"]},
        ]},
        {"name": "Crack MD5 Hashes", "min_difficulty": "normal", "techniques": [
            {"id": "cr_3", "description": "Crack the admin's MD5 password hash.", "target_page": "/",
             "payload": "admin123", "hint": "Use crackstation.net, hashcat, or john to crack the MD5 hash.",
             "steps_easy": ["Copy the admin hash from /api/users", "Go to https://crackstation.net", "Paste the hash — result: admin123",
                 "Or run: echo '<hash>' > hash.txt && john --format=raw-md5 hash.txt"]},
        ]},
    ],
    "external_labs": {"free": [("CryptoHack", "https://cryptohack.org"), ("TryHackMe — Crack the Hash", "https://tryhackme.com/room/crackthehash")], "paid": []},
}
