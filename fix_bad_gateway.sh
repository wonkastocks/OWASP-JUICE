#!/bin/bash
# Fix bad gateway error - restart Docker container and check services

echo "==========================================="
echo "🔧 FIXING BAD GATEWAY ERROR"
echo "==========================================="

echo -e "\n1. Checking Docker containers..."
docker ps -a | grep -E "juice|wonka" || echo "No containers found"

echo -e "\n2. Restarting any stopped containers..."
# Try to restart various possible container names
docker start juice-shop 2>/dev/null || echo "juice-shop not found"
docker start juice3 2>/dev/null || echo "juice3 not found"
docker start juice1 2>/dev/null || echo "juice1 not found"
docker start wonka 2>/dev/null || echo "wonka not found"

echo -e "\n3. If no containers exist, create new one..."
if ! docker ps | grep -q juice; then
    echo "Creating new Juice Shop container..."
    docker run -d \
        --name juice-shop \
        --restart unless-stopped \
        -p 3000:3000 \
        bkimminich/juice-shop
    echo "Waiting for container to start..."
    sleep 10
fi

echo -e "\n4. Checking Apache status..."
systemctl status apache2 | grep Active || systemctl restart apache2

echo -e "\n5. Checking Cloudflare tunnel..."
ps aux | grep cloudflared | grep -v grep
if [ $? -ne 0 ]; then
    echo "Cloudflare tunnel not running!"
    # Check if cloudflared is installed
    which cloudflared && {
        echo "Starting cloudflared tunnel..."
        # Try to start tunnel (config dependent)
        cloudflared tunnel run 2>/dev/null &
    } || echo "cloudflared not installed"
fi

echo -e "\n6. Testing local endpoints..."
curl -s http://localhost:3000 -o /dev/null -w "Port 3000: %{http_code}\n" || echo "Port 3000 down"
curl -s http://localhost:80 -o /dev/null -w "Port 80: %{http_code}\n" || echo "Port 80 down"
curl -s http://localhost:443 -o /dev/null -w "Port 443: %{http_code}\n" || echo "Port 443 down"

echo -e "\n7. Checking what's on port 3000..."
netstat -tlnp | grep :3000 || echo "Nothing listening on port 3000"

echo -e "\n8. Docker logs (last 20 lines)..."
docker logs juice-shop 2>&1 | tail -20 || docker logs juice3 2>&1 | tail -20 || echo "No logs available"

echo -e "\n9. Final container status..."
docker ps | grep juice && echo "✅ Container running" || {
    echo "❌ No container running - starting one..."
    docker run -d --name juice-main --restart unless-stopped -p 3000:3000 bkimminich/juice-shop
}

echo ""
echo "==========================================="
echo "✅ FIXES APPLIED"
echo "==========================================="
echo ""
echo "The container should now be running on port 3000"
echo "Check https://juice3.wonkatech.org in a minute"
echo ""
echo "If still broken, check:"
echo "1. Cloudflare tunnel configuration"
echo "2. DNS settings in Cloudflare"
echo "3. Apache proxy settings"