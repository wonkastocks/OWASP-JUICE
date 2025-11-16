# OWASP Juice Shop - Complete Challenge Writeups

## 110 Comprehensive Challenge Solutions

This directory contains detailed, educational writeups for all 110 OWASP Juice Shop challenges.

### Writeup Structure

Each writeup includes:
- ✅ Introduction & Vulnerability Explanation
- ✅ CVSS Scores & CVE References
- ✅ 5-10 Real-World Examples
- ✅ Terms & Glossary
- ✅ Attack Types & Tools
- ✅ Mermaid Diagrams (Attack Flow & Architecture)
- ✅ Mitigations & Secure Code Examples
- ✅ Manual & Automated Solutions (Python)
- ✅ 10 Discussion Questions with Answers
- ✅ 10 NIST References (APA Format)

---

## Challenges by Category


### Broken Access Control (11 challenges)

- [Admin Section](./Broken_Access_Control/Admin_Section.md) - ⭐ - Access the administration section of the store
- [View Basket](./Broken_Access_Control/View_Basket.md) - ⭐⭐ - View another user's shopping basket
- [Five-Star Feedback](./Broken_Access_Control/Five-Star_Feedback.md) - ⭐⭐ - Get rid of all 5-star customer feedback
- [Forged Feedback](./Broken_Access_Control/Forged_Feedback.md) - ⭐⭐⭐ - Post feedback in another user's name
- [Manipulate Basket](./Broken_Access_Control/Manipulate_Basket.md) - ⭐⭐⭐ - Put an additional product into another user's shopping basket
- [Product Tampering](./Broken_Access_Control/Product_Tampering.md) - ⭐⭐⭐ - Change the href of the link within the OWASP SSL Advanced Forensic Tool (O-Saft) product description
- [Forged Review](./Broken_Access_Control/Forged_Review.md) - ⭐⭐⭐ - Post a product review as another user or edit any user's existing review
- [Deluxe Fraud](./Broken_Access_Control/Deluxe_Fraud.md) - ⭐⭐⭐ - Obtain a Deluxe Membership without paying for it
- [Privacy Policy Inspection](./Broken_Access_Control/Privacy_Policy_Inspection.md) - ⭐⭐⭐ - Prove that you actually read our privacy policy
- [GDPR Data Theft](./Broken_Access_Control/GDPR_Data_Theft.md) - ⭐⭐⭐⭐ - Steal someone else's personal data without using Injection
- [Easter Egg](./Broken_Access_Control/Easter_Egg.md) - ⭐⭐⭐⭐ - Find the hidden easter egg

### Broken Authentication (7 challenges)

- [Password Strength](./Broken_Authentication/Password_Strength.md) - ⭐⭐ - Log in with the administrator's user credentials without SQL Injection
- [Login Admin](./Broken_Authentication/Login_Admin.md) - ⭐⭐ - Log in with the administrator's user account
- [Login Jim](./Broken_Authentication/Login_Jim.md) - ⭐⭐⭐ - Log in with Jim's user account
- [Login Bender](./Broken_Authentication/Login_Bender.md) - ⭐⭐⭐ - Log in with Bender's user account
- [GDPR Data Erasure](./Broken_Authentication/GDPR_Data_Erasure.md) - ⭐⭐⭐ - Log in with Chris' erased user account
- [Reset Password](./Broken_Authentication/Reset_Password.md) - ⭐⭐⭐⭐ - Reset Jim's password via the Forgot Password mechanism
- [Reset Bjoern's Password](./Broken_Authentication/Reset_Bjoern's_Password.md) - ⭐⭐⭐⭐⭐ - Reset Bjoern's password via the Forgot Password mechanism

### Sensitive Data Exposure (7 challenges)

- [Confidential Document](./Sensitive_Data_Exposure/Confidential_Document.md) - ⭐ - Access a confidential document
- [Exposed Metrics](./Sensitive_Data_Exposure/Exposed_Metrics.md) - ⭐ - Find the endpoint that serves usage data to be scraped by a popular monitoring system
- [Meta Geo Stalking](./Sensitive_Data_Exposure/Meta_Geo_Stalking.md) - ⭐⭐ - Determine the answer to John's security question by looking at an upload of him to the Photo Wall
- [Visual Geo Stalking](./Sensitive_Data_Exposure/Visual_Geo_Stalking.md) - ⭐⭐ - Determine the answer to Emma's security question by looking at an upload of her to the Photo Wall
- [Leaked Access Logs](./Sensitive_Data_Exposure/Leaked_Access_Logs.md) - ⭐⭐⭐⭐ - Gain access to any access log file of the server
- [Leaked Unsafe Product](./Sensitive_Data_Exposure/Leaked_Unsafe_Product.md) - ⭐⭐⭐⭐ - Inform the development team about a danger to some of their customers
- [Login Support Team](./Sensitive_Data_Exposure/Login_Support_Team.md) - ⭐⭐⭐⭐⭐⭐ - Log in with the support team's original user credentials

### XSS (Cross-Site Scripting) (7 challenges)

