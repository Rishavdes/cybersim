"""
CyberSim Monthly Quiz Server
Serves a beautiful timed quiz in the browser.
Runs on localhost:5555, auto-closes after submission.
"""
import json
import os
import time
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# ─── ANSI Colors ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

QUIZ_PORT = 5555
quiz_result = {"score": 0, "total": 0, "submitted": False, "time_taken": 0}
quiz_questions = []
quiz_time_limit = 900  # 15 minutes default


def _build_quiz_html(questions: list, time_limit: int, player_name: str) -> str:
    """Generate the full quiz HTML page."""
    q_html = ""
    for i, q in enumerate(questions):
        options_html = ""
        for opt in q["options"]:
            options_html += f'''
                <label class="option">
                    <input type="radio" name="q{i}" value="{opt}" required>
                    <span class="option-text">{opt}</span>
                </label>'''
        
        q_html += f'''
            <div class="question-card" id="qcard-{i}">
                <div class="question-number">Question {i+1}</div>
                <div class="question-text">{q["q"]}</div>
                <div class="options">{options_html}</div>
            </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberSim Monthly Knowledge Test</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 30%, #0d1b2a 70%, #000000 100%);
            color: #e0e0e0;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        .cyber-grid {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(0, 255, 136, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 136, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }}

        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid rgba(0, 255, 136, 0.3);
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            color: #00ff88;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
            letter-spacing: 2px;
        }}

        .header .subtitle {{
            color: #888;
            margin-top: 8px;
            font-size: 0.9rem;
        }}

        .timer-bar {{
            position: sticky;
            top: 0;
            background: rgba(10, 14, 39, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 255, 136, 0.2);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
            border-radius: 0 0 10px 10px;
        }}

        .timer {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: #00ff88;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}

        .timer.warning {{ color: #ffaa00; text-shadow: 0 0 10px rgba(255, 170, 0, 0.5); }}
        .timer.danger {{ color: #ff4444; text-shadow: 0 0 10px rgba(255, 68, 68, 0.5); animation: pulse 1s infinite; }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .progress-info {{
            font-size: 0.85rem;
            color: #888;
        }}

        .question-card {{
            background: rgba(20, 25, 52, 0.8);
            border: 1px solid rgba(0, 255, 136, 0.15);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}

        .question-card:hover {{
            border-color: rgba(0, 255, 136, 0.4);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
        }}

        .question-number {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #00ff88;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }}

        .question-text {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 20px;
            line-height: 1.5;
        }}

        .options {{ display: flex; flex-direction: column; gap: 10px; }}

        .option {{
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: rgba(0, 255, 136, 0.03);
            border: 1px solid rgba(0, 255, 136, 0.1);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .option:hover {{
            background: rgba(0, 255, 136, 0.08);
            border-color: rgba(0, 255, 136, 0.3);
        }}

        .option input[type="radio"] {{ margin-right: 12px; accent-color: #00ff88; }}

        .option-text {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }}

        .submit-section {{
            text-align: center;
            padding: 30px 0;
        }}

        .submit-btn {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
            font-weight: 700;
            color: #000;
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            border: none;
            padding: 15px 50px;
            border-radius: 8px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 3px;
            transition: all 0.3s ease;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        }}

        .submit-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 50px rgba(0, 255, 136, 0.5);
        }}

        .result-overlay {{
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}

        .result-card {{
            background: linear-gradient(135deg, #0a0e27, #1a1a3e);
            border: 2px solid #00ff88;
            border-radius: 20px;
            padding: 50px;
            text-align: center;
            max-width: 500px;
            box-shadow: 0 0 60px rgba(0, 255, 136, 0.3);
        }}

        .score-text {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 4rem;
            font-weight: 700;
            color: #00ff88;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        }}

        .grade {{ font-size: 1.5rem; margin-top: 10px; }}
        .close-msg {{ color: #888; margin-top: 20px; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="cyber-grid"></div>
    <div class="container">
        <div class="header">
            <h1>⚡ MONTHLY KNOWLEDGE TEST</h1>
            <div class="subtitle">Operator: {player_name} | CyberSim Assessment Engine</div>
        </div>

        <div class="timer-bar">
            <div class="timer" id="timer">15:00</div>
            <div class="progress-info" id="progress">0 / {len(questions)} answered</div>
        </div>

        <form id="quizForm" action="/submit" method="POST">
            {q_html}
            <div class="submit-section">
                <button type="submit" class="submit-btn">⚡ SUBMIT ANSWERS ⚡</button>
            </div>
        </form>
    </div>

    <div class="result-overlay" id="resultOverlay">
        <div class="result-card">
            <div class="score-text" id="scoreText"></div>
            <div class="grade" id="gradeText"></div>
            <div class="close-msg">This window will close automatically...</div>
        </div>
    </div>

    <script>
        // Timer
        let timeLeft = {time_limit};
        const timerEl = document.getElementById('timer');
        
        const timerInterval = setInterval(() => {{
            timeLeft--;
            const mins = Math.floor(timeLeft / 60);
            const secs = timeLeft % 60;
            timerEl.textContent = mins.toString().padStart(2, '0') + ':' + secs.toString().padStart(2, '0');
            
            if (timeLeft <= 60) timerEl.className = 'timer danger';
            else if (timeLeft <= 180) timerEl.className = 'timer warning';
            
            if (timeLeft <= 0) {{
                clearInterval(timerInterval);
                document.getElementById('quizForm').submit();
            }}
        }}, 1000);

        // Track answered
        document.querySelectorAll('input[type="radio"]').forEach(r => {{
            r.addEventListener('change', () => {{
                const answered = new Set();
                document.querySelectorAll('input[type="radio"]:checked').forEach(c => {{
                    answered.add(c.name);
                }});
                document.getElementById('progress').textContent = answered.size + ' / {len(questions)} answered';
            }});
        }});

        // Handle submit
        document.getElementById('quizForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            clearInterval(timerInterval);
            
            const formData = new FormData(e.target);
            const response = await fetch('/submit', {{
                method: 'POST',
                body: formData
            }});
            const result = await response.json();
            
            document.getElementById('scoreText').textContent = result.score + '/' + result.total;
            const pct = (result.score / result.total) * 100;
            let grade = '';
            if (pct >= 90) grade = '🏆 ELITE OPERATOR';
            else if (pct >= 70) grade = '✅ MISSION PASSED';
            else if (pct >= 50) grade = '⚠️ NEEDS IMPROVEMENT';
            else grade = '❌ STUDY MORE!';
            document.getElementById('gradeText').textContent = grade;
            
            const overlay = document.getElementById('resultOverlay');
            overlay.style.display = 'flex';
            
            setTimeout(() => {{ window.close(); }}, 5000);
        }});
    </script>
</body>
</html>'''


