"""
CyberSim Monthly Quiz Generator
Generates quiz questions from completed mission topics.
"""
import random
from core.mission_data import get_mission, MISSIONS

# ─── Question Bank by Topic Category ─────────────────────────────────────────
# Each category has multiple Q&A pairs. The quiz picks from categories
# that match the user's completed missions.

QUIZ_BANK = {
    "networking": [
        {"q": "What is the default port for SSH?", "options": ["21", "22", "23", "25"], "answer": "22"},
        {"q": "Which Nmap flag performs a SYN stealth scan?", "options": ["-sT", "-sS", "-sU", "-sV"], "answer": "-sS"},
        {"q": "What protocol resolves domain names to IP addresses?", "options": ["DHCP", "ARP", "DNS", "FTP"], "answer": "DNS"},
        {"q": "Which OSI layer handles routing?", "options": ["Layer 1", "Layer 2", "Layer 3", "Layer 4"], "answer": "Layer 3"},
        {"q": "What does the TCP 3-way handshake consist of?", "options": ["SYN, ACK, FIN", "SYN, SYN-ACK, ACK", "SYN, RST, ACK", "FIN, ACK, RST"], "answer": "SYN, SYN-ACK, ACK"},
        {"q": "Which port does HTTP use by default?", "options": ["443", "8080", "80", "8000"], "answer": "80"},
        {"q": "What Nmap flag detects service versions?", "options": ["-sV", "-sS", "-O", "-A"], "answer": "-sV"},
        {"q": "What is the loopback IP address?", "options": ["0.0.0.0", "127.0.0.1", "192.168.1.1", "10.0.0.1"], "answer": "127.0.0.1"},
    ],
    "linux": [
        {"q": "Which command finds files with SUID permissions?", "options": ["ls -la", "find / -perm -4000", "chmod +s file", "grep -r suid"], "answer": "find / -perm -4000"},
        {"q": "What file stores Linux user password hashes?", "options": ["/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/group"], "answer": "/etc/shadow"},
        {"q": "Which command changes file ownership?", "options": ["chmod", "chown", "chgrp", "usermod"], "answer": "chown"},
        {"q": "What does 'chmod 755' mean?", "options": ["rwx for owner, rx for group/others", "rw for all", "rwx for all", "r only for owner"], "answer": "rwx for owner, rx for group/others"},
        {"q": "Which command shows listening ports on Linux?", "options": ["netstat -tlnp", "ifconfig", "route", "arp -a"], "answer": "netstat -tlnp"},
        {"q": "What is the root user's UID?", "options": ["1", "0", "100", "1000"], "answer": "0"},
    ],
    "python": [
        {"q": "Which Python library is used for HTTP requests?", "options": ["socket", "requests", "os", "sys"], "answer": "requests"},
        {"q": "What Python library creates raw network sockets?", "options": ["http", "urllib", "socket", "flask"], "answer": "socket"},
        {"q": "How do you spawn an interactive shell in Python?", "options": ["os.system('bash')", "import pty; pty.spawn('/bin/bash')", "subprocess.run('sh')", "exec('shell')"], "answer": "import pty; pty.spawn('/bin/bash')"},
        {"q": "What does 'pip freeze' do?", "options": ["Freezes Python", "Lists installed packages", "Installs packages", "Updates pip"], "answer": "Lists installed packages"},
    ],
    "web_security": [
        {"q": "What does OWASP stand for?", "options": ["Open Web App Security Project", "Online Web Attack Surface Platform", "Open Wireless Access Security Protocol", "Original Web App Scanning Program"], "answer": "Open Web App Security Project"},
        {"q": "Which attack injects SQL commands via user input?", "options": ["XSS", "CSRF", "SQL Injection", "SSRF"], "answer": "SQL Injection"},
        {"q": "What tool intercepts HTTP requests for web testing?", "options": ["Nmap", "Burp Suite", "Wireshark", "John"], "answer": "Burp Suite"},
        {"q": "What is the most basic XSS payload?", "options": ["' OR 1=1--", "<script>alert(1)</script>", "../../etc/passwd", "{{7*7}}"], "answer": "<script>alert(1)</script>"},
        {"q": "What HTTP status code means 'Forbidden'?", "options": ["401", "403", "404", "500"], "answer": "403"},
    ],
    "cryptography": [
        {"q": "Which hash is 32 hex characters long?", "options": ["SHA-256", "MD5", "SHA-1", "bcrypt"], "answer": "MD5"},
        {"q": "What tool cracks password hashes offline?", "options": ["Nmap", "Burp Suite", "John the Ripper", "Metasploit"], "answer": "John the Ripper"},
        {"q": "What type of encryption uses a shared key?", "options": ["Asymmetric", "Symmetric", "Hashing", "Encoding"], "answer": "Symmetric"},
    ],
    "privilege_escalation": [
        {"q": "What does SUID stand for?", "options": ["Set User ID", "Super User ID", "System User Identity", "Secure UID"], "answer": "Set User ID"},
        {"q": "Which tool automates Linux privilege escalation checks?", "options": ["Nmap", "LinPEAS", "Burp Suite", "Gobuster"], "answer": "LinPEAS"},
        {"q": "What file controls sudo permissions?", "options": ["/etc/passwd", "/etc/sudoers", "/etc/shadow", "/etc/group"], "answer": "/etc/sudoers"},
    ],
    "active_directory": [
        {"q": "What attack extracts service account hashes from AD?", "options": ["Pass-the-Hash", "Kerberoasting", "Golden Ticket", "Silver Ticket"], "answer": "Kerberoasting"},
        {"q": "Which tool maps AD trust relationships?", "options": ["Nmap", "BloodHound", "Burp Suite", "Wireshark"], "answer": "BloodHound"},
        {"q": "What protocol does AD use for authentication?", "options": ["NTLM", "OAuth", "Kerberos", "SAML"], "answer": "Kerberos"},
    ],
    "malware": [
        {"q": "What is the purpose of a C2 server?", "options": ["Compile code", "Command and Control", "Certificate Authority", "Cloud Computing"], "answer": "Command and Control"},
        {"q": "What technique hides malware inside a legitimate process?", "options": ["DLL Injection", "Port Scanning", "SQL Injection", "Phishing"], "answer": "DLL Injection"},
        {"q": "What does AMSI stand for?", "options": ["Anti-Malware Scan Interface", "Advanced Malware Security Integration", "Automated Monitoring System Interface", "Anti-Malware Software Inspector"], "answer": "Anti-Malware Scan Interface"},
    ],
    "blue_team": [
        {"q": "What does SOC stand for?", "options": ["Security Operations Center", "System Online Control", "Server Operations Command", "Secure Output Channel"], "answer": "Security Operations Center"},
        {"q": "Which tool is the industry standard for log analysis?", "options": ["Nmap", "Splunk", "Burp Suite", "Metasploit"], "answer": "Splunk"},
        {"q": "What does DFIR stand for?", "options": ["Digital Forensics and Incident Response", "Data Flow Integration Report", "Distributed Firewall Intelligence Rule", "Defense Framework for IR"], "answer": "Digital Forensics and Incident Response"},
    ],
}

