"""
CyberSim AI Defender - The Blue Team Agent
Monitors Docker container logs in real-time and responds to attacks.
Active in 'normal' (passive) and 'hard' (aggressive) modes.
"""
import subprocess
import threading
import time
import re
import os
from datetime import datetime
from collections import deque

# --- Detection Signatures ---
NMAP_SIGNATURES = [
    r"Nmap scan report",
    r"SYN Stealth Scan",
    r"nmap",
    r"masscan",
]
BRUTE_FORCE_SIGNATURES = [
    r"Failed password",
    r"authentication failure",
    r"Invalid user",
]
SQLI_SIGNATURES = [
    r"' OR '",
    r"UNION SELECT",
    r"1=1",
    r"--",
    r"sqlmap",
]
WEB_SCAN_SIGNATURES = [
    r"nikto",
    r"dirbuster",
    r"gobuster",
    r"wfuzz",
    r"User-Agent: Mozilla.*sqlmap",
]

BLOCK_DURATION = 30  # seconds for normal mode
HARD_BLOCK_DURATION = 120  # seconds for hard mode

class AIDefender:
    def __init__(self, container_name: str, difficulty: str, mentor_callback=None, config=None):
        self.container_name = container_name
        self.difficulty = difficulty
        self.mentor_callback = mentor_callback  # Called when user is blocked
        self.config = config or {}
        self.blocked_ips = {}
        self.strike_counters = {}  # {ip: deque([timestamps], maxlen=10)}
        self.running = False
        self.log_buffer = []
        self._thread = None

    def start(self):
        """Start the defender daemon in a background thread."""
        self.running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        print(f"\n[🛡️  DEFENDER] AI Blue Team Agent is ACTIVE ({self.difficulty.upper()} mode)")

    def stop(self):
        """Stop the defender."""
        self.running = False
        print("\n[🛡️  DEFENDER] AI Blue Team Agent deactivated.")

    def _monitor_loop(self):
        """Continuously reads Docker container logs."""
        try:
            proc = subprocess.Popen(
                ["docker", "logs", "-f", "--tail", "0", self.container_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            while self.running:
                line = proc.stdout.readline()
                if not line:
                    break  # EOF reached (container stopped or docker logs exited)
                
                self.log_buffer.append(line.strip())
                self._analyze(line.strip())
            proc.terminate()
        except Exception as e:
            print(f"[!] Defender monitor error: {e}")

    def _analyze(self, log_line: str):
        """Analyze a single log line for attack signatures."""
        attack_type = None
        attacker_ip = self._extract_ip(log_line)

        for sig in NMAP_SIGNATURES:
            if re.search(sig, log_line, re.IGNORECASE):
                # Rate-limit detection: allow stealthy/slow scans
                if attacker_ip not in self.strike_counters:
                    self.strike_counters[attacker_ip] = deque(maxlen=15)
                
                now = time.time()
                self.strike_counters[attacker_ip].append(now)
                
                # If we saw 15 packets in the last 5 seconds, it's aggressive
                if len(self.strike_counters[attacker_ip]) == 15:
                    oldest = self.strike_counters[attacker_ip][0]
                    if now - oldest < 5.0:
                        attack_type = "Port Scan (Nmap/Masscan)"
                        self.strike_counters[attacker_ip].clear()  # Reset strikes after triggering
                break

        if not attack_type:
            for sig in BRUTE_FORCE_SIGNATURES:
                if re.search(sig, log_line, re.IGNORECASE):
                    attack_type = "Brute Force (SSH/Login)"
                    break
        if not attack_type:
            for sig in SQLI_SIGNATURES:
                if re.search(sig, log_line, re.IGNORECASE):
                    attack_type = "SQL Injection"
                    break
        if not attack_type:
            for sig in WEB_SCAN_SIGNATURES:
                if re.search(sig, log_line, re.IGNORECASE):
                    attack_type = "Web Directory Scan"
                    break

        if attack_type:
            self._respond(attack_type, attacker_ip, log_line)

    def _respond(self, attack_type: str, attacker_ip: str, log_line: str):
        """Execute defensive response based on difficulty."""
        # Check if IP is already blocked to prevent log spam/fluctuation
        if attacker_ip and attacker_ip in self.blocked_ips:
            if time.time() < self.blocked_ips[attacker_ip]:
                return  # Skip response, IP is already actively blocked

        # Remove the extra DETECTED header, just print the block directly later
        
        block_duration = self.config.get("block_duration", BLOCK_DURATION if self.difficulty == "normal" else HARD_BLOCK_DURATION)

        if self.difficulty == "normal":
            # Block only on very noisy scans
            if "Nmap" in attack_type and attacker_ip:
                self._block_ip(attacker_ip, block_duration)

        elif self.difficulty == "hard":
            if attacker_ip:
                self._block_ip(attacker_ip, block_duration)
            
            if self.config.get("kill_sessions", True):
                self._kill_sessions()
            if self.config.get("patch_vulns", True):
                self._patch_vulnerability(attack_type)

            # Trigger Mentor to give evasion advice
            if self.mentor_callback:
                defender_log = "\n".join(self.log_buffer[-20:])
                advice = self.mentor_callback(defender_log, attack_type)
                print(f"\n[🧠 MENTOR - EVASION ADVICE]:\n{advice}\n")

    def _extract_ip(self, log_line: str) -> str:
        """Extract IP address from a log line."""
        match = re.search(r'\b(\d{1,3}\.){3}\d{1,3}\b', log_line)
        return match.group(0) if match else "172.20.0.1"  # Default attacker IP

    def _block_ip(self, ip: str, duration: int):
        """Block an IP using iptables inside the Docker container."""
        print(f"\n[🛡️  DEFENDER] 🚫 Blocking attacker {ip} for {duration} seconds via iptables...")
        print(f"[🛡️  DEFENDER] ⏳ Wait {duration}s for the IP block to be lifted so you can test again.")
        try:
            # Add block rule inside the container, with fallback for Alpine/nftables
            subprocess.run(
                ["docker", "exec", self.container_name,
                 "sh", "-c", f"iptables -A INPUT -s {ip} -j DROP || iptables-nft -A INPUT -s {ip} -j DROP"],
                capture_output=True, timeout=5
            )
            self.blocked_ips[ip] = time.time() + duration
            # Schedule unblock
            threading.Timer(duration, self._unblock_ip, args=[ip]).start()
        except Exception as e:
            print(f"[!] Could not block IP: {e}")

    def _unblock_ip(self, ip: str):
        """Remove the iptables block after duration expires."""
        try:
            subprocess.run(
                ["docker", "exec", self.container_name,
                 "sh", "-c", f"iptables -D INPUT -s {ip} -j DROP || iptables-nft -D INPUT -s {ip} -j DROP"],
                capture_output=True, timeout=5
            )
            print(f"\n[🛡️  DEFENDER] 🟢 IP {ip} has been UNBLOCKED. You may resume attacks.")
            self.blocked_ips.pop(ip, None)
        except Exception as e:
            print(f"[!] Could not unblock IP: {e}")

    def _kill_sessions(self):
        """Kill all active SSH/netcat sessions inside the container."""
        print("[🛡️  DEFENDER] Killing active sessions...")
        try:
            subprocess.run(
                ["docker", "exec", self.container_name,
                 "killall", "-9", "sshd"],
                capture_output=True, timeout=5
            )
            subprocess.run(
                ["docker", "exec", self.container_name,
                 "killall", "-9", "nc"],
                capture_output=True, timeout=5
            )
        except Exception as e:
            print(f"[!] Could not kill sessions: {e}")

    def _patch_vulnerability(self, attack_type: str):
        """Simulate a SysAdmin patching the vulnerability being attacked."""
        print(f"[🛡️  DEFENDER] SysAdmin woke up! Patching: {attack_type}...")
        try:
            if "SSH" in attack_type or "Brute" in attack_type:
                # Change the SSH password
                subprocess.run(
                    ["docker", "exec", self.container_name,
                     "bash", "-c", "echo 'root:$(openssl rand -base64 12)' | chpasswd"],
                    capture_output=True, timeout=5
                )
                print("[🛡️  DEFENDER] SSH password changed! Find another way in.")
            elif "SQL" in attack_type:
                # Restart the web app with WAF enabled (simulated)
                subprocess.run(
                    ["docker", "exec", self.container_name,
                     "bash", "-c", "touch /var/www/html/.waf_enabled"],
                    capture_output=True, timeout=5
                )
                print("[🛡️  DEFENDER] WAF enabled on web app!")
        except Exception as e:
            print(f"[!] Patch failed: {e}")