- [DOM XSS](./XSS_Cross-Site_Scripting/DOM_XSS.md) - ⭐ - Perform a DOM XSS attack
- [Reflected XSS](./XSS_Cross-Site_Scripting/Reflected_XSS.md) - ⭐⭐ - Perform a reflected XSS attack
- [Client-Side XSS Protection](./XSS_Cross-Site_Scripting/Client-Side_XSS_Protection.md) - ⭐⭐⭐ - Perform an XSS attack on a legacy page within the application
- [API-only XSS](./XSS_Cross-Site_Scripting/API-only_XSS.md) - ⭐⭐⭐ - Perform an XSS attack with <iframe src="javascript:alert(`xss`)">
- [Server-side XSS Protection](./XSS_Cross-Site_Scripting/Server-side_XSS_Protection.md) - ⭐⭐⭐⭐ - Perform a persisted XSS attack bypassing a server-side security mechanism
- [CSP Bypass](./XSS_Cross-Site_Scripting/CSP_Bypass.md) - ⭐⭐⭐⭐ - Bypass a Content Security Policy mechanism
- [Bonus Payload](./XSS_Cross-Site_Scripting/Bonus_Payload.md) - ⭐⭐⭐⭐⭐⭐ - Use the bonus payload in the DOM XSS challenge

### Injection (9 challenges)

- [Login Admin (SQL)](./Injection/Login_Admin_(SQL).md) - ⭐⭐ - Log in with the administrator's user account using SQL Injection
- [Login Jim (SQL)](./Injection/Login_Jim_(SQL).md) - ⭐⭐⭐ - Log in with Jim's user account using SQL Injection
- [Login Bender (SQL)](./Injection/Login_Bender_(SQL).md) - ⭐⭐⭐ - Log in with Bender's user account using SQL Injection
- [Database Schema](./Injection/Database_Schema.md) - ⭐⭐⭐ - Exfiltrate the entire DB schema definition via SQL Injection
- [User Credentials](./Injection/User_Credentials.md) - ⭐⭐⭐⭐ - Retrieve a list of all user credentials via SQL Injection
- [Christmas Special](./Injection/Christmas_Special.md) - ⭐⭐⭐⭐ - Order the Christmas special offer of 2014
- [NoSQL DoS](./Injection/NoSQL_DoS.md) - ⭐⭐⭐⭐ - Let the server sleep for some time via NoSQL Injection
- [NoSQL Manipulation](./Injection/NoSQL_Manipulation.md) - ⭐⭐⭐⭐ - Update multiple product reviews at the same time
- [Ephemeral Accountant](./Injection/Ephemeral_Accountant.md) - ⭐⭐⭐⭐ - Log in with the (non-existing) accountant without ever registering that user

### Security Misconfiguration (7 challenges)

- [Error Handling](./Security_Misconfiguration/Error_Handling.md) - ⭐ - Provoke an error that is not very gracefully handled
- [Outdated Allowlist](./Security_Misconfiguration/Outdated_Allowlist.md) - ⭐ - Let us redirect you to a donation site that went out of business
- [Deprecated Interface](./Security_Misconfiguration/Deprecated_Interface.md) - ⭐⭐ - Use a deprecated B2B interface
- [Security Policy](./Security_Misconfiguration/Security_Policy.md) - ⭐⭐ - Behave like any "white-hat" should before getting into the action
- [Misplaced Signature File](./Security_Misconfiguration/Misplaced_Signature_File.md) - ⭐⭐⭐⭐ - Access a misplaced SIEM signature file
- [Arbitrary File Write](./Security_Misconfiguration/Arbitrary_File_Write.md) - ⭐⭐⭐⭐⭐⭐ - Overwrite the Legal Information file
- [Premium Paywall](./Security_Misconfiguration/Premium_Paywall.md) - ⭐⭐⭐⭐⭐⭐ - Unlock Premium Challenge to access exclusive content

### Broken Anti Automation (3 challenges)

- [CAPTCHA Bypass](./Broken_Anti_Automation/CAPTCHA_Bypass.md) - ⭐⭐⭐ - Submit 10 or more customer feedbacks within 20 seconds
- [Mass Dispel](./Broken_Anti_Automation/Mass_Dispel.md) - ⭐⭐⭐⭐⭐ - Close multiple chatbot messages at once
- [Multiple Likes](./Broken_Anti_Automation/Multiple_Likes.md) - ⭐⭐⭐⭐⭐⭐ - Like any review at least three times as the same user

### Cryptographic Issues (6 challenges)

- [Weird Crypto](./Cryptographic_Issues/Weird_Crypto.md) - ⭐⭐ - Inform the shop about a vulnerable library it is using
- [Nested Easter Egg](./Cryptographic_Issues/Nested_Easter_Egg.md) - ⭐⭐⭐⭐ - Apply advanced cryptanalysis to find the real easter egg
- [Unsigned JWT](./Cryptographic_Issues/Unsigned_JWT.md) - ⭐⭐⭐⭐⭐ - Forge an unsigned JWT token
- [Blockchain Hype](./Cryptographic_Issues/Blockchain_Hype.md) - ⭐⭐⭐⭐⭐ - Learn about the Token Sale
- [Premium Paywall](./Cryptographic_Issues/Premium_Paywall.md) - ⭐⭐⭐⭐⭐⭐ - Solve the challenge with an unencrypted premium content file
- [Forged Coupon](./Cryptographic_Issues/Forged_Coupon.md) - ⭐⭐⭐⭐⭐⭐ - Forge a coupon code

