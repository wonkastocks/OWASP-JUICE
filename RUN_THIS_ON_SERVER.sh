#!/bin/bash
# QUICK RESTORE - Run this directly on the server

echo "==========================================="
echo "🚀 QUICK RESTORE SCRIPT"  
echo "==========================================="

# 1. Start Apache
echo "[1/5] Starting Apache..."
systemctl start apache2
systemctl enable apache2

# 2. Create basic CTF page
echo "[2/5] Creating CTF landing page..."
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Wonka Tech CTF</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #2c3e50; color: white; }
        h1 { color: #3498db; }
        a { color: #e74c3c; font-size: 20px; }
    </style>
</head>
<body>
    <h1>🎯 Wonka Tech CTF Platform</h1>
    <h2>Available Instances:</h2>
    <p><a href="https://juice3.wonkatech.org">Juice Shop (Cloudflare)</a></p>
    <p><a href="http://155.138.197.128:4000">Juice Shop (No Filters - XSS Works!)</a></p>
</body>
</html>
EOF

# 3. Open firewall
echo "[3/5] Opening firewall ports..."
ufw allow 80/tcp
ufw allow 4000/tcp
ufw --force enable

# 4. Quick Juice Shop standalone install
echo "[4/5] Installing Juice Shop on port 4000..."
if [ ! -d /opt/juice-shop-standalone ]; then
    apt-get update
    apt-get install -y nodejs npm git
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
    cd juice-shop-standalone
    echo "server:" > config/default.yml
    echo "  port: 4000" >> config/default.yml
    echo "application:" >> config/default.yml
    echo "  xssProtection: false" >> config/default.yml
    echo "challenges:" >> config/default.yml
    echo "  xssProtection: false" >> config/default.yml
    npm install --production
fi

# 5. Start Juice Shop
echo "[5/5] Starting Juice Shop..."
cd /opt/juice-shop-standalone
killall node 2>/dev/null
nohup node app.js > /var/log/juice.log 2>&1 &

echo ""
echo "✅ DONE! Services should be available at:"
echo "   http://155.138.197.128 - CTF page"
echo "   http://155.138.197.128:4000 - Juice Shop (XSS works!)"