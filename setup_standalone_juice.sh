#!/bin/bash
# Setup Juice Shop standalone (without Docker) on Ubuntu

echo "==========================================="
echo "🚀 SETTING UP STANDALONE JUICE SHOP"
echo "==========================================="

# Prerequisites
echo -e "\n1. Installing Node.js and npm..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs
node --version
npm --version

echo -e "\n2. Installing required packages..."
apt-get update
apt-get install -y git build-essential python3

echo -e "\n3. Cloning Juice Shop repository..."
cd /opt
rm -rf juice-shop-standalone
git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
cd juice-shop-standalone

echo -e "\n4. Installing dependencies..."
npm install --production

echo -e "\n5. Creating systemd service..."
cat > /etc/systemd/system/juice-shop-standalone.service << 'EOF'
[Unit]
Description=OWASP Juice Shop Standalone
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/juice-shop-standalone
ExecStart=/usr/bin/node app.js
Restart=on-failure
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=juice-shop-standalone
Environment="NODE_ENV=unsafe"
Environment="NODE_CONFIG={\"challenges\":{\"xssProtection\":false}}"

[Install]
WantedBy=multi-user.target
EOF

echo -e "\n6. Starting Juice Shop standalone..."
systemctl daemon-reload
systemctl enable juice-shop-standalone
systemctl start juice-shop-standalone

echo -e "\n7. Setting up direct access on port 4000..."
# Use port 4000 to avoid conflicts
cat > /opt/juice-shop-standalone/config/local.yml << 'EOF'
server:
  port: 4000
application:
  xssProtection: false
challenges:
  xssProtection: false
EOF

echo -e "\n8. Restarting with new configuration..."
systemctl restart juice-shop-standalone

echo -e "\n9. Opening firewall port..."
ufw allow 4000/tcp

echo -e "\n10. Setting up Apache proxy for standalone instance..."
cat > /etc/apache2/sites-available/juice-standalone.conf << 'EOF'
<VirtualHost *:80>
    ServerName juice-standalone.wonkatech.org
    
    ProxyPreserveHost On
    ProxyPass / http://localhost:4000/
    ProxyPassReverse / http://localhost:4000/
    
    # NO ModSecurity or filtering
    <IfModule mod_security2.c>
        SecRuleEngine Off
    </IfModule>
</VirtualHost>
EOF

a2ensite juice-standalone
systemctl reload apache2

echo -e "\n==========================================="
echo "✅ STANDALONE JUICE SHOP INSTALLED"
echo "==========================================="
echo ""
echo "Access methods:"
echo "1. Direct (no filtering): http://155.138.197.128:4000"
echo "2. Via Apache: http://juice-standalone.wonkatech.org"
echo ""
echo "Why this solves XSS issues:"
echo "- No Docker isolation/security layers"
echo "- Direct Node.js execution"
echo "- XSS protection explicitly disabled"
echo "- No container networking issues"
echo "- Clean environment without filters"
echo ""
echo "Test XSS now:"
echo "1. Go to http://155.138.197.128:4000"
echo "2. Open console: location.href = '#/search?q=<iframe src=\"javascript:alert(1)\">'"
echo ""
echo "Check status:"
echo "systemctl status juice-shop-standalone"
echo "journalctl -u juice-shop-standalone -f"