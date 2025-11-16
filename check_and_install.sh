#!/bin/bash
# Check current status and install if needed

echo "==========================================="
echo "🔍 CHECKING SERVER STATUS"
echo "==========================================="

echo -e "\n1. Checking if Node.js is installed..."
which node && node --version || echo "Node.js not installed"

echo -e "\n2. Checking if any Juice Shop is running..."
ps aux | grep -E "juice|node" | grep -v grep || echo "No Juice Shop processes found"

echo -e "\n3. Checking listening ports..."
netstat -tlnp | grep -E ":3000|:4000|:8080" || echo "No relevant ports listening"

echo -e "\n4. Checking Docker containers..."
docker ps | grep juice || echo "No Juice Shop containers running"

echo -e "\n5. Checking systemd services..."
systemctl status juice-standalone 2>/dev/null || echo "juice-standalone service not found"

echo -e "\n6. Checking if /opt/juice-shop-standalone exists..."
ls -la /opt/juice-shop-standalone 2>/dev/null || echo "Directory does not exist"

echo -e "\n7. Checking firewall rules..."
ufw status | grep 4000 || echo "Port 4000 not in firewall rules"

echo ""
echo "==========================================="
echo "📝 INSTALLATION STATUS"
echo "==========================================="
echo "The standalone Juice Shop is NOT installed yet."
echo "Run the installation script to set it up."