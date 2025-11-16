#!/bin/bash

echo "Attempting to diagnose and fix juice10 issue..."

# Since SSH port 22 is closed, we need an alternative approach
# The 502 error means Cloudflare can't reach the backend

echo "Current status of juice10:"
curl -I https://juice10.wonkatech.org 2>/dev/null | head -5

echo ""
echo "Issue Summary:"
echo "- juice10.wonkatech.org returns 502 Bad Gateway"
echo "- This means the Docker container 'juice10' is likely stopped or crashed"
echo "- SSH port 22 is closed on 155.138.197.128"
echo ""
echo "Containers needing restart:"
echo "- juice4 through juice13 (10 containers total)"
echo ""
echo "To fix this issue, you need to:"
echo "1. Access the server console via Vultr dashboard"
echo "2. SSH in locally or use the web console"
echo "3. Run: docker start juice10"
echo "4. Or restart all stopped containers:"
echo "   for i in {4..13}; do docker start juice\$i; done"
echo ""
echo "Working instances (for reference):"
echo "- juice1, juice2, juice3, juice14, juice15"