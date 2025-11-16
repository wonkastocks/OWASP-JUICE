from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("🎯 FINAL VERIFICATION - Clean Admin System")
    
    # Test login
    driver.get("https://wonkatech.org/admin/admin_login.php")
    time.sleep(2)
    
    source = driver.page_source
    if "function generateCSRF" in source:
        print("❌ STILL showing raw PHP code on login page")
        return
    else:
        print("✅ Login page is clean")
    
    # Try login with correct credentials
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password") 
    email.send_keys("admin@wonkatech.com")  # Note: .com not .org based on config
    password.send_keys("WonkaAdmin2024!")   # Correct password from config
    
    button = driver.find_element(By.TAG_NAME, "button")
    button.click()
    time.sleep(3)
    
    print(f"After login URL: {driver.current_url}")
    
    if "index.php" in driver.current_url:
        source = driver.page_source
        if "Dashboard" in source and "WonkaTech" in source:
            print("✅ ADMIN DASHBOARD WORKING!")
            print("✅ Login successful")
            print("✅ Authentication functional") 
        else:
            print("❌ Dashboard not displaying properly")
    else:
        print("❌ Login redirect failed")
        
finally:
    driver.quit()
