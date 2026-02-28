"""
CyberSim Ollama Brain Auto-Configuration
Detects system specs and recommends the optimal Ollama model.
"""
import os
import json
import subprocess
import shutil

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

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "ollama_config.json")

# ─── Expanded Model Database ─────────────────────────────────────────────────
# Sorted from lightest to heaviest. Each entry has:
#   name, params, min_ram_gb, min_vram_gb (0 = CPU-only OK), description, best_for
OLLAMA_MODELS = [
    {
        "name": "tinyllama:1.1b",
        "params": "1.1B",
        "min_ram_gb": 2,
        "min_vram_gb": 0,
        "size_gb": 0.6,
        "description": "Ultra-lightweight, fastest possible. Basic Q&A only.",
        "best_for": "Very low-end systems (2-4 GB RAM, no GPU)",
    },
    {
        "name": "phi3:mini",
        "params": "3.8B",
        "min_ram_gb": 4,
        "min_vram_gb": 0,
        "size_gb": 2.2,
        "description": "Microsoft's efficient small model. Great reasoning for its size.",
        "best_for": "Budget laptops (4-6 GB RAM, no GPU)",
    },
    {
        "name": "llama3.2:1b",
        "params": "1B",
        "min_ram_gb": 4,
        "min_vram_gb": 0,
        "size_gb": 1.3,
        "description": "Meta's latest ultra-compact model. Fast and capable.",
        "best_for": "Low-RAM systems needing speed (4-8 GB RAM)",
    },
    {
        "name": "llama3.2:3b",
        "params": "3B",
        "min_ram_gb": 6,
        "min_vram_gb": 0,
        "size_gb": 2.0,
        "description": "Bigger Llama 3.2 with better reasoning and instruction following.",
        "best_for": "Mid-range systems (6-8 GB RAM, no GPU)",
    },
    {
        "name": "mistral:7b",
        "params": "7B",
        "min_ram_gb": 8,
        "min_vram_gb": 0,
        "size_gb": 4.1,
        "description": "Mistral's flagship 7B. Excellent code and reasoning.",
        "best_for": "8 GB+ RAM systems, good all-rounder",
    },
    {
        "name": "gemma2:9b",
        "params": "9B",
        "min_ram_gb": 8,
        "min_vram_gb": 0,
        "size_gb": 5.4,
        "description": "Google's Gemma 2.  Strong instruction following and safety.",
        "best_for": "8-12 GB RAM, well-rounded performance",
    },
    {
        "name": "llama3.1:8b",
        "params": "8B",
        "min_ram_gb": 8,
        "min_vram_gb": 4,
        "size_gb": 4.7,
        "description": "Meta's powerful 8B model. Excellent for cybersecurity mentoring.",
        "best_for": "8-16 GB RAM with GPU (best quality/speed ratio)",
    },
    {
        "name": "deepseek-coder-v2:16b",
        "params": "16B",
        "min_ram_gb": 12,
        "min_vram_gb": 6,
        "size_gb": 8.9,
        "description": "DeepSeek's coding specialist. Best for exploit/script generation.",
        "best_for": "12+ GB RAM with 6+ GB VRAM (code-focused)",
    },
    {
        "name": "codellama:13b",
        "params": "13B",
        "min_ram_gb": 12,
        "min_vram_gb": 6,
        "size_gb": 7.4,
        "description": "Meta's code-focused LLM. Trained specifically on code generation.",
        "best_for": "12+ GB RAM with GPU (code/exploit writing)",
    },
    {
        "name": "mixtral:8x7b",
        "params": "47B MoE",
        "min_ram_gb": 16,
        "min_vram_gb": 8,
        "size_gb": 26.0,
        "description": "Mistral's Mixture-of-Experts. Near GPT-4 quality.",
        "best_for": "16+ GB RAM with 8+ GB VRAM (premium quality)",
    },
    {
        "name": "llama3.1:70b",
        "params": "70B",
        "min_ram_gb": 48,
        "min_vram_gb": 24,
        "size_gb": 40.0,
        "description": "Meta's largest open model. State-of-the-art instruction and reasoning.",
        "best_for": "Workstations with 48+ GB RAM (research grade)",
    },
]


