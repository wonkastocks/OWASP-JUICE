#!/usr/bin/env python3
"""
Real verification of admin panel
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
    print("Testing admin login...")
    driver.get("https://wonkatech.org/admin/admin_login.php")
    time.sleep(2)
    
    # Check if login page loads
    page_source = driver.page_source
    print("Login page content preview:")
    print(page_source[:300])
    
    # Try to login
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    email_field.send_keys("admin@wonkatech.org")
    password_field.send_keys("R00tbeer")
    
    submit_button = driver.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()
    
    time.sleep(3)
    print(f"After login URL: {driver.current_url}")
    
    # Check dashboard content
    if "admin_dashboard.php" in driver.current_url or "index.php" in driver.current_url:
        print("Checking dashboard content...")
        source = driver.page_source
        if "Fatal error" in source:
            print("❌ DASHBOARD HAS FATAL ERROR:")
            error_start = source.find("Fatal error")
            print(source[error_start:error_start+300])
        elif "function" in source[:1000]:
            print("❌ DASHBOARD SHOWING RAW PHP CODE:")
            print(source[:500])
        else:
            print("✅ Dashboard appears clean")
            
    # Test users page specifically
    driver.get("https://wonkatech.org/admin/users.php")
    time.sleep(2)
    source = driver.page_source
    
    print("\nUsers page test:")
    if "Fatal error" in source:
        print("❌ USERS PAGE FATAL ERROR")
        error_start = source.find("Fatal error")
        print(source[error_start:error_start+300])
    elif "function formatDate" in source or "// Reset user" in source:
        print("❌ USERS PAGE SHOWING RAW PHP CODE")
        print("Raw code preview:", source[:400])
    elif "User Management" in source:
        print("✅ Users page working - shows User Management")
    else:
        print("❌ Users page has unknown issues")
        print("Page preview:", source[:300])
        
finally:
    driver.quit()

test_admin_panel()
