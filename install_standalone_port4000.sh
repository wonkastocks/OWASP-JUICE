#!/bin/bash
# Install ADDITIONAL standalone Juice Shop on port 4000 (keeping Docker instance)

echo "==========================================="
echo "🚀 INSTALLING STANDALONE JUICE SHOP"
echo "Port 4000 - IP Access Only"
echo "Keeping existing Docker instance on port 3000"
echo "==========================================="

# Check if port 4000 is already in use
echo -e "\n1. Checking if port 4000 is available..."
netstat -tlnp | grep :4000 && {
    echo "❌ Port 4000 is already in use!"
    exit 1
} || echo "✅ Port 4000 is available"

# Install Node.js if not already installed
echo -e "\n2. Installing Node.js..."
which node > /dev/null 2>&1
if [ $? -ne 0 ]; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi
echo "Node version: $(node --version)"
echo "NPM version: $(npm --version)"

# Install build tools
echo -e "\n3. Installing build dependencies..."
apt-get update
apt-get install -y git build-essential python3

# Clone Juice Shop for standalone
echo -e "\n4. Setting up standalone Juice Shop..."
cd /opt
rm -rf juice-shop-standalone
git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
cd juice-shop-standalone

# Create configuration
echo -e "\n5. Creating configuration (no XSS protection)..."
mkdir -p config
cat > config/default.yml << 'EOF'
server:
  port: 4000
  basePath: ''
application:
  domain: "155.138.197.128:4000"
  name: "OWASP Juice Shop (Standalone - No Filters)"
  logo: "JuiceShop_Logo.png"
  favicon: "favicon_js.ico"
  theme: "bluegrey-lightgreen"
  showVersionNumber: true
  showGitHubLinks: false
  localBackupEnabled: true
  xssProtection: false
  showChallengeSolvedNotifications: true
  showChallengeHints: true
  showVulnerabilityMitigations: false
  welcomeBanner:
    showOnFirstStart: true
    title: "Welcome to Juice Shop Standalone!"
    message: "This instance has NO security filters - all XSS challenges will work!"
challenges:
  showSolvedChallenges: true
  showDisabledChallenges: true
  showPromo: true
  xssProtection: false
  safetyOverride: true
  overwriteUrlForProductTamperingChallenge: "http://155.138.197.128:4000"
hackingInstructor:
  isEnabled: true
  avatarImage: "juicy_bot.png"
EOF

# Install dependencies
echo -e "\n6. Installing npm packages (this may take a few minutes)..."
npm install --production

# Create systemd service
echo -e "\n7. Creating systemd service..."
cat > /etc/systemd/system/juice-standalone.service << 'EOF'
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
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=juice-standalone
Environment="NODE_ENV=unsafe"

[Install]
WantedBy=multi-user.target
EOF

# Start the service
echo -e "\n8. Starting Juice Shop standalone service..."
systemctl daemon-reload
systemctl enable juice-standalone
systemctl start juice-standalone

# Open firewall port
echo -e "\n9. Opening firewall port 4000..."
ufw allow 4000/tcp
ufw reload

# Wait for startup
echo -e "\n10. Waiting for service to start..."
sleep 10

# Check status
echo -e "\n11. Checking service status..."
systemctl is-active juice-standalone
if [ $? -eq 0 ]; then
    echo "✅ Service is running!"
else
    echo "❌ Service failed. Checking logs..."
    journalctl -u juice-standalone -n 50
fi

# Test access
echo -e "\n12. Testing access..."
curl -s http://localhost:4000 -o /dev/null -w "Local test: HTTP %{http_code}\n"
curl -s "http://localhost:4000/rest/products/search?q=<script>test</script>" -o /dev/null -w "XSS test: HTTP %{http_code} (should be 200, not 500)\n"

echo ""
echo "==========================================="
echo "✅ INSTALLATION COMPLETE!"
echo "==========================================="
echo ""
echo "You now have TWO Juice Shop instances:"
echo ""
echo "1. DOCKER INSTANCE (with Cloudflare/filters):"
echo "   URL: https://juice3.wonkatech.org"
echo "   Port: 3000 (internal)"
echo "   Security: Cloudflare WAF + ModSecurity"
echo ""
echo "2. STANDALONE INSTANCE (no filters):"
echo "   URL: http://155.138.197.128:4000"
echo "   Port: 4000"
echo "   Security: NONE - All XSS works!"
echo ""
echo "Test DOM XSS on standalone:"
echo "1. Open: http://155.138.197.128:4000"
echo "2. Press F12 for console"
echo "3. Type: location.href = '#/search?q=<iframe src=\"javascript:alert(1)\">'"
echo ""
echo "Service commands:"
echo "  Status: systemctl status juice-standalone"
echo "  Logs: journalctl -u juice-standalone -f"
echo "  Restart: systemctl restart juice-standalone"
echo "  Stop: systemctl stop juice-standalone"