BONUS_QUESTIONS = [
    {
        "title": "Stealth Scan Challenge",
        "description": "Can you scan the target using only a SYN scan (-sS) with timing T1 to avoid detection?",
        "hint": "nmap -sS -T1 -p- <TARGET_IP>",
    },
    {
        "title": "One-Liner Wizard",
        "description": "Find all files owned by root with SUID bit set in /usr using a single command.",
        "hint": "find /usr -user root -perm -4000 2>/dev/null",
    },
    {
        "title": "Banner Grabber",
        "description": "Write a Python script using the socket library to grab the banner from port 22 of localhost.",
        "hint": "s=socket.socket(); s.connect(('localhost',22)); print(s.recv(1024))",
    },
    {
        "title": "GTFOBins Lookup",
        "description": "If 'vim' has SUID, what GTFOBins command would give you a root shell?",
        "hint": "vim -c ':!/bin/sh'",
    },
    {
        "title": "Hash Identifier",
        "description": "What type of hash is this: 5f4dcc3b5aa765d61d8327deb882cf99?",
        "hint": "It's MD5. The plaintext is 'password'.",
    },
    {
        "title": "Blind SQLi",
        "description": "What payload would you use for a time-based blind SQLi test on a login form?",
        "hint": "' OR IF(1=1, SLEEP(5), 0)-- -",
    },
    {
        "title": "Directory Brute Forcing",
        "description": "What gobuster command would you use to aggressively enumerate directories on http://10.10.10.10 with the common.txt wordlist?",
        "hint": "gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -t 50",
    },
    {
        "title": "John the Ripper",
        "description": "You dumped an /etc/shadow file into 'hashes.txt'. How do you crack it using john and rockyou.txt?",
        "hint": "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
    },
    {
        "title": "Reverse Shell Upgrading",
        "description": "You just caught a netcat reverse shell. What python one-liner upgrades it to a fully interactive TTY?",
        "hint": "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
    },
    {
        "title": "SSH Port Forwarding",
        "description": "How do you use SSH to forward local port 8080 to remote internal IP 192.168.1.5:80 through a pivot machine at 10.10.10.10?",
        "hint": "ssh -L 8080:192.168.1.5:80 user@10.10.10.10",
    },
    {
        "title": "Netcat Listener",
        "description": "What is the standard command to set up a listening netcat server on port 4444 to catch a reverse shell?",
        "hint": "nc -lvnp 4444",
    },
    {
        "title": "Nmap OS Detection",
        "description": "What Nmap flag enables Operating System (OS) fingerprinting?",
        "hint": "-O",
    },
    {
        "title": "Linux Kernel Exploit Check",
        "description": "What command quickly prints the Linux kernel version so you can search for exploits like DirtyCOW?",
        "hint": "uname -a",
    },
    {
        "title": "File Transfer with Python",
        "description": "How do you quickly host a directory of files over HTTP on port 8000 using Python 3?",
        "hint": "python3 -m http.server 8000",
    },
    {
        "title": "XSS Payload",
        "description": "What is the most basic Cross-Site Scripting (XSS) payload to trigger a javascript alert pop-up?",
        "hint": "<script>alert(1)</script>",
    }
]
