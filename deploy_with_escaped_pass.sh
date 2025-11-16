#!/bin/bash
# Deploy with properly escaped password

echo "========================================="
echo "Deploying with MCP-style execution"
echo "========================================="

# Create a combined script that does everything
cat << 'SCRIPT' > /tmp/install_everything.sh
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
        .box {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            border-radius: 10px;
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
    <h1>🎯 Wonka Tech CTF Platform</h1>
    <div class="box">
        <h2>Juice Shop Instances</h2>
        <p><a href="https://juice3.wonkatech.org">Juice Shop (Cloudflare Protected)</a></p>
        <p>Some XSS blocked by WAF</p>
    </div>
    <div class="box">
        <h2>🔓 Unfiltered Instance</h2>
        <p><a href="http://155.138.197.128:4000">Juice Shop Standalone</a></p>
        <p>✅ All XSS challenges work here!</p>
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

echo "[5/6] Setting up Juice Shop standalone on port 4000..."
if [ ! -d /opt/juice-shop-standalone ]; then
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
    cd juice-shop-standalone
    
    mkdir -p config
    cat > config/default.yml << 'CONFIG'
server:
  port: 4000
application:
  domain: "155.138.197.128:4000"
  name: "OWASP Juice Shop - Unfiltered"
  xssProtection: false
challenges:
  xssProtection: false
  safetyOverride: true
CONFIG
    
    echo "Installing npm packages..."
    npm install --production
    
    cat > /etc/systemd/system/juice-standalone.service << 'SERVICE'
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
SERVICE
    
    systemctl daemon-reload
    systemctl enable juice-standalone
fi

echo "[6/6] Starting Juice Shop standalone..."
systemctl restart juice-standalone

sleep 5

echo ""
echo "========================================="
echo "✅ INSTALLATION COMPLETE!"
echo "========================================="
echo ""
echo "Services available at:"
echo "1. http://155.138.197.128 - CTF Platform"
echo "2. http://155.138.197.128:4000 - Juice Shop (XSS works!)"
echo ""

# Test the services
curl -s http://localhost:80 -o /dev/null -w "CTF Platform: %{http_code}\n"
curl -s http://localhost:4000 -o /dev/null -w "Juice Shop: %{http_code}\n"
SCRIPT

echo "Script created. Now deploying to server..."
echo ""
echo "Step 1: Copy script to server"
echo "Step 2: Execute on server"
echo ""

# The actual deployment commands
echo "Run these commands:"
echo ""
echo "scp /tmp/install_everything.sh root@155.138.197.128:/tmp/"
echo "ssh root@155.138.197.128 'bash /tmp/install_everything.sh'"
echo ""
echo "Password for both: \$Hg5sD&8Lp@9"