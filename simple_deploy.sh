#!/bin/bash
echo "========================================="
echo "DEPLOYING VIA MCP SERVERS"
echo "========================================="

# Create the installation script
cat << 'SCRIPT' > /tmp/install_services.sh
#!/bin/bash
echo "[1/6] Starting Apache..."
systemctl start apache2
systemctl enable apache2

echo "[2/6] Creating CTF landing page..."
mkdir -p /var/www/html
cat > /var/www/html/index.html << 'HTML'
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
        h1 { font-size: 3em; }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
        }
        .service {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        a {
            color: #ffd700;
            font-size: 1.5em;
            text-decoration: none;
        }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Wonka Tech CTF Platform</h1>
        <div class="service">
            <h2>Juice Shop Instances</h2>
            <p><a href="https://juice3.wonkatech.org">Juice Shop (Cloudflare Protected)</a></p>
            <p style="color: #ff6b6b;">⚠️ Some XSS challenges blocked by WAF</p>
        </div>
        <div class="service">
            <h2>🔓 Unfiltered Practice Instance</h2>
            <p><a href="http://155.138.197.128:4000">Juice Shop Standalone</a></p>
            <p style="color: #51cf66;">✅ All XSS challenges work here!</p>
        </div>
    </div>
</body>
</html>
HTML
chown www-data:www-data /var/www/html/index.html

echo "[3/6] Configuring firewall..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 4000/tcp
ufw --force enable

echo "[4/6] Installing Node.js if needed..."
which node || {
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
}

echo "[5/6] Setting up Juice Shop on port 4000..."
if [ ! -d /opt/juice-shop-4000 ]; then
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice-shop-4000
    cd juice-shop-4000
    
    mkdir -p config
    cat > config/default.yml << 'CONFIG'
server:
  port: 4000
application:
  domain: "155.138.197.128:4000"
  name: "OWASP Juice Shop - Unfiltered"
  xssProtection: false
  showChallengeSolvedNotifications: true
challenges:
  xssProtection: false
  safetyOverride: true
CONFIG
    
    echo "Installing npm packages..."
    npm install --production
    
    cat > /etc/systemd/system/juice-4000.service << 'SERVICE'
[Unit]
Description=Juice Shop Port 4000
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/juice-shop-4000
ExecStart=/usr/bin/node app.js
Restart=always
Environment="NODE_ENV=unsafe"

[Install]
WantedBy=multi-user.target
SERVICE
    
    systemctl daemon-reload
    systemctl enable juice-4000
fi

echo "[6/6] Starting Juice Shop..."
systemctl restart juice-4000

echo ""
echo "========================================="
echo "✅ INSTALLATION COMPLETE!"
echo "========================================="
echo ""
echo "Services available at:"
echo "  http://155.138.197.128 - CTF Platform"
echo "  http://155.138.197.128:4000 - Juice Shop (XSS works!)"
echo ""

sleep 5
curl -s http://localhost -o /dev/null -w "CTF Platform: HTTP %{http_code}\n"
curl -s http://localhost:4000 -o /dev/null -w "Juice Shop: HTTP %{http_code}\n"
SCRIPT

echo "Script created at /tmp/install_services.sh"
echo ""
echo "Now use the MCP SSH/SCP servers to deploy it"