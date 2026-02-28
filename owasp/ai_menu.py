"""
AI Vulnerability Testing Menu — Launch ARIA AI app and run 8 challenge types.
Includes model selection: lightweight (1B), normal (3B), large (8B).
"""
import os, sys, subprocess, time, webbrowser, urllib.request, json

CYAN="\033[96m"; GREEN="\033[92m"; YELLOW="\033[93m"; RED="\033[91m"
BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"; MAGENTA="\033[95m"; BLUE="\033[94m"

AI_VULNSITE_URL = "http://localhost:5001"
AI_VULNSITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "targets", "ai_vulnsite")

XP_TABLE = {
    "easy": {"per_challenge": 15, "section_bonus": 200},
    "normal": {"per_challenge": 30, "section_bonus": 400},
    "hard": {"per_challenge": 60, "section_bonus": 700},
    "ultra_hard": {"per_challenge": 120, "section_bonus": 1000},
}
DIFF_LABELS = {"easy":f"{GREEN}EASY{RESET}","normal":f"{YELLOW}NORMAL{RESET}","hard":f"{RED}HARD{RESET}","ultra_hard":f"{MAGENTA}ULTRA HARD{RESET}"}

MODEL_OPTIONS = {
    "1": {"key": "lightweight", "name": "llama3.2:1b", "label": "Lightweight (1B)", "desc": "Fast, basic responses"},
    "2": {"key": "normal",      "name": "llama3.2:latest", "label": "Normal (Balanced)",  "desc": "Balanced intelligence and speed"},
    "3": {"key": "large",       "name": "llama3:latest", "label": "Large (Advanced)", "desc": "Smartest, hardest to exploit"},
}


def select_ai_model():
    print(f"\n{BOLD}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║     SELECT AI MODEL (LLM Brain)      ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
    for k, m in MODEL_OPTIONS.items():
        print(f"  {CYAN}[{k}]{RESET} 🧠 {m['label']} — {DIM}{m['desc']}{RESET}")
    choice = input(f"\n{CYAN}Select [1/2/3]: {RESET}").strip()
    selected = MODEL_OPTIONS.get(choice, MODEL_OPTIONS["1"])
    print(f"  {GREEN}Selected: {selected['label']} ({selected['name']}){RESET}")

    # Ensure model is pulled
    print(f"  {DIM}Checking if model is available...{RESET}")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if selected["name"] not in result.stdout:
            print(f"  {YELLOW}[!] Pulling {selected['name']}... (first time only){RESET}")
            subprocess.run(["ollama", "pull", selected["name"]], timeout=600)
    except Exception:
        pass

    return selected


def select_ai_difficulty():
    print(f"\n{BOLD}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║     AI SECURITY LEVEL                ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
    print(f"  {GREEN}[1] Easy{RESET}       — No guardrails, AI shares everything")
    print(f"  {YELLOW}[2] Normal{RESET}     — Basic defense (simple instruction protection)")
    print(f"  {RED}[3] Hard{RESET}       — ChatGPT-level (input/output filtering + guardrails)")
    print(f"  {MAGENTA}[4] Ultra Hard{RESET} — Gemini/Claude-level (full defense, rate limiting)")
    choice = input(f"\n{CYAN}Select [1/2/3/4]: {RESET}").strip()
    return {"1":"easy","2":"normal","3":"hard","4":"ultra_hard"}.get(choice, "easy")


def start_ai_vulnsite(difficulty, model_name):
    compose = f"""version: "3.8"
services:
  ai_vulnsite:
    build: .
    container_name: cybersim_ai_vulnsite
    network_mode: "host"
    environment:
      - DIFFICULTY={difficulty}
      - OLLAMA_URL=http://127.0.0.1:11434
      - MODEL={model_name}
    restart: unless-stopped
"""
    with open(os.path.join(AI_VULNSITE_DIR, "docker-compose.yml"), "w") as f:
        f.write(compose)

    print(f"\n{CYAN}[🤖 AI ARENA]{RESET} Starting ARIA (model: {model_name}, security: {difficulty.upper()})...")
    try:
        subprocess.run(["docker-compose", "down"], cwd=AI_VULNSITE_DIR, capture_output=True, timeout=30)
        result = subprocess.run(["docker-compose", "up", "-d", "--build"], cwd=AI_VULNSITE_DIR,
                                capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"{RED}[!] Failed: {result.stderr[:200]}{RESET}")
            return False
        for _ in range(15):
            try:
                urllib.request.urlopen(AI_VULNSITE_URL, timeout=3)
                print(f"{GREEN}[✓] ARIA is LIVE at {AI_VULNSITE_URL}{RESET}")
                return True
            except:
                time.sleep(2)
        print(f"{YELLOW}[!] Try {AI_VULNSITE_URL} manually.{RESET}")
        return True
    except FileNotFoundError:
        print(f"{RED}[!] docker-compose not found.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
        return False


def verify_ai_flag(flag):
    try:
        data = json.dumps({"flag": flag}).encode()
        req = urllib.request.Request(f"{AI_VULNSITE_URL}/api/verify-flag", data=data,
                                     headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read().decode()).get("valid", False)
    except:
        return False


def ai_menu(state: dict) -> int:
    from owasp.ai_challenges import AI_CHALLENGES

    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║    🤖 AI VULNERABILITY TESTING (2026)                    ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n{CYAN}[📖 THEORY]{RESET}")
    print(f"AI systems face new threats: prompt injection, jailbreaking,")
    print(f"PII leakage, adversarial inputs, hallucination exploitation.")
    print(f"Test a REAL AI chatbot (ARIA) with configurable defenses.\n")

    # Step 1: Select AI model
    model = select_ai_model()

    # Step 2: Select difficulty (security level)
    difficulty = select_ai_difficulty()

    # Step 3: Launch AI VulnSite
    if not start_ai_vulnsite(difficulty, model["name"]):
        input(f"{DIM}Press Enter...{RESET}")
        return 0

    webbrowser.open(AI_VULNSITE_URL)
    print(f"\n{GREEN}[🤖]{RESET} ARIA chatbot opened at {BOLD}{AI_VULNSITE_URL}{RESET}")
    print(f"{DIM}Model: {model['label']} | Security: {DIFF_LABELS[difficulty]}{RESET}")
    print(f"{DIM}You can also switch models in the browser dropdown!{RESET}")
    input(f"\n{DIM}Press Enter to start challenges...{RESET}")

    xp_config = XP_TABLE[difficulty]
    total_xp = 0
    completed = 0

    for ch in AI_CHALLENGES:
        print(f"\n{BOLD}{'─'*55}{RESET}")
        print(f"  {CYAN}[{ch['id']}]{RESET} {BOLD}{ch['name']}{RESET}")
        print(f"  {ch['description']}")
        print(f"  {DIM}→ Target: {AI_VULNSITE_URL}{RESET}")

        if difficulty == "easy":
            print(f"\n  {GREEN}[STEP-BY-STEP]{RESET}")
            for i, s in enumerate(ch.get("steps_easy", []), 1):
                print(f"    {i}. {s}")
        elif difficulty == "normal":
            print(f"\n  {YELLOW}[HINT]{RESET} {ch.get('hint','Explore.')}")
        elif difficulty == "hard":
            print(f"\n  {RED}[OBJECTIVE]{RESET} Complete this challenge. No guidance.")
        else:
            print(f"\n  {MAGENTA}[BLIND]{RESET} Find the vulnerability.")

        while True:
            print(f"\n    [f] Submit FLAG | [d] Done | [k] Knowledge | [s] Skip | [q] Quit")
            choice = input(f"    {CYAN}> {RESET}").strip().lower()

            if choice == "f":
                flag = input(f"    {YELLOW}Paste FLAG: {RESET}").strip()
                if verify_ai_flag(flag):
                    print(f"    {GREEN}{BOLD}[🚩 AI FLAG CAPTURED!] +{xp_config['per_challenge']*3} XP{RESET}")
                    total_xp += xp_config["per_challenge"] * 3
                    completed += 1
                    break
                print(f"    {RED}[✗] Invalid flag.{RESET}")
            elif choice == "d":
                print(f"    {GREEN}[✓] +{xp_config['per_challenge']} XP{RESET}")
                total_xp += xp_config["per_challenge"]
                completed += 1
                break
            elif choice == "k":
                print(f"\n  {GREEN}📚 {ch['name']}{RESET}")
                print(f"  {ch['description']}")
                for s in ch.get("steps_easy", []):
                    print(f"  • {s}")
            elif choice == "s":
                print(f"    {YELLOW}Skipped.{RESET}")
                break
            elif choice == "q":
                return total_xp

    if completed == len(AI_CHALLENGES):
        print(f"\n{GREEN}{BOLD}🏆 ALL AI CHALLENGES COMPLETE! +{xp_config['section_bonus']} XP{RESET}")
        total_xp += xp_config["section_bonus"]

    print(f"\n{BOLD}Total AI XP: {CYAN}{total_xp}{RESET}")
    input(f"{DIM}Press Enter...{RESET}")
    return total_xp
