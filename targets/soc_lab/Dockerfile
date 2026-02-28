FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server bash python3 python3-pip curl jq gawk \
    netcat-openbsd tcpdump rsyslog \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/sshd && \
    echo "root:toor" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN mkdir -p /var/log/soc /var/log/ids /var/log/firewall /opt/soc/pcaps

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 22 9999
CMD ["/start.sh"]
