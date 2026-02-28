#!/bin/bash
# Start SSH
/usr/sbin/sshd

# Determine which binary to serve
DIFF="${DIFFICULTY:-easy}"
BIN="vuln_easy"

if [ "$DIFF" = "normal" ]; then
    BIN="vuln_normal"
elif [ "$DIFF" = "hard" ]; then
    BIN="vuln_hard"
    # Enable ASLR for hard mode
    echo 2 > /proc/sys/kernel/randomize_va_space 2>/dev/null || true
fi

echo "[*] BOF Lab - $DIFF mode - serving $BIN on port 9999"

# Serve the binary on port 9999 using socat (restarts after each connection)
while true; do
    socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/opt/bof/$BIN,pty,stderr,setsid 2>/dev/null
    sleep 1
done