class QuizHandler(BaseHTTPRequestHandler):
    """HTTP handler for the quiz server."""

    def log_message(self, format, *args):
        pass  # Suppress server logs

    def do_GET(self):
        global quiz_questions, quiz_time_limit
        html = _build_quiz_html(quiz_questions, quiz_time_limit, "Operator")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):
        global quiz_result, quiz_questions
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        answers = parse_qs(body)

        score = 0
        total = len(quiz_questions)
        for i, q in enumerate(quiz_questions):
            user_ans = answers.get(f"q{i}", [""])[0]
            if user_ans == q["answer"]:
                score += 1

        quiz_result["score"] = score
        quiz_result["total"] = total
        quiz_result["submitted"] = True

        result_json = json.dumps({"score": score, "total": total})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(result_json.encode())

        # Schedule server shutdown
        threading.Thread(target=self._shutdown_after, daemon=True).start()

    def _shutdown_after(self):
        time.sleep(6)
        self.server.shutdown()


def run_monthly_quiz(state: dict) -> dict:
    """Launch the browser-based monthly quiz and return results."""
    global quiz_questions, quiz_result, quiz_time_limit

    from core.quiz_generator import generate_quiz

    quiz_questions = generate_quiz(state, num_questions=10)
    quiz_time_limit = 900  # 15 minutes
    quiz_result = {"score": 0, "total": 0, "submitted": False}

    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║         📝 MONTHLY KNOWLEDGE TEST                           ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n{CYAN}[⚡] Launching quiz in your browser...{RESET}")
    print(f"{DIM}   10 questions | 15 minute time limit | Topics from your completed missions{RESET}")
    print(f"{YELLOW}   Complete the quiz in the browser. Results will appear here.{RESET}\n")

    server = HTTPServer(("127.0.0.1", QUIZ_PORT), QuizHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    webbrowser.open(f"http://127.0.0.1:{QUIZ_PORT}")

    # Wait for submission
    while not quiz_result["submitted"]:
        time.sleep(1)

    server.shutdown()
    server_thread.join(timeout=5)

    # Display results in terminal
    score = quiz_result["score"]
    total = quiz_result["total"]
    pct = int((score / total) * 100) if total > 0 else 0

    print(f"\n{BOLD}{'═' * 50}{RESET}")
    if pct >= 90:
        print(f"{GREEN}{BOLD}  🏆 ELITE OPERATOR! Score: {score}/{total} ({pct}%){RESET}")
        xp_bonus = 200
    elif pct >= 70:
        print(f"{GREEN}{BOLD}  ✅ MISSION PASSED! Score: {score}/{total} ({pct}%){RESET}")
        xp_bonus = 100
    elif pct >= 50:
        print(f"{YELLOW}{BOLD}  ⚠️  NEEDS IMPROVEMENT. Score: {score}/{total} ({pct}%){RESET}")
        xp_bonus = 50
    else:
        print(f"{RED}{BOLD}  ❌ STUDY MORE! Score: {score}/{total} ({pct}%){RESET}")
        xp_bonus = 25
    
    print(f"  {CYAN}+{xp_bonus} XP Bonus!{RESET}")
    print(f"{BOLD}{'═' * 50}{RESET}")

    return {"score": score, "total": total, "xp_bonus": xp_bonus}
