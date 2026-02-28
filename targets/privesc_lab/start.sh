#!/bin/bash

FLAG="${CYBERSIM_FLAG:-FLAG{privesc_default}}"
echo "$FLAG" > /root/flag.txt
chmod 600 /root/flag.txt

/usr/sbin/sshd
cron

echo "[*] Privilege Escalation Lab started"
echo "[*] Login as 'player' / 'player123'"
echo "[*] Goal: Escalate to root and read /root/flag.txt"
tail -f /dev/null
