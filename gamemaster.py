#!/usr/bin/env python3
"""
CyberSim Gamemaster - Main Entry Point
The AI-powered cybersecurity training game.
"""
import os
import sys
import time
import json
import random
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.mentor import ask_mentor, get_evasion_advice
from core.state import load_state, save_state, award_xp, get_rank, is_mode_completed, get_next_required_mode
from core.mission_data import get_mission_for_day, get_mission
from core.docker_mgr import start_arena, stop_arena, get_container_ip, check_docker
from core.bonus_questions import BONUS_QUESTIONS
from core.history import show_mission_history
from core.ollama_config import ollama_brain_config
from core.resources import show_mission_resources
from core.quiz_server import run_monthly_quiz
from owasp.owasp_menu import owasp_menu
from core.rewards import reward_shop, get_active_title
from core.academy import academy_menu
from offensive.offensive_menu import offensive_menu

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

# ─── Practice Lab Recommendations ─────────────────────────────────────────────
PRACTICE_LABS = {
    101: {
        "topic": "Network Recon & Port Scanning",
        "free": [
            ("TryHackMe - Nmap", "https://tryhackme.com/room/furthernmap"),
            ("TryHackMe - Network Services", "https://tryhackme.com/room/networkservices"),
            ("HackTheBox - Starting Point", "https://app.hackthebox.com/starting-point"),
        ],
        "paid": [
            ("HTB Academy - Network Enumeration with Nmap", "https://academy.hackthebox.com/module/details/19"),
            ("INE - Network Scanning", "https://my.ine.com"),
        ],
    },
    201: {
        "topic": "Linux Fundamentals & Shell",
        "free": [
            ("TryHackMe - Linux Fundamentals 1-3", "https://tryhackme.com/room/linuxfundamentalspart1"),
            ("OverTheWire - Bandit", "https://overthewire.org/wargames/bandit/"),
            ("LinuxSurvival.com", "https://linuxsurvival.com"),
        ],
        "paid": [
            ("HTB Academy - Linux Fundamentals", "https://academy.hackthebox.com/module/details/18"),
            ("INE - Linux Host Security", "https://my.ine.com"),
        ],
    },
    301: {
        "topic": "Python Scripting for Hackers",
        "free": [
            ("TryHackMe - Python Basics", "https://tryhackme.com/room/pythonbasics"),
            ("Automate the Boring Stuff", "https://automatetheboringstuff.com"),
            ("HackerRank - Python", "https://www.hackerrank.com/domains/python"),
        ],
        "paid": [
            ("TCM Security - Python 101 for Hackers", "https://academy.tcm-sec.com"),
        ],
    },
    401: {
        "topic": "Linux Privilege Escalation",
        "free": [
            ("TryHackMe - Linux Privesc", "https://tryhackme.com/room/linprivesc"),
            ("TryHackMe - Linux Privesc Arena", "https://tryhackme.com/room/dvwa"),
            ("GTFOBins", "https://gtfobins.github.io"),
        ],
        "paid": [
            ("TCM Security - Linux Privilege Escalation", "https://academy.tcm-sec.com"),
            ("HTB Academy - Linux Privilege Escalation", "https://academy.hackthebox.com/module/details/51"),
        ],
    },
    501: {
        "topic": "Cryptography & Steganography",
        "free": [
            ("TryHackMe - Crack the Hash", "https://tryhackme.com/room/crackthehash"),
            ("CryptoHack", "https://cryptohack.org"),
            ("PicoCTF (Crypto challenges)", "https://picoctf.org"),
        ],
        "paid": [
            ("HTB Academy - Intro to Cryptography", "https://academy.hackthebox.com"),
        ],
    },
    801: {
        "topic": "Web Application Exploitation",
        "free": [
            ("TryHackMe - OWASP Top 10", "https://tryhackme.com/room/owasptop10"),
            ("PortSwigger Web Security Academy", "https://portswigger.net/web-security"),
            ("DVWA (Damn Vulnerable Web App)", "https://github.com/digininja/DVWA"),
        ],
        "paid": [
            ("HTB Academy - SQL Injection Fundamentals", "https://academy.hackthebox.com/module/details/33"),
            ("PentesterLab Pro", "https://pentesterlab.com"),
        ],
    },
}


