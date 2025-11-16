# 🥤 OWASP Juice Shop - All 110 Challenges Complete Guide

## 📊 Challenge Overview
- **Total Challenges**: 110
- **Instance URL**: https://juice3.wonkatech.org
- **Score Board**: https://juice3.wonkatech.org/#/score-board

## 🎯 Challenges by Difficulty Level

### Level 1 (⭐) - 14 Challenges

1. **Bonus Payload** - XSS
   - Solution: Use SoundCloud iframe XSS payload in search
   - URL: `/#/search?q=<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076"></iframe>`

2. **Bully Chatbot** - Miscellaneous
   - Solution: Repeatedly ask chatbot for coupon (10-20 times)
   - Manual interaction required in Support Chat

3. **Confidential Document** - Sensitive Data Exposure
   - Solution: Access `/ftp/acquisitions.md`
   - Direct URL: https://juice3.wonkatech.org/ftp/acquisitions.md

4. **DOM XSS** - XSS
   - Solution: Search with `<iframe src="javascript:alert(`xss`)">`
   - URL: `/#/search?q=<iframe src="javascript:alert(`xss`)">`

5. **Error Handling** - Security Misconfiguration
   - Solution: Access non-existent API endpoint
   - URL: https://juice3.wonkatech.org/rest/qwertz

6. **Exposed Metrics** - Sensitive Data Exposure
   - Solution: Access Prometheus metrics endpoint
   - URL: https://juice3.wonkatech.org/metrics

7. **Mass Dispel** - Miscellaneous
   - Solution: Click 'X' to close all notifications at once
   - Manual action required

8. **Missing Encoding** - Improper Input Validation
   - Solution: Access photo with emoji in filename
   - URL: `/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg`

9. **Outdated Allowlist** - Unvalidated Redirects
   - Solution: Redirect to outdated domain
   - URL: `/redirect?to=https://blockchain.info`

10. **Privacy Policy** - Miscellaneous
    - Solution: Navigate to privacy policy page
    - URL: https://juice3.wonkatech.org/#/privacy-security

11. **Repetitive Registration** - Improper Input Validation
    - Solution: Register without password repeat field
    - API: POST `/api/Users/` with only email and password

12. **Score Board** - Miscellaneous
    - Solution: Find hidden score board
    - URL: https://juice3.wonkatech.org/#/score-board

13. **Web3 Sandbox** - Broken Access Control
    - Solution: Access Web3 sandbox
    - URL: https://juice3.wonkatech.org/#/web3-sandbox

14. **Zero Stars** - Improper Input Validation
    - Solution: Give product 0 stars rating
    - API: PUT `/api/Feedbacks/` with rating: 0

### Level 2 (⭐⭐) - 15 Challenges

15. **Admin Section** - Broken Access Control
    - Solution: Access administration panel
    - URL: https://juice3.wonkatech.org/#/administration

16. **Deprecated Interface** - Security Misconfiguration
    - Solution: Upload XML file to deprecated B2B interface
    - Use file upload with XML content

17. **Empty User Registration** - Improper Input Validation
    - Solution: Register with empty email
    - API: POST `/api/Users/` with empty email field

18. **Exposed credentials** - Sensitive Data Exposure
    - Solution: Find backup files in FTP
    - URL: `/ftp/package.json.bak`

19. **Five-Star Feedback** - Broken Access Control
    - Solution: Delete all 5-star feedback
    - API: DELETE `/api/Feedbacks/{id}` for 5-star reviews

20. **Login Admin** - Injection
    - Solution: SQL injection on login
    - Payload: `admin@juice-sh.op'--`

21. **Login MC SafeSearch** - Sensitive Data Exposure
    - Solution: Login with password "Mr. N00dles"
    - Credentials: mc.safesearch@juice-sh.op / Mr. N00dles

22. **Meta Geo Stalking** - Sensitive Data Exposure
    - Solution: Extract EXIF data from uploaded images
    - Check photo wall images for metadata

23. **NFT Takeover** - Sensitive Data Exposure
    - Solution: Take over NFT in Web3 sandbox
    - Manipulate NFT ownership

24. **Password Strength** - Broken Authentication
    - Solution: Login admin with weak password
    - Password: admin123

