#!/bin/bash

# Script to enable SSH access on 155.138.197.128

echo "=== Enable SSH Access on 155.138.197.128 ==="
echo ""
echo "Since you can't SSH in directly, you'll need to access the server through:"
echo ""
echo "Option 1: Vultr Console (Recommended)"
echo "1. Log into your Vultr account at https://my.vultr.com"
echo "2. Find your server (155.138.197.128)"
echo "3. Click 'View Console' or the console icon"
echo "4. Login as root with your password"
echo ""
echo "Once you're in the console, run these commands:"
echo ""
echo "# 1. Check SSH service status"
echo "systemctl status ssh"
echo ""
echo "# 2. If SSH is not running, start it"
echo "systemctl start ssh"
echo "systemctl enable ssh"
echo ""
echo "# 3. Check if root login is allowed"
echo "grep 'PermitRootLogin' /etc/ssh/sshd_config"
echo ""
echo "# 4. If PermitRootLogin is 'no' or commented out, fix it:"
echo "sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config"
echo ""
echo "# 5. Also ensure password authentication is enabled:"
echo "sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config"
echo ""
echo "# 6. Restart SSH service"
echo "systemctl restart ssh"
echo ""
echo "# 7. Check firewall (if ufw is installed)"
echo "ufw status"
echo "ufw allow 22/tcp"
echo ""
echo "# 8. Set a root password if needed"
echo "passwd root"
echo ""
echo "========================================"
echo ""
echo "Option 2: If you have a working web shell on the server"
echo "You could create a PHP file to execute these commands:"
echo ""
cat > /tmp/enable_ssh.php << 'EOF'
<?php
// enable_ssh.php - Upload this to your web server
if(isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    if($cmd == 'enable') {
        exec('systemctl start ssh');
        exec('systemctl enable ssh');
        exec("sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config");
        exec("sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config");
        exec('systemctl restart ssh');
        echo "SSH should be enabled now";
    }
    if($cmd == 'status') {
        echo "<pre>";
        echo shell_exec('systemctl status ssh 2>&1');
        echo "</pre>";
    }
    if($cmd == 'setpass') {
        // Set root password to a known value
        exec('echo "root:YourNewPasswordHere" | chpasswd');
        echo "Password set";
    }
}
?>
<h3>SSH Enable Tool</h3>
<a href="?cmd=status">Check SSH Status</a><br>
<a href="?cmd=enable">Enable SSH</a><br>
<a href="?cmd=setpass">Set Root Password</a><br>
EOF

echo "PHP helper saved to /tmp/enable_ssh.php"
echo ""
echo "========================================"
echo "Your root password should be what you set when creating the VPS."
echo "If you forgot it, you can reset it from Vultr console."