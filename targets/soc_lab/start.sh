#!/bin/bash

FLAG="${CYBERSIM_FLAG:-FLAG{soc_default_flag}}"

# 1. Auth.log - Brute force attack followed by successful login
cat > /var/log/auth.log << 'AUTHLOG'
Feb 25 08:00:01 webserver sshd[2001]: Failed password for root from 10.13.37.100 port 42001 ssh2
Feb 25 08:00:02 webserver sshd[2002]: Failed password for root from 10.13.37.100 port 42002 ssh2
Feb 25 08:00:03 webserver sshd[2003]: Failed password for root from 10.13.37.100 port 42003 ssh2
Feb 25 08:00:04 webserver sshd[2004]: Failed password for root from 10.13.37.100 port 42004 ssh2
Feb 25 08:00:05 webserver sshd[2005]: Failed password for root from 10.13.37.100 port 42005 ssh2
Feb 25 08:00:06 webserver sshd[2006]: Failed password for admin from 10.13.37.100 port 42006 ssh2
Feb 25 08:00:07 webserver sshd[2007]: Failed password for admin from 10.13.37.100 port 42007 ssh2
Feb 25 08:00:08 webserver sshd[2008]: Failed password for admin from 10.13.37.100 port 42008 ssh2
Feb 25 08:00:10 webserver sshd[2010]: Accepted password for admin from 10.13.37.100 port 42010 ssh2
Feb 25 08:00:10 webserver sshd[2010]: pam_unix(sshd:session): session opened for user admin
Feb 25 08:01:15 webserver sudo[3001]:    admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/bash
Feb 25 08:01:15 webserver sudo[3001]: pam_unix(sudo:session): session opened for user root
Feb 25 08:02:00 webserver sshd[3100]: Received disconnect from 10.13.37.100 port 42010:11: disconnected by user
Feb 25 09:00:01 webserver sshd[4001]: Accepted publickey for deploy from 192.168.1.5 port 50001 ssh2
Feb 25 09:15:00 webserver sshd[4001]: pam_unix(sshd:session): session closed for user deploy
Feb 25 10:30:00 webserver sshd[5001]: Accepted password for jdoe from 192.168.1.50 port 51001 ssh2
Feb 25 14:00:00 webserver sshd[5001]: pam_unix(sshd:session): session closed for user jdoe
AUTHLOG

# 2. Web access log - SQL injection attempts
cat > /var/log/soc/web_access.log << 'WEBLOG'
10.13.37.100 - - [25/Feb/2026:08:05:00 +0000] "GET / HTTP/1.1" 200 1234
10.13.37.100 - - [25/Feb/2026:08:05:10 +0000] "GET /login HTTP/1.1" 200 567
10.13.37.100 - - [25/Feb/2026:08:05:15 +0000] "POST /login HTTP/1.1" 302 0
10.13.37.100 - - [25/Feb/2026:08:06:00 +0000] "GET /admin HTTP/1.1" 403 213
10.13.37.100 - - [25/Feb/2026:08:06:05 +0000] "GET /admin?id=1 HTTP/1.1" 200 456
10.13.37.100 - - [25/Feb/2026:08:06:10 +0000] "GET /admin?id=1' OR '1'='1 HTTP/1.1" 200 8901
10.13.37.100 - - [25/Feb/2026:08:06:15 +0000] "GET /admin?id=1' UNION SELECT username,password FROM users-- HTTP/1.1" 200 2345
10.13.37.100 - - [25/Feb/2026:08:06:20 +0000] "GET /admin?id=1' UNION SELECT table_name,null FROM information_schema.tables-- HTTP/1.1" 200 5678
10.13.37.100 - - [25/Feb/2026:08:07:00 +0000] "GET /uploads/shell.php HTTP/1.1" 200 45
10.13.37.100 - - [25/Feb/2026:08:07:05 +0000] "GET /uploads/shell.php?cmd=whoami HTTP/1.1" 200 12
10.13.37.100 - - [25/Feb/2026:08:07:10 +0000] "GET /uploads/shell.php?cmd=cat%20/etc/passwd HTTP/1.1" 200 1500
192.168.1.10 - - [25/Feb/2026:09:00:00 +0000] "GET / HTTP/1.1" 200 1234
192.168.1.10 - - [25/Feb/2026:09:00:05 +0000] "GET /products HTTP/1.1" 200 3456
192.168.1.15 - - [25/Feb/2026:10:00:00 +0000] "GET / HTTP/1.1" 200 1234
WEBLOG

