#!/bin/bash
echo "========================================="
echo "RESTORING JUICE SHOP DOCKER SETUP"
echo "========================================="

# 1. Check and restart Docker containers
echo "[1/5] Checking Docker containers..."
docker ps -a | grep juice

# 2. Restart the Juice Shop containers
echo "[2/5] Restarting Juice Shop containers..."
for i in 1 2 3; do
    docker restart juice-shop-instance-$i 2>/dev/null || {
        echo "Starting juice-shop-instance-$i..."
        docker run -d --name juice-shop-instance-$i \
            -p 300$i:3000 \
            -e NODE_ENV=unsafe \
            bkimminich/juice-shop
    }
done

# 3. Configure Cloudflare Tunnel
echo "[3/5] Checking Cloudflare tunnel..."
systemctl status cloudflared || {
    echo "Restarting Cloudflare tunnel..."
    systemctl restart cloudflared
}

# 4. Check tunnel configuration
echo "[4/5] Verifying tunnel configuration..."
cat /etc/cloudflared/config.yml

# 5. Test connectivity
echo "[5/5] Testing services..."
echo ""
echo "Local Docker instances:"
curl -s http://localhost:3001 -o /dev/null -w "  Instance 1 (3001): %{http_code}\n"
curl -s http://localhost:3002 -o /dev/null -w "  Instance 2 (3002): %{http_code}\n"
curl -s http://localhost:3003 -o /dev/null -w "  Instance 3 (3003): %{http_code}\n"

echo ""
echo "========================================="
echo "RESTORATION COMPLETE!"
echo "========================================="
echo ""
echo "Access Juice Shop at:"
echo "  https://juice1.wonkatech.org"
echo "  https://juice2.wonkatech.org"
echo "  https://juice3.wonkatech.org"