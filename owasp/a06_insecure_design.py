"""A06:2025 — Insecure Design — VulnSite Challenges"""
SECTION = {
    "id": "a06", "name": "A06:2025 — Insecure Design",
    "theory": "Insecure Design: flaws in application logic, weak password reset,\nbusiness logic bypasses, race conditions.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Password Reset Exploit", "min_difficulty": "easy", "techniques": [
            {"id": "id_1", "description": "Reset another user's password using their security question.", "target_page": "/forgot-password",
             "payload": "fluffy", "hint": "Users leak personal info in product reviews. Check reviews for clues.",
             "steps_easy": ["Go to /forgot-password", "Enter john@shopsim.com", "Security Q: 'What city were you born in?'",
                 "Check John's review on product 1 — he mentions 'Born in New York'", "Answer: new york"]},
        ]},
        {"name": "Business Logic Bypass", "min_difficulty": "normal", "techniques": [
            {"id": "id_2", "description": "Buy a product with a negative quantity to get a refund.", "target_page": "/product/1",
             "payload": "quantity=-5", "hint": "What happens if the quantity is negative?",
             "steps_easy": ["Login, go to /product/1", "Change the quantity input to -5", "Submit — the total becomes negative (refund!)"]},
            {"id": "id_3", "description": "Apply a coupon code that gives 50% off.", "target_page": "/product/1",
             "payload": "DISCOUNT50", "hint": "Try common coupon codes.", "steps_easy": ["Go to any product", "Enter coupon: DISCOUNT50", "50% discount applied!"]},
        ]},
    ],
    "external_labs": {"free": [("PortSwigger — Logic Flaws", "https://portswigger.net/web-security/logic-flaws")], "paid": []},
}