25. **Reflected XSS** - XSS
    - Solution: XSS in order tracking
    - URL: `/track-result?id=<iframe src='javascript:alert(`xss`)'>`

26. **Security Policy** - Miscellaneous
    - Solution: Access security.txt
    - URL: https://juice3.wonkatech.org/.well-known/security.txt

27. **View Basket** - Broken Access Control
    - Solution: View another user's basket
    - API: GET `/rest/basket/{id}` with different IDs

28. **Visual Geo Stalking** - Sensitive Data Exposure
    - Solution: Find location from photo wall images
    - Analyze background/landmarks in photos

29. **Weird Crypto** - Cryptographic Issues
    - Solution: Solve crypto puzzle in Web3 sandbox
    - Involves MD5 hash collisions

### Level 3 (⭐⭐⭐) - 24 Challenges

30. **API-only XSS** - XSS
    - Solution: Persisted XSS via API without frontend
    - API: POST to reviews endpoint with XSS payload

31. **Admin Registration** - Improper Input Validation
    - Solution: Register with admin role
    - API: POST `/api/Users/` with role: "admin"

32. **Bjoern's Favorite Pet** - Broken Authentication
    - Solution: Reset password with security answer
    - Answer: "Zaya" or "Lenny"

33. **CAPTCHA Bypass** - Broken Anti Automation
    - Solution: Submit feedback 10+ times rapidly
    - Ignore CAPTCHA field in requests

34. **Client-side XSS Protection** - XSS
    - Solution: Bypass client filter with alternate payload
    - Payload: `<<SCRIPT>alert('XSS')//<</SCRIPT>`

35. **CSRF** - Broken Access Control
    - Solution: Change password without CSRF token
    - Create malicious form

36. **Database Schema** - Injection
    - Solution: Extract schema via SQL injection
    - Payload: `' UNION SELECT sql FROM sqlite_master--`

37. **Deluxe Fraud** - Improper Input Validation
    - Solution: Get deluxe membership without payment
    - Manipulate payment flow

38. **Forged Feedback** - Broken Access Control
    - Solution: Post feedback as another user
    - API: PUT `/api/Feedbacks/` with different UserId

39. **Forged Review** - Broken Access Control
    - Solution: Post review as another user
    - API: PUT `/api/Products/1/reviews` with author field

40. **GDPR Data Erasure** - Broken Authentication
    - Solution: Delete user data
    - Use data erasure feature

41. **Login Amy** - Sensitive Data Exposure
    - Solution: Login with password from comic
    - Password: K1f.....................

42. **Login Bender** - Injection
    - Solution: SQL injection login
    - Payload: `bender@juice-sh.op'--`

43. **Login Jim** - Injection
    - Solution: SQL injection login
    - Payload: `jim@juice-sh.op'--`

44. **Manipulate Basket** - Broken Access Control
    - Solution: Add negative quantity to basket
    - API: POST `/api/BasketItems/` with quantity: -10

45. **Mint the Honey Pot** - Improper Input Validation
    - Solution: Mint NFT honey pot
    - Use Web3 sandbox features

46. **Payback Time** - Improper Input Validation
    - Solution: Checkout with negative total
    - Add negative quantities then checkout

47. **Privacy Policy Inspection** - Security through Obscurity
    - Solution: Find hot link in privacy policy
    - Check privacy policy carefully

48. **Product Tampering** - Broken Access Control
    - Solution: Change product description
    - API: PUT `/api/Products/1` with new description

49. **Reset Jim's Password** - Broken Authentication
    - Solution: Reset with security answer
    - Answer: "Samuel" or about replicants

50. **Security Advisory** - Miscellaneous
    - Solution: Find security advisory
    - Check security-related pages

51. **Upload Size** - Improper Input Validation
    - Solution: Upload file >100KB
    - Bypass client-side size check

52. **Upload Type** - Improper Input Validation
    - Solution: Upload non-PDF file
    - Change content-type header

53. **XXE Data Access** - XXE
    - Solution: XXE to read files
    - XML: `<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>`

### Level 4 (⭐⭐⭐⭐) - 25 Challenges