def show_practice_labs(level_id: int):
    """Show recommended practice labs after completing a level."""
    labs = PRACTICE_LABS.get(level_id)
    if not labs:
        return

    print(f"\n{BOLD}╔══════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║        🏋️  PRACTICE LABS: {labs['topic'][:28]:<28} ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")

    print(f"\n  {GREEN}── FREE Labs ──{RESET}")
    for i, (name, url) in enumerate(labs["free"], 1):
        print(f"    {i}. {name}")
        print(f"       {DIM}{url}{RESET}")

    print(f"\n  {YELLOW}── PAID Labs ──{RESET}")
    for i, (name, url) in enumerate(labs["paid"], 1):
        print(f"    {i}. {name}")
        print(f"       {DIM}{url}{RESET}")

    bonus = random.choice(BONUS_QUESTIONS)
    if bonus:
        print(f"\n  {CYAN}── ⚡ BONUS QUICK CHALLENGE ──{RESET}")
        print(f"    {BOLD}{bonus['title']}{RESET}")
        print(f"    {bonus['description']}")
        try_it = input(f"\n    {CYAN}Want to try? (y/n): {RESET}").strip().lower()
        if try_it == "y":
            answer = input(f"    {YELLOW}Your Answer: {RESET}").strip()
            if answer:
                print(f"\n    {GREEN}[🧠 MENTOR SAYS]:{RESET} The recommended approach is:")
                print(f"    {DIM}{bonus['hint']}{RESET}")
                if answer.lower().strip() == bonus["hint"].lower().strip():
                    print(f"    {GREEN}[✓] Exactly right! +25 XP Bonus!{RESET}")
                else:
                    print(f"    {YELLOW}[~] Good attempt! Compare your answer with the mentor's.{RESET}")
    print()


def get_level_for_day(day: int) -> int | None:
    return get_mission_for_day(day)


def banner():
    print(f"""
{CYAN}{BOLD}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗███╗   ███╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║████╗ ████║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██║██╔████╔██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██║██║╚██╔╝██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║██║ ╚═╝ ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝
{RESET}
{DIM}   Professional Cybersecurity Training Range | AI-Powered{RESET}
{YELLOW}   "Hack to Learn. Learn to Hack."{RESET}
""")