# 3. Firewall log
cat > /var/log/firewall/fw.log << 'FWLOG'
Feb 25 08:00:00 firewall ALLOW TCP 192.168.1.5 -> 172.16.0.10:443 (HTTPS)
Feb 25 08:05:00 firewall ALLOW TCP 10.13.37.100 -> 172.16.0.10:22 (SSH)
Feb 25 08:07:30 firewall ALLOW TCP 10.13.37.100 -> 172.16.0.10:80 (HTTP)
Feb 25 08:08:00 firewall ALLOW TCP 172.16.0.10 -> 10.13.37.100:4444 (REVERSE SHELL)
Feb 25 08:10:00 firewall ALLOW TCP 172.16.0.10 -> 185.141.25.99:443 (C2 - SUSPICIOUS)
Feb 25 08:10:30 firewall ALLOW TCP 172.16.0.10 -> 185.141.25.99:443 (1.2MB UPLOAD)
Feb 25 08:11:00 firewall ALLOW TCP 172.16.0.10 -> 185.141.25.99:443 (3.5MB UPLOAD)
Feb 25 08:11:30 firewall ALLOW TCP 172.16.0.10 -> 185.141.25.99:443 (8.1MB UPLOAD)
Feb 25 08:12:00 firewall DENY TCP 172.16.0.10 -> 185.141.25.99:443 (BLOCKED BY IDS)
Feb 25 09:00:00 firewall ALLOW TCP 192.168.1.50 -> 172.16.0.10:443 (HTTPS)
Feb 25 10:00:00 firewall ALLOW TCP 192.168.1.15 -> 172.16.0.10:80 (HTTP)
FWLOG

# 4. IDS alerts
cat > /var/log/ids/alerts.log << 'IDSLOG'
[**] [1:2001219:9] ET SCAN Nmap Scripting Engine User-Agent Detected [**]
[Classification: Web Application Attack] [Priority: 2]
02/25-08:04:50 10.13.37.100:45678 -> 172.16.0.10:80

[**] [1:2006546:3] ET WEB_SERVER SQL Injection Attempt [**]
[Classification: Web Application Attack] [Priority: 1]
02/25-08:06:10 10.13.37.100:45690 -> 172.16.0.10:80

[**] [1:2010935:2] ET WEB_SERVER WebShell Access Detected [**]
[Classification: A Network Trojan was detected] [Priority: 1]
02/25-08:07:00 10.13.37.100:45700 -> 172.16.0.10:80

[**] [1:2016978:1] ET POLICY Outbound Connection to External IP on Non-Standard Port [**]
[Classification: Potential Corporate Privacy Violation] [Priority: 1]
02/25-08:08:00 172.16.0.10:54321 -> 10.13.37.100:4444

[**] [1:2024312:1] ET EXFILTRATION Large Outbound Data Transfer [**]
[Classification: Data Exfiltration] [Priority: 1]
02/25-08:10:00 172.16.0.10:55432 -> 185.141.25.99:443
IDSLOG

# 5. Plant the flag
cat > /opt/soc/investigation_template.txt << TEMPLATE
=== SOC INCIDENT REPORT ===
Case ID: SOC-2026-0225
Analyst: [YOUR NAME]

ATTACKER IP: [FIND THIS]
ATTACK VECTOR: [IDENTIFY THIS]

When you have completed the analysis, the flag is: $FLAG
TEMPLATE
chmod 600 /opt/soc/investigation_template.txt

cat > /opt/soc/README.txt << 'README'
=== SOC ANALYST CHALLENGE ===

Analyze security logs and answer these questions:

1. What IP conducted the brute-force? (/var/log/auth.log)
2. What web attack was used? (/var/log/soc/web_access.log)
3. Was there a reverse shell? To what port? (/var/log/firewall/fw.log)
4. How much data was exfiltrated? (/var/log/firewall/fw.log)
5. What IDS alerts triggered? (/var/log/ids/alerts.log)

Tools: grep, awk, sort, uniq, wc, cut

After investigation, check: /opt/soc/investigation_template.txt
README

/usr/sbin/sshd

while true; do
    echo "SOC Lab Active. Analyze the logs in /var/log/" | nc -l -p 9999 -w 1 2>/dev/null
done &

echo "[*] SOC Lab started - Log analysis challenge active"
tail -f /dev/null
