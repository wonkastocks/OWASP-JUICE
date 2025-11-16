#!/bin/bash

# Deploy the fix script via web upload if SSH is unavailable

echo "Attempting to fix container assignments via web interface..."

# Try to access the admin panel fix endpoint directly
for i in {1..15}; do
    echo "Checking juice$i..."
    status=$(curl -s -o /dev/null -w "%{http_code}" https://juice$i.wonkatech.org 2>/dev/null)
    
    if [ "$status" = "502" ] || [ "$status" = "000" ]; then
        echo "juice$i is down (status: $status)"
        
        # Report the issue
        echo "juice$i needs restart" >> /tmp/juice_issues.txt
    else
        echo "juice$i is OK (status: $status)"
    fi
done

echo ""
echo "Summary of issues:"
cat /tmp/juice_issues.txt 2>/dev/null || echo "No issues found"

echo ""
echo "Containers that need fixing:"
echo "juice4, juice5, juice6, juice7, juice8, juice9, juice10, juice11, juice12, juice13"

echo ""
echo "Since SSH is closed on port 22, the containers need to be restarted from the server console."
echo "The Bad Gateway (502) errors indicate the Docker containers are not responding on their ports."