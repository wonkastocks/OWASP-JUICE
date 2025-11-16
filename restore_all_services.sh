#!/bin/bash
# Restore all services - CTF platform and Juice Shop

echo "==========================================="
echo "🔧 RESTORING ALL SERVICES"
echo "==========================================="

# 1. Fix Apache and ensure it's running
echo -e "\n[1/8] Starting Apache web server..."
systemctl stop apache2
systemctl start apache2
systemctl enable apache2

# 2. Check if CTF platform files exist, if not create them
echo -e "\n[2/8] Checking/Restoring CTF platform files..."
if [ ! -f /var/www/html/index.php ] && [ ! -f /var/www/html/index.html ]; then
    echo "Creating CTF platform landing page..."
    cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Wonka Tech CTF Platform</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
        }
        h1 { font-size: 3em; margin-bottom: 30px; }
        .service-box {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        a {
            color: #ffd700;
            text-decoration: none;
            font-size: 1.2em;
        }
        a:hover { text-decoration: underline; }
        .status { color: #90EE90; }
        .error { color: #FF6B6B; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Wonka Tech CTF Platform</h1>
        <p>Welcome to the Capture The Flag training environment!</p>
        
        <div class="service-box">
            <h2>📚 Available CTF Services</h2>
            <p><a href="https://juice3.wonkatech.org">OWASP Juice Shop (Cloudflare Protected)</a></p>
            <p>Docker instance with Cloudflare WAF - Some XSS challenges blocked</p>
        </div>
        
        <div class="service-box">
            <h2>🔓 Unfiltered Practice Instance</h2>
            <p><a href="http://155.138.197.128:4000">OWASP Juice Shop (Standalone)</a></p>
            <p>Direct access - All XSS and security challenges work!</p>
        </div>
        
        <div class="service-box">
            <h2>📊 Challenge Progress</h2>
            <p>Track your progress on the Score Board in each Juice Shop instance</p>
            <p>Target: Complete 50% of challenges (55/110)</p>
        </div>
    </div>
</body>
</html>
EOF
    chown www-data:www-data /var/www/html/index.html
fi

# 3. Configure Apache to serve on port 80
echo -e "\n[3/8] Configuring Apache..."
cat > /etc/apache2/sites-available/000-default.conf << 'EOF'
<VirtualHost *:80>
    ServerAdmin admin@wonkatech.org
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

a2ensite 000-default
a2dissite default-ssl 2>/dev/null
systemctl reload apache2

# 4. Ensure firewall allows HTTP/HTTPS
echo -e "\n[4/8] Configuring firewall..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3000/tcp
ufw allow 3001/tcp
ufw allow 4000/tcp
ufw --force enable
ufw reload

# 5. Start Juice Shop Docker container
echo -e "\n[5/8] Starting Juice Shop Docker container..."
docker stop $(docker ps -aq --filter name=juice) 2>/dev/null
docker rm $(docker ps -aq --filter name=juice) 2>/dev/null
docker run -d \
    --name juice3 \
    --restart unless-stopped \
    -p 3001:3000 \
    bkimminich/juice-shop
echo "Waiting for Docker container to start..."
sleep 10

# 6. Install and start standalone Juice Shop on port 4000
echo -e "\n[6/8] Setting up standalone Juice Shop on port 4000..."

# Install Node.js if not present
which node > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi

# Setup standalone Juice Shop
if [ ! -d /opt/juice-shop-standalone ]; then
    echo "Installing Juice Shop standalone..."
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
    cd juice-shop-standalone
    
    # Create config to disable XSS protection
    mkdir -p config
    cat > config/default.yml << 'EOJS'
server:
  port: 4000
  basePath: ''
application:
  domain: "155.138.197.128:4000"
  name: "OWASP Juice Shop - Unfiltered"
  logo: "JuiceShop_Logo.png"
  favicon: "favicon_js.ico"
  theme: "bluegrey-lightgreen"
  showVersionNumber: true
  showGitHubLinks: true
  localBackupEnabled: true
  xssProtection: false
  showChallengeSolvedNotifications: true
  showChallengeHints: true
challenges:
  showSolvedChallenges: true
  xssProtection: false
  safetyOverride: true
hackingInstructor:
  isEnabled: true
EOJS
    
    echo "Installing npm packages (this will take a few minutes)..."
    npm install --production
    
    # Create systemd service
    cat > /etc/systemd/system/juice-standalone.service << 'EOSVC'
[Unit]
Description=OWASP Juice Shop Standalone (Port 4000)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/juice-shop-standalone
ExecStart=/usr/bin/node app.js
Restart=always
RestartSec=10
Environment="NODE_ENV=unsafe"

[Install]
WantedBy=multi-user.target
EOSVC
    
    systemctl daemon-reload
    systemctl enable juice-standalone
fi

# Start the standalone service
systemctl restart juice-standalone
echo "Waiting for standalone Juice Shop to start..."
sleep 10

# 7. Test all services
echo -e "\n[7/8] Testing services..."
echo ""
echo "Testing Apache on port 80..."
curl -s -o /dev/null -w "  HTTP Status: %{http_code}\n" http://localhost:80 || echo "  ❌ Not responding"

echo "Testing Juice Shop Docker on port 3001..."
curl -s -o /dev/null -w "  HTTP Status: %{http_code}\n" http://localhost:3001 || echo "  ❌ Not responding"

echo "Testing Juice Shop Standalone on port 4000..."
curl -s -o /dev/null -w "  HTTP Status: %{http_code}\n" http://localhost:4000 || echo "  ❌ Not responding"

# 8. Show final status
echo -e "\n[8/8] Final Status..."
echo ""
echo "==========================================="
echo "✅ SERVICE STATUS"
echo "==========================================="
echo ""

# Check service status
systemctl is-active apache2 >/dev/null 2>&1 && echo "✅ Apache: Running" || echo "❌ Apache: Not running"
docker ps | grep juice3 >/dev/null 2>&1 && echo "✅ Juice Shop Docker: Running" || echo "❌ Juice Shop Docker: Not running"
systemctl is-active juice-standalone >/dev/null 2>&1 && echo "✅ Juice Shop Standalone: Running" || echo "❌ Juice Shop Standalone: Not running"

echo ""
echo "==========================================="
echo "🌐 ACCESS URLS"
echo "==========================================="
echo ""
echo "1. CTF Platform:"
echo "   http://155.138.197.128"
echo "   https://wonkatech.org"
echo ""
echo "2. Juice Shop (Docker/Filtered):"
echo "   https://juice3.wonkatech.org"
echo "   http://155.138.197.128:3001"
echo ""
echo "3. Juice Shop (Standalone/Unfiltered):"
echo "   http://155.138.197.128:4000"
echo "   ⚡ All XSS challenges work here!"
echo ""
echo "==========================================="

# Show any errors
echo -e "\nChecking for errors..."
journalctl -u apache2 -n 5 --no-pager | grep -i error || echo "No Apache errors"
journalctl -u juice-standalone -n 5 --no-pager | grep -i error || echo "No standalone errors"
docker logs juice3 2>&1 | tail -5 | grep -i error || echo "No Docker errors"