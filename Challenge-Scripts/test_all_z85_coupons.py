#!/usr/bin/env python3

import requests
import time

def test_z85_coupons(base_url, server_name):
    print(f"\n🎯 Testing all Z85 coupons on {server_name}")
    
    session = requests.Session()
    email = f"finaltest{int(time.time())}@test.com"
    password = "Test123!"
    
    # Setup
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
        
        # Add products
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        for i in range(2):  # Add 2 products
            session.post(f"{base_url}/api/BasketItems/", json={
                "ProductId": products[i]['id'], "quantity": 1
            })
        
        basket_id = session.get(f"{base_url}/rest/user/whoami").json()['user'].get('bid', 1)
        
        # Test all generated Z85 coupons
        z85_coupons = [
            ("h7Z^wpEw8p", "OCT25-80", "80%"),  # Original sample
            ("g+yZwl}6D#", "DEC24-90", "90%"),  # December 2024
            ("h7Z^Bpes[C", "NOV25-85", "85%"),  # November 2025
            ("h7Z*Gl}6D#", "DEC25-99", "99%"),  # December 2025
        ]
        
        print(f"   Testing {len(z85_coupons)} Z85 encoded coupons...")
        
        for encoded, plaintext, expected in z85_coupons:
            print(f"   Testing {encoded} ({plaintext} = {expected})")
            
            response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{encoded}", json={})
            
            if response.status_code == 200:
                result = response.json()
                discount = result.get('discount', 0)
                
                if discount >= 80:
                    print(f"   🎉 SUCCESS! {encoded} gives {discount}% discount!")
                    print(f"   🏆 CHALLENGE SOLVED on {server_name}!")
                    return True
                elif discount > 0:
                    print(f"   ✅ Valid: {discount}% (insufficient)")
                else:
                    print(f"   ❌ No discount applied")
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
    
    return False

# Test both servers
if test_z85_coupons("https://juice5.wonkatech.org", "Cloudflare"):
    print("\n🎉 Challenge solved via Cloudflare!")
elif test_z85_coupons("http://66.42.93.220", "Direct Server"):
    print("\n🎉 Challenge solved via Direct Server!")
else:
    print("\n❌ Challenge not solved on either server")
    print("🔍 Coupons might be disabled or need different activation")
