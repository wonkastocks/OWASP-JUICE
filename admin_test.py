#!/usr/bin/env python3
"""
Test WonkaTech admin panel with Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def test_admin_panel():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("🔍 Testing WonkaTech Admin Panel...")
        
        # Step 1: Login
        print("\n1. Navigating to login page...")
        driver.get("https://wonkatech.org/admin/admin_login.php")
        time.sleep(2)
        
        print("2. Entering credentials...")
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        
        email_field.send_keys("admin@wonkatech.org")
        password_field.send_keys("R00tbeer")
        
        print("3. Submitting login...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        time.sleep(3)
        
        # Check if redirected to dashboard
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        # Step 2: Test Dashboard
        print("\n4. Testing Dashboard...")
        driver.get("https://wonkatech.org/admin/admin_dashboard.php")
        time.sleep(2)
        
        page_source = driver.page_source
        if "Fatal error" in page_source:
            print("❌ Dashboard has fatal errors")
            print("Error found:", page_source[page_source.find("Fatal error"):page_source.find("Fatal error")+200])
        elif "function" in page_source and "<?php" in page_source:
            print("❌ Dashboard showing raw PHP code")
        else:
            print("✅ Dashboard loads cleanly")
        
        # Step 3: Test Users Page
        print("\n5. Testing Users page...")
        driver.get("https://wonkatech.org/admin/users.php")
        time.sleep(2)
        
        page_source = driver.page_source
        if "Fatal error" in page_source:
            print("❌ Users page has fatal errors")
            print("Error:", page_source[page_source.find("Fatal error"):page_source.find("Fatal error")+200])
        elif "function formatDate" in page_source or "// Reset user" in page_source:
            print("❌ Users page showing raw PHP code")
        else:
            print("✅ Users page loads cleanly")
            # Check if user data is displayed
            if "Registered Users" in page_source:
                print("✅ User data is displaying")
        
        # Step 4: Test Containers Page  
        print("\n6. Testing Containers page...")
        driver.get("https://wonkatech.org/admin/containers.php")
        time.sleep(2)
        
        page_source = driver.page_source
        if "Fatal error" in page_source:
            print("❌ Containers page has fatal errors")
        elif "Container Management" in page_source:
            print("✅ Containers page loads cleanly")
        else:
            print("❌ Containers page has issues")
            
        print("\n📊 Final Status:")
        print("Admin panel verification completed.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_admin_panel()