### Unvalidated Redirects (2 challenges)

- [Outdated Allowlist](./Unvalidated_Redirects/Outdated_Allowlist.md) - ⭐ - Let us redirect you to a donation site
- [Allowlist Bypass](./Unvalidated_Redirects/Allowlist_Bypass.md) - ⭐⭐⭐⭐ - Enforce a redirect to a page you are not supposed to redirect to

### Improper Input Validation (11 challenges)

- [Zero Stars](./Improper_Input_Validation/Zero_Stars.md) - ⭐ - Give a feedback with a rating of 0 stars
- [Empty User Registration](./Improper_Input_Validation/Empty_User_Registration.md) - ⭐ - Register a user with an empty email and password
- [Admin Registration](./Improper_Input_Validation/Admin_Registration.md) - ⭐⭐⭐ - Register as a user with administrator privileges
- [Payback Time](./Improper_Input_Validation/Payback_Time.md) - ⭐⭐⭐ - Place an order that makes you rich
- [Upload Size](./Improper_Input_Validation/Upload_Size.md) - ⭐⭐⭐ - Upload a file larger than 100 kB
- [Upload Type](./Improper_Input_Validation/Upload_Type.md) - ⭐⭐⭐ - Upload a file of a type that should not be accepted
- [XXE Data Access](./Improper_Input_Validation/XXE_Data_Access.md) - ⭐⭐⭐⭐ - Access data in the server via XXE
- [Poison Null Byte](./Improper_Input_Validation/Poison_Null_Byte.md) - ⭐⭐⭐⭐ - Bypass a security control with a Poison Null Byte
- [XXE DoS](./Improper_Input_Validation/XXE_DoS.md) - ⭐⭐⭐⭐⭐ - Give the server something to chew on for quite a while
- [NFT Takeover](./Improper_Input_Validation/NFT_Takeover.md) - ⭐⭐⭐⭐⭐ - Take over the wallet containing our official Soul Bound Token (NFT)
- [SSTi](./Improper_Input_Validation/SSTi.md) - ⭐⭐⭐⭐⭐⭐ - Infect the server with juicy malware by abusing arbitrary command execution

### Vulnerable Components (3 challenges)

- [Vulnerable Library](./Vulnerable_Components/Vulnerable_Library.md) - ⭐⭐⭐⭐ - Inform the shop about a vulnerable library it is using
- [Legacy Typosquatting](./Vulnerable_Components/Legacy_Typosquatting.md) - ⭐⭐⭐⭐ - Inform the shop about a typosquatting trick it has been a victim of
- [Frontend Typosquatting](./Vulnerable_Components/Frontend_Typosquatting.md) - ⭐⭐⭐⭐⭐ - Inform the shop about a typosquatting imposter that dug itself deep into the frontend

### Security Through Obscurity (3 challenges)

- [Score Board](./Security_Through_Obscurity/Score_Board.md) - ⭐ - Find the carefully hidden 'Score Board' page
- [Privacy Policy](./Security_Through_Obscurity/Privacy_Policy.md) - ⭐ - Read our privacy policy
- [Blockchain Hype](./Security_Through_Obscurity/Blockchain_Hype.md) - ⭐⭐⭐⭐⭐ - Learn about the Token Sale before its official announcement

### XXE (XML External Entities) (2 challenges)

- [XXE Data Access](./XXE_XML_External_Entities/XXE_Data_Access.md) - ⭐⭐⭐⭐ - Retrieve the content of C:\Windows\system.ini or /etc/passwd from the server
- [XXE DoS](./XXE_XML_External_Entities/XXE_DoS.md) - ⭐⭐⭐⭐⭐ - Give the server something to chew on for quite a while

### Insecure Deserialization (1 challenges)

- [Arbitrary File Write](./Insecure_Deserialization/Arbitrary_File_Write.md) - ⭐⭐⭐⭐⭐⭐ - Overwrite a file using an insecure deserialization vulnerability


---

## Quick Navigation

**By Difficulty:**
- [⭐ Level 1 (Trivial)](#level-1)
- [⭐⭐ Level 2 (Easy)](#level-2)
- [⭐⭐⭐ Level 3 (Medium)](#level-3)
- [⭐⭐⭐⭐ Level 4 (Hard)](#level-4)
- [⭐⭐⭐⭐⭐ Level 5 (Expert)](#level-5)
- [⭐⭐⭐⭐⭐⭐ Level 6 (Bonus)](#level-6)

**Total Challenges:** 79

**Generated:** 2025-11-16 07:22:57

---

*All writeups are for educational purposes only. Always obtain proper authorization before testing.*
