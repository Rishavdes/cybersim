"""
CyberSim Mission History Viewer
Shows completed missions with full details, tools, and difficulty info.
"""
from core.mission_data import MISSIONS, get_mission
from core.state import is_mode_completed

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


def show_mission_history(state: dict):
    """Display completed missions and let user drill into details."""
    completions = state.get("mission_completions", {})

    if not completions:
        print(f"\n{YELLOW}[📜] No missions completed yet! Go finish your first mission.{RESET}")
        input(f"{DIM}Press Enter to continue...{RESET}")
        return

    while True:
        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║                   📜 MISSION HISTORY                        ║{RESET}")
        print(f"{BOLD}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}║  #   │ Mission Name                │ Easy │ Normal │ Hard   ║{RESET}")
        print(f"{BOLD}╠══════════════════════════════════════════════════════════════╣{RESET}")

        mission_ids = sorted([int(k) for k in completions.keys()])
        for idx, mid in enumerate(mission_ids, 1):
            mission = get_mission(mid)
            if not mission:
                continue
            name = mission["name"][:28]
            e = "✅" if is_mode_completed(state, mid, "easy") else "⬜"
            n = "✅" if is_mode_completed(state, mid, "normal") else "⬜"
            h = "✅" if is_mode_completed(state, mid, "hard") else "⬜"
            print(f"  {CYAN}{idx:>3}{RESET}  │ {name:<28} │  {e}  │  {n}   │  {h}")

        print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n  {DIM}Enter a mission number for details, or 'back' to return.{RESET}")

        choice = input(f"\n{CYAN}Select: {RESET}").strip().lower()
        if choice == "back" or choice == "b" or choice == "":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(mission_ids):
                _show_mission_detail(state, mission_ids[idx])
            else:
                print(f"{RED}[!] Invalid selection.{RESET}")
        except ValueError:
            print(f"{RED}[!] Enter a number or 'back'.{RESET}")


def _show_mission_detail(state: dict, mission_id: int):
    """Show full details for a specific completed mission."""
    mission = get_mission(mission_id)
    if not mission:
        print(f"{RED}[!] Mission data not found.{RESET}")
        return

    completions = state.get("mission_completions", {}).get(str(mission_id), [])

    print(f"\n{BOLD}{'═' * 62}{RESET}")
    print(f"{BOLD}  📋 MISSION {mission_id}: {mission['name'].upper()}{RESET}")
    print(f"{BOLD}{'═' * 62}{RESET}")

    difficulties = ["easy", "normal", "hard"]
    diff_colors = {"easy": GREEN, "normal": YELLOW, "hard": RED}
    diff_icons = {"easy": "🟢", "normal": "🟡", "hard": "🔴"}

    for diff in difficulties:
        if diff not in completions:
            print(f"\n  {DIM}{diff_icons[diff]} {diff.upper()} — Not completed yet{RESET}")
            continue

        data = mission.get(diff, {})
        color = diff_colors[diff]

        print(f"\n  {color}{BOLD}{diff_icons[diff]} {diff.upper()} MODE ✅{RESET}")
        print(f"  {'─' * 50}")

        # Objective
        if data.get("objective"):
            print(f"  {CYAN}🎯 Objective:{RESET} {data['objective']}")

        # Briefing (truncated to first 3 lines)
        if data.get("briefing"):
            lines = data["briefing"].strip().split("\n")
            print(f"\n  {CYAN}📄 Briefing:{RESET}")
            for line in lines[:3]:
                print(f"     {DIM}{line.strip()}{RESET}")
            if len(lines) > 3:
                print(f"     {DIM}... ({len(lines) - 3} more lines){RESET}")

        # Methods
        if data.get("methods"):
            print(f"\n  {CYAN}⚔️  Methods:{RESET}")
            for m in data["methods"]:
                print(f"     • {m}")

        # Tools
        if data.get("tools"):
            print(f"\n  {CYAN}🔧 Tools:{RESET}")
            for t in data["tools"]:
                if isinstance(t, tuple):
                    print(f"     • {t[0]}: {DIM}{t[1]}{RESET}")
                else:
                    print(f"     • {t}")

        # Security Level
        if data.get("security_level"):
            print(f"\n  {CYAN}🛡️  Security:{RESET} {data['security_level']}")

        # XP Reward
        if data.get("xp_reward"):
            print(f"  {CYAN}⭐ XP Earned:{RESET} {data['xp_reward']}")

    print(f"\n{BOLD}{'═' * 62}{RESET}")
    input(f"{DIM}Press Enter to go back...{RESET}")
