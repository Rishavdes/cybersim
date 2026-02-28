"""
CyberSim Mentor - Powered by Ollama (Local AI)
Provides guidance based on difficulty mode and game context.
"""
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def _load_model():
    """Load configured model from ollama_config.json, or use default."""
    import os, json
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "ollama_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f).get("model", "llama3.2:1b")
        except Exception:
            pass
    return "llama3.2:1b"

MENTOR_MODEL = _load_model()

SYSTEM_PROMPTS = {
    "easy": (
        "You are an expert cybersecurity mentor for a beginner. "
        "Respond EXACTLY with the commands needed and a 1-sentence explanation. "
        "DO NOT write long paragraphs. Be direct. "
        "Always tell them exactly what terminal command to run."
    ),
    "normal": (
        "You are a cybersecurity coach. "
        "Give exactly one short hint. Do NOT give away the full answer immediately. "
        "DO NOT use filler words. Keep it under 2 sentences."
    ),
    "hard": (
        "You are a Red Team advisor. You are SILENT unless the user was blocked by the Defender. "
        "When blocked, analyze the log and provide exactly ONE evasion technique. "
        "Format: 'Technique: [Name] - [Command]'. Keep it extremely concise."
    ),
}


def ask_mentor(prompt: str, difficulty: str, context: str = "") -> str:
    """
    Sends a prompt to the Ollama model and returns the response.
    
    Args:
        prompt: The user's question or situation.
        difficulty: 'easy', 'normal', or 'hard'.
        context: Optional extra context (e.g., defender log output).
    
    Returns:
        The AI mentor's response as a string.
    """
    system = SYSTEM_PROMPTS.get(difficulty, SYSTEM_PROMPTS["normal"])
    full_prompt = f"{prompt}"
    if context:
        full_prompt = f"[DEFENDER LOG / CONTEXT]:\n{context}\n\n[USER SITUATION]:\n{prompt}"

    payload = {
        "model": MENTOR_MODEL,
        "system": system,
        "prompt": full_prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Mentor is offline. Check if ollama is running.")
    except requests.exceptions.ConnectionError:
        return "[!] Mentor Offline: Cannot connect to Ollama. Run 'ollama serve' in a terminal."
    except requests.exceptions.Timeout:
        return "[!] Mentor Timeout: Ollama took too long to respond."
    except Exception as e:
        return f"[!] Mentor Error: {e}"


def get_evasion_advice(defender_log: str, attack_type: str) -> str:
    """
    Called specifically when the AI Defender blocks the user (Hard Mode).
    Analyzes the block and suggests evasion techniques.
    """
    prompt = (
        f"The user was running a '{attack_type}' attack and got blocked by the AI Defender. "
        f"Analyze the defender log and tell the user specifically why they were caught "
        f"and give 2-3 concrete evasion techniques to try next."
    )
    return ask_mentor(prompt, "hard", context=defender_log)
