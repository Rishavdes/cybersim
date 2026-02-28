"""
Offensive Attacks Menu — Run attack phases against VulnSite target.
Uses existing VulnSite Docker container as practice target.
"""
import os, sys

CYAN="\033[96m"; GREEN="\033[92m"; YELLOW="\033[93m"; RED="\033[91m"
BOLD="\033[1m"; DIM="\033[2m"; RESET="\033[0m"; MAGENTA="\033[95m"; BLUE="\033[94m"

XP_TABLE = {
    "easy": {"per_technique": 10, "phase_bonus": 50, "total_bonus": 300},
    "normal": {"per_technique": 25, "phase_bonus": 75, "total_bonus": 500},
    "hard": {"per_technique": 50, "phase_bonus": 100, "total_bonus": 800},
    "ultra_hard": {"per_technique": 100, "phase_bonus": 150, "total_bonus": 1200},
}
DIFF_LABELS = {"easy":f"{GREEN}EASY{RESET}","normal":f"{YELLOW}NORMAL{RESET}","hard":f"{RED}HARD{RESET}","ultra_hard":f"{MAGENTA}ULTRA HARD{RESET}"}


def select_difficulty():
    print(f"\n{BOLD}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║     OFFENSIVE DIFFICULTY              ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════╝{RESET}")
    print(f"  {GREEN}[1] Easy{RESET}       — Full commands + step-by-step")
    print(f"  {YELLOW}[2] Normal{RESET}     — Hints + partial commands")
    print(f"  {RED}[3] Hard{RESET}       — Objective only")
    print(f"  {MAGENTA}[4] Ultra Hard{RESET} — Blind mode")
    choice = input(f"\n{CYAN}Select [1/2/3/4]: {RESET}").strip()
    return {"1":"easy","2":"normal","3":"hard","4":"ultra_hard"}.get(choice, "easy")


def run_phase(phase, difficulty):
    xp_config = XP_TABLE[difficulty]
    phase_xp = 0
    completed = 0
    total = len(phase["techniques"])

    print(f"\n{BOLD}{'─'*55}{RESET}")
    print(f"  {RED}⚔️  {phase['name']}{RESET}")
    print(f"  {DIM}{phase['theory']}{RESET}")
    print(f"  {DIM}Techniques: {total} | Difficulty: {DIFF_LABELS[difficulty]}{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}")

    for tech in phase["techniques"]:
        print(f"\n  {CYAN}[{tech['id']}]{RESET} {BOLD}{tech['description']}{RESET}")

        if difficulty == "easy":
            print(f"\n  {GREEN}[COMMAND]{RESET} {tech.get('command','')}")
            print(f"\n  {GREEN}[STEPS]{RESET}")
            for i, s in enumerate(tech.get("steps_easy", []), 1):
                print(f"    {i}. {s}")
        elif difficulty == "normal":
            print(f"\n  {YELLOW}[HINT]{RESET} {tech.get('hint','')}")
        elif difficulty == "hard":
            print(f"\n  {RED}[OBJECTIVE]{RESET} Complete this technique.")
        else:
            print(f"\n  {MAGENTA}[BLIND]{RESET} Figure it out.")

        while True:
            print(f"\n    [f] Submit FLAG | [g] Read Guide & Methods | [d] Done | [s] Skip | [q] Quit phase")
            choice = input(f"    {CYAN}> {RESET}").strip().lower()

            if choice == "f":
                expected_flag = tech.get("flag")
                if expected_flag:
                    user_flag = input(f"    {YELLOW}Enter FLAG: {RESET}").strip()
                    if user_flag == expected_flag or user_flag.lower() == expected_flag.lower():
                        print(f"    {GREEN}{BOLD}[🚩 FLAG CAPTURED!] +{xp_config['per_technique']*3} XP{RESET}")
                        phase_xp += xp_config["per_technique"] * 3
                        completed += 1
                        break
                    else:
                        print(f"    {RED}[✗] Incorrect flag.{RESET}")
                else:
                    # Generic proof
                    proof = input(f"    {YELLOW}Enter proof of completion (concept/output): {RESET}").strip()
                    if len(proof) > 3:
                        print(f"    {GREEN}{BOLD}[🚩 SUBMISSION ACCEPTED] +{xp_config['per_technique']*2} XP{RESET}")
                        phase_xp += xp_config["per_technique"] * 2
                        completed += 1
                        break
                    else:
                        print(f"    {RED}[✗] Proof too short.{RESET}")

            elif choice == "g":
                print(f"\n{BOLD}{MAGENTA}=== METHODOLOGY & GUIDE ==={RESET}")
                print(f"{CYAN}Technique:{RESET} {tech['description']}")
                print(f"{CYAN}Methodology:{RESET}\n{tech.get('guide', 'Explore the system and use standard techniques.')}")
                print(f"{MAGENTA}==========================={RESET}\n")

            elif choice == "d":
                print(f"    {GREEN}[✓] +{xp_config['per_technique']} XP{RESET}")
                phase_xp += xp_config["per_technique"]
                completed += 1
                break
            elif choice == "s":
                if difficulty == "easy":
                    print(f"    {DIM}Command was: {tech.get('command','N/A')}{RESET}")
                print(f"    {YELLOW}Skipped.{RESET}")
                break
            elif choice == "q":
                return phase_xp

    if completed == total:
        print(f"\n  {GREEN}{BOLD}[✓] Phase Complete! +{xp_config['phase_bonus']} XP{RESET}")
        phase_xp += xp_config["phase_bonus"]

    return phase_xp


def offensive_menu(state: dict) -> int:
    from offensive.attack_phases import ATTACK_PHASES

    total_xp = 0
    while True:
        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║    ⚔️  OFFENSIVE ATTACKS TRAINING                        ║{RESET}")
        print(f"{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
        for i, phase in enumerate(ATTACK_PHASES, 1):
            print(f"  {CYAN}[{i:2d}]{RESET} {phase['name']}")
        print(f"\n  {DIM}[b] Back to Main Menu{RESET}")

        choice = input(f"\n{CYAN}Select phase [1-{len(ATTACK_PHASES)}] or [b]: {RESET}").strip()
        if choice.lower() == "b":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(ATTACK_PHASES):
                difficulty = select_difficulty()
                xp = run_phase(ATTACK_PHASES[idx], difficulty)
                total_xp += xp
        except (ValueError, IndexError):
            print(f"  {RED}Invalid choice.{RESET}")

    return total_xp
