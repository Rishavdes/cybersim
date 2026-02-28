FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    samba \
    samba-dsdb-modules \
    samba-vfs-modules \
    smbclient \
    ldap-utils \
    krb5-user \
    openssh-server \
    bash \
    netcat-openbsd \
    python3 \
    python3-pip \
    curl \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# SSH Setup
RUN mkdir -p /run/sshd && \
    echo "root:toor" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create simulated AD users and shares
RUN mkdir -p /srv/samba/shared /srv/samba/admin_only /srv/samba/it_dept

RUN useradd -m -s /bin/bash jdoe && echo "jdoe:Welcome123" | chpasswd && \
    useradd -m -s /bin/bash svc_backup && echo "svc_backup:Backup2024!" | chpasswd && \
    useradd -m -s /bin/bash admin && echo "admin:P@ssw0rd2024" | chpasswd && \
    useradd -m -s /bin/bash hr_user && echo "hr_user:HumanRes1" | chpasswd && \
    useradd -m -s /bin/bash it_admin && echo "it_admin:ITadmin#1" | chpasswd

RUN groupadd domain_admins && \
    groupadd domain_users && \
    groupadd it_department && \
    groupadd hr_department && \
    groupadd backup_operators && \
    usermod -aG domain_admins admin && \
    usermod -aG domain_users jdoe && \
    usermod -aG it_department it_admin && \
    usermod -aG hr_department hr_user && \
    usermod -aG backup_operators svc_backup

COPY smb.conf /etc/samba/smb.conf
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 22 88 135 139 389 445 636

CMD ["/start.sh"]