def _get_ram_gb() -> float:
    """Get total system RAM in GB."""
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    return round(kb / 1024 / 1024, 1)
    except Exception:
        pass
    return 0.0


def _get_cpu_info() -> dict:
    """Get CPU info: cores, model name."""
    info = {"cores": os.cpu_count() or 1, "model": "Unknown"}
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    info["model"] = line.split(":")[1].strip()
                    break
    except Exception:
        pass
    return info


def _get_gpu_info() -> dict:
    """Check for NVIDIA GPU and VRAM."""
    info = {"available": False, "name": "None", "vram_gb": 0}
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split(",")
            info["available"] = True
            info["name"] = parts[0].strip()
            info["vram_gb"] = round(int(parts[1].strip()) / 1024, 1)
    except (FileNotFoundError, Exception):
        pass
    return info


def _get_disk_free_gb() -> float:
    """Get free disk space in GB."""
    try:
        usage = shutil.disk_usage("/")
        return round(usage.free / (1024 ** 3), 1)
    except Exception:
        return 0.0


def _recommend_models(ram_gb: float, cpu_cores: int, gpu_vram_gb: float, disk_free_gb: float) -> list:
    """Return a list of compatible models sorted best-first."""
    compatible = []
    for model in OLLAMA_MODELS:
        # Check RAM
        if ram_gb < model["min_ram_gb"]:
            continue
        # Check disk space
        if disk_free_gb < model["size_gb"] + 1.0:  # Need 1GB buffer
            continue
        # Check VRAM requirement
        if model["min_vram_gb"] > 0 and gpu_vram_gb < model["min_vram_gb"]:
            continue
        compatible.append(model)

    # Return in reverse order (best first)
    return list(reversed(compatible))


def _get_installed_models() -> list:
    """Get list of locally installed Ollama models."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            models = []
            for line in lines:
                parts = line.split()
                if parts:
                    models.append(parts[0])
            return models
    except Exception:
        pass
    return []


def load_ollama_config() -> dict:
    """Load saved Ollama config from disk."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_configured_model() -> str:
    """Get the configured model name, or default."""
    config = load_ollama_config()
    return config.get("model", "llama3.2:1b")


