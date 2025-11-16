#!/bin/bash
# Fix Juice Shop Docker instance and Cloudflare tunnel

echo "==========================================="
echo "🔧 FIXING JUICE SHOP DOCKER INSTANCE"
echo "==========================================="

echo -e "\n1. Checking Docker container status..."
docker ps -a | grep juice || echo "No Juice Shop containers found"

echo -e "\n2. Checking if container needs restart..."
docker ps | grep juice
if [ $? -ne 0 ]; then
    echo "Container not running, attempting to start..."
    docker start juice-shop || docker start juice3 || docker start juice1
fi

echo -e "\n3. Checking Cloudflare tunnel status..."
ps aux | grep cloudflared | grep -v grep || echo "Cloudflare tunnel not running"

echo -e "\n4. Checking tunnel configuration..."
ls -la /root/.cloudflared/ 2>/dev/null || echo "Cloudflare config not found"

echo -e "\n5. Checking Apache proxy status..."
systemctl status apache2 | head -10

echo -e "\n6. Testing local access..."
curl -s http://localhost:3000 -o /dev/null -w "Local port 3000: %{http_code}\n" || echo "Port 3000 not responding"
curl -s http://localhost:3001 -o /dev/null -w "Local port 3001: %{http_code}\n" || echo "Port 3001 not responding"

echo -e "\n7. Checking DNS resolution..."
nslookup juice3.wonkatech.org

echo -e "\n8. If container is down, restart it..."
docker restart juice-shop 2>/dev/null || docker restart juice3 2>/dev/null || {
    echo "Starting new container..."
    docker run -d --name juice-shop --restart unless-stopped -p 3000:3000 bkimminich/juice-shop
}

echo -e "\n9. Final status check..."
docker ps | grep juice && echo "✅ Container is running" || echo "❌ Container failed to start"

echo ""
echo "==========================================="
echo "📝 NEXT STEPS IF STILL BROKEN:"
echo "==========================================="
echo "1. Check Cloudflare Dashboard for tunnel status"
echo "2. Restart cloudflared service if needed"
echo "3. Check Apache configuration"
echo "4. Verify DNS points to correct tunnel"