54. **Access Log** - Sensitive Data Exposure
    - Solution: Access server logs
    - URL: `/support/logs` or similar

55. **Allowlist Bypass** - Unvalidated Redirects
    - Solution: Bypass redirect allowlist
    - Use URL encoding or case variations

56. **Christmas Special** - Injection
    - Solution: SQL injection with special date
    - Search for products on Christmas

57. **CSP Bypass** - XSS
    - Solution: Bypass Content Security Policy
    - Use allowed sources for XSS

58. **Easter Egg** - Broken Access Control
    - Solution: Find 3D easter egg
    - URL: `/ftp/easter.egg`

59. **Ephemeral Accountant** - Injection
    - Solution: Login as accountant
    - Use NoSQL injection

60. **Expired Coupon** - Improper Input Validation
    - Solution: Use expired coupon
    - Manipulate date or use old codes

61. **Forgotten Developer Backup** - Sensitive Data Exposure
    - Solution: Find developer backup
    - URL: `/ftp/package.json.bak`

62. **Forgotten Sales Backup** - Sensitive Data Exposure
    - Solution: Find sales backup
    - URL: `/ftp/coupons_2013.md.bak`

63. **GDPR Data Theft** - Sensitive Data Exposure
    - Solution: Steal personal data
    - Export all user data

64. **HTTP-Header XSS** - XSS
    - Solution: XSS via HTTP headers
    - Use True-Client-IP header

65. **Leaked API Key** - Sensitive Data Exposure
    - Solution: Find API keys in code
    - Check JavaScript files

66. **Leaked Unsafe Product** - Sensitive Data Exposure
    - Solution: Find recalled product
    - Access hidden product pages

67. **Legacy Typosquatting** - Vulnerable Components
    - Solution: Find typosquatted package
    - Check package.json dependencies

68. **Login Bjoern** - Broken Authentication
    - Solution: Login as Bjoern
    - OAuth bypass or password

69. **Misplaced Signature File** - Sensitive Data Exposure
    - Solution: Find signature file
    - URL: `/ftp/suspicious_errors.yml`

70. **Nested Easter Egg** - Cryptographic Issues
    - Solution: Find nested easter egg
    - Decode multiple layers

71. **NoSQL DoS** - Injection
    - Solution: DoS via NoSQL injection
    - Use sleep operators

72. **NoSQL Manipulation** - Injection
    - Solution: Manipulate NoSQL queries
    - Use MongoDB operators

73. **Poison Null Byte** - Improper Input Validation
    - Solution: Use null byte injection
    - Add %00 to bypass filters

74. **Reset Bender's Password** - Broken Authentication
    - Solution: Reset via security question
    - Answer related to Futurama

75. **Reset Uvogin's Password** - Sensitive Data Exposure
    - Solution: Reset via security question
    - Answer from social media

76. **Server-side XSS Protection** - XSS
    - Solution: Bypass server XSS filter
    - Use encoding or obfuscation

77. **Steganography** - Security through Obscurity
    - Solution: Find hidden message in image
    - Analyze images for stego

78. **User Credentials** - Injection
    - Solution: Extract all credentials via SQLi
    - UNION SELECT passwords

### Level 5 (⭐⭐⭐⭐⭐) - 20 Challenges

79. **Blockchain Hype** - Security through Obscurity
    - Solution: Find blockchain reference
    - Check whitepapers

80. **Blocked RCE DoS** - Insecure Deserialization
    - Solution: Attempt RCE that gets blocked
    - Serialize malicious object

81. **Change Bender's Password** - Broken Authentication
    - Solution: Change password without old one
    - CSRF or authorization bypass

82. **Cross-Site Imaging** - Security Misconfiguration
    - Solution: Embed image from another site
    - Use image upload feature

83. **Email Leak** - Sensitive Data Exposure
    - Solution: Access all email addresses
    - API endpoint enumeration

84. **Extra Language** - Broken Anti Automation
    - Solution: Add Klingon language
    - Manipulate language files

85. **Frontend Typosquatting** - Vulnerable Components
    - Solution: Find frontend typo package
    - Check npm dependencies

86. **Kill Chatbot** - Vulnerable Components
    - Solution: Crash the chatbot
    - Send malformed input