def save_ollama_config(model: str, specs: dict):
    """Save Ollama configuration to disk."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    config = {
        "model": model,
        "specs": specs,
        "configured": True,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def ollama_brain_config(state: dict):
    """Interactive Ollama Brain auto-configuration."""
    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║              🧠 OLLAMA BRAIN CONFIGURATION                  ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")

    # ── Step 1: Detect System Specs ──
    print(f"\n{CYAN}[⚙️] Detecting your system specifications...{RESET}\n")

    ram_gb = _get_ram_gb()
    cpu = _get_cpu_info()
    gpu = _get_gpu_info()
    disk_free = _get_disk_free_gb()

    specs = {
        "ram_gb": ram_gb,
        "cpu_cores": cpu["cores"],
        "cpu_model": cpu["model"],
        "gpu_available": gpu["available"],
        "gpu_name": gpu["name"],
        "gpu_vram_gb": gpu["vram_gb"],
        "disk_free_gb": disk_free,
    }

    print(f"  {BOLD}{'─' * 50}{RESET}")
    print(f"  {CYAN}💻 CPU:{RESET}       {cpu['model']}")
    print(f"  {CYAN}🧮 Cores:{RESET}     {cpu['cores']}")
    print(f"  {CYAN}🐏 RAM:{RESET}       {ram_gb} GB")
    if gpu["available"]:
        print(f"  {GREEN}🎮 GPU:{RESET}       {gpu['name']} ({gpu['vram_gb']} GB VRAM)")
    else:
        print(f"  {DIM}🎮 GPU:{RESET}       {DIM}Not detected (CPU-only mode){RESET}")
    print(f"  {CYAN}💾 Disk Free:{RESET}  {disk_free} GB")
    print(f"  {BOLD}{'─' * 50}{RESET}")

    # ── Step 2: Get Installed Models ──
    installed = _get_installed_models()
    if installed:
        print(f"\n  {GREEN}📦 Installed Models:{RESET}")
        for m in installed:
            print(f"     • {m}")

    # ── Step 3: Recommend Models ──
    compatible = _recommend_models(ram_gb, cpu["cores"], gpu["vram_gb"], disk_free)

    if not compatible:
        print(f"\n{RED}[!] Your system doesn't meet minimum requirements for any model.{RESET}")
        print(f"    Minimum: 2 GB RAM, 1 GB free disk space.")
        input(f"{DIM}Press Enter to continue...{RESET}")
        return

    print(f"\n{BOLD}  🏆 RECOMMENDED MODELS (best for your system first):{RESET}\n")
    print(f"  {BOLD}{'#':>3}  {'Model':<25} {'Params':<10} {'Size':<8} {'Best For'}{RESET}")
    print(f"  {'─' * 85}")

    for i, model in enumerate(compatible, 1):
        is_installed = "✅" if model["name"] in installed else "  "
        print(f"  {CYAN}{i:>3}{RESET}  {model['name']:<25} {model['params']:<10} {model['size_gb']:.1f} GB  {is_installed} {DIM}{model['best_for']}{RESET}")

    # Highlight the top recommendation
    top = compatible[0]
    print(f"\n  {GREEN}{BOLD}⭐ TOP RECOMMENDATION: {top['name']}{RESET}")
    print(f"     {top['description']}")

    # ── Step 4: User Selection ──
    print(f"\n  {DIM}Enter the number of the model you want, or 'back' to cancel.{RESET}")
    choice = input(f"\n{CYAN}  Select model [{top['name']}]: {RESET}").strip()

    if choice.lower() in ("back", "b", ""):
        # Default to top recommendation if user just presses Enter
        if choice == "":
            selected = top
        else:
            return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(compatible):
                selected = compatible[idx]
            else:
                print(f"{RED}[!] Invalid selection.{RESET}")
                return
        except ValueError:
            print(f"{RED}[!] Enter a number or 'back'.{RESET}")
            return

    # ── Step 5: Pull the Model ──
    print(f"\n{YELLOW}[⬇️] Setting up {selected['name']}...{RESET}")

    if selected["name"] in installed:
        print(f"{GREEN}[✓] Model already installed!{RESET}")
    else:
        print(f"{YELLOW}[⬇️] Downloading {selected['name']} ({selected['size_gb']} GB)...{RESET}")
        print(f"{DIM}    This may take a few minutes depending on your internet speed.{RESET}")
        try:
            subprocess.run(["ollama", "pull", selected["name"]], timeout=1200)
            print(f"{GREEN}[✓] Model downloaded successfully!{RESET}")
        except subprocess.TimeoutExpired:
            print(f"{RED}[!] Download timed out. Try: ollama pull {selected['name']}{RESET}")
            return
        except FileNotFoundError:
            print(f"{RED}[!] Ollama not found! Install it: curl -fsSL https://ollama.com/install.sh | sh{RESET}")
            return
        except Exception as e:
            print(f"{RED}[!] Error pulling model: {e}{RESET}")
            return

    # ── Step 6: Save Configuration ──
    save_ollama_config(selected["name"], specs)
    print(f"\n{GREEN}{BOLD}[✓] Brain configured! CyberSim will now use: {selected['name']}{RESET}")
    print(f"    {DIM}Config saved to: {CONFIG_FILE}{RESET}")
    input(f"\n{DIM}Press Enter to continue...{RESET}")
