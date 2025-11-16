#!/bin/bash
# Complete fix for bad gateway and setup standalone Juice Shop

echo "==========================================="
echo "🔧 COMPLETE FIX FOR WONKATECH.ORG"
echo "==========================================="

# Fix 1: Ensure Apache is running and configured correctly
echo -e "\n[1/10] Fixing Apache configuration..."
systemctl stop apache2
systemctl start apache2
systemctl status apache2 --no-pager

# Fix 2: Check what should be at wonkatech.org root
echo -e "\n[2/10] Checking web root configuration..."
if [ -f /var/www/html/index.php ]; then
    echo "✅ CTF platform files found at /var/www/html/"
    # Ensure PHP is working
    apt-get install -y php php-mysql php-curl php-gd php-mbstring php-xml libapache2-mod-php
    systemctl restart apache2
elif [ -f /var/www/html/index.html ]; then
    echo "⚠️ Static HTML found, CTF platform may be missing"
else
    echo "❌ No web files found, creating placeholder"
    cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Wonka Tech CTF Platform</title>
</head>
<body>
    <h1>Wonka Tech CTF Platform</h1>
    <h2>Available Services:</h2>
    <ul>
        <li><a href="https://juice3.wonkatech.org">Juice Shop (Docker with Cloudflare)</a></li>
        <li><a href="http://155.138.197.128:4000">Juice Shop (Standalone - No Filters)</a></li>
    </ul>
</body>
</html>
EOF
    chown www-data:www-data /var/www/html/index.html
fi

# Fix 3: Check MySQL for CTF database
echo -e "\n[3/10] Checking MySQL database..."
systemctl start mysql
systemctl status mysql --no-pager
mysql -e "SHOW DATABASES;" 2>/dev/null | grep ctf_platform && echo "✅ CTF database exists" || echo "⚠️ CTF database not found"

# Fix 4: Check Cloudflare tunnel configuration
echo -e "\n[4/10] Checking Cloudflare tunnel..."
if [ -f /root/.cloudflared/cert.pem ]; then
    echo "✅ Cloudflare certificate found"
    # Check if tunnel is running
    ps aux | grep cloudflared | grep -v grep
    if [ $? -ne 0 ]; then
        echo "Starting Cloudflare tunnel..."
        # Try to find and run the tunnel
        if [ -f /etc/systemd/system/cloudflared.service ]; then
            systemctl start cloudflared
        else
            echo "⚠️ Cloudflare tunnel service not configured"
        fi
    fi
else
    echo "⚠️ Cloudflare not configured, using direct Apache"
fi

# Fix 5: Fix/restart Juice Shop Docker for juice3.wonkatech.org
echo -e "\n[5/10] Fixing Juice Shop Docker container..."
# Stop all juice containers
docker stop $(docker ps -aq --filter name=juice) 2>/dev/null

# Start fresh container for juice3
docker run -d \
    --name juice3 \
    --restart unless-stopped \
    -p 3001:3000 \
    bkimminich/juice-shop

echo "Waiting for container to start..."
sleep 5
docker ps | grep juice3 && echo "✅ Juice3 container running" || echo "❌ Container failed"

# Fix 6: Configure Apache VirtualHosts
echo -e "\n[6/10] Configuring Apache VirtualHosts..."

# Main site (wonkatech.org)
cat > /etc/apache2/sites-available/000-default.conf << 'EOF'
<VirtualHost *:80>
    ServerName wonkatech.org
    ServerAlias www.wonkatech.org
    DocumentRoot /var/www/html
    
    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

# Juice Shop subdomain
cat > /etc/apache2/sites-available/juice3.conf << 'EOF'
<VirtualHost *:80>
    ServerName juice3.wonkatech.org
    
    ProxyPreserveHost On
    ProxyPass / http://localhost:3001/
    ProxyPassReverse / http://localhost:3001/
    
    ErrorLog ${APACHE_LOG_DIR}/juice3-error.log
    CustomLog ${APACHE_LOG_DIR}/juice3-access.log combined
</VirtualHost>
EOF

a2ensite 000-default
a2ensite juice3
a2enmod proxy proxy_http
systemctl reload apache2

# Fix 7: Install standalone Juice Shop on port 4000
echo -e "\n[7/10] Installing standalone Juice Shop on port 4000..."
if [ ! -d /opt/juice-shop-standalone ]; then
    # Install Node.js if needed
    which node || {
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt-get install -y nodejs
    }
    
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
    cd juice-shop-standalone
    
    # Configure for port 4000 with no filters
    mkdir -p config
    cat > config/default.yml << 'EOFC'
server:
  port: 4000
application:
  domain: "155.138.197.128:4000"
  name: "OWASP Juice Shop (Standalone - No Filters)"
  xssProtection: false
challenges:
  xssProtection: false
  safetyOverride: true
EOFC
    
    npm install --production
    
    # Create systemd service
    cat > /etc/systemd/system/juice-standalone.service << 'EOFS'
[Unit]
Description=Juice Shop Standalone Port 4000
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/juice-shop-standalone
ExecStart=/usr/bin/node app.js
Restart=always
Environment="NODE_ENV=unsafe"

[Install]
WantedBy=multi-user.target
EOFS
    
    systemctl daemon-reload
    systemctl enable juice-standalone
    systemctl start juice-standalone
else
    echo "Standalone already installed, restarting..."
    systemctl restart juice-standalone
fi

# Fix 8: Open firewall ports
echo -e "\n[8/10] Opening firewall ports..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3001/tcp
ufw allow 4000/tcp
ufw reload

# Fix 9: Test all endpoints
echo -e "\n[9/10] Testing all endpoints..."
echo "Testing wonkatech.org (port 80)..."
curl -s http://localhost:80 -o /dev/null -w "  Local port 80: %{http_code}\n"

echo "Testing Juice Shop Docker (port 3001)..."
curl -s http://localhost:3001 -o /dev/null -w "  Local port 3001: %{http_code}\n"

echo "Testing Juice Shop Standalone (port 4000)..."
curl -s http://localhost:4000 -o /dev/null -w "  Local port 4000: %{http_code}\n"

# Fix 10: Final status
echo -e "\n[10/10] Final Status Check..."
echo ""
echo "==========================================="
echo "✅ FIXES APPLIED - SUMMARY"
echo "==========================================="
echo ""
echo "Services Status:"
systemctl is-active apache2 >/dev/null && echo "✅ Apache: Running" || echo "❌ Apache: Stopped"
systemctl is-active mysql >/dev/null && echo "✅ MySQL: Running" || echo "❌ MySQL: Stopped"
docker ps | grep juice3 >/dev/null && echo "✅ Juice Docker: Running" || echo "❌ Juice Docker: Stopped"
systemctl is-active juice-standalone >/dev/null && echo "✅ Juice Standalone: Running" || echo "❌ Juice Standalone: Stopped"

echo ""
echo "Access URLs:"
echo "1. https://wonkatech.org - Main CTF site"
echo "2. https://juice3.wonkatech.org - Juice Shop (Docker/Cloudflare)"
echo "3. http://155.138.197.128:4000 - Juice Shop (Standalone/No filters)"
echo ""
echo "If wonkatech.org still shows bad gateway:"
echo "- Check Cloudflare DNS settings"
echo "- Ensure tunnel is configured correctly"
echo "- Or disable Cloudflare proxy (grey cloud)"