# Map mission ID ranges to quiz categories
MISSION_TO_CATEGORY = {
    (101, 199): "networking",
    (201, 299): "linux",
    (301, 399): "python",
    (401, 499): "cryptography",
    (501, 599): "privilege_escalation",
    (601, 699): "cryptography",
    (701, 899): "web_security",
    (901, 999): "networking",
    (1001, 1099): "active_directory",
    (1101, 1299): "privilege_escalation",
    (1301, 1399): "web_security",
    (1401, 1599): "blue_team",
    (1601, 1699): "blue_team",
    (1701, 1899): "malware",
    (1901, 2099): "malware",
    (2101, 2399): "web_security",
}


def get_categories_for_completed(state: dict) -> list:
    """Get quiz categories based on completed missions."""
    completions = state.get("mission_completions", {})
    categories = set()
    for mid_str in completions.keys():
        mid = int(mid_str)
        for (lo, hi), cat in MISSION_TO_CATEGORY.items():
            if lo <= mid <= hi:
                categories.add(cat)
                break
    return list(categories) if categories else ["networking"]  # Fallback


def generate_quiz(state: dict, num_questions: int = 10) -> list:
    """Generate a quiz from completed topic categories."""
    categories = get_categories_for_completed(state)
    
    # Collect all available questions from matching categories
    pool = []
    for cat in categories:
        pool.extend(QUIZ_BANK.get(cat, []))
    
    # If not enough from completed topics, pad with networking basics
    if len(pool) < num_questions:
        for cat in QUIZ_BANK:
            if cat not in categories:
                pool.extend(QUIZ_BANK[cat])
    
    # Shuffle and pick
    random.shuffle(pool)
    return pool[:num_questions]
