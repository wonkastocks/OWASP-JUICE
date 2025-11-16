#!/bin/bash
# Set up juice-raw.wonkatech.org without Cloudflare proxy

echo "==========================================="
echo "🚀 SETTING UP JUICE-RAW (NO CLOUDFLARE)"
echo "==========================================="

# First, add DNS record in Cloudflare:
echo "STEP 1: Add DNS record in Cloudflare Dashboard:"
echo "----------------------------------------"
echo "Type: A"
echo "Name: juice-raw"
echo "Content: 155.138.197.128"
echo "Proxy status: DNS only (GREY cloud, not orange)"
echo ""
echo "This makes juice-raw.wonkatech.org bypass Cloudflare!"
echo ""

# Set up standalone Juice Shop
echo "STEP 2: Installing standalone Juice Shop..."
echo "----------------------------------------"

# Install Node.js if not present
which node || {
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
}

# Clone and setup
cd /opt
rm -rf juice-shop-raw
git clone https://github.com/juice-shop/juice-shop.git juice-shop-raw
cd juice-shop-raw

# Install with XSS disabled
cat > config/local.yml << 'EOF'
server:
  port: 4000
application:
  xssProtection: false
  showChallengeSolvedNotifications: true
challenges:
  xssProtection: false
  safetyOverride: true
EOF

npm install --production

# Create service
cat > /etc/systemd/system/juice-raw.service << 'EOF'
[Unit]
Description=Juice Shop Raw (No Filters)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/juice-shop-raw
ExecStart=/usr/bin/node app.js
Restart=on-failure
Environment="NODE_ENV=unsafe"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable juice-raw
systemctl start juice-raw

# Apache config for juice-raw
cat > /etc/apache2/sites-available/juice-raw.conf << 'EOF'
<VirtualHost *:80>
    ServerName juice-raw.wonkatech.org
    
    # NO security filters
    <IfModule mod_security2.c>
        SecRuleEngine Off
    </IfModule>
    
    ProxyPass / http://localhost:4000/
    ProxyPassReverse / http://localhost:4000/
</VirtualHost>
EOF

a2ensite juice-raw
systemctl reload apache2

# Open firewall
ufw allow 4000/tcp

echo ""
echo "==========================================="
echo "✅ JUICE-RAW SETUP COMPLETE!"
echo "==========================================="
echo ""
echo "Access methods (NO Cloudflare filtering):"
echo "1. http://juice-raw.wonkatech.org (DNS only)"
echo "2. http://155.138.197.128:4000 (direct IP)"
echo ""
echo "DOM XSS will work here!"