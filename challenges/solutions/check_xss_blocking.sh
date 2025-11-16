#!/bin/bash
# Check what's blocking XSS on the server

echo "==========================================="
echo "🔍 CHECKING XSS BLOCKING CONFIGURATION"
echo "==========================================="

# Check if ModSecurity is enabled in Apache
echo -e "\n1. Checking Apache ModSecurity..."
if [ -f /etc/apache2/mods-enabled/security2.conf ]; then
    echo "ModSecurity is ENABLED - this could be blocking XSS"
    echo "Checking rules..."
    grep -r "SecRule" /etc/modsecurity/ 2>/dev/null | grep -i "script\|alert\|xss" | head -5
fi

# Check Apache configuration for filtering
echo -e "\n2. Checking Apache proxy configuration..."
grep -i "proxy\|rewrite\|filter\|substitute" /etc/apache2/sites-enabled/000-default-le-ssl.conf 2>/dev/null

# Check if there's any WAF in Docker
echo -e "\n3. Checking Docker containers..."
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"

# Check Juice Shop environment
echo -e "\n4. Checking Juice Shop container settings..."
docker inspect juice-shop | grep -A5 -B5 "Env\|CMD"

# Check iptables/firewall rules
echo -e "\n5. Checking firewall rules..."
iptables -L -n | grep -i "REJECT\|DROP" | head -5

# Check for any proxy filtering
echo -e "\n6. Testing direct access to Juice Shop..."
curl -s "http://localhost:3000/rest/products/search?q=<script>test</script>" -o /dev/null -w "Direct to port 3000: %{http_code}\n"
curl -s "https://juice3.wonkatech.org/rest/products/search?q=<script>test</script>" -o /dev/null -w "Through Apache proxy: %{http_code}\n"

echo -e "\n==========================================="
echo "SOLUTION: Disable ModSecurity temporarily"
echo "==========================================="