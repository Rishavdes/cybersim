"""A03:2025 — Supply Chain Failures — VulnSite Challenges"""
SECTION = {
    "id": "a03", "name": "A03:2025 — Supply Chain Failures (NEW)",
    "theory": "NEW for 2025! Covers vulnerable dependencies, outdated libraries, typosquatting.\n\n🎯 TARGET: ShopSim VulnSite at http://localhost:8080",
    "stages": [
        {"name": "Detect Outdated Libraries", "min_difficulty": "easy", "techniques": [
            {"id": "sc_1", "description": "Inspect the VulnSite's dependencies for known vulnerabilities.", "target_page": "/debug",
             "payload": "Check /debug for version info, then search CVEs",
             "hint": "The debug endpoint may reveal framework and library versions.",
             "steps_easy": ["Go to /debug to see the Flask version", "Search for known CVEs for that version", "Report: which CVE?"]},
        ]},
        {"name": "Identify Supply Chain Risk", "min_difficulty": "normal", "techniques": [
            {"id": "sc_2", "description": "Find the requirements.txt or package info to audit dependencies.", "target_page": "/",
             "payload": "pip list --outdated or pip-audit",
             "hint": "If you have access to the container, audit its packages.",
             "steps_easy": ["Run: docker exec cybersim_vulnsite pip list", "Run: docker exec cybersim_vulnsite pip list --outdated", "Identify vulnerable packages"]},
        ]},
    ],
    "external_labs": {"free": [("Snyk Learn", "https://learn.snyk.io"), ("OWASP Dependency-Check", "https://owasp.org/www-project-dependency-check/")], "paid": []},
}
