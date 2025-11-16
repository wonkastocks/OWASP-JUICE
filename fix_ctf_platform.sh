#!/bin/bash
# Fix the CTF platform at wonkatech.org and set up standalone Juice Shop

echo "==========================================="
echo "🔧 FIXING CTF PLATFORM & JUICE SHOP"
echo "==========================================="

echo -e "\n1. Checking what's currently running..."
docker ps -a
echo ""
netstat -tlnp | grep -E ":80|:443|:3000|:4000"

echo -e "\n2. Checking Apache configuration..."
ls -la /etc/apache2/sites-enabled/
cat /etc/apache2/sites-enabled/000-default-le-ssl.conf | grep -E "ServerName|ProxyPass"

echo -e "\n3. Checking web root for CTF platform..."
ls -la /var/www/html/

echo -e "\n4. Restarting CTF platform services..."
# Check if CTF platform files exist
if [ -f /var/www/html/index.php ]; then
    echo "CTF platform files found"
    # Ensure Apache is running
    systemctl restart apache2
    systemctl restart mysql
else
    echo "CTF platform files missing - need to restore"
fi

echo -e "\n5. Fixing Juice Shop Docker container..."
# Check for Juice Shop containers
docker ps | grep juice
if [ $? -ne 0 ]; then
    echo "Starting Juice Shop container..."
    docker run -d --name juice3 --restart unless-stopped -p 3001:3000 bkimminich/juice-shop
fi

echo -e "\n6. Installing standalone Juice Shop on port 4000..."
# Check if Node.js is installed
which node || {
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
}

# Clone and setup standalone if not exists
if [ ! -d /opt/juice-shop-standalone ]; then
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
    cd juice-shop-standalone
    
    # Configure for port 4000
    mkdir -p config
    cat > config/default.yml << 'EOF'
server:
  port: 4000
application:
  xssProtection: false
challenges:
  xssProtection: false
  safetyOverride: true
EOF
    
    npm install --production
    
    # Create service
    cat > /etc/systemd/system/juice-standalone.service << 'EOF'
[Unit]
Description=Juice Shop Standalone
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/juice-shop-standalone
ExecStart=/usr/bin/node app.js
Restart=always
Environment="NODE_ENV=unsafe"

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable juice-standalone
    systemctl start juice-standalone
fi

echo -e "\n7. Opening firewall ports..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3001/tcp
ufw allow 4000/tcp
ufw reload

echo -e "\n8. Final status check..."
echo "Services running:"
systemctl is-active apache2 && echo "✅ Apache (CTF platform)"
systemctl is-active mysql && echo "✅ MySQL (CTF database)"
docker ps | grep juice && echo "✅ Juice Shop Docker"
systemctl is-active juice-standalone && echo "✅ Juice Shop Standalone"

echo ""
echo "==========================================="
echo "✅ CONFIGURATION COMPLETE"
echo "==========================================="
echo ""
echo "Access points:"
echo "1. https://wonkatech.org - CTF Registration Platform"
echo "2. https://juice3.wonkatech.org - Juice Shop (Docker/Cloudflare)"
echo "3. http://155.138.197.128:4000 - Juice Shop Standalone (No filters)"
echo ""