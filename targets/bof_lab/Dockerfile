FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    gdb \
    python3 \
    python3-pip \
    netcat-openbsd \
    socat \
    openssh-server \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install pwntools for the player
RUN pip3 install --no-cache-dir pwntools 2>/dev/null || true

# Setup SSH
RUN mkdir -p /run/sshd && \
    echo "root:toor" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Copy and compile vulnerable binaries
COPY vuln_easy.c /opt/bof/
COPY vuln_normal.c /opt/bof/
COPY vuln_hard.c /opt/bof/

WORKDIR /opt/bof

# Easy: No protections at all
RUN gcc -o vuln_easy vuln_easy.c -fno-stack-protector -z execstack -no-pie -m32 2>/dev/null || \
    gcc -o vuln_easy vuln_easy.c -fno-stack-protector -z execstack -no-pie

# Normal: DEP ON, no canary, no PIE
RUN gcc -o vuln_normal vuln_normal.c -fno-stack-protector -no-pie

# Hard: ASLR+DEP+PIE (ASLR is set at runtime)
RUN gcc -o vuln_hard vuln_hard.c -fno-stack-protector -pie -fPIC

# Make binaries SUID root so player can practice privesc too
RUN chmod u+s vuln_easy vuln_normal vuln_hard

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 22 9999

CMD ["/start.sh"]
