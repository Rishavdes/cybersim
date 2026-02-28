"""
CyberSim Learning Academy v2.0 — 8-Phase Roadmap Structure
Browse missions by roadmap phase, access study materials, and launch missions directly.
Course data is loaded from db/academy_courses.json (editable without code changes).
Phases map to the 2-year roadmap: Phase 1-4 (Year 1), Phase 5-8 (Year 2).
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

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMY_FILE = os.path.join(BASE_DIR, "db", "academy_courses.json")

# ─── Platform Icons ───────────────────────────────────────────────────────────
PLATFORM_ICONS = {
    "telegram": "📱", "gdrive": "📁", "elhacker": "💀",
    "web": "🌐", "youtube": "▶️", "lab": "🧪",
}

# ─── Phase Definitions (order matters) ────────────────────────────────────────
PHASES = [
    {"key": "phase_0", "icon": "⚪", "label": "Phase 0 — Absolute Beginner Intro",    "months": "Days 1-5",    "year": 0},
    {"key": "phase_1", "icon": "🟢", "label": "Phase 1 — IT Foundations",            "months": "Months 1-3",   "year": 1},
    {"key": "phase_2", "icon": "🟢", "label": "Phase 2 — Security Concepts",         "months": "Months 4-6",   "year": 1},
    {"key": "phase_3", "icon": "🟡", "label": "Phase 3 — Offensive Foundations",      "months": "Months 7-9",   "year": 1},
    {"key": "phase_4", "icon": "🟡", "label": "Phase 4 — CEH + CTF Practice",        "months": "Months 10-12", "year": 1},
    {"key": "phase_5", "icon": "🔴", "label": "Phase 5 — Professional (AD/WiFi)",    "months": "Months 13-15", "year": 2},
    {"key": "phase_6", "icon": "🔴", "label": "Phase 6 — Exploit Development",       "months": "Months 16-18", "year": 2},
    {"key": "phase_7", "icon": "🔵", "label": "Phase 7 — Blue Team Defense",         "months": "Months 19-21", "year": 2},
    {"key": "phase_8", "icon": "⚫", "label": "Phase 8 — Advanced Red Team",         "months": "Months 22-24", "year": 2},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def _load_academy_data() -> dict:
    """Load academy course data from JSON file."""
    if os.path.exists(ACADEMY_FILE):
        try:
            with open(ACADEMY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"  {RED}[!] Error loading academy data: {e}{RESET}")
    return {}


def _get_mission_data(mission_id: int) -> dict:
    """Get mission data from the mission databases."""
    from core.mission_data import get_mission
    return get_mission(mission_id) or {}


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN ACADEMY MENU — 8 PHASES
# ═══════════════════════════════════════════════════════════════════════════════

def academy_menu(state: dict) -> int:
    """
    Main Learning Academy entry point — 8-phase roadmap.
    Returns XP earned from studying (if any).
    """
    data = _load_academy_data()
    if not data:
        print(f"\n  {RED}[!] No academy data found. Check db/academy_courses.json{RESET}")
        input(f"\n  {DIM}Press Enter to return...{RESET}")
        return 0

    xp_earned = 0
    current_day = state.get("current_day", 1)
    specialization = state.get("specialization", "")

    while True:
        os.system("clear")
        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║          📚 CYBERSIM LEARNING ACADEMY v2.0                  ║{RESET}")
        print(f"{BOLD}╠══════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}║  8-Phase Roadmap • Zero to Expert in 2 Years               ║{RESET}")
        print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")

        # Phase 0 intro
        print(f"\n  {BOLD}{DIM}━━━ GETTING STARTED ━━━{RESET}")
        _print_phase_summary(state, data, PHASES[0], 0, current_day)

        # Year divider
        print(f"\n  {BOLD}{GREEN}━━━ YEAR 1 (Foundations → CEH) ━━━{RESET}")
        for i, phase in enumerate(PHASES[1:5], 1):
            _print_phase_summary(state, data, phase, i, current_day)

        print(f"\n  {BOLD}{RED}━━━ YEAR 2 (Professional → Expert) ━━━{RESET}")
        if specialization:
            spec_label = {'red': '🔴 Red Team', 'blue': '🔵 Blue Team', 'purple': '🟣 Purple'}.get(specialization, '')
            print(f"  {DIM}Specialization: {spec_label}{RESET}")
        for i, phase in enumerate(PHASES[5:], 5):
            _print_phase_summary(state, data, phase, i, current_day)

        print(f"\n  {GREEN}[a]{RESET} 📋 All Missions (browse & pick any)")
        print(f"  {DIM}[b] Back to Main Menu{RESET}")
        choice = input(f"\n  {CYAN}Select phase [0-8], [a]ll missions, or [b]: {RESET}").strip().lower()

        if choice == "b":
            break
        elif choice == "a":
            xp = _all_missions_browser(state, data)
            xp_earned += xp
            continue
        try:
            idx = int(choice)
            if 0 <= idx < len(PHASES):
                phase_key = PHASES[idx]["key"]
                xp = _phase_menu(state, phase_key, data)
                xp_earned += xp
        except ValueError:
            print(f"  {RED}[!] Invalid choice.{RESET}")

    return xp_earned


def _print_phase_summary(state, data, phase, number, current_day):
    """Print a single phase line with progress stats."""
    phase_data = data.get(phase["key"], {})
    topics = phase_data.get("topics", {})
    total_missions = sum(len(t.get("mission_ids", [])) for t in topics.values())
    completed = _count_completed_missions(state, phase["key"], data)

    # Determine if phase is current, locked, or completed
    phase_ranges = {0: (1, 5), 1: (6, 90), 2: (91, 180), 3: (181, 270), 4: (271, 365),
                    5: (366, 485), 6: (486, 545), 7: (546, 635), 8: (636, 730)}
    start, end = phase_ranges.get(number, (0, 0))

    if current_day >= start and current_day <= end:
        marker = f"{YELLOW}◀ YOU ARE HERE{RESET}"
    elif current_day > end:
        marker = f"{GREEN}✅{RESET}" if completed == total_missions and total_missions > 0 else ""
    else:
        marker = f"{DIM}🔒{RESET}"

    print(f"\n  {CYAN}[{number}]{RESET} {phase['icon']} {BOLD}{phase['label']}{RESET} {marker}")
    print(f"      {DIM}{phase['months']} | {len(topics)} topics | {total_missions} missions | ✅ {completed} done{RESET}")


def _count_completed_missions(state: dict, phase_key: str, data: dict) -> int:
    """Count how many missions in a phase the user has completed."""
    completed = state.get("completed_levels", [])
    phase_data = data.get(phase_key, {})
    topics = phase_data.get("topics", {})
    count = 0
    for topic in topics.values():
        for mid in topic.get("mission_ids", []):
            if mid in completed:
                count += 1
    return count


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE MENU (Shows topics within a phase)
# ═══════════════════════════════════════════════════════════════════════════════

def _phase_menu(state: dict, phase_key: str, data: dict) -> int:
    """Show topics within a phase. User can browse topics or play missions."""
    phase_data = data.get(phase_key, {})
    label = phase_data.get("label", phase_key)
    topics = phase_data.get("topics", {})
    topic_names = list(topics.keys())
    xp_earned = 0

    if not topic_names:
        print(f"\n  {YELLOW}[!] No topics defined for this phase yet.{RESET}")
        print(f"  {DIM}Add topics in db/academy_courses.json under \"{phase_key}\"{RESET}")
        input(f"\n  {DIM}Press Enter to return...{RESET}")
        return 0

    while True:
        os.system("clear")
        completed = state.get("completed_levels", [])
        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║  {label:^58}║{RESET}")
        print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
        desc = phase_data.get("description", "")
        if desc:
            print(f"  {DIM}{desc}{RESET}")
        print()

        for i, tname in enumerate(topic_names, 1):
            topic = topics[tname]
            mission_ids = topic.get("mission_ids", [])
            tdesc = topic.get("description", "")
            done = sum(1 for mid in mission_ids if mid in completed)
            total = len(mission_ids)
            vids = len(topic.get("videos", []))
            pdfs = len(topic.get("pdfs", []))
            labs = len(topic.get("labs", []))

            if total > 0 and done == total:
                status = f"{GREEN}[✅ COMPLETE]{RESET}"
            elif done > 0:
                status = f"{YELLOW}[{done}/{total} done]{RESET}"
            else:
                status = f"{DIM}[not started]{RESET}"

            print(f"  {CYAN}[{i:2d}]{RESET} {BOLD}{tname}{RESET}  {status}")
            print(f"       {DIM}{tdesc}{RESET}")
            print(f"       {DIM}📹 {vids} videos | 📄 {pdfs} PDFs | 🧪 {labs} labs | 🎯 {total} missions{RESET}")
            print()

        print(f"  {DIM}[b] Back{RESET}")
        choice = input(f"\n  {CYAN}Select topic [1-{len(topic_names)}] or [b]: {RESET}").strip().lower()

        if choice == "b":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(topic_names):
                tname = topic_names[idx]
                xp = _topic_menu(state, tname, topics[tname])
                xp_earned += xp
        except ValueError:
            print(f"  {RED}[!] Invalid choice.{RESET}")

    return xp_earned


# ═══════════════════════════════════════════════════════════════════════════════
#  TOPIC MENU (Shows resources + missions for a specific topic)
# ═══════════════════════════════════════════════════════════════════════════════

def _topic_menu(state: dict, topic_name: str, topic_data: dict) -> int:
    """Show everything about a topic: resources + playable missions."""
    xp_earned = 0

    while True:
        os.system("clear")
        mission_ids = topic_data.get("mission_ids", [])
        videos = topic_data.get("videos", [])
        pdfs = topic_data.get("pdfs", [])
        labs = topic_data.get("labs", [])
        completed = state.get("completed_levels", [])

        print(f"\n{BOLD}{'═' * 62}{RESET}")
        print(f"{BOLD}  📖 {topic_name}{RESET}")
        print(f"{BOLD}{'═' * 62}{RESET}")
        print(f"  {DIM}{topic_data.get('description', '')}{RESET}")
        print()

        # ─── Study Materials ──────────────────────────────────
        print(f"  {BOLD}┌─── 📹 VIDEO LECTURES ───────────────────────┐{RESET}")
        if videos:
            for i, v in enumerate(videos, 1):
                icon = PLATFORM_ICONS.get(v.get("platform", "web"), "📄")
                url = v.get("url", "PLACEHOLDER")
                name = v.get("name", "Unknown")
                note = v.get("note", "")
                if url == "PLACEHOLDER":
                    url_display = f"{DIM}(Add link in db/academy_courses.json){RESET}"
                else:
                    url_display = f"{BLUE}{url}{RESET}"
                print(f"  {icon} {i}. {name}")
                print(f"     {url_display}")
                if note:
                    print(f"     {YELLOW}⚠ {note}{RESET}")
        else:
            print(f"  {DIM}  No videos yet — add in db/academy_courses.json{RESET}")

        print(f"\n  {BOLD}┌─── 📄 PDF MATERIALS ────────────────────────┐{RESET}")
        if pdfs:
            for i, p in enumerate(pdfs, 1):
                icon = PLATFORM_ICONS.get(p.get("platform", "web"), "📄")
                url = p.get("url", "PLACEHOLDER")
                if url == "PLACEHOLDER":
                    url_display = f"{DIM}(Add link in db/academy_courses.json){RESET}"
                else:
                    url_display = f"{BLUE}{url}{RESET}"
                print(f"  {icon} {i}. {p['name']}")
                print(f"     {url_display}")
        else:
            print(f"  {DIM}  No PDFs yet — add in db/academy_courses.json{RESET}")

        print(f"\n  {BOLD}┌─── 🧪 HANDS-ON LABS ────────────────────────┐{RESET}")
        if labs:
            for i, l in enumerate(labs, 1):
                icon = PLATFORM_ICONS.get(l.get("platform", "web"), "📄")
                url = l.get("url", "")
                if url.startswith("docker:"):
                    url_display = f"{GREEN}[CyberSim Docker Lab — launch from missions]{RESET}"
                elif url == "PLACEHOLDER":
                    url_display = f"{DIM}(Add link in db/academy_courses.json){RESET}"
                else:
                    url_display = f"{BLUE}{url}{RESET}"
                print(f"  {icon} {i}. {l['name']}")
                print(f"     {url_display}")
        else:
            print(f"  {DIM}  No labs yet — add in db/academy_courses.json{RESET}")

        # ─── Playable Missions ────────────────────────────────
        if mission_ids:
            print(f"\n  {BOLD}┌─── 🎯 MISSIONS (Play Now!) ─────────────────┐{RESET}")
            for i, mid in enumerate(mission_ids, 1):
                m = _get_mission_data(mid)
                if m:
                    name = m.get("name", f"Mission {mid}")
                    mtype = m.get("type", "?")
                    docker = m.get("docker_image", "")
                    easy_xp = m.get("easy", {}).get("xp_reward", 0)
                    hard_xp = m.get("hard", {}).get("xp_reward", 0)

                    done = "✅" if mid in completed else "⬜"
                    docker_tag = f" {GREEN}[Docker]{RESET}" if docker else ""

                    print(f"  {done} {CYAN}[M{i}]{RESET} {BOLD}{name}{RESET} (ID: {mid}){docker_tag}")
                    print(f"       {DIM}XP: {easy_xp}-{hard_xp} | Type: {mtype}{RESET}")

                    # Show brief tools info
                    easy = m.get("easy", {})
                    tools = easy.get("tools", [])
                    if tools:
                        tool_names = []
                        for t in tools[:3]:
                            if isinstance(t, dict):
                                tool_names.append(t.get("name", "?"))
                            elif isinstance(t, (list, tuple)):
                                tool_names.append(t[0])
                        print(f"       {DIM}Tools: {', '.join(tool_names)}{RESET}")
                else:
                    print(f"  ⬜ {CYAN}[M{i}]{RESET} {DIM}Mission {mid} — data not found{RESET}")

        # ─── Actions ──────────────────────────────────────────
        print(f"\n  {BOLD}┌─── ACTIONS ─────────────────────────────────┐{RESET}")
        if mission_ids:
            print(f"  {GREEN}[p]{RESET} Play a mission from this topic")
        print(f"  {YELLOW}[d]{RESET} View detailed mission briefing")
        print(f"  {DIM}[b]{RESET} Back")

        choice = input(f"\n  {CYAN}Choice: {RESET}").strip().lower()

        if choice == "b":
            break
        elif choice == "p" and mission_ids:
            xp = _play_mission_from_topic(state, mission_ids)
            xp_earned += xp
        elif choice == "d" and mission_ids:
            _show_mission_detail(state, mission_ids)
        else:
            print(f"  {RED}[!] Invalid choice.{RESET}")

    return xp_earned


# ═══════════════════════════════════════════════════════════════════════════════
#  PLAY MISSION FROM TOPIC
# ═══════════════════════════════════════════════════════════════════════════════

def _play_mission_from_topic(state: dict, mission_ids: list) -> int:
    """Let user select and play a specific mission."""
    print(f"\n  {BOLD}Select mission to play:{RESET}")
    completed = state.get("completed_levels", [])

    for i, mid in enumerate(mission_ids, 1):
        m = _get_mission_data(mid)
        name = m.get("name", f"Mission {mid}") if m else f"Mission {mid}"
        done = "✅" if mid in completed else "⬜"
        print(f"  {done} {CYAN}[{i}]{RESET} {name} (ID: {mid})")

    print(f"  {DIM}[b] Cancel{RESET}")
    choice = input(f"\n  {CYAN}Mission to play [1-{len(mission_ids)}] or [b]: {RESET}").strip().lower()

    if choice == "b":
        return 0

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(mission_ids):
            mid = mission_ids[idx]
            # Import and run the mission
            from core.mission_runner import run_mission
            from core.state import save_state

            print(f"\n  {GREEN}[⚡] Launching Mission {mid}...{RESET}")
            run_mission(mid, state)
            save_state(state)
            return 0  # XP is awarded by mission_runner directly
    except (ValueError, ImportError) as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

    return 0


# ═══════════════════════════════════════════════════════════════════════════════
#  DETAILED MISSION VIEW
# ═══════════════════════════════════════════════════════════════════════════════

def _show_mission_detail(state: dict, mission_ids: list):
    """Show detailed briefing, tools, methods, and advice for a mission."""
    print(f"\n  {BOLD}Select mission to view details:{RESET}")

    for i, mid in enumerate(mission_ids, 1):
        m = _get_mission_data(mid)
        name = m.get("name", f"Mission {mid}") if m else f"Mission {mid}"
        print(f"  {CYAN}[{i}]{RESET} {name} (ID: {mid})")

    print(f"  {DIM}[b] Cancel{RESET}")
    choice = input(f"\n  {CYAN}Mission [1-{len(mission_ids)}] or [b]: {RESET}").strip().lower()

    if choice == "b":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(mission_ids):
            mid = mission_ids[idx]
            m = _get_mission_data(mid)
            if not m:
                print(f"  {RED}[!] Mission data not found.{RESET}")
                return

            difficulty = state.get("difficulty", "easy")
            diff_data = m.get(difficulty, m.get("easy", {}))

            print(f"\n{BOLD}{'═' * 62}{RESET}")
            print(f"{BOLD}  🎯 MISSION {mid}: {m.get('name', 'Unknown')}{RESET}")
            print(f"{BOLD}  Difficulty: {difficulty.upper()}{RESET}")
            print(f"{BOLD}{'═' * 62}{RESET}")

            # Briefing
            briefing = diff_data.get("briefing", "No briefing available.")
            print(f"\n  {BOLD}📋 BRIEFING:{RESET}")
            for line in briefing.split("\n"):
                print(f"  {line}")

            # Objective
            objective = diff_data.get("objective", "")
            if objective:
                print(f"\n  {BOLD}🎯 OBJECTIVE:{RESET}")
                print(f"  {GREEN}{objective}{RESET}")

            # Methods & Techniques
            methods = diff_data.get("methods", [])
            if methods:
                print(f"\n  {BOLD}🔧 METHODS & TECHNIQUES:{RESET}")
                for j, method in enumerate(methods, 1):
                    print(f"  {CYAN}{j}.{RESET} {method}")

            # Tools with commands
            tools = diff_data.get("tools", [])
            if tools:
                print(f"\n  {BOLD}🛠️  TOOLS & COMMANDS:{RESET}")
                for tool in tools:
                    if isinstance(tool, dict):
                        print(f"\n  {YELLOW}▸ {tool['name']}{RESET}")
                        print(f"    Command: {GREEN}{tool['cmd']}{RESET}")
                        print(f"    Purpose: {DIM}{tool['desc']}{RESET}")
                    elif isinstance(tool, (list, tuple)):
                        print(f"\n  {YELLOW}▸ {tool[0]}{RESET}")

            # Step-by-step guide
            guide = diff_data.get("step_by_step_guide", "")
            if guide:
                print(f"\n  {BOLD}📝 STEP-BY-STEP GUIDE:{RESET}")
                for line in guide.split("\n"):
                    print(f"  {line}")

            # Security level
            sec = diff_data.get("security_level", "")
            if sec:
                print(f"\n  {BOLD}🛡️  SECURITY LEVEL:{RESET}")
                print(f"  {RED}{sec}{RESET}")

            # XP reward
            xp = diff_data.get("xp_reward", 0)
            print(f"\n  {BOLD}⭐ XP REWARD:{RESET} {GREEN}{xp} XP{RESET}")

            # Docker info
            docker = m.get("docker_image", "")
            if docker:
                print(f"\n  {BOLD}🐳 DOCKER LAB:{RESET} {BLUE}{docker}{RESET}")
                print(f"  {DIM}This mission uses a Docker container for hands-on practice.{RESET}")

            # Advice section
            print(f"\n  {BOLD}💡 ADVICE:{RESET}")
            if difficulty == "easy":
                print(f"  {DIM}• Take your time — this is the learning difficulty{RESET}")
                print(f"  {DIM}• Follow the step-by-step guide exactly{RESET}")
                print(f"  {DIM}• If stuck, use the AI Mentor (Settings > Ask Mentor){RESET}")
            elif difficulty == "normal":
                print(f"  {DIM}• Try without the guide first, then refer to it if stuck{RESET}")
                print(f"  {DIM}• The target has basic monitoring — be stealthier{RESET}")
                print(f"  {DIM}• Research each tool to understand WHY you're using it{RESET}")
            else:
                print(f"  {DIM}• No hand-holding — you need to figure out the approach{RESET}")
                print(f"  {DIM}• Active defenses mean your tools will be detected{RESET}")
                print(f"  {DIM}• Think like a real attacker — evasion is key{RESET}")

            print(f"\n{'─' * 62}")
            input(f"\n  {DIM}Press Enter to return...{RESET}")

    except ValueError:
        print(f"  {RED}[!] Invalid choice.{RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
#  ALL MISSIONS BROWSER — Pick any mission from a single list
# ═══════════════════════════════════════════════════════════════════════════════

def _all_missions_browser(state: dict, data: dict) -> int:
    """
    Show ALL missions across all phases in one list, grouped by topic.
    User can select any mission to jump to its topic page.
    """
    xp_earned = 0
    completed = state.get("completed_levels", [])

    # Build flat list: [(mission_id, mission_name, topic_name, phase_label, topic_data)]
    all_missions = []
    for phase in PHASES:
        phase_data = data.get(phase["key"], {})
        phase_label = phase_data.get("label", phase["label"])
        topics = phase_data.get("topics", {})
        for topic_name, topic_data in topics.items():
            for mid in topic_data.get("mission_ids", []):
                m = _get_mission_data(mid)
                mname = m.get("name", f"Mission {mid}") if m else f"Mission {mid}"
                mtype = m.get("type", "?") if m else "?"
                all_missions.append({
                    "id": mid,
                    "name": mname,
                    "type": mtype,
                    "topic": topic_name,
                    "phase_label": phase_label,
                    "topic_data": topic_data,
                })

    TYPE_ICONS = {"lab": "🧪", "theory": "📖", "project": "🔨", "external": "🌐", "career": "🎓"}
    PAGE_SIZE = 20
    page = 0
    total_pages = (len(all_missions) + PAGE_SIZE - 1) // PAGE_SIZE

    while True:
        os.system("clear")
        start = page * PAGE_SIZE
        end = min(start + PAGE_SIZE, len(all_missions))

        print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}║        📋 ALL MISSIONS ({len(all_missions)} total)  Page {page+1}/{total_pages}         ║{RESET}")
        print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {DIM}✅ = completed  |  Pick any number to view topic & play{RESET}\n")

        current_phase = ""
        current_topic = ""
        for i in range(start, end):
            entry = all_missions[i]
            # Phase header
            if entry["phase_label"] != current_phase:
                current_phase = entry["phase_label"]
                print(f"\n  {BOLD}{YELLOW}─── {current_phase} ───{RESET}")
                current_topic = ""
            # Topic header
            if entry["topic"] != current_topic:
                current_topic = entry["topic"]
                print(f"  {BOLD}{CYAN}  📂 {current_topic}{RESET}")

            done = "✅" if entry["id"] in completed else "⬜"
            icon = TYPE_ICONS.get(entry["type"], "📄")
            print(f"    {done} {GREEN}[{i+1:3d}]{RESET} {icon} {entry['name']}")

        # Navigation
        print(f"\n  {'─' * 55}")
        nav = []
        if page > 0:
            nav.append(f"{CYAN}[p]{RESET} Prev page")
        if page < total_pages - 1:
            nav.append(f"{CYAN}[n]{RESET} Next page")
        nav.append(f"{DIM}[b]{RESET} Back")
        print(f"  {'  |  '.join(nav)}")

        choice = input(f"\n  {CYAN}Pick mission [1-{len(all_missions)}] or navigate: {RESET}").strip().lower()

        if choice == "b":
            break
        elif choice == "n" and page < total_pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(all_missions):
                    entry = all_missions[idx]
                    # Jump to that topic
                    xp = _topic_menu(state, entry["topic"], entry["topic_data"])
                    xp_earned += xp
            except ValueError:
                pass

    return xp_earned
