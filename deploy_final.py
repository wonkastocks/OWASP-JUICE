#!/usr/bin/env python3
import os
import sys

print("="*50)
print("FINAL DEPLOYMENT SOLUTION")
print("="*50)

# Since automated login isn't working, let's create a single command solution
print("\nSince the password starts with $ and has special characters,")
print("we need to handle it carefully.\n")

print("Please run these commands manually:\n")

print("1. First, SSH to the server:")
print("   ssh root@155.138.197.128")
print("   Password: $Hg5sD&8Lp@9")
print("")

print("2. Once logged in, paste this ENTIRE block at once:")
print("-"*50)

script = '''
cat > /tmp/install.sh << 'ENDSCRIPT'
#!/bin/bash
echo "Installing everything..."

# Start Apache
systemctl start apache2
systemctl enable apache2

# Create CTF page
cat > /var/www/html/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head><title>CTF Platform</title></head>
<body style="text-align:center; padding:50px; font-family:Arial;">
<h1>Wonka Tech CTF Platform</h1>
<h2>Available Services:</h2>
<p><a href="https://juice3.wonkatech.org">Juice Shop (Cloudflare)</a></p>
<p><a href="http://155.138.197.128:4000">Juice Shop Standalone - XSS Works!</a></p>
</body>
</html>
HTML

# Open firewall
ufw allow 80/tcp
ufw allow 4000/tcp
ufw --force enable

# Install Node if needed
which node || {
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
}

# Install Juice Shop on port 4000
if [ ! -d /opt/juice4000 ]; then
    cd /opt
    git clone https://github.com/juice-shop/juice-shop.git juice4000
    cd juice4000
    cat > config/default.yml << 'CONFIG'
server:
  port: 4000
application:
  xssProtection: false
challenges:
  xssProtection: false
CONFIG
    npm install --production
fi

# Start Juice Shop
cd /opt/juice4000
pkill -f "node app.js"
nohup node app.js > /dev/null 2>&1 &

echo "Done! Services available at:"
echo "  http://155.138.197.128 - CTF"
echo "  http://155.138.197.128:4000 - Juice Shop"
ENDSCRIPT

bash /tmp/install.sh
'''

print(script)
print("-"*50)

print("\n3. The installation will take about 5-10 minutes")
print("   (npm install is the slow part)")
print("")
print("4. After completion, test:")
print("   http://155.138.197.128 - Should show CTF page")
print("   http://155.138.197.128:4000 - Should show Juice Shop")
print("")
print("5. Test DOM XSS on standalone:")
print("   Open http://155.138.197.128:4000")
print("   Press F12 for console")
print("   Type: location.href = '#/search?q=<iframe src=\"javascript:alert(1)\">'")
print("")
print("="*50)