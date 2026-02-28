"""
Level 04: Privilege Escalation
Phase 2 - Month 4: Privilege Escalation
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.docker_mgr import start_arena, stop_arena, get_container_ip
from core.defender import AIDefender
from core.mission_data import get_mission
from core.mission_runner import run_mission

def run(state: dict, defender_callback=None) -> bool:
    """Main level runner using universal mission architecture."""
    # level_04 corresponds to mission_id 401
    mission_id = 401
    full_mission = get_mission(mission_id)
    difficulty = state["difficulty"]
    
    level_dir = full_mission.get("docker_image")
    container_name = full_mission.get("container")
    
    # Start the Docker arena
    if not start_arena(level_dir):
        print(f"\n\033[91m[!] Failed to start the arena. Is Docker running?\033[0m")
        return False

    target_ip = get_container_ip(container_name)
    print(f"\n\033[92m[🎯 TARGET]\033[0m IP Address: \033[1m{target_ip}\033[0m")
    print(f"\033[2mThe arena is live. Connect via SSH: ssh user@{target_ip} (pass: user123)\033[0m\n")

    # Start AI Defender if applicable
    defender = None
    if difficulty in ("normal", "hard"):
        defender_config = full_mission[difficulty].get("defender_config", {})
        defender = AIDefender(
            container_name=container_name,
            difficulty=difficulty,
            mentor_callback=defender_callback,
            config=defender_config
        )
        defender.start()

    # Run the universal UI and submission loop
    success = False
    try:
        success = run_mission(state, mission_id, difficulty, full_mission)
    finally:
        if defender:
            defender.stop()
        stop_arena(level_dir)

    return success
