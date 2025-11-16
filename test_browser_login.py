#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("=" * 60)
    print("TESTING ADMIN PANEL LOGIN FLOW")
    print("=" * 60)

    # Step 1: Go to login page
    print("\n1. Navigating to admin login...")
    driver.get("https://wonkatech.org/admin/admin_login.php")
    time.sleep(2)
    print(f"   Current URL: {driver.current_url}")
    print("   ✅ Login page loaded")

    # Step 2: Enter credentials
    print("\n2. Entering credentials...")
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")

    email_field.clear()
    email_field.send_keys("admin@wonkatech.org")
    password_field.clear()
    password_field.send_keys("R00tbeer")
    print("   ✅ Credentials entered")

    # Step 3: Submit form
    print("\n3. Submitting login form...")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(3)

    # Step 4: Check where we ended up
    print("\n4. Checking post-login status...")
    final_url = driver.current_url
    print(f"   Final URL: {final_url}")

    if "dashboard.php" in final_url:
        print("   ✅ Successfully redirected to dashboard!")

        # Check dashboard content
        page_source = driver.page_source
        if "CTF Admin Dashboard" in page_source:
            print("   ✅ Dashboard content loaded correctly")
        elif "Fatal error" in page_source:
            print("   ❌ Dashboard has fatal error")
        else:
            print("   ⚠️ Dashboard loaded but content unclear")

    elif "index.php" in final_url:
        print("   ⚠️ Redirected to index.php")
        page_source = driver.page_source
        if "Dashboard" in page_source:
            print("   ✅ Index page shows dashboard content")
        else:
            print("   ❌ Index page doesn't show dashboard")

    elif "admin_login.php" in final_url:
        print("   ❌ Still on login page - authentication failed")

    elif "login.php" in final_url:
        print("   ❌ Redirected to wrong login.php")

    else:
        print(f"   ❌ Unexpected redirect to: {final_url}")

    print("\n" + "=" * 60)

finally:
    driver.quit()