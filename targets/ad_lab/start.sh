#!/bin/bash

# Get the flag from environment
FLAG="${CYBERSIM_FLAG:-FLAG{ad_default_flag}}"

# ─── Plant flags in various locations based on difficulty ──────────────
# Easy: Flag on public share
echo "$FLAG" > /srv/samba/shared/README.txt
echo "Welcome to CORP domain. The IT department password policy is weak." >> /srv/samba/shared/README.txt

# Normal: Flag on admin share
echo "$FLAG" > /srv/samba/admin_only/domain_backup.txt
echo "Domain Admin backup credentials - CONFIDENTIAL" >> /srv/samba/admin_only/domain_backup.txt

# Hard: Flag in kerberos ticket cache simulation
mkdir -p /tmp/krb5cc
echo "Kerberos Ticket Cache: $FLAG" > /tmp/krb5cc/krb5cc_admin
chmod 600 /tmp/krb5cc/krb5cc_admin
chown admin:admin /tmp/krb5cc/krb5cc_admin

# Plant password hashes (simulated NTDS.dit dump)
mkdir -p /var/lib/samba/private
cat > /var/lib/samba/private/sam_hashes.txt << HASHES
admin:500:aad3b435b51404eeaad3b435b51404ee:32ed87bdb5fdc5e9cba88547376818d4:::
jdoe:1001:aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c:::
svc_backup:1002:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
it_admin:1003:aad3b435b51404eeaad3b435b51404ee:fc525c9683e8fe067095ba2ddc971889:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:b4b9b02e6f09e9d7ea3f7fea444558d4:::
HASHES
chmod 600 /var/lib/samba/private/sam_hashes.txt

# GPP password (simulated Group Policy Preferences vuln)
mkdir -p /srv/samba/shared/SYSVOL/corp.local/Policies
cat > /srv/samba/shared/SYSVOL/corp.local/Policies/Groups.xml << GPPXML
<?xml version="1.0" encoding="utf-8"?>
<Groups>
<User name="localadmin" action="U" newName="" fullName="Local Admin" description="Built-in admin">
<Properties action="U" userName="localadmin" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" />
</User>
</Groups>
GPPXML

# Create login history
mkdir -p /var/log/samba
cat > /var/log/samba/auth.log << AUTHLOG
Feb 25 10:00:01 CORP samba[1234]: Login OK: jdoe from 192.168.1.50
Feb 25 10:05:23 CORP samba[1234]: Login FAILED: admin from 192.168.1.100
Feb 25 10:05:24 CORP samba[1234]: Login FAILED: admin from 192.168.1.100
Feb 25 10:05:25 CORP samba[1234]: Login FAILED: admin from 192.168.1.100
Feb 25 10:05:26 CORP samba[1234]: Login FAILED: admin from 192.168.1.100
Feb 25 10:05:27 CORP samba[1234]: Login OK: admin from 192.168.1.100
Feb 25 10:10:00 CORP samba[1234]: Share accessed: admin -> admin_only
Feb 25 10:15:00 CORP samba[1234]: Login OK: svc_backup from 10.0.0.5
AUTHLOG

# Set proper permissions
chmod 777 /srv/samba/shared
chmod 750 /srv/samba/admin_only
chmod 750 /srv/samba/it_dept
chown -R admin:admin /srv/samba/admin_only

# Set samba passwords
(echo "Welcome123"; echo "Welcome123") | smbpasswd -a -s jdoe
(echo "Backup2024!"; echo "Backup2024!") | smbpasswd -a -s svc_backup
(echo "P@ssw0rd2024"; echo "P@ssw0rd2024") | smbpasswd -a -s admin
(echo "HumanRes1"; echo "HumanRes1") | smbpasswd -a -s hr_user
(echo "ITadmin#1"; echo "ITadmin#1") | smbpasswd -a -s it_admin

# Start services
/usr/sbin/sshd
smbd -D
nmbd -D

echo "[*] AD Lab started - CORP domain active"
echo "[*] Users: jdoe, svc_backup, admin, hr_user, it_admin"
echo "[*] Shares: shared, admin_only, it_dept"

# Simulate Kerberos service on port 88 (mock)
while true; do
    echo "KRB5KDC: corp.local - Authentication Service" | nc -l -p 88 -w 1 2>/dev/null
done &

# Keep alive
tail -f /dev/null
