FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server sudo cron nano vim less nmap python3 bash curl \
    netcat-traditional gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/sshd && \
    echo "root:toor" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN useradd -m -s /bin/bash player && echo "player:player123" | chpasswd

# PrivEsc Vector 1: SUID Binary (find)
RUN cp /usr/bin/find /usr/bin/find_suid && chmod u+s /usr/bin/find_suid

# PrivEsc Vector 2: Sudo Misconfiguration
RUN echo "player ALL=(root) NOPASSWD: /usr/bin/less" >> /etc/sudoers
RUN echo "player ALL=(root) NOPASSWD: /usr/bin/vim" >> /etc/sudoers

# PrivEsc Vector 3: Weak Cron Job
RUN echo "* * * * * root /usr/local/bin/backup.sh >/dev/null 2>&1" > /etc/cron.d/weak_cron
RUN printf '#!/bin/bash\ntar -czf /var/backups/www.tgz /var/www/html/* 2>/dev/null\n' > /usr/local/bin/backup.sh && \
    chmod 777 /usr/local/bin/backup.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 22
CMD ["/start.sh"]
