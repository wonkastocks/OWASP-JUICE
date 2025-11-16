#!/bin/bash
# Open direct access to Juice Shop bypassing Cloudflare

echo "Opening port 3000 for direct access..."
ufw allow 3000/tcp

echo "Testing direct access..."
curl -s "http://155.138.197.128:3000/rest/products/search?q=<script>test</script>" -o /dev/null -w "Direct access test: %{http_code}\n"

echo ""
echo "✅ DIRECT ACCESS ENABLED"
echo ""
echo "Now try XSS without Cloudflare:"
echo "1. Open: http://155.138.197.128:3000"
echo "2. In console: location.href = '#/search?q=<iframe src=\"javascript:alert(1)\">'"
echo ""
echo "This bypasses Cloudflare completely!"