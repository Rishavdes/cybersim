"""
OWASP Challenge Engine v3 — Launches CyberSim VulnSite (custom target)
Opens browser, gives difficulty-scaled guidance. No auto-fill of payloads.
"""
import time, subprocess, webbrowser, os, urllib.request

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
MAGENTA= "\033[95m"
BLUE   = "\033[94m"

VULNSITE_URL = "http://localhost:8080"
VULNSITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "targets", "vulnsite")

XP_TABLE = {
    "easy":      {"per_technique": 10, "stage_bonus": 50,  "section_bonus": 200},
    "normal":    {"per_technique": 25, "stage_bonus": 75,  "section_bonus": 300},
    "hard":      {"per_technique": 50, "stage_bonus": 100, "section_bonus": 500},
    "ultra_hard":{"per_technique": 100,"stage_bonus": 150, "section_bonus": 750},
}

DIFFICULTY_LABELS = {
    "easy": f"{GREEN}EASY{RESET}",
    "normal": f"{YELLOW}NORMAL{RESET}",
    "hard": f"{RED}HARD{RESET}",
    "ultra_hard": f"{MAGENTA}ULTRA HARD{RESET}",
}

DIFF_MAP = {"easy": "easy", "normal": "normal", "hard": "hard", "ultra_hard": "ultra_hard"}


