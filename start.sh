#!/bin/bash
# CyberSim Launcher Script
# Run this to start the game: bash start.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export PATH="$HOME/.local/bin:$PATH"

echo "╔══════════════════════════════════════╗"
echo "║        CyberSim Launcher             ║"
echo "╚══════════════════════════════════════╝"

# ── 1. Check Docker ────────────────────────────────────────────────────────────
if ! docker info > /dev/null 2>&1; then
    echo "[!] Docker is not running. Starting Docker..."
    sudo service docker start
    sleep 2
fi
echo "[✓] Docker is running."

# ── 2. Check Ollama ────────────────────────────────────────────────────────────
if ! pgrep -x "ollama" > /dev/null; then
    echo "[*] Starting Ollama AI..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi
echo "[✓] Ollama is running."

# ── 3. Pull AI model if needed ─────────────────────────────────────────────────
if ! ollama list 2>/dev/null | grep -qw "llama3.2:1b"; then
    echo "[*] Pulling ultra-fast Llama 3.2 (1B) model (~1GB, one-time download)..."
    ollama pull llama3.2:1b
    # Ensure mentor is hooked to the right model
    sed -i 's/MENTOR_MODEL = .*/MENTOR_MODEL = "llama3.2:1b"  # 1B parameter model: insanely fast on CPU, highly responsive/' core/mentor.py
fi
echo "[✓] AI model ready."

# ── 4. Python venv setup ───────────────────────────────────────────────────────
if [ ! -d ".venv" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt -q
echo "[✓] Python environment ready."

# ── 5. Launch Gamemaster ───────────────────────────────────────────────────────
echo ""
python3 gamemaster.py
