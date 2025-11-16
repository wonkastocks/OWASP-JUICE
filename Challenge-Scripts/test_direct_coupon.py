#!/usr/bin/env python3

import requests
import json
import time

# Direct test approach
base_url = "https://juice5.wonkatech.org"
session = requests.Session()

print("🔧 Direct coupon test approach...")

# Step 1: Register
email = f"directtest{int(time.time())}@test.com"
password = "Test123456!"

register_data = {
    "email": email,
    "password": password,
    "passwordRepeat": password,
    "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
    "securityAnswer": "test"
}

register_response = session.post(f"{base_url}/api/Users/", json=register_data)
print(f"Registration: {register_response.status_code}")

# Step 2: Login
login_response = session.post(f"{base_url}/rest/user/login", json={
    "email": email, 
    "password": password
})

if login_response.status_code == 200:
    auth_data = login_response.json()
    token = auth_data.get('authentication', {}).get('token')
    session.headers['Authorization'] = f'Bearer {token}'
    print(f"✅ Login successful")
    
    # Step 3: Get products and add to basket
    products_response = session.get(f"{base_url}/rest/products/search")
    products = products_response.json().get('data', [])
    
    if products:
        product_id = products[0]['id']
        print(f"Adding product {product_id} to basket...")
        
        # Add to basket
        basket_response = session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": product_id,
            "quantity": 1
        })
        print(f"Basket add: {basket_response.status_code}")
        
        # Step 4: Get user info to find basket ID  
        whoami_response = session.get(f"{base_url}/rest/user/whoami")
        if whoami_response.status_code == 200:
            user_info = whoami_response.json().get('user', {})
            basket_id = user_info.get('bid', 1)
            print(f"Basket ID: {basket_id}")
            
            # Step 5: Test the discovered coupon code
            test_codes = ["8343D2", "PROMOTION"]
            
            for code in test_codes:
                print(f"\nTesting coupon: {code}")
                coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{code}", json={})
                print(f"Status: {coupon_response.status_code}")
                
                if coupon_response.status_code == 200:
                    result = coupon_response.json()
                    print(f"Response: {result}")
                    
                    discount = result.get('discount', 0)
                    if discount > 0:
                        print(f"🎉 SUCCESS! {code} gives {discount}% discount!")
                        exit(0)
                else:
                    print(f"Failed: {coupon_response.text}")

print("❌ No valid coupons found")
