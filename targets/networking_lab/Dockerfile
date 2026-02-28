FROM alpine:3.18

RUN apk add --no-cache \
    openssh \
    netcat-openbsd \
    bash \
    curl \
    iptables \
    tcpdump

# Setup SSH
RUN ssh-keygen -A && \
    echo "root:toor" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create the hidden service on port 9999
# Reads CYBERSIM_FLAG env var at runtime (set via docker-compose)
RUN printf '#!/bin/sh\nwhile true; do\n  echo "Welcome to the hidden service! ${CYBERSIM_FLAG}" | nc -l -p 9999\ndone\n' > /usr/local/bin/flag_service.sh && \
    chmod +x /usr/local/bin/flag_service.sh

# Startup script
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'syslogd -O /dev/stdout &' >> /start.sh && \
    echo '/usr/sbin/sshd' >> /start.sh && \
    echo '/usr/local/bin/flag_service.sh &' >> /start.sh && \
    echo 'tcpdump -i eth0 -l -nn "tcp[tcpflags] == tcp-syn" 2>/dev/null | while read line; do echo "Nmap scan report: $line"; done &' >> /start.sh && \
    echo 'tail -f /dev/null' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 22 9999

CMD ["/start.sh"]
