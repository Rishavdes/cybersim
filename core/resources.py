"""
CyberSim Resource System
Maps missions to external learning resources (Telegram, Google Drive, Oracle Cloud).
Resources are shown AFTER completing a mission as a reward.
URLs use placeholder tokens that the user fills in via db/resources.json.
"""
import os
import json

# ─── ANSI Colors ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "resources.json")

# ─── Platform Icons ───────────────────────────────────────────────────────────
PLATFORM_ICONS = {
    "telegram": "📱",
    "gdrive": "📁",
    "oracle_cloud": "☁️",
    "web": "🌐",
    "youtube": "▶️",
    "lab": "🧪",
    "elhacker": "💀",
}

# ─── Default Resource Map ─────────────────────────────────────────────────────
# Each mission ID maps to a list of resources.
# URLs marked "PLACEHOLDER" should be replaced by the user in db/resources.json

DEFAULT_RESOURCES = {
    # ── Stage 1: Networking (Month 1) ──
    "101": [
        {"type": "course", "title": "Aprende Redes desde Cero", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "CompTIA Network+", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Cisco CCNA 200-301", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "lab", "title": "TryHackMe - Nmap", "platform": "web", "url": "https://tryhackme.com/room/furthernmap"},
        {"type": "course", "title": "Cisco CCNA 200-301 Complete", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Cisco%20CCNA%20200-301%20en%20espa%C3%B1ol/"},
        {"type": "course", "title": "2in1 CCNA 200-301 + Python Network", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/2%20in%201!%20Cisco%20CCNA%20200-301%20+%20Python%20Network%20Automation/"},
        {"type": "course", "title": "Networking Fundamentals for Cybersecurity", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Networking%20Fundamentals%20for%20Cybersecurity/"},
    ],
    "102": [
        {"type": "course", "title": "CompTIA Network+", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Cisco CCNA 200-301", "platform": "telegram", "url": "PLACEHOLDER"},
    ],

    # ── Stage 1: Linux (Month 2) ──
    "201": [
        {"type": "course", "title": "Curso Básico de Linux", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Linux Mastery", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Administracion de servidores Linux", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "lab", "title": "TryHackMe - Linux Fundamentals", "platform": "web", "url": "https://tryhackme.com/room/linuxfundamentalspart1"},
        {"type": "lab", "title": "OverTheWire - Bandit", "platform": "web", "url": "https://overthewire.org/wargames/bandit/"},
        {"type": "course", "title": "Linux Mastery - Command Line 11.5h", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Linux%20Mastery%20Master%20the%20Linux%20Command%20Line%20in%2011.5%20Hours/"},
        {"type": "course", "title": "Linux de Noob a Pro en 9 horas", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Linux%20de%20Noob%20a%20Pro%20en%209%20horas/"},
        {"type": "course", "title": "Curso de Linux s4vitar", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Curso%20de%20Linux%20s4vitar/"},
        {"type": "course", "title": "Linux Security & Server Hardening", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Linux%20Security%20%26%20Server%20Hardening/"},
    ],

    # ── Stage 1: Python (Month 3) ──
    "301": [
        {"type": "course", "title": "Aprende Python desde 0 a Experto", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Master Python Programming Essentials", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Python for Pentesters", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Learn Python Ethical Hacking From Scratch", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "HACKING Con Python3 - Audita, Defiende, Crea", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/10.%20%E2%9C%94HACKING%20Con%20%5B%20Python3%20%5D.%20Audita%2C%20Defiende%2C%20Crea!.%20A%C3%B1o%202019/"},
        {"type": "course", "title": "Python for Red-Blue Teams", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Python%20for%20Red-Blue%20Teams%20from%20Scratch/"},
        {"type": "course", "title": "Python for Cyber Defense", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Python%20for%20Cyber%20Defense/"},
        {"type": "course", "title": "Pentester Academy Python For Pentesters", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Pentester%20Academy%20-%20Python%20For%20Pentesters/"},
    ],

    # ── Stage 1: Security Basics ──
    "401": [
        {"type": "course", "title": "Fundamentos de la ciberseguridad", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Cyber Security Fundamentals", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Curso de Introducción a la Seguridad Informática", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "CompTIA Security+ (SY0-701) Full Training", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/CompTIA%20Security+%20(SY0-701%20%26%20SY0-601)%20Full%20Training%20Guide/"},
        {"type": "course", "title": "Cyber Security Fundamentals", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Cyber%20Security%20Fundamentals/"},
    ],

    # ── Stage 2: CEH (Month 4-6) ──
    "501": [
        {"type": "course", "title": "CEH v11 / v12 / v13", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Certified Ethical Hacker Practical Labs", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "CEHv13 Latest", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/CEHv13/"},
        {"type": "course", "title": "CEH v12 Videos + PDF + Lab Manuals", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Certified%20Ethical%20Hacker%20(CEH)%20v12%20-%20Videos%20+%20PDF%20Lessons%20+%20Lab%20Manuals/"},
        {"type": "course", "title": "CEH v11 Complete Course", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Certified%20Ethical%20Hacker%20(CEH)%20v11/"},
        {"type": "course", "title": "Ethical Hacking in 43 Hours CSEH+CEH 2024", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Ethical%20Hacking%20in%2043%20Hours%20Certificated%20CSEH+CEH%202024/"},
    ],

    # ── Stage 2: Scanning & Enumeration ──
    "601": [
        {"type": "course", "title": "NMAP Para Pentester", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Nessus Scanner Course", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Wireshark Course", "platform": "telegram", "url": "PLACEHOLDER"},
    ],

    # ── Stage 2: Web Hacking ──
    "701": [
        {"type": "course", "title": "Mastering SQL Injection", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Burp Suite Bug Bounty", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "OWASP ZAP Course", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Hacking Web Applications", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Mastering SQL Injection Hands-On", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Mastering%20SQL%20Injection%20-%20The%20Ultimate%20Hands-On%20Course/"},
        {"type": "course", "title": "Burp Suite Complete Crash Course", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Burp%20Suite%20Complete%20Crash%20Course/"},
        {"type": "course", "title": "Advanced Web Hacking (NotSoSecure)", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/NotSoSecure%20-%20Advanced%20Web%20Hacking%202022/"},
        {"type": "course", "title": "TCM Advanced Web Hacking 2025", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/TCM%20-%20Advanced%20Web%20Hacking%202025.5%20tg/"},
        {"type": "course", "title": "OWASP ZAP Website Hacking Course", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/OWASP%20ZAP%20%20Website%20Hacking%20%26%20Penetration%20Testing%20Course/"},
    ],

    # ── Stage 2: Wireless ──
    "901": [
        {"type": "course", "title": "Complete WiFi Hacking Course", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Complete WiFi Hacking Beginner-Advanced", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Complete%20WiFi%20Hacking%20Course%20Beginner%20to%20Advanced/"},
        {"type": "course", "title": "WiFi Hacking WPA3/WPA2/WPA/WEP 2025", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Learn%20Wi-Fi%20Hacking%20from%20scratch%20(WPA3WPA2WPAWEP)/"},
        {"type": "course", "title": "Master in WiFi Ethical Hacking", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Master%20in%20Wi-Fi%20ethical%20Hacking/"},
    ],

    # ── Stage 3: Active Directory ──
    "1001": [
        {"type": "course", "title": "Active Directory Exploitation and Lateral Movement", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Active Directory Pentesting With Kali Linux", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Learn Active Directory Pentesting", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "AD Exploitation & Lateral Movement Black-Box", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Active%20Directory%20Exploitation%20and%20Lateral%20Movement%20Black-Box/"},
        {"type": "course", "title": "AD Pentesting With Kali Linux RedTeam", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Active%20Directory%20Pentesting%20With%20Kali%20Linux-RedTeam/"},
        {"type": "course", "title": "AD Protection & Tiering", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Active%20Directory%20Protection%20%26%20Tiering/"},
        {"type": "course", "title": "QURE Advanced Attacks Against AD", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/QURE%20Academy%20-%20Advanced%20Attacks%20Against%20Active%20Directory/"},
    ],

    # ── Stage 3: Privilege Escalation ──
    "1101": [
        {"type": "course", "title": "Pentester Academy - Windows PrivEsc", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Linux Rootkits for Red-Blue Teams", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Complete Pentesting & PrivEsc Course", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/The%20Complete%20Pentesting%20%26%20Privilege%20Escalation%20Course/"},
        {"type": "course", "title": "Linux Rootkits for Red-Blue Teams", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Pentester%20Academy%20-%20Linux%20Rootkits%20for%20Red-Blue%20Teams/"},
    ],

    # ── Stage 3: Buffer Overflow ──
    "1201": [
        {"type": "course", "title": "Pentester Academy - Exploiting Buffer Overflows", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Exploit Development Tutorial", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Assembly 101", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "64-Bit Assembly & Shellcoding", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "64-Bit Assembly & Shellcoding for Ethical Hackers", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/64-Bit%20Assembly%20%26%20Shellcoding%20for%20Ethical%20Hackers/"},
        {"type": "course", "title": "Exploit Development & Buffer Overflows", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Pentester%20Academy%20-%20Exploiting%20Simple%20Buffer%20Overflows%20on%20Win32/"},
        {"type": "course", "title": "Assembly Language for Reverse Engineering", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Assembly%20Language%20Programming%20for%20Reverse%20Engineering/"},
        {"type": "course", "title": "Certified Exploit Development Professional", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Certified%20Exploit%20Development%20Professional%20%5BCEDP%5D/"},
    ],

    # ── Stage 3: Practice Labs ──
    "1301": [
        {"type": "course", "title": "PNPT Live Learn to Hack", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "How to Hack The Box To Your OSCP", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Hack The Box Pro Labs", "platform": "telegram", "url": "PLACEHOLDER"},
    ],

    # ── Stage 3: Blue Team SOC ──
    "1401": [
        {"type": "course", "title": "Infosec4TC - SOC Analyst Blue Team BootCamp", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Security Operations And Threat Hunting", "platform": "telegram", "url": "PLACEHOLDER"},
    ],

    # ── Stage 3: Splunk ──
    "1501": [
        {"type": "course", "title": "The Complete Splunk Course from Zero to Hero", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "CompTIA CySA Cybersecurity Analyst", "platform": "telegram", "url": "PLACEHOLDER"},
    ],

    # ── Stage 3: DFIR ──
    "1601": [
        {"type": "course", "title": "INE - Digital Forensics Professional (eCDFP)", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Incident Handling and Response Professional", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Network Security Monitoring with Zeek", "platform": "telegram", "url": "PLACEHOLDER"},
    ],

    # ── Stage 4: Malware Development ──
    "1701": [
        {"type": "course", "title": "Malware Development Course 2022", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Practical Linux Malware Development", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Malware Development 2 Advanced Injection", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "M4ld3v Malware Development", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Practical Linux Malware Development", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Practical%20Linux%20Malware%20Development/"},
        {"type": "course", "title": "Red Team Operator Malware Dev Essentials", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Red%20Team%20Operator%20Malware%20Development%20Essentials/"},
        {"type": "course", "title": "Malware Analysis Noob2Ninja", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Malware%20analysis%20-%20Noob2ninja/"},
        {"type": "course", "title": "Mandiant Malware Analysis 2025", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Mandiant%20-%20Malware%20Analysis%202025/"},
        {"type": "course", "title": "ABCs of Malware Analysis", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/(Absolute%20Basic%20Concepts)%20ABCs%20of%20Malware%20Analysis/"},
    ],

    # ── Stage 4: Process Injection ──
    "1801": [
        {"type": "course", "title": "Windows Process Injection For Red-Blue Team", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Process Injection Analyst", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Windows Process Injection Red-Blue Team", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/A-Windows_Process_Injection_For_Red-Blue_Team/"},
        {"type": "course", "title": "Process Injection Analyst [CPIA]", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Process%20Injection%20Analyst%20%5BCPIA%5D/"},
    ],

    # ── Stage 4: Evasion ──
    "1901": [
        {"type": "course", "title": "Red Team Operator Malware Development", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "PowerShell for Cyber Offense", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Linux Rootkits for Red-Blue Teams", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Sektor7 Malware Dev Intermediate", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Sektor7%20Malware%20Development%20Intermediate/"},
        {"type": "course", "title": "Certified Windows Internals RTO", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Certified%20Windows%20Internals%20Red%20Team%20Operator%20%5BCWI-RTO%5D/"},
        {"type": "course", "title": "Stealth Cyber Operator [CSCO]", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Stealth%20Cyber%20Operator%20%5BCSCO%5D/"},
    ],

    # ── Stage 4: C2 & Red Team ──
    "2001": [
        {"type": "course", "title": "Pentesting with Cobalt Strike", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Offensive Cyber Operations", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Certified Red Team Analyst (CRTA)", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Active Directory RedTeam Lab Setup", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "AD Lateral Movement Black-Box", "platform": "telegram", "url": "PLACEHOLDER"},
        {"type": "course", "title": "Red Team Ops with Cobalt Strike", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Red%20Team%20Ops%20with%20Cobalt%20Strike/"},
        {"type": "course", "title": "Red Team Ops I & II", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Red%20Team%20Ops%20I/"},
        {"type": "course", "title": "Certified Red Team Analyst CRTA", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Certified%20Red%20Team%20Analyst%20-%20CRTA/"},
        {"type": "course", "title": "SEC670 Red Teaming Tools - C2 Development", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/SEC670%20Red%20Teaming%20Tools%20-%20Developing%20Windows%20Implants%2C%20Shellcode%2C%20Command%20and%20Control/"},
        {"type": "course", "title": "BruteRatel C4 Adversary Simulation", "platform": "elhacker", "url": "https://ns2.elhacker.info/descargas/Red%20Team%20and%20Adversary%20Simulation%20with%20BruteRatel%20C4/"},
    ],

    # ── Stage 4: Cert Prep ──
    "2101": [
        {"type": "lab", "title": "HackTheBox - 10 Hard Machines Exam Simulation", "platform": "web", "url": "https://app.hackthebox.com"},
        {"type": "lab", "title": "TryHackMe - Offensive Pentesting Path", "platform": "web", "url": "https://tryhackme.com/path/outline/pentesting"},
    ],

    # ── Stage 4: Bug Bounty ──
    "2201": [
        {"type": "lab", "title": "HackerOne - Vulnerability Disclosure Programs", "platform": "web", "url": "https://hackerone.com/directory/programs"},
        {"type": "lab", "title": "Bugcrowd", "platform": "web", "url": "https://bugcrowd.com"},
    ],
}


def _load_user_overrides() -> dict:
    """Load user-provided resource URL overrides from db/resources.json."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_default_config():
    """Save default resource config so user can edit it."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_RESOURCES, f, indent=2)


def get_resources_for_mission(mission_id: int) -> list:
    """Get resources for a mission, with user overrides applied."""
    _save_default_config()
    overrides = _load_user_overrides()
    mid = str(mission_id)
    
    # User overrides take priority
    if mid in overrides:
        return overrides[mid]
    return DEFAULT_RESOURCES.get(mid, [])


def show_mission_resources(mission_id: int, difficulty: str):
    """Display resources after mission completion."""
    resources = get_resources_for_mission(mission_id)
    if not resources:
        return

    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║          📚 LEARNING RESOURCES UNLOCKED!                    ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{DIM}  These resources match your current mission topic.{RESET}")
    print(f"{DIM}  Complete the course to deepen your understanding!{RESET}\n")

    for i, res in enumerate(resources, 1):
        icon = PLATFORM_ICONS.get(res.get("platform", "web"), "📄")
        url = res.get("url", "PLACEHOLDER")
        title = res.get("title", "Unknown")

        if url == "PLACEHOLDER":
            url_display = f"{DIM}(Add link in db/resources.json){RESET}"
        else:
            url_display = f"{BLUE}{url}{RESET}"

        print(f"  {icon} {BOLD}{i}. {title}{RESET}")
        print(f"     {url_display}")

    print(f"\n{DIM}  💡 To add your Telegram/Drive links, edit: db/resources.json{RESET}")
    print()
