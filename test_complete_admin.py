#!/usr/bin/env python3
"""
Complete test of the admin management system
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_with_requests():
    print("=" * 60)
    print("TESTING WITH REQUESTS (Server-side)")
    print("=" * 60)

    session = requests.Session()

    # Login
    print("1. Testing login...")
    response = session.post(
        "https://wonkatech.org/admin/admin_login.php",
        data={'email': 'admin@wonkatech.org', 'password': 'R00tbeer'},
        allow_redirects=False
    )
    print(f"   Login status: {response.status_code}")
    print(f"   Redirect: {response.headers.get('Location')}")
    print(f"   Cookies: {session.cookies.get_dict()}")

    # Test dashboard
    print("\n2. Testing dashboard...")
    dash = session.get("https://wonkatech.org/admin/dashboard.php")
    if "Dashboard" in dash.text or "WonkaTech" in dash.text:
        print("   ✅ Dashboard accessible")
    else:
        print("   ❌ Dashboard not accessible")

    # Test users page
    print("\n3. Testing users page...")
    users = session.get("https://wonkatech.org/admin/users.php")
    if users.status_code == 200 and "User" in users.text:
        print("   ✅ Users page accessible")
    else:
        print(f"   ❌ Users page status: {users.status_code}")

    # Test containers page
    print("\n4. Testing containers page...")
    containers = session.get("https://wonkatech.org/admin/containers.php")
    if containers.status_code == 200 and ("Container" in containers.text or "Port" in containers.text):
        print("   ✅ Containers page accessible")
    else:
        print(f"   ❌ Containers page status: {containers.status_code}")

def test_with_browser():
    print("\n" + "=" * 60)
    print("TESTING WITH BROWSER (Client-side)")
    print("=" * 60)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("\n1. Testing browser login...")
        driver.get("https://wonkatech.org/admin/admin_login.php")
        time.sleep(2)

        # Login
        email = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        email.send_keys("admin@wonkatech.org")
        password.send_keys("R00tbeer")

        submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit.click()
        time.sleep(3)

        print(f"   Final URL: {driver.current_url}")

        if "dashboard.php" in driver.current_url:
            print("   ✅ Successfully logged in and redirected to dashboard")
            source = driver.page_source
            if "Dashboard" in source or "WonkaTech" in source:
                print("   ✅ Dashboard content loaded")
            else:
                print("   ⚠️ Dashboard loaded but content unclear")
        else:
            print("   ❌ Login failed or redirected incorrectly")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_with_requests()
    test_with_browser()

    print("\n" + "=" * 60)
    print("ADMIN MANAGEMENT SYSTEM TEST COMPLETE")
    print("=" * 60)