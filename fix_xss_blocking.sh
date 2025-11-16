#!/bin/bash
# Fix XSS blocking issue on the server

echo "==========================================="
echo "🔧 FIXING XSS BLOCKING ON SERVER"
echo "==========================================="

echo -e "\n1. Disabling ModSecurity if enabled..."
a2dismod security2 2>/dev/null || echo "ModSecurity not found or already disabled"

echo -e "\n2. Checking Apache configuration..."
# Remove any XSS filtering rules from Apache
sed -i 's/.*SecRuleEngine.*/#SecRuleEngine Off/g' /etc/apache2/apache2.conf 2>/dev/null
sed -i 's/.*SecRuleEngine.*/#SecRuleEngine Off/g' /etc/apache2/sites-enabled/*.conf 2>/dev/null

echo -e "\n3. Restarting Juice Shop container without security filters..."
docker stop juice-shop 2>/dev/null
docker rm juice-shop 2>/dev/null

# Start Juice Shop with XSS protection disabled
docker run -d \
  --name juice-shop \
  --restart unless-stopped \
  -p 3000:3000 \
  -e "NODE_ENV=development" \
  -e "NODE_CONFIG={\"challenges\":{\"xssProtection\":false},\"application\":{\"xssProtection\":false}}" \
  bkimminich/juice-shop

echo -e "\n4. Waiting for container to start..."
sleep 5

echo -e "\n5. Updating Apache proxy configuration..."
cat > /etc/apache2/sites-enabled/000-default-le-ssl.conf << 'EOF'
<VirtualHost *:443>
    ServerName juice3.wonkatech.org
    
    # Disable mod_security for this site
    <IfModule mod_security2.c>
        SecRuleEngine Off
    </IfModule>
    
    # Proxy to Juice Shop without filtering
    ProxyPreserveHost On
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/
    
    # Allow all methods and content
    <Proxy *>
        Order allow,deny
        Allow from all
    </Proxy>
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/juice3.wonkatech.org/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/juice3.wonkatech.org/privkey.pem
</VirtualHost>
EOF

echo -e "\n6. Reloading Apache..."
systemctl reload apache2

echo -e "\n7. Testing XSS endpoint..."
curl -s "http://localhost:3000/rest/products/search?q=<script>test</script>" -o /dev/null -w "Direct test: HTTP %{http_code}\n"

echo -e "\n==========================================="
echo "✅ XSS BLOCKING SHOULD BE DISABLED NOW"
echo "==========================================="
echo ""
echo "Try the DOM XSS challenge again:"
echo "1. Go to https://juice3.wonkatech.org"
echo "2. Open browser console (F12)"
echo "3. Type: location.href = \"#/search?q=<iframe src='javascript:alert(1)'>\""
echo ""
echo "If it still doesn't work, try accessing directly on port 3000:"
echo "http://155.138.197.128:3000"