def start_vulnsite(difficulty="easy") -> bool:
    """Start VulnSite Docker container with the given difficulty."""
    print(f"\n{CYAN}[🐳 ARENA]{RESET} Starting CyberSim VulnSite ({difficulty.upper()} security)...")
    print(f"{DIM}Building & starting the target website...{RESET}")

    # Update docker-compose with the right difficulty
    compose_content = f"""version: "3.8"
services:
  vulnsite:
    build: .
    container_name: cybersim_vulnsite
    ports:
      - "8080:5000"
    environment:
      - DIFFICULTY={difficulty}
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
"""
    compose_path = os.path.join(VULNSITE_DIR, "docker-compose.yml")
    with open(compose_path, "w") as f:
        f.write(compose_content)

    try:
        # Stop existing container first
        subprocess.run(["docker-compose", "down"], cwd=VULNSITE_DIR,
                        capture_output=True, timeout=30)
        # Build and start
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            cwd=VULNSITE_DIR,
            capture_output=True, text=True, timeout=300
        )
        if result.returncode != 0:
            print(f"{RED}[!] Failed to start VulnSite: {result.stderr[:200]}{RESET}")
            return False

        # Wait for ready
        print(f"{DIM}Waiting for VulnSite to initialize...{RESET}")
        for i in range(20):
            try:
                urllib.request.urlopen(VULNSITE_URL, timeout=3)
                print(f"{GREEN}[✓] VulnSite is LIVE at {BOLD}{VULNSITE_URL}{RESET}")
                return True
            except Exception:
                time.sleep(2)

        print(f"{YELLOW}[!] VulnSite starting... Try {VULNSITE_URL} manually.{RESET}")
        return True
    except FileNotFoundError:
        print(f"{RED}[!] docker-compose not found.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
        return False


def stop_vulnsite():
    subprocess.run(["docker-compose", "down"], cwd=VULNSITE_DIR,
                    capture_output=True, timeout=30)


def open_browser(path=""):
    """Open VulnSite page. Never includes payloads in URL."""
    url = f"{VULNSITE_URL}{path}"
    try:
        webbrowser.open(url)
    except Exception:
        print(f"{YELLOW}[!] Open manually: {url}{RESET}")


def select_owasp_difficulty() -> str:
    print(f"\n{BOLD}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║     SELECT OWASP DIFFICULTY          ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
    print(f"  {GREEN}[1] Easy{RESET}       — Full guidance + website has NO security")
    print(f"  {YELLOW}[2] Normal{RESET}     — Hints only + light sanitization active")
    print(f"  {RED}[3] Hard{RESET}       — Objective only + WAF active on website")
    print(f"  {MAGENTA}[4] Ultra Hard{RESET} — Zero hints + WAF + rate limiting + IP blocking")
    choice = input(f"\n{CYAN}Select [1/2/3/4]: {RESET}").strip()
    return {"1": "easy", "2": "normal", "3": "hard", "4": "ultra_hard"}.get(choice, "easy")


def run_stage(stage: dict, difficulty: str, state: dict) -> int:
    diff_order = ["easy", "normal", "hard", "ultra_hard"]
    if diff_order.index(difficulty) < diff_order.index(stage.get("min_difficulty", "easy")):
        return 0

    xp_config = XP_TABLE[difficulty]
    stage_xp = 0
    completed = 0
    total = len(stage["techniques"])

    print(f"\n{BOLD}{'─'*58}{RESET}")
    print(f"{BOLD}  ⚔️  Stage: {stage['name']}{RESET}")
    print(f"  {DIM}Challenges: {total} | Difficulty: {DIFFICULTY_LABELS[difficulty]}{RESET}")
    print(f"{BOLD}{'─'*58}{RESET}")

    for tech in stage["techniques"]:
        print(f"\n  {CYAN}[{tech['id']}]{RESET} {BOLD}{tech['description']}{RESET}")

        # Show the target page — user navigates manually
        target_page = tech.get("target_page", "/")
        print(f"  {DIM}→ Target page: {VULNSITE_URL}{target_page}{RESET}")

        # Guidance based on difficulty
        if difficulty == "easy":
            print(f"\n  {GREEN}[STEP-BY-STEP GUIDE]{RESET}")
            for i, step in enumerate(tech.get("steps_easy", []), 1):
                print(f"    {i}. {step}")
        elif difficulty == "normal":
            print(f"\n  {YELLOW}[HINT]{RESET} {tech.get('hint', 'No hint. Explore the page.')}")
        elif difficulty == "hard":
            print(f"\n  {RED}[OBJECTIVE]{RESET} Complete this challenge. No guidance.")
        else:
            print(f"\n  {MAGENTA}[BLIND]{RESET} Find and exploit the vulnerability.")

        while True:
            print(f"\n    [f] Submit FLAG (from website)")
            print(f"    [d] Done (no flag needed)")
            print(f"    [k] Knowledge Base")
            print(f"    [s] Skip")
            print(f"    [q] Quit stage")

            choice = input(f"    {CYAN}> {RESET}").strip().lower()

            if choice == "f":
                flag = input(f"    {YELLOW}Paste FLAG: {RESET}").strip()
                # Verify against VulnSite API
                verified = _verify_flag_api(flag)
                if verified:
                    print(f"    {GREEN}{BOLD}[🚩 FLAG CAPTURED!] +{xp_config['per_technique'] * 3} XP{RESET}")
                    stage_xp += xp_config["per_technique"] * 3
                    completed += 1
                    break
                else:
                    # Fallback: check against payload
                    if flag and tech.get("payload") and _check_answer(flag, tech["payload"]):
                        print(f"    {GREEN}[✓] Correct payload! +{xp_config['per_technique'] * 2} XP{RESET}")
                        stage_xp += xp_config["per_technique"] * 2
                        completed += 1
                        break
                    print(f"    {RED}[✗] Invalid flag. Keep hacking the website!{RESET}")
            elif choice == "d":
                print(f"    {GREEN}[✓] +{xp_config['per_technique']} XP{RESET}")
                stage_xp += xp_config["per_technique"]
                completed += 1
                break
            elif choice == "k":
                from owasp.knowledge_base import show_knowledge
                show_knowledge(tech["id"])
            elif choice == "s":
                if difficulty in ("easy", "normal"):
                    print(f"    {DIM}The expected approach was: {tech.get('payload','N/A')}{RESET}")
                print(f"    {YELLOW}[!] Skipped.{RESET}")
                break
            elif choice == "q":
                return stage_xp

    if completed == total:
        print(f"\n  {GREEN}{BOLD}[✓] Stage Complete! +{xp_config['stage_bonus']} XP Bonus{RESET}")
        stage_xp += xp_config["stage_bonus"]
    else:
        print(f"\n  {YELLOW}Completed {completed}/{total} challenges.{RESET}")

    return stage_xp


def _verify_flag_api(flag: str) -> bool:
    """Verify a flag against the VulnSite API."""
    try:
        import json
        data = json.dumps({"flag": flag}).encode()
        req = urllib.request.Request(
            f"{VULNSITE_URL}/api/verify-flag",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        result = json.loads(resp.read().decode())
        return result.get("valid", False)
    except Exception:
        return False


def _check_answer(user_answer: str, expected: str) -> bool:
    if user_answer.strip().lower() == expected.strip().lower():
        return True
    tokens = [t for t in expected.lower().split() if len(t) > 2]
    if tokens and all(t in user_answer.lower() for t in tokens):
        return True
    return False


def run_owasp_section(section: dict, state: dict) -> int:
    print(f"\n{BOLD}╔══════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║  {section['name']:<52}║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")

    # Theory
    print(f"\n{CYAN}[📖 THEORY]{RESET}")
    print(f"{section['theory']}\n")

    # Select difficulty FIRST (affects website security level)
    difficulty = select_owasp_difficulty()

    # Start VulnSite with matching difficulty
    if not start_vulnsite(difficulty):
        print(f"{RED}[!] Cannot proceed without the target. Check Docker.{RESET}")
        input(f"{DIM}Press Enter to return...{RESET}")
        return 0

    # Open browser
    open_browser()
    print(f"\n{GREEN}[🌐 TARGET]{RESET} ShopSim VulnSite is open at {BOLD}{VULNSITE_URL}{RESET}")
    print(f"{DIM}Security level: {DIFFICULTY_LABELS[difficulty]}")
    print(f"Use your browser + tools to hack it!")
    print(f"Come back to THIS terminal to track progress.{RESET}\n")
    input(f"{DIM}Press Enter to start challenges...{RESET}")

    total_xp = 0
    stages_completed = 0

    for stage in section["stages"]:
        xp = run_stage(stage, difficulty, state)
        total_xp += xp
        if xp > 0:
            stages_completed += 1

    xp_config = XP_TABLE[difficulty]
    if stages_completed == len(section["stages"]):
        print(f"\n{GREEN}{BOLD}🏆 SECTION COMPLETE! +{xp_config['section_bonus']} XP{RESET}")
        total_xp += xp_config["section_bonus"]

    # External labs
    labs = section.get("external_labs", {})
    if labs:
        print(f"\n{BOLD}── 🏋️ Practice More ──{RESET}")
        for name, url in labs.get("free", []):
            print(f"  {GREEN}[FREE]{RESET} {name} — {DIM}{url}{RESET}")
        for name, url in labs.get("paid", []):
            print(f"  {YELLOW}[PAID]{RESET} {name} — {DIM}{url}{RESET}")

    print(f"\n{BOLD}Total XP: {CYAN}{total_xp}{RESET}")
    input(f"\n{DIM}Press Enter to return...{RESET}")
    return total_xp
