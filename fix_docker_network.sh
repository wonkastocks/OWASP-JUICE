#!/bin/bash

cat << 'FIX_EOF' > /tmp/fix_docker_network.sh
#!/bin/bash

echo "================================================"
echo "Fixing Docker Network Issues"
echo "================================================"

# Step 1: Fix iptables
echo "Step 1: Fixing iptables..."
systemctl restart docker
sleep 5

# Step 2: Remove old networks and containers
echo "Step 2: Cleaning up Docker..."
cd /opt/juice-shop-ctf
docker-compose down 2>/dev/null
docker network prune -f
docker container prune -f

# Step 3: Restart Docker
echo "Step 3: Restarting Docker service..."
systemctl restart docker
sleep 10

# Step 4: Start services again
echo "Step 4: Starting services..."
cd /opt/juice-shop-ctf
docker-compose up -d

# Wait for services
echo "Waiting for services to start..."
sleep 30

# Step 5: Check status
echo ""
echo "Step 5: Checking service status..."
docker ps

echo ""
echo "Step 6: Testing services..."
# Test Juice Shop
echo -n "Juice Shop (port 3000): "
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 && echo " ✓ OK" || echo " ✗ Failed"

# Test CTFd
echo -n "CTFd (port 8000): "
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 && echo " ✓ OK" || echo " ✗ Failed"

# Test nginx proxy
echo -n "Nginx proxy (port 8080): "
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 && echo " ✓ OK" || echo " ✗ Failed"

echo ""
echo "================================================"
echo "✓ Docker network fixed!"
echo "================================================"
FIX_EOF

echo "Fix script created at /tmp/fix_docker_network.sh"