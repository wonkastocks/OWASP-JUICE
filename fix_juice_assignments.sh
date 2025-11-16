#!/bin/bash

# Fix container assignments and Bad Gateway issues

echo "=== Fixing Container Assignments and Bad Gateway Issues ==="

# Step 1: Check container status
echo "Checking container status..."
sshpass -p 'Ocean4Waves' ssh -o StrictHostKeyChecking=no root@155.138.197.128 "docker ps -a | grep juice"

# Step 2: Restart stopped containers
echo "Restarting any stopped containers..."
sshpass -p 'Ocean4Waves' ssh -o StrictHostKeyChecking=no root@155.138.197.128 "
docker ps -a | grep 'Exited' | grep juice | awk '{print \$NF}' | while read container; do 
    echo \"Restarting \$container\"
    docker start \$container
    sleep 2
done
"

# Step 3: Update database assignments
echo "Updating container assignments in database..."
sshpass -p 'Ocean4Waves' ssh -o StrictHostKeyChecking=no root@155.138.197.128 "mysql -u root ctf_platform << 'EOF'
-- Clear existing assignments
UPDATE containers SET user_id = NULL, allocated = 0;

-- Assign containers based on users table
UPDATE containers c
JOIN users u ON u.instance_url = CONCAT('https://juice', c.container_id, '.wonkatech.org')
SET c.user_id = u.id, c.allocated = 1
WHERE u.instance_url IS NOT NULL;

-- Show assignments
SELECT c.container_id, c.container_name, u.username, c.allocated, c.status
FROM containers c
LEFT JOIN users u ON c.user_id = u.id
ORDER BY c.container_id;
EOF"

# Step 4: Check each instance
echo "Testing each Juice Shop instance..."
for i in {1..15}; do
    echo -n "juice$i: "
    status=$(curl -s -o /dev/null -w "%{http_code}" https://juice$i.wonkatech.org 2>/dev/null)
    if [ "$status" = "200" ] || [ "$status" = "301" ] || [ "$status" = "302" ]; then
        echo "OK ($status)"
    else
        echo "FAILED ($status) - Attempting fix..."
        # Try to restart the specific container
        sshpass -p 'Ocean4Waves' ssh -o StrictHostKeyChecking=no root@155.138.197.128 "
            docker stop juice$i 2>/dev/null
            docker rm juice$i 2>/dev/null
            docker run -d --name juice$i -p $((3000 + i)):3000 bkimminich/juice-shop
        "
    fi
done

echo "=== Fix Complete ==="
echo "Check admin panel at: https://wonkatech.org/admin/containers.php"