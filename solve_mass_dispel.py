#!/usr/bin/env python3
"""
Solve the Mass Dispel challenge on OWASP Juice Shop
This challenge requires closing 5 notifications within 5 seconds
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

BASE_URL = "http://155.138.197.128:5000"

def solve_mass_dispel():
    """Solve the Mass Dispel challenge using Selenium"""
    
    print("🎯 Solving Mass Dispel Challenge")
    print("="*60)
    print("Goal: Close 5 notifications within 5 seconds")
    print("="*60)
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Uncomment for headless mode
    # options.add_argument('--headless')
    
    try:
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        actions = ActionChains(driver)
        
        print("\n1️⃣ Navigating to Juice Shop...")
        driver.get(BASE_URL)
        time.sleep(3)
        
        # First, dismiss any existing notifications
        print("\n2️⃣ Clearing existing notifications...")
        try:
            # Dismiss welcome banner
            dismiss_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close Welcome Banner')]")
            dismiss_btn.click()
            print("   ✅ Dismissed welcome banner")
        except:
            pass
        
        try:
            # Dismiss cookie notice
            cookie_dismiss = driver.find_element(By.XPATH, "//a[contains(@aria-label, 'dismiss cookie message')]")
            cookie_dismiss.click()
            print("   ✅ Dismissed cookie notice")
        except:
            pass
        
        time.sleep(2)
        
        print("\n3️⃣ Triggering multiple notifications...")
        
        # Method 1: Try to trigger errors by multiple actions
        print("   Attempting to trigger multiple errors...")
        
        # Try login with wrong credentials multiple times
        try:
            # Navigate to login
            driver.get(f"{BASE_URL}/#/login")
            time.sleep(1)
            
            email_field = driver.find_element(By.ID, "email")
            password_field = driver.find_element(By.ID, "password")
            login_btn = driver.find_element(By.ID, "loginButton")
            
            # Trigger multiple login failures quickly
            for i in range(5):
                email_field.clear()
                password_field.clear()
                email_field.send_keys(f"test{i}@test.com")
                password_field.send_keys("wrongpass")
                login_btn.click()
                time.sleep(0.2)  # Small delay to let notifications appear
                
        except Exception as e:
            print(f"   ⚠️ Login trigger failed: {e}")
        
        # Method 2: Try basket operations
        print("   Attempting basket operations...")
        try:
            driver.get(f"{BASE_URL}/#/basket")
            time.sleep(1)
            
            # Try to checkout empty basket multiple times
            for i in range(5):
                try:
                    checkout = driver.find_element(By.ID, "checkoutButton")
                    checkout.click()
                except:
                    pass
                time.sleep(0.1)
                
        except:
            pass
        
        # Method 3: Try product operations
        print("   Attempting product operations...")
        try:
            driver.get(BASE_URL)
            time.sleep(2)
            
            # Try to add invalid quantities
            products = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Add to Basket')]")
            for i, product in enumerate(products[:5]):
                try:
                    product.click()
                    time.sleep(0.1)
                except:
                    pass
                    
        except:
            pass
        
        print("\n4️⃣ Looking for notifications to close...")
        time.sleep(1)
        
        # Find all notifications/snackbars
        notification_selectors = [
            "//simple-snack-bar",
            "//mat-snack-bar-container",
            "//div[contains(@class, 'mat-snack-bar')]",
            "//div[contains(@class, 'cdk-overlay-pane')]//snack-bar-container",
            "//div[contains(@class, 'notification')]",
            "//div[contains(@class, 'alert')]",
            "//div[@role='alert']"
        ]
        
        notifications_found = []
        for selector in notification_selectors:
            try:
                notifications = driver.find_elements(By.XPATH, selector)
                if notifications:
                    notifications_found.extend(notifications)
                    print(f"   Found {len(notifications)} notifications with selector: {selector}")
            except:
                pass
        
        if len(notifications_found) >= 5:
            print(f"\n5️⃣ Found {len(notifications_found)} notifications! Attempting rapid close...")
            
            # Record start time
            start_time = time.time()
            closed_count = 0
            
            # Try to close all notifications quickly
            for notification in notifications_found[:5]:
                try:
                    # Look for close button within notification
                    close_btns = [
                        notification.find_element(By.XPATH, ".//button"),
                        notification.find_element(By.XPATH, ".//a[contains(@class, 'close')]"),
                        notification.find_element(By.XPATH, ".//*[contains(text(), 'X')]"),
                        notification.find_element(By.XPATH, ".//*[contains(@aria-label, 'Close')]")
                    ]
                    
                    for btn in close_btns:
                        try:
                            btn.click()
                            closed_count += 1
                            print(f"   ✅ Closed notification {closed_count}")
                            break
                        except:
                            pass
                except:
                    # Try clicking the notification itself
                    try:
                        notification.click()
                        closed_count += 1
                        print(f"   ✅ Closed notification {closed_count}")
                    except:
                        pass
            
            elapsed_time = time.time() - start_time
            print(f"\n   ⏱️ Closed {closed_count} notifications in {elapsed_time:.2f} seconds")
            
            if closed_count >= 5 and elapsed_time <= 5:
                print("\n✅ Challenge should be solved!")
            
        else:
            print(f"\n⚠️ Only found {len(notifications_found)} notifications, need 5")
            
            # Try alternative method - programmatically trigger notifications
            print("\n6️⃣ Trying to trigger notifications programmatically...")
            
            # Execute JavaScript to create multiple notifications
            driver.execute_script("""
                // Try to trigger multiple errors
                for(let i = 0; i < 5; i++) {
                    // Trigger API errors
                    fetch('/rest/user/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({email: 'test' + i + '@test.com', password: 'wrong'})
                    });
                }
            """)
            
            time.sleep(2)
            
            # Look for notifications again
            notifications = driver.find_elements(By.XPATH, "//mat-snack-bar-container")
            if len(notifications) >= 5:
                print(f"   Found {len(notifications)} new notifications!")
                
                start_time = time.time()
                for notification in notifications[:5]:
                    try:
                        # Click the action button or the notification
                        action_btn = notification.find_element(By.XPATH, ".//button")
                        action_btn.click()
                    except:
                        notification.click()
                
                elapsed_time = time.time() - start_time
                print(f"   ⏱️ Closed notifications in {elapsed_time:.2f} seconds")
        
        print("\n7️⃣ Checking scoreboard...")
        driver.get(f"{BASE_URL}/#/score-board")
        time.sleep(3)
        
        # Look for Mass Dispel challenge status
        try:
            dispel_rows = driver.find_elements(By.XPATH, "//mat-row[contains(., 'Mass Dispel')]")
            for row in dispel_rows:
                if "✓" in row.text or "solved" in row.text.lower():
                    print("   ✅ Mass Dispel challenge SOLVED!")
                else:
                    print("   ❓ Mass Dispel challenge status unclear")
        except:
            pass
        
        print("\n" + "="*60)
        print("💡 Manual tips if not solved:")
        print("1. Trigger multiple errors quickly (bad logins, etc)")
        print("2. When 5+ notifications appear, close them all quickly")
        print("3. Must close 5 notifications within 5 seconds")
        print("4. Try using keyboard shortcuts or rapid clicking")
        print("="*60)
        
        # Keep browser open for manual inspection
        input("\n⏸️  Press Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you have Chrome and ChromeDriver installed:")
        print("   brew install --cask google-chrome")
        print("   brew install chromedriver")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_mass_dispel()