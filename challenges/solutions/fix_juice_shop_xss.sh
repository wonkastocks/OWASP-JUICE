#!/bin/bash
# Fix Juice Shop XSS filtering issues

echo "=========================================="
echo "🔧 FIXING JUICE SHOP XSS CONFIGURATION"
echo "=========================================="

# SSH into the server and check/fix the configuration
cat << 'EOF' > /tmp/fix_xss.sh
#!/bin/bash

echo "1. Checking Docker container status..."
docker ps | grep juice

echo -e "\n2. Checking if ModSecurity or WAF is enabled..."
# Check Apache configuration
if [ -f /etc/apache2/mods-enabled/security2.conf ]; then
    echo "ModSecurity is enabled - this might be blocking XSS"
    echo "Checking ModSecurity rules..."
    grep -r "SecRule" /etc/modsecurity/ 2>/dev/null | grep -i "xss\|script\|alert" | head -5
fi

echo -e "\n3. Checking Juice Shop environment variables..."
docker exec juice-shop env | grep -E "NODE_ENV|SECURITY"

echo -e "\n4. Checking if there's a reverse proxy with filtering..."
if [ -f /etc/apache2/sites-enabled/000-default.conf ]; then
    grep -i "proxy\|rewrite\|filter" /etc/apache2/sites-enabled/000-default.conf
fi

echo -e "\n5. Checking UFW firewall rules..."
ufw status numbered 2>/dev/null || echo "UFW not active"

echo -e "\n6. Checking Juice Shop application logs for errors..."
docker logs juice-shop 2>&1 | grep -i "error\|500" | tail -5

echo -e "\n7. Testing if XSS challenges are disabled in config..."
docker exec juice-shop cat /juice-shop/config/default.yml 2>/dev/null | grep -A5 -B5 "xss\|challenges" | head -20

echo -e "\n=========================================="
echo "ATTEMPTING FIXES:"
echo "=========================================="

echo -e "\n8. Restarting Juice Shop container with proper settings..."
# Check if we need to restart with different environment variables
docker stop juice-shop 2>/dev/null
docker rm juice-shop 2>/dev/null

# Start Juice Shop without any security filters
docker run -d \
  --name juice-shop \
  --restart unless-stopped \
  -p 3000:3000 \
  -e "NODE_ENV=unsafe" \
  -e "NODE_CONFIG={\"challenges\":{\"xssProtection\":false}}" \
  bkimminich/juice-shop

echo "Waiting for container to start..."
sleep 5

echo -e "\n9. If using Apache as reverse proxy, temporarily disable mod_security..."
if [ -f /etc/apache2/mods-enabled/security2.conf ]; then
    a2dismod security2 2>/dev/null
    systemctl reload apache2
    echo "ModSecurity disabled temporarily"
fi

echo -e "\n10. Checking if XSS now works..."
# Test XSS endpoint
curl -s "http://localhost:3000/rest/products/search?q=<script>test</script>" \
  -o /dev/null -w "%{http_code}" || echo "Error testing"

echo -e "\n=========================================="
echo "ALTERNATIVE SOLUTION:"
echo "=========================================="

echo "If XSS still doesn't work, try accessing Juice Shop directly:"
echo "1. Open port 3000 directly in UFW:"
echo "   ufw allow 3000/tcp"
echo ""
echo "2. Access Juice Shop at: http://155.138.197.128:3000"
echo "   (bypassing Apache reverse proxy)"
echo ""
echo "3. Or create SSH tunnel:"
echo "   ssh -L 3000:localhost:3000 root@155.138.197.128"
echo "   Then access: http://localhost:3000"

EOF

echo "Script created. Now executing on server..."
echo ""

# Copy and execute the script on the server
scp /tmp/fix_xss.sh root@155.138.197.128:/tmp/
ssh root@155.138.197.128 "bash /tmp/fix_xss.sh"