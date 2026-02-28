FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    bash \
    grep \
    && rm -rf /var/lib/apt/lists/*

# Create player user
RUN useradd -m -s /bin/bash player && \
    echo "player:player" | chpasswd

# Challenge 1: Hidden file
RUN echo "FLAG{h1dd3n_f1l3s_4r3_n0t_s4f3}" > /home/player/.secret && \
    chown player:player /home/player/.secret

# Challenge 2: Root flag + sudo access
RUN echo "FLAG{sud0_g1v3s_p0w3r}" > /root/flag.txt && \
    echo "player ALL=(root) NOPASSWD: /bin/cat /root/flag.txt" >> /etc/sudoers

# Challenge 3: Flag buried in syslog
RUN mkdir -p /var/log && \
    python3 -c "
import random, string
lines = []
for i in range(500):
lines.append('Feb 18 10:' + str(random.randint(10,59)) + ':' + str(random.randint(10,59)) + ' server syslogd: ' + ''.join(random.choices(string.ascii_letters, k=40)))
lines.insert(random.randint(100,400), 'Feb 18 10:30:00 server kernel: FLAG{gr3p_1s_y0ur_b3st_fr13nd} - system event logged')
with open('/var/log/syslog', 'w') as f:
f.write('\n'.join(lines))
" 2>/dev/null || echo "Feb 18 10:30:00 server kernel: FLAG{gr3p_1s_y0ur_b3st_fr13nd}" > /var/log/syslog

# SSH setup
RUN mkdir /var/run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
