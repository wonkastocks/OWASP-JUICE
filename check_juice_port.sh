#!/bin/bash
# Check what port Juice Shop is actually running on

echo "==========================================="
echo "🔍 CHECKING JUICE SHOP PORT CONFIGURATION"
echo "==========================================="

echo -e "\n1. Checking Docker containers and ports..."
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}" | grep -E "juice|NAMES"

echo -e "\n2. Checking all listening ports..."
netstat -tlnp | grep -E "LISTEN|docker|node" | head -20

echo -e "\n3. Checking Apache proxy configuration..."
grep -E "ProxyPass|localhost" /etc/apache2/sites-enabled/*.conf | head -10

echo -e "\n4. Checking specific Juice Shop containers..."
docker ps -a | grep juice

echo -e "\n5. Checking if there are multiple Juice Shop instances..."
docker ps --format "{{.Names}}" | grep juice | while read container; do
    echo "Container: $container"
    docker inspect $container | grep -E "HostPort|ContainerPort" | head -10
done

echo -e "\n6. Testing different ports..."
for port in 3000 3001 3002 3003 3004 3005 8080 8000; do
    curl -s "http://localhost:$port" -o /dev/null -w "Port $port: %{http_code}\n" --connect-timeout 1
done

echo -e "\n7. Checking iptables rules..."
iptables -L -n -t nat | grep -E "DNAT|3000|juice" | head -10

echo -e "\n8. Getting full container details..."
docker inspect juice-shop 2>/dev/null | grep -A10 -B10 "Ports" || echo "juice-shop container not found"

# Check for other juice containers
for i in 1 2 3 4 5; do
    if docker inspect juice$i 2>/dev/null | grep -A10 "Ports" > /dev/null; then
        echo -e "\nFound juice$i container:"
        docker inspect juice$i | grep -A10 "Ports"
    fi
done