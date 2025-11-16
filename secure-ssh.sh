#!/bin/bash

# Secure SSH from brute force attempts
SERVER="155.138.197.128"

echo "This script will help secure your SSH from brute force attacks"
echo ""

cat > /tmp/secure_ssh.sh << 'EOF'
#!/bin/bash

echo "Securing SSH..."

# Install fail2ban to block brute force attempts
apt-get update
apt-get install -y fail2ban

# Configure fail2ban for SSH
cat > /etc/fail2ban/jail.local << 'F2B'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
F2B

# Change SSH port (optional but recommended)
# sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config

# Disable root login and use key-based auth (for later)
# sed -i 's/^PermitRootLogin yes/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config

# Restart services
systemctl restart fail2ban
systemctl restart ssh

echo "fail2ban installed and configured"
echo "Current banned IPs:"
fail2ban-client status sshd

EOF

echo "Commands prepared. To secure your SSH, run:"
echo ""
echo "scp /tmp/secure_ssh.sh root@$SERVER:/tmp/"
echo "ssh root@$SERVER 'bash /tmp/secure_ssh.sh'"
echo ""
echo "This will install fail2ban which will automatically block IPs after 3 failed login attempts."