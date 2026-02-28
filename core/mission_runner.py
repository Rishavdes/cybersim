"""
Universal Mission Runner for CyberSim.
Handles the rendering of the mission UI, displaying methods, tools, and guides
for a specific difficulty, and processes flag submission.
"""
import time
from core.mentor import ask_mentor
from core.state import save_state, award_xp, record_mission_completion

# ANSI Colors
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"

def run_mission(state: dict, level_id: int, difficulty: str, full_mission: dict) -> bool:
    """
    Renders the mission UI and handles the flag submission loop.
    Returns True if the mission was completed successfully, False if aborted.
    """
    diff_data = full_mission.get(difficulty)
    if not diff_data:
        print(f"{RED}[!] Error: Difficulty '{difficulty}' not found for mission {level_id}.{RESET}")
        return False
        
    print(f"\n{BOLD}{MAGENTA}══════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{CYAN}  MISSION: {full_mission['name']} [{difficulty.upper()} MODE] {RESET}")
    print(f"{BOLD}{MAGENTA}══════════════════════════════════════════════════════════════════════{RESET}")
    
    # 1. Briefing
    briefing = diff_data.get('briefing', full_mission.get('description', 'No briefing available.'))
    print(f"\n{BOLD}🎯 BRIEFING{RESET}")
    print(f"{DIM}{briefing}{RESET}")
    
    # 2. Objective
    objective = diff_data.get('objective', 'Complete this mission.')
    print(f"\n{BOLD}🚩 OBJECTIVE{RESET}")
    print(f"{GREEN}{objective}{RESET}")
    
    # Security Level
    security_level = diff_data.get('security_level', 'Standard')
    print(f"\n{BOLD}🛡️  SECURITY LEVEL{RESET}")
    sec_color = GREEN if difficulty == "easy" else (YELLOW if difficulty == "normal" else RED)
    print(f"{sec_color}{security_level}{RESET}")
    
    # 3. Methods & Tools
    if "methods" in diff_data and diff_data["methods"]:
        print(f"\n{BOLD}🛠️  RECOMMENDED METHODS{RESET}")
        for m in diff_data["methods"]:
            print(f"  {DIM}•{RESET} {m}")
            
    if "tools" in diff_data and diff_data["tools"]:
        print(f"\n{BOLD}🧰 TOOLS AVAILABLE{RESET}")
        for t in diff_data["tools"]:
            if isinstance(t, dict):
                print(f"  {CYAN}{t['name']:<15}{RESET} : {YELLOW}{t['cmd']:<40}{RESET} {DIM}({t['desc']}){RESET}")
            elif isinstance(t, (list, tuple)) and len(t) >= 3:
                print(f"  {CYAN}{t[0]:<15}{RESET} : {YELLOW}{t[1]:<40}{RESET} {DIM}({t[2]}){RESET}")

    # Topics (for theory missions)
    if "topics" in diff_data and diff_data["topics"]:
        print(f"\n{BOLD}📝 KEY TOPICS{RESET}")
        for topic in diff_data["topics"]:
            print(f"  {DIM}•{RESET} {topic}")

    # 4. Guide
    guide = diff_data.get('step_by_step_guide', full_mission.get('procedure', 'Follow the mission objective.'))
    if guide:
        print(f"\n{BOLD}📜 STEP-BY-STEP GUIDE{RESET}")
        print(f"{DIM}{guide}{RESET}")
    
    print(f"\n{BOLD}{MAGENTA}══════════════════════════════════════════════════════════════════════{RESET}")
    
    # Ensure flag format — auto-generate if missing
    correct_flag = diff_data.get('flag')
    if not correct_flag:
        # Generate a deterministic flag from mission name + difficulty
        import hashlib
        slug = full_mission['name'].lower().replace(' ', '_')[:20]
        correct_flag = f"FLAG{{{slug}_{difficulty}_2024}}"
    xp_reward = diff_data.get('xp_reward', 100)
    
    # ── Flag submission loop with 5-attempt limit ──
    MAX_ATTEMPTS = 5
    attempts = 0

    while True:
        remaining = MAX_ATTEMPTS - attempts
        if remaining > 0:
            print(f"\n{DIM}Enter the captured flag, type '{YELLOW}mentor{DIM}' for a hint, or '{RED}exit{DIM}' to abort. ({YELLOW}{remaining} attempts left{DIM}){RESET}")
        submission = input(f"{CYAN}cyber@sim:~$ {RESET}").strip()
        
        if submission.lower() in ('exit', 'quit'):
            print(f"\n{YELLOW}Mission aborted. Retiring to dashboard.{RESET}")
            return False
            
        if submission.lower() == 'mentor':
            if difficulty == "hard":
                print(f"\n{RED}[!] The Mentor is largely disconnected in HARD mode. General evasion advice only.{RESET}")
            prompt = input(f"\n{GREEN}[?] What do you need help with? {RESET}")
            if prompt:
                print(f"    {DIM}Consulting AI Mentor...{RESET}")
                context = f"Mission: {full_mission['name']}\nObjective: {diff_data['objective']}\nGuide: {diff_data['step_by_step_guide']}"
                try:
                    response = ask_mentor(prompt, difficulty, context)
                    print(f"\n    {GREEN}[🧠 MENTOR]:{RESET} {response}")
                except Exception as e:
                    print(f"\n    {RED}[!] Mentor connection failed: {e}{RESET}")
            continue
            
        if submission == correct_flag:
            print(f"\n{BOLD}{GREEN}🎉 FLAG ACCEPTED! MISSION ACCOMPLISHED! 🎉{RESET}")
            
            # Record completion specific to this difficulty
            record_mission_completion(state, level_id, difficulty)
            
            # Award XP
            state = award_xp(state, xp_reward, f"Completed {full_mission['name']} on {difficulty.upper()}")
            
            # Add to legacy completed_levels if not present
            if level_id not in state["completed_levels"]:
                state["completed_levels"].append(level_id)
                
            if correct_flag not in state["flags_captured"]:
                state["flags_captured"].append(correct_flag)
                
            save_state(state)
            return True
            
        else:
            attempts += 1
            if attempts < MAX_ATTEMPTS:
                print(f"\n{RED}[!] Incorrect flag. Keep digging. ({MAX_ATTEMPTS - attempts} attempts remaining){RESET}")
            else:
                # ── 5 attempts exhausted — Mentor Knowledge Question ──
                print(f"\n{YELLOW}{'═' * 60}{RESET}")
                print(f"{YELLOW}{BOLD}  ⚠️  ALL 5 FLAG ATTEMPTS EXHAUSTED!{RESET}")
                print(f"{YELLOW}{'═' * 60}{RESET}")
                print(f"\n{CYAN}[🧠 MENTOR]: I see you're stuck. Let me test your knowledge.{RESET}")
                print(f"{DIM}Answer this question correctly to pass the mission.{RESET}\n")

                # Generate a knowledge question from the mission context
                try:
                    q_prompt = (
                        f"Generate exactly ONE short cybersecurity quiz question about: "
                        f"'{full_mission['name']}'. The topic is: {diff_data['objective']}. "
                        f"Format: 'Question: <question>\\nAnswer: <short answer>'. "
                        f"Keep both extremely brief. One-line question, one-word or one-phrase answer."
                    )
                    q_response = ask_mentor(q_prompt, "easy")
                    
                    # Parse question and answer
                    q_lines = q_response.strip().split("\n")
                    question = ""
                    answer = ""
                    for line in q_lines:
                        if line.lower().startswith("question:"):
                            question = line.split(":", 1)[1].strip()
                        elif line.lower().startswith("answer:"):
                            answer = line.split(":", 1)[1].strip()
                    
                    if question and answer:
                        print(f"  {BOLD}❓ {question}{RESET}")
                        user_answer = input(f"\n  {CYAN}Your Answer: {RESET}").strip()
                        
                        if user_answer.lower() == answer.lower() or answer.lower() in user_answer.lower():
                            print(f"\n  {GREEN}{BOLD}✅ CORRECT! The Mentor approves your knowledge.{RESET}")
                            print(f"  {DIM}You demonstrated understanding even without the flag.{RESET}")
                            
                            record_mission_completion(state, level_id, difficulty)
                            reduced_xp = max(25, xp_reward // 2)
                            state = award_xp(state, reduced_xp, f"Knowledge Pass: {full_mission['name']} ({difficulty.upper()})")
                            
                            if level_id not in state["completed_levels"]:
                                state["completed_levels"].append(level_id)
                            save_state(state)
                            return True
                        else:
                            print(f"\n  {RED}[✘] Incorrect. The correct answer was: {BOLD}{answer}{RESET}")
                            print(f"  {YELLOW}[🧠 MENTOR]: Study this topic more and try the mission again!{RESET}")
                            return False
                    else:
                        # Fallback if AI response parsing fails
                        raise ValueError("Could not parse question")
                        
                except Exception:
                    # Offline fallback — ask a generic question
                    print(f"  {BOLD}❓ What is the main objective of this mission?{RESET}")
                    user_answer = input(f"\n  {CYAN}Your Answer: {RESET}").strip()
                    
                    if len(user_answer) > 10:  # Basic effort check
                        print(f"\n  {GREEN}{BOLD}✅ Good effort! The Mentor approves.{RESET}")
                        record_mission_completion(state, level_id, difficulty)
                        reduced_xp = max(25, xp_reward // 2)
                        state = award_xp(state, reduced_xp, f"Knowledge Pass: {full_mission['name']} ({difficulty.upper()})")
                        if level_id not in state["completed_levels"]:
                            state["completed_levels"].append(level_id)
                        save_state(state)
                        return True
                    else:
                        print(f"\n  {RED}[✘] Please provide a more detailed answer. Try the mission again.{RESET}")
                        return False
