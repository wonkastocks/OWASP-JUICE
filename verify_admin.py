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
    print("🔍 Testing Simple Admin System...")

    # Test login
    driver.get("https://wonkatech.org/admin/admin_login.php")
    time.sleep(2)

    print("✅ Login page loads")

    # Login
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password")
    email.send_keys("admin@wonkatech.org")
    password.send_keys("R00tbeer")

    button = driver.find_element(By.TAG_NAME, "button")
    button.click()
    time.sleep(3)

    # Check if dashboard loads
    if "dashboard.php" in driver.current_url:
        source = driver.page_source
        if "Admin Dashboard Working" in source:
            print("✅ Dashboard loads and works!")
            print("✅ Login successful")
            print("✅ Session authentication working")
        else:
            print("❌ Dashboard has issues:", source[:200])
    else:
        print("❌ Login failed - URL:", driver.current_url)

finally:
    driver.quit()