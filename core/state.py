"""
CyberSim State Manager
Persists user progress: current day, XP, difficulty, completed levels.
"""
import json
import os

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "state.json")

DEFAULT_STATE = {
    "player_name": "Hacker",
    "current_day": 1,
    "xp": 0,
    "streak": 0,
    "last_played": None,
    "difficulty": "normal",
    "completed_levels": [],
    "flags_captured": [],
    "mission_completions": {},
}


def load_state() -> dict:
    """Load state from disk, or create default if not exists."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            # Backwards compatibility
            if "mission_completions" not in state:
                state["mission_completions"] = {}
            return state
    return DEFAULT_STATE.copy()

def is_mode_completed(state: dict, level_id: int, difficulty: str) -> bool:
    """Check if a specific difficulty was completed for a level."""
    return difficulty in state.get("mission_completions", {}).get(str(level_id), [])

def get_next_required_mode(state: dict, level_id: int) -> str:
    """Returns the next difficulty the user must complete ('easy', 'normal', 'hard', 'done')."""
    comps = state.get("mission_completions", {}).get(str(level_id), [])
    if "easy" not in comps: return "easy"
    if "normal" not in comps: return "normal"
    if "hard" not in comps: return "hard"
    return "done"

def record_mission_completion(state: dict, level_id: int, difficulty: str):
    """Record completion of a specific difficulty."""
    comps = state.get("mission_completions", {})
    lid = str(level_id)
    if lid not in comps:
        comps[lid] = []
    if difficulty not in comps[lid]:
        comps[lid].append(difficulty)
    state["mission_completions"] = comps
    save_state(state)


def save_state(state: dict):
    """Save state to disk."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def award_xp(state: dict, amount: int, reason: str) -> dict:
    """Award XP to the player."""
    state["xp"] += amount
    print(f"\n[⭐ XP] +{amount} XP — {reason}! (Total: {state['xp']} XP)")
    save_state(state)
    return state


def get_rank(xp: int) -> str:
    """Return player rank based on XP."""
    if xp < 100:
        return "Script Kiddie"
    elif xp < 500:
        return "Hacker"
    elif xp < 1500:
        return "Penetration Tester"
    elif xp < 3000:
        return "Red Teamer"
    else:
        return "Elite Operator"