def select_difficulty(state: dict) -> str:
    print(f"\n{BOLD}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║       SELECT DIFFICULTY MODE         ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
    print(f"\n  {GREEN}[1] Script Kiddie (Easy){RESET}")
    print(f"      AI Mentor guides every step. No active defense.")
    print(f"\n  {YELLOW}[2] Hacker (Normal){RESET}")
    print(f"      Hints on request. Passive monitoring.")
    print(f"\n  {RED}[3] Elite (Hard){RESET}")
    print(f"      No hints. Active AI Defender. Get caught = get blocked.")
    print(f"\n  {DIM}[Enter] Keep current: {state['difficulty'].upper()}{RESET}")

    choice = input(f"\n{CYAN}Select [1/2/3]: {RESET}").strip()
    mapping = {"1": "easy", "2": "normal", "3": "hard"}
    if choice in mapping:
        state["difficulty"] = mapping[choice]
        save_state(state)
        print(f"\n{GREEN}[✓] Difficulty set to: {state['difficulty'].upper()}{RESET}")
    return state["difficulty"]


def show_dashboard(state: dict):
    rank = get_rank(state["xp"])
    day = state["current_day"]
    mission_id = get_level_for_day(day)
    full_mission = get_mission(mission_id) if mission_id else None
    level_name = full_mission["name"] if full_mission else "Theory Day"

    print(f"\n{BOLD}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║              OPERATOR DASHBOARD              ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════╝{RESET}")
    print(f"  {CYAN}Player:{RESET}     {state['player_name']}")
    print(f"  {CYAN}Rank:{RESET}       {BOLD}{rank}{RESET}")
    print(f"  {CYAN}XP:{RESET}         {state['xp']}")
    print(f"  {CYAN}Day:{RESET}        {day}/730")
    print(f"  {CYAN}Streak:{RESET}     {state['streak']} days 🔥")
    print(f"  {CYAN}Today:{RESET}      {level_name}")

    if mission_id and full_mission:
        e_done = "✅" if is_mode_completed(state, mission_id, "easy") else "⬜"
        n_done = "✅" if is_mode_completed(state, mission_id, "normal") else "⬜"
        h_done = "✅" if is_mode_completed(state, mission_id, "hard") else "⬜"
        print(f"  {CYAN}Progress:{RESET}   {e_done} Easy  {n_done} Normal  {h_done} Hard")
    print()


def _get_phase_label(day: int) -> str:
    """Get current roadmap phase based on day number."""
    if day <= 5:     return "Phase 0 — Getting Started"
    if day <= 90:    return "Phase 1 — IT Foundations"
    if day <= 180:   return "Phase 2 — Security Concepts"
    if day <= 270:   return "Phase 3 — Offensive Foundations"
    if day <= 365:   return "Phase 4 — CEH + CTF Practice"
    if day <= 485:   return "Phase 5 — Professional (AD/WiFi)"
    if day <= 545:   return "Phase 6 — Exploit Development"
    if day <= 635:   return "Phase 7 — Blue Team Defense"
    return "Phase 8 — Advanced Red Team"


def main_menu(state: dict) -> str:
    title = get_active_title(state)
    day = state['current_day']
    phase = _get_phase_label(day)
    spec = state.get('specialization', '')
    spec_icon = '🔴' if spec == 'red' else '🔵' if spec == 'blue' else ''

    print(f"{BOLD}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║        C Y B E R S I M  v2.0         ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
    if title != "Recruit":
        print(f"  {MAGENTA}Rank: {title}{RESET} {spec_icon}")
    print(f"  {DIM}{phase} • Day {day}/730{RESET}")
    print()
    print(f"  {GREEN}[1]{RESET} 🎯 Continue Journey (Day {day})")
    print(f"  {CYAN}[2]{RESET} 📚 Learning Academy")
    print(f"  {YELLOW}[3]{RESET} 🏪 Rewards & Progress")
    print(f"  {MAGENTA}[5]{RESET} 📋 All Missions (77 total)")
    print(f"  {BLUE}[4]{RESET} ⚙️  Settings")
    print(f"  {DIM}[0]{RESET} Exit")
    return input(f"\n{CYAN}Choice: {RESET}").strip()


def settings_menu(state: dict) -> str:
    """Sub-menu for all settings and configuration."""
    print(f"\n{BOLD}  ⚙️  SETTINGS{RESET}")
    print(f"  {'─' * 35}")
    print(f"  {YELLOW}[1]{RESET} Change Difficulty ({state.get('difficulty', 'easy')})")
    print(f"  {CYAN}[2]{RESET} Ask AI Mentor a Question")
    print(f"  {BLUE}[3]{RESET} View Progress / Roadmap")
    print(f"  {GREEN}[4]{RESET} 📜 Mission History")
    print(f"  {CYAN}[5]{RESET} 🧠 Ollama Brain Config")
    print(f"  {RED}[6]{RESET} Reset Progression")
    print(f"  {DIM}[0]{RESET} ← Back")
    return input(f"\n{CYAN}Choice: {RESET}").strip()


def rewards_menu(state: dict) -> str:
    """Sub-menu for rewards and progress tracking."""
    print(f"\n{BOLD}  🏪 REWARDS & PROGRESS{RESET}")
    print(f"  {'─' * 35}")
    print(f"  {YELLOW}[1]{RESET} 🏪 Reward Shop")
    print(f"  {RED}[2]{RESET} 🛡️ OWASP Top 10 Training")
    print(f"  {RED}[3]{RESET} ⚔️  Offensive Attacks Training")
    print(f"  {DIM}[0]{RESET} ← Back")
    return input(f"\n{CYAN}Choice: {RESET}").strip()


def specialization_choice(state: dict):
    """Year 2 specialization choice — Red or Blue team path."""
    if state.get('specialization'):
        return  # Already chosen

    os.system("clear")
    print(f"\n{BOLD}{'═' * 50}{RESET}")
    print(f"{BOLD}  🎯 CONGRATULATIONS! YEAR 1 COMPLETE!{RESET}")
    print(f"{BOLD}{'═' * 50}{RESET}")
    print(f"\n  You've completed 365 days of training!")
    print(f"  Now it's time to {BOLD}choose your specialization{RESET}.")
    print(f"\n  {RED}[1] 🔴 Red Team Specialist{RESET}")
    print(f"      Focus: Malware, C2, EDR evasion, advanced exploitation")
    print(f"\n  {BLUE}[2] 🔵 Blue Team Specialist{RESET}")
    print(f"      Focus: SOC analysis, DFIR, threat hunting, detection")
    print(f"\n  {MAGENTA}[3] 🟣 Purple Team (Both){RESET}")
    print(f"      Focus: Attack + Defense — the hardest but most valuable")
    print(f"\n{'─' * 50}")

    while True:
        c = input(f"\n{CYAN}Choose your path (1/2/3): {RESET}").strip()
        if c == '1':
            state['specialization'] = 'red'
            print(f"\n{RED}{BOLD}🔴 Red Team path activated! Attack is the best defense.{RESET}")
            break
        elif c == '2':
            state['specialization'] = 'blue'
            print(f"\n{BLUE}{BOLD}🔵 Blue Team path activated! Protect and defend.{RESET}")
            break
        elif c == '3':
            state['specialization'] = 'purple'
            print(f"\n{MAGENTA}{BOLD}🟣 Purple Team path activated! Master of both worlds.{RESET}")
            break
    save_state(state)
    input(f"\n{DIM}Press Enter to continue...{RESET}")


def ask_mentor_interactive(state: dict):
    print(f"\n{CYAN}[🧠 MENTOR] What do you want to know?{RESET}")
    print(f"{DIM}(Type your question, or 'back' to return to Main Menu){RESET}")
    while True:
        question = input(f"\n{YELLOW}You: {RESET}").strip()
        if question.lower() == "back":
            return
        if not question:
            continue
        print(f"\n{DIM}Thinking...{RESET}")
        response = ask_mentor(question, state["difficulty"])
        print(f"\n{GREEN}[🧠 MENTOR]:{RESET}\n{response}\n")


def view_roadmap(state: dict):
    print(f"\n{BOLD}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║           2-YEAR MASTER ROADMAP              ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════╝{RESET}")
    phases = [
        ("🟢 Stage 1 (Month 1-3)", "Networking, Linux, Python", 1, 90),
        ("🔵 Stage 2 (Month 4-7)", "Security+, PrivEsc, Crypto, Web", 91, 210),
        ("🔵 Stage 2 (Month 8-9)", "CEH, Scanning, WiFi", 211, 270),
        ("🟠 Stage 3 (Month 10-12)", "Active Directory, BOF, THM/HTB", 271, 365),
        ("🟠 Stage 3 (Month 13-16)", "Blue Team: SOC, Splunk, DFIR", 366, 485),
        ("🔴 Stage 4 (Month 17-20)", "Malware Dev, Injection, Evasion, C2", 486, 625),
        ("🔴 Stage 4 (Month 21-22)", "Cert Prep, Bug Bounty", 626, 695),
        ("🏆 Final (Month 23-24)", "Portfolio, Interview, Job Hunt", 696, 730),
    ]
    current_day = state["current_day"]
    for name, topics, start, end in phases:
        status = "✅" if current_day > end else ("🔥" if current_day >= start else "🔒")
        progress = min(100, max(0, int((current_day - start) / (end - start) * 100))) if current_day >= start else 0
        bar = "█" * (progress // 5) + "░" * (20 - progress // 5)
        print(f"\n  {status} {BOLD}{name}{RESET}")
        print(f"     Topics: {DIM}{topics}{RESET}")
        print(f"     [{bar}] {progress}%")
    print()
    input(f"{DIM}Press Enter to continue...{RESET}")


def run_level(level_id: int, state: dict):
    """Run a mission natively passing through universal mechanics."""
    from core.mission_runner import run_mission
    from core.defender import AIDefender
    
    full_mission = get_mission(level_id)
    if not full_mission:
        print(f"[!] Mission {level_id} not found.")
        return

    # Progression Enforcement
    req_mode = get_next_required_mode(state, level_id)
    if req_mode == "done":
        print(f"\n{GREEN}You have already completed all difficulties for this mission.{RESET}")
        print(f"{DIM}Running on Hard mode by default for replay.{RESET}")
        state["difficulty"] = "hard"
    elif req_mode != state["difficulty"] and req_mode in ["easy", "normal"]:
        print(f"\n{YELLOW}[!] PROGRESSION ENFORCEMENT:{RESET}")
        print(f"    You must complete {BOLD}{req_mode.upper()}{RESET} mode before advancing to harder difficulties.")
        print(f"    Adjusting difficulty to {req_mode.upper()}...")
        state["difficulty"] = req_mode
        save_state(state)
        time.sleep(1.5)

    difficulty = state["difficulty"]
    is_lab = full_mission.get("type", "lab") == "lab"
    
    # Check if there is a specific legacy module for this (e.g. 101 -> level_01_network)
    # We refactored legacy modules to simply wrap run_mission. Rather than mapping them, 
    # we just replicate the docker start/stop logic here.
    
    level_dir = full_mission.get("docker_image")
    container_name = full_mission.get("container")
    
    if is_lab and level_dir:
        print(f"\n{DIM}Initialize Arena...{RESET}")
        
        target_flag = full_mission[difficulty].get("flag")
        
        if not start_arena(level_dir, target_flag=target_flag):
            print(f"{RED}[!] Failed to start Docker arena.{RESET}")
            return
            
        target_ip = get_container_ip(container_name)
        print(f"{GREEN}[🎯 TARGET]{RESET} IP Address: {BOLD}{target_ip}{RESET}")
        
        # ── Universal Dynamic Flag Injection ──
        if target_flag and container_name:
            import subprocess
            
            # 1. Replace static FLAG{...} patterns in all files
            static_cmd = f"find / -type f -not -path '*/\\.*' -not -path '*/proc/*' -not -path '*/sys/*' -not -path '*/dev/*' -exec grep -l 'FLAG{{' {{}} + 2>/dev/null | xargs -r -I {{}} sed -i 's/FLAG{{[^}}]*}}/{target_flag}/g' {{}}"
            subprocess.run(["docker", "exec", container_name, "sh", "-c", static_cmd], capture_output=True)
            
            # 2. Container-specific restarts or dynamic overrides
            if "linux_gym" in container_name:
                # Override all three challenge flags to match the specific day's mission
                linux_cmd = f"echo '{target_flag}' > /home/player/.secret && echo '{target_flag}' > /root/flag.txt && echo 'Feb 18 10:30:00 server kernel: {target_flag}' >> /var/log/syslog"
                subprocess.run(["docker", "exec", container_name, "sh", "-c", linux_cmd], capture_output=True)
            elif "vulnsite" in container_name or "web" in container_name:
                # Replace dynamic UUID flags generated in app.py targets
                py_cmd = rf"sed -i 's/\"FLAG{{\" + uuid\.uuid4()\.hex\[:16\] + \"}}\"/\"{target_flag}\"/g' /app/app.py 2>/dev/null || true"
                subprocess.run(["docker", "exec", container_name, "sh", "-c", py_cmd], capture_output=True)

    defender = None
    if difficulty in ("normal", "hard") and container_name:
        defender_config = full_mission[difficulty].get("defender_config", {})
        defender_cb = get_evasion_advice if difficulty == "hard" else None
        defender = AIDefender(
            container_name=container_name,
            difficulty=difficulty,
            mentor_callback=defender_cb,
            config=defender_config
        )
        defender.start()

    try:
        success = run_mission(state, level_id, difficulty, full_mission)
        if success:
            print(f"\n{BOLD}╔══════════════════════════════════════╗{RESET}")
            print(f"{BOLD}║             LEVEL CLEARED            ║{RESET}")
            print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
            
            show_practice_labs(level_id)
            show_mission_resources(level_id, difficulty)
            
            new_req_mode = get_next_required_mode(state, level_id)
            if new_req_mode == "done":
                # Mastered the entire day!
                print(f"  {GREEN}[1]{RESET} Excellent work! Advance to Day {state['current_day'] + 1}")
                input(f"\n{CYAN}Press Enter to advance...{RESET}")
                state["current_day"] += 1
                state["streak"] += 1
            else:
                print(f"  {YELLOW}[1]{RESET} Next Required Phase: {BOLD}{new_req_mode.upper()}{RESET}")
                input(f"\n{CYAN}Press Enter to start next phase...{RESET}")
                state["difficulty"] = new_req_mode
                print(f"\n{GREEN}[✓] Difficulty increased to {new_req_mode.upper()}! Run mission again from menu.{RESET}")

            save_state(state)
            time.sleep(1.5)
            
    except Exception as e:
        print(f"[!] Level error: {e}")
    finally:
        if defender:
            defender.stop()
        if is_lab and level_dir:
            stop_arena(level_dir)


def main():
    banner()

    # Check Docker
    if not check_docker():
        print(f"{RED}[!] Docker is not running! Please start Docker first.{RESET}")
        print(f"    Run: {CYAN}sudo service docker start{RESET}")
        sys.exit(1)

    state = load_state()

    # First run setup
    if state.get("player_name") == "Hacker":
        print(f"{YELLOW}Welcome to CyberSim! Let's set up your profile.{RESET}")
        name = input(f"Enter your hacker name: ").strip()
        if name:
            state["player_name"] = name
        select_difficulty(state)
        save_state(state)

    while True:
        os.system("clear")
        banner()
        show_dashboard(state)
        choice = main_menu(state)

        # ── [1] Continue Journey ──
        if choice == "1":
            day = state["current_day"]

            # Year 2 specialization check (Day 366)
            if day >= 366 and not state.get('specialization'):
                specialization_choice(state)

            # ── Monthly Quiz Check (every 30 days) ──
            if day > 1 and day % 30 == 0 and day not in state.get("quizzes_taken", []):
                print(f"\n{YELLOW}{BOLD}📝 MONTHLY KNOWLEDGE TEST REQUIRED!{RESET}")
                print(f"{DIM}You must complete the quiz before continuing to the next mission.{RESET}")
                input(f"\n{CYAN}Press Enter to start the quiz...{RESET}")
                result = run_monthly_quiz(state)
                if "quizzes_taken" not in state:
                    state["quizzes_taken"] = []
                state["quizzes_taken"].append(day)
                state = award_xp(state, result["xp_bonus"], f"Monthly Quiz (Day {day})")
                save_state(state)
                input(f"\n{DIM}Press Enter to continue to your mission...{RESET}")

            level_id = get_level_for_day(day)
            if level_id:
                run_level(level_id, state)
            else:
                print(f"\n{YELLOW}[📚 THEORY DAY]{RESET} Day {day} is a theory day.")
                print("Open your roadmap resources and study for 1 hour.")
                print("Resources are in: roadmap.md")
                input(f"\n{DIM}Press Enter when done to mark day complete...{RESET}")
                state = award_xp(state, 50, "Theory Day Completed")
                state["current_day"] += 1
                state["streak"] += 1
                save_state(state)

        # ── [2] Learning Academy ──
        elif choice == "2":
            academy_xp = academy_menu(state)
            if academy_xp > 0:
                state = award_xp(state, academy_xp, "Academy Study")
            save_state(state)

        # ── [3] Rewards & Progress (sub-menu) ──
        elif choice == "3":
            while True:
                os.system("clear")
                banner()
                rc = rewards_menu(state)
                if rc == "1":
                    state = reward_shop(state)
                    save_state(state)
                elif rc == "2":
                    owasp_xp = owasp_menu(state)
                    if owasp_xp != 0:
                        state = award_xp(state, owasp_xp, "OWASP Training" if owasp_xp > 0 else "Exam Penalty")
                        save_state(state)
                elif rc == "3":
                    off_xp = offensive_menu(state)
                    if off_xp > 0:
                        state = award_xp(state, off_xp, "Offensive Training")
                        save_state(state)
                elif rc == "0" or not rc:
                    break

        # ── [5] All Missions Browser ──
        elif choice == "5":
            from core.academy import _all_missions_browser, _load_academy_data
            adata = _load_academy_data()
            if adata:
                mission_xp = _all_missions_browser(state, adata)
                if mission_xp > 0:
                    state = award_xp(state, mission_xp, "Mission Browser")
                save_state(state)
            else:
                print(f"{RED}[!] No academy data found.{RESET}")
                input(f"\n{DIM}Press Enter...{RESET}")

        # ── [4] Settings (sub-menu) ──
        elif choice == "4":
            while True:
                os.system("clear")
                banner()
                sc = settings_menu(state)
                if sc == "1":
                    select_difficulty(state)
                elif sc == "2":
                    ask_mentor_interactive(state)
                elif sc == "3":
                    view_roadmap(state)
                elif sc == "4":
                    show_mission_history(state)
                elif sc == "5":
                    ollama_brain_config(state)
                elif sc == "6":
                    confirm = input(f"\n{RED}Are you sure you want to reset all progress to Day 1? (y/n): {RESET}").strip().lower()
                    if confirm == 'y':
                        state["xp"] = 0
                        state["current_day"] = 1
                        state["streak"] = 0
                        state["difficulty"] = "easy"
                        state["completed_levels"] = []
                        state["unlocked_rewards"] = []
                        state["active_title"] = "Recruit"
                        state.pop('specialization', None)
                        save_state(state)
                        print(f"\n{GREEN}[✓] Progression reset! Welcome back to Day 1.{RESET}")
                        time.sleep(1.5)
                elif sc == "0" or not sc:
                    break

        elif choice == "0":
            print(f"\n{CYAN}Stay curious. Stay dangerous. See you tomorrow.{RESET}\n")
            break


if __name__ == "__main__":
    main()