87. **Leaked API Key** - Sensitive Data Exposure
    - Solution: Find API keys
    - Check source code

88. **Leaked Access Logs** - Sensitive Data Exposure
    - Solution: Find access logs
    - Directory traversal

89. **Local File Read** - Vulnerable Components
    - Solution: Read local files
    - Path traversal vulnerability

90. **Memory Bomb** - Insecure Deserialization
    - Solution: Cause memory exhaustion
    - Send large deserialized object

91. **NoSQL Exfiltration** - Injection
    - Solution: Extract data via NoSQL
    - Use aggregation pipeline

92. **Reset Bjoern's Password** - Broken Authentication
    - Solution: Reset via CAPTCHA bypass
    - Manipulate reset flow

93. **Reset Morty's Password** - Broken Anti Automation
    - Solution: Reset via answer
    - Answer: 5N0wb41l

94. **Retrieve Blueprint** - Sensitive Data Exposure
    - Solution: Find blueprint file
    - Check FTP directory

95. **Supply Chain Attack** - Vulnerable Components
    - Solution: Find malicious dependency
    - Check lock files

96. **Two Factor Authentication** - Broken Authentication
    - Solution: Bypass 2FA
    - Use TOTP manipulation

97. **Unsigned JWT** - Vulnerable Components
    - Solution: Forge unsigned JWT
    - Set alg: none

98. **XXE DoS** - XXE
    - Solution: DoS via XXE
    - Billion laughs attack

### Level 6 (⭐⭐⭐⭐⭐⭐) - 12 Challenges

99. **Arbitrary File Write** - Vulnerable Components
    - Solution: Write to arbitrary location
    - Zip slip vulnerability

100. **Forged Coupon** - Cryptographic Issues
     - Solution: Create valid coupon
     - Forge Z85 encoded coupon

101. **Forged Signed JWT** - Vulnerable Components
     - Solution: Forge RSA signed JWT
     - Key confusion attack

102. **Imaginary Challenge** - Cryptographic Issues
     - Solution: Solve imaginary challenge
     - Find in obfuscated code

103. **Login Support Team** - Security Misconfiguration
     - Solution: Login as support
     - Default credentials

104. **Multiple Likes** - Broken Anti Automation
     - Solution: Like review multiple times
     - Race condition exploit

105. **Premium Paywall** - Cryptographic Issues
     - Solution: Bypass paywall
     - Manipulate JWT claims

106. **SSRF** - Broken Access Control
     - Solution: Server-Side Request Forgery
     - Make server request internal URL

107. **SSTi** - Injection
     - Solution: Server-Side Template Injection
     - Inject template code

108. **Successful RCE DoS** - Insecure Deserialization
     - Solution: Successful RCE
     - Execute commands on server

109. **Video XSS** - XSS
     - Solution: XSS in video upload
     - Embed XSS in video metadata

110. **Wallet Depletion** - Miscellaneous
     - Solution: Drain wallet
     - Exploit payment system

## 🛠️ Tools and Scripts

### Master Solver Script
```bash
#!/bin/bash
# Run all automated challenges
./master_solver.sh
```

### Python Solvers
- `complete_solver.py` - Level 1-2 challenges
- `advanced_solver.py` - Level 2-3 challenges
- `ultimate_solver.py` - Comprehensive solver

### Manual Challenges
Some challenges require manual interaction:
- Bully Chatbot - Chat interaction
- Mass Dispel - Click notifications
- Visual inspections - Photo analysis

## 📈 Progress Tracking

Use the Score Board to track progress:
https://juice3.wonkatech.org/#/score-board

Current Status: 19/110 challenges completed

## 🎓 Learning Resources

- [OWASP Juice Shop Official Docs](https://owasp.org/www-project-juice-shop/)
- [Pwning OWASP Juice Shop](https://pwning.owasp-juice.shop/)
- [YouTube Walkthroughs](https://www.youtube.com/playlist?list=PLcsrjMNFrcmbAFV8BxDKXZCcPrOlaYfWK)

## ⚠️ Disclaimer

These solutions are for educational purposes only. Only use on authorized instances like the WonkaTech CTF platform.