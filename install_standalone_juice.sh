#!/bin/bash
# Install standalone Juice Shop on port 4000 - IP access only

echo "==========================================="
echo "🚀 INSTALLING STANDALONE JUICE SHOP"
echo "Port 4000 - IP Access Only (No Cloudflare)"
echo "==========================================="

# Install Node.js if not already installed
echo -e "\n1. Checking/Installing Node.js..."
which node > /dev/null 2>&1
if [ $? -ne 0 ]; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi
node --version
npm --version

# Install required packages
echo -e "\n2. Installing system dependencies..."
apt-get update
apt-get install -y git build-essential python3

# Remove any existing installation
echo -e "\n3. Cleaning up old installations..."
systemctl stop juice-standalone 2>/dev/null
systemctl disable juice-standalone 2>/dev/null
rm -rf /opt/juice-shop-standalone

# Clone Juice Shop
echo -e "\n4. Cloning Juice Shop repository..."
cd /opt
git clone https://github.com/juice-shop/juice-shop.git juice-shop-standalone
cd juice-shop-standalone

# Create configuration to disable XSS protection
echo -e "\n5. Creating configuration (XSS protection disabled)..."
mkdir -p config
cat > config/local.yml << 'EOF'
server:
  port: 4000
application:
  domain: "155.138.197.128:4000"
  name: "OWASP Juice Shop (Standalone)"
  logo: "JuiceShop_Logo.png"
  favicon: "favicon_js.ico"
  showVersionNumber: true
  showGitHubLinks: false
  localBackupEnabled: true
  xssProtection: false
  showChallengeSolvedNotifications: true
  showChallengeHints: true
  showVulnerabilityMitigations: false
challenges:
  showSolvedChallenges: true
  showDisabledChallenges: true
  showPromo: true
  xssProtection: false
  safetyOverride: true
  overwriteUrlForProductTamperingChallenge: "http://155.138.197.128:4000"
hackingInstructor:
  isEnabled: true
EOF

# Install dependencies
echo -e "\n6. Installing npm dependencies..."
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
Restart=on-failure
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=juice-standalone
Environment="NODE_ENV=unsafe"
Environment="NODE_CONFIG={\"server\":{\"port\":4000},\"application\":{\"xssProtection\":false},\"challenges\":{\"xssProtection\":false,\"safetyOverride\":true}}"

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
echo -e "\n8. Starting Juice Shop service..."
systemctl daemon-reload
systemctl enable juice-standalone
systemctl start juice-standalone

# Open firewall port
echo -e "\n9. Opening firewall port 4000..."
ufw allow 4000/tcp
ufw reload

# Wait for service to start
echo -e "\n10. Waiting for service to start..."
sleep 5

# Check if service is running
systemctl is-active juice-standalone
if [ $? -eq 0 ]; then
    echo -e "\n✅ Juice Shop is running!"
else
    echo -e "\n❌ Service failed to start. Checking logs..."
    journalctl -u juice-standalone -n 20
fi

# Test the installation
echo -e "\n11. Testing the installation..."
curl -s http://localhost:4000 -o /dev/null -w "Local test: HTTP %{http_code}\n"
curl -s "http://localhost:4000/rest/products/search?q=<script>test</script>" -o /dev/null -w "XSS test: HTTP %{http_code}\n"

echo ""
echo "==========================================="
echo "✅ STANDALONE JUICE SHOP INSTALLED!"
echo "==========================================="
echo ""
echo "Access URL: http://155.138.197.128:4000"
echo ""
echo "Features:"
echo "  - No Docker containerization"
echo "  - No Apache reverse proxy"
echo "  - No Cloudflare WAF"
echo "  - No ModSecurity"
echo "  - XSS protection disabled"
echo "  - All 110 challenges available"
echo ""
echo "Test DOM XSS:"
echo "1. Open: http://155.138.197.128:4000"
echo "2. Open browser console (F12)"
echo "3. Type: location.href = '#/search?q=<iframe src=\"javascript:alert(1)\">'"
echo ""
echo "Service management:"
echo "  - Status: systemctl status juice-standalone"
echo "  - Logs: journalctl -u juice-standalone -f"
echo "  - Restart: systemctl restart juice-standalone"
echo "  - Stop: systemctl stop juice-standalone"