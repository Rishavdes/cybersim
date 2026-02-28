"""
OWASP Top 10 Training — Submenu
[1-10] Guided training against CyberSim VulnSite
[11]   AI Security Testing (prompt injection, jailbreak, etc.)
[12]   Juice Shop EXAM (timed, XP penalty on failure)
"""
import os, sys, subprocess, webbrowser, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owasp.owasp_engine import run_owasp_section
from owasp.a01_access_control import SECTION as A01
from owasp.a02_misconfig import SECTION as A02
from owasp.a03_supply_chain import SECTION as A03
from owasp.a04_crypto_failures import SECTION as A04
from owasp.a05_injection import SECTION as A05
from owasp.a06_insecure_design import SECTION as A06
from owasp.a07_auth_failures import SECTION as A07
from owasp.a08_data_integrity import SECTION as A08
from owasp.a09_logging import SECTION as A09
from owasp.a10_exceptions import SECTION as A10

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
MAGENTA= "\033[95m"
BLUE   = "\033[94m"

OWASP_SECTIONS = {
    "1": A01, "2": A02, "3": A03, "4": A04, "5": A05,
    "6": A06, "7": A07, "8": A08, "9": A09, "10": A10,
}

JUICE_SHOP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "targets", "juice_shop")

# ─── EXAM CHALLENGES (for Juice Shop timed exam) ─────────────────
EXAM_CHALLENGES = [
    {"id": "exam_scoreboard", "name": "Find the Score Board", "points": 10,
     "answer_keywords": ["score-board", "score board", "/#/score-board"]},
    {"id": "exam_admin_login", "name": "Login as Admin", "points": 15,
     "answer_keywords": ["admin@juice-sh.op", "admin"]},
    {"id": "exam_xss", "name": "Perform a DOM XSS attack", "points": 20,
     "answer_keywords": ["<script>", "alert", "xss", "<iframe"]},
    {"id": "exam_sqli", "name": "SQL Injection on Login", "points": 20,
     "answer_keywords": ["' or", "1=1", "or true", "--"]},
    {"id": "exam_confidential", "name": "Find the Confidential Document", "points": 15,
     "answer_keywords": ["ftp", "confidential", "acquisitions"]},
    {"id": "exam_feedback", "name": "Post Feedback as another User", "points": 15,
     "answer_keywords": ["user_id", "forged", "intercept"]},
    {"id": "exam_basket", "name": "View another User's Basket", "points": 15,
     "answer_keywords": ["basket", "idor", "session"]},
    {"id": "exam_redirect", "name": "Find an Unvalidated Redirect", "points": 10,
     "answer_keywords": ["redirect", "url", "to="]},
    {"id": "exam_upload", "name": "Upload a file > 100KB", "points": 10,
     "answer_keywords": ["upload", "bypass", "size"]},
    {"id": "exam_api", "name": "Access the hidden /api endpoint", "points": 10,
     "answer_keywords": ["/api", "api", "swagger"]},
]


