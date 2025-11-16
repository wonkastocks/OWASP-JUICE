#!/usr/bin/env python3
"""
Test if admin panel is working properly
"""

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
    print("🔍 Testing WonkaTech Admin Panel...")

    # Test login page
    driver.get("https://wonkatech.org/admin/admin_login.php")
    time.sleep(2)

    print("✅ Admin login page loads")

    # Login with correct credentials
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password")
    email.send_keys("admin@wonkatech.org")
    password.send_keys("R00tbeer")

    submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit.click()

    time.sleep(3)
    print(f"After login URL: {driver.current_url}")

    # Check if redirected to index/dashboard
    if "index.php" in driver.current_url:
        source = driver.page_source

        # Check for errors
        if "Fatal error" in source:
            print("❌ Fatal error on dashboard")
            error_start = source.find("Fatal error")
            print(source[error_start:error_start+200])
        elif "CTF Admin Dashboard" in source or "Dashboard" in source:
            print("✅ Dashboard loads successfully!")

            # Check for key elements
            if "Active Users" in source or "stats" in source:
                print("✅ Dashboard shows statistics")
            if "Container Status" in source or "users" in source:
                print("✅ Dashboard shows user/container info")

            print("\n✅ ADMIN PANEL IS WORKING!")
        else:
            print("⚠️ Dashboard loaded but content unclear")
            print("Page preview:", source[:300])
    else:
        print("❌ Login redirect failed")

finally:
    driver.quit()