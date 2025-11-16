# Challenge 1: Score Board

## Difficulty: ⭐ (1/5)

## Objective
Find the carefully hidden 'Score Board' page which lists all available challenges and tracks your progress.

## Hints
- The Score Board is not linked from anywhere in the application
- Check JavaScript files for hidden paths
- Look for routes that aren't visible in the UI

## Solution Method 1: JavaScript Analysis

### Manual Steps:
1. Open browser Developer Tools (F12)
2. Go to Sources tab
3. Look for `main.js` or `app.js` files
4. Search for "score" or "board" in the JavaScript files
5. You'll find reference to `/score-board` route

### Automated Script:
```bash
#!/bin/bash
# save as: find_score_board.sh

TARGET="https://juice3.wonkatech.org"

echo "🔍 Finding Score Board..."

# Method 1: Check common paths
echo "Checking common hidden paths..."
curl -s "${TARGET}/score-board" -o /dev/null -w "%{http_code}" | grep -q "200" && echo "✅ Found at: ${TARGET}/score-board"

# Method 2: Extract from JavaScript
echo "Analyzing JavaScript files..."
curl -s "${TARGET}/main.js" 2>/dev/null | grep -o 'score[^"]*board' | head -1 && echo "✅ Score Board reference found in main.js"

echo "📋 Access the Score Board at: ${TARGET}/#/score-board"
```

## Solution Method 2: Direct Access

Simply navigate to:
```
https://[your-instance].wonkatech.org/#/score-board
```

## Python Automation:
```python
#!/usr/bin/env python3
# save as: challenge_01_score_board.py

import requests
import re

def find_score_board(base_url):
    """Find the hidden Score Board page"""
    
    print(f"🎯 Challenge 1: Finding Score Board on {base_url}")
    
    # Method 1: Direct access attempt
    score_board_url = f"{base_url}/#/score-board"
    
    # Method 2: Search in JavaScript files
    try:
        # Get main JavaScript file
        response = requests.get(f"{base_url}/main.js")
        if 'score-board' in response.text.lower():
            print("✅ Found 'score-board' reference in main.js")
    except:
        pass
    
    print(f"✅ Score Board URL: {score_board_url}")
    print(f"📋 Navigate to: {score_board_url}")
    
    # The score board is at /#/score-board route
    return score_board_url

if __name__ == "__main__":
    # Replace with your instance
    BASE_URL = "https://juice3.wonkatech.org"
    find_score_board(BASE_URL)
```

## Flag/Completion
Once you access the Score Board, you'll see all available challenges and your progress. The challenge is marked as complete when you successfully access the page.

## Learning Points
- Hidden functionality can often be found in JavaScript source code
- Not all application routes are visible in the UI
- Client-side code analysis is an important reconnaissance technique