def launch_juice_shop_exam(state: dict) -> int:
    """Timed Juice Shop exam with XP penalty on failure."""
    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║    📝 JUICE SHOP EXAM — TIMED ASSESSMENT                ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")

    # Check training progress
    current_day = state.get("current_day", 1)
    if current_day < 30:
        days_left = 30 - current_day
        print(f"\n{RED}[!] EXAM LOCKED — Complete {days_left} more days of training first!{RESET}")
        print(f"{DIM}You must train for at least 30 days before taking the exam.{RESET}")
        print(f"{DIM}Current day: {current_day}/30{RESET}")
        input(f"\n{DIM}Press Enter to return...{RESET}")
        return 0

    print(f"\n{YELLOW}⚠️  EXAM RULES:{RESET}")
    print(f"  • Time limit: {BOLD}60 minutes{RESET}")
    print(f"  • {len(EXAM_CHALLENGES)} challenges from your training syllabus")
    print(f"  • Total points: {sum(c['points'] for c in EXAM_CHALLENGES)}")
    print(f"  • Pass: ≥70% → {GREEN}+500 bonus XP{RESET}")
    print(f"  • Fail: <70% → {RED}XP PENALTY: (100 - score%) × 5{RESET}")
    print(f"  • Your current XP: {CYAN}{state.get('xp',0)}{RESET}")

    confirm = input(f"\n{RED}Start exam? (y/n): {RESET}").strip().lower()
    if confirm != "y":
        return 0

    # Launch Juice Shop
    print(f"\n{CYAN}[🐳]{RESET} Starting Juice Shop...")
    try:
        subprocess.run(["docker-compose", "up", "-d"], cwd=JUICE_SHOP_DIR,
                        capture_output=True, text=True, timeout=300)
        import urllib.request
        for _ in range(30):
            try:
                urllib.request.urlopen("http://localhost:3000", timeout=3)
                break
            except:
                time.sleep(2)
        webbrowser.open("http://localhost:3000")
    except Exception as e:
        print(f"{RED}[!] Failed to start Juice Shop: {e}{RESET}")
        input(f"{DIM}Press Enter...{RESET}")
        return 0

    # Start timed exam
    start_time = time.time()
    time_limit = 60 * 60  # 60 minutes
    total_points = sum(c["points"] for c in EXAM_CHALLENGES)
    earned_points = 0
    completed = 0

    print(f"\n{BOLD}{'═'*55}{RESET}")
    print(f"{BOLD}  📝 EXAM STARTED — Timer: 60 minutes{RESET}")
    print(f"{BOLD}{'═'*55}{RESET}\n")

    for ch in EXAM_CHALLENGES:
        elapsed = time.time() - start_time
        remaining = max(0, time_limit - elapsed)
        mins = int(remaining // 60)
        secs = int(remaining % 60)

        if remaining <= 0:
            print(f"\n{RED}{BOLD}⏰ TIME'S UP!{RESET}")
            break

        print(f"\n  {CYAN}[{ch['id']}]{RESET} {BOLD}{ch['name']}{RESET} ({ch['points']} pts)")
        print(f"  {DIM}⏱️ Time remaining: {mins}m {secs}s{RESET}")

        while True:
            elapsed = time.time() - start_time
            if elapsed >= time_limit:
                print(f"\n{RED}⏰ TIME'S UP!{RESET}")
                break

            print(f"\n    [f] Submit proof | [s] Skip | [q] End exam")
            choice = input(f"    {CYAN}> {RESET}").strip().lower()

            if choice == "f":
                answer = input(f"    {YELLOW}Your proof/answer: {RESET}").strip()
                if any(kw in answer.lower() for kw in ch["answer_keywords"]):
                    print(f"    {GREEN}[✓] Correct! +{ch['points']} points{RESET}")
                    earned_points += ch["points"]
                    completed += 1
                    break
                else:
                    print(f"    {RED}[✗] Wrong. Try again or skip.{RESET}")
            elif choice == "s":
                print(f"    {YELLOW}Skipped.{RESET}")
                break
            elif choice == "q":
                break
        else:
            continue
        if choice == "q" or (time.time() - start_time >= time_limit):
            break

    # Calculate results
    elapsed_total = time.time() - start_time
    score_pct = (earned_points / total_points) * 100 if total_points > 0 else 0
    passed = score_pct >= 70

    print(f"\n{BOLD}{'═'*55}{RESET}")
    print(f"{BOLD}  📊 EXAM RESULTS{RESET}")
    print(f"{BOLD}{'═'*55}{RESET}")
    print(f"  Score: {earned_points}/{total_points} ({score_pct:.0f}%)")
    print(f"  Completed: {completed}/{len(EXAM_CHALLENGES)}")
    print(f"  Time: {int(elapsed_total//60)}m {int(elapsed_total%60)}s")

    xp_change = 0
    if passed:
        xp_change = 500
        print(f"\n  {GREEN}{BOLD}✅ PASSED! +{xp_change} XP bonus{RESET}")
        if score_pct == 100:
            xp_change = 1000
            print(f"  {GREEN}{BOLD}🏆 PERFECT SCORE! +1000 XP!{RESET}")
    else:
        xp_penalty = int((100 - score_pct) * 5)
        xp_change = -xp_penalty
        print(f"\n  {RED}{BOLD}❌ FAILED — -{xp_penalty} XP penalty{RESET}")
        print(f"  {DIM}Study more and retake the exam after more training.{RESET}")

    print(f"{BOLD}{'═'*55}{RESET}")
    input(f"\n{DIM}Press Enter...{RESET}")
    return xp_change


def owasp_menu(state: dict) -> int:
    total_xp = 0

    while True:
        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║        🛡️  OWASP TOP 10 TRAINING (2025)                  ║{RESET}")
        print(f"{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n  {BOLD}── GUIDED TRAINING (CyberSim VulnSite) ──{RESET}")
        print(f"  {RED}[1]{RESET}  A01: Broken Access Control + SSRF")
        print(f"  {RED}[2]{RESET}  A02: Security Misconfiguration")
        print(f"  {YELLOW}[3]{RESET}  A03: Supply Chain Failures {MAGENTA}(NEW 2025){RESET}")
        print(f"  {YELLOW}[4]{RESET}  A04: Cryptographic Failures")
        print(f"  {GREEN}[5]{RESET}  A05: Injection (SQLi / XSS / CmdI)")
        print(f"  {GREEN}[6]{RESET}  A06: Insecure Design")
        print(f"  {CYAN}[7]{RESET}  A07: Authentication Failures")
        print(f"  {CYAN}[8]{RESET}  A08: Data Integrity Failures")
        print(f"  {BLUE}[9]{RESET}  A09: Logging & Alerting Failures")
        print(f"  {BLUE}[10]{RESET} A10: Mishandling Exceptions {MAGENTA}(NEW 2025){RESET}")
        print(f"\n  {BOLD}── AI SECURITY (2026) ──{RESET}")
        print(f"  {MAGENTA}[11]{RESET} 🤖 AI Vulnerability Testing (prompt injection, jailbreak...)")
        print(f"\n  {BOLD}── EXAM MODE ──{RESET}")
        print(f"  {RED}[12]{RESET} 📝 Juice Shop EXAM (timed, 60min, XP penalty on fail)")
        print(f"\n  {DIM}[b] Back to Main Menu{RESET}")

        choice = input(f"\n{CYAN}Select [1-12 or b]: {RESET}").strip()

        if choice.lower() == "b":
            break

        if choice == "11":
            from owasp.ai_menu import ai_menu
            xp = ai_menu(state)
            total_xp += xp
            continue

        if choice == "12":
            xp = launch_juice_shop_exam(state)
            total_xp += xp
            continue

        section = OWASP_SECTIONS.get(choice)
        if section:
            xp = run_owasp_section(section, state)
            total_xp += xp
        else:
            print(f"{RED}[!] Invalid choice.{RESET}")

    return total_xp
