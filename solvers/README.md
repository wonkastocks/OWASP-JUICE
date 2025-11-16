# Automated Solvers

This directory contains automated tools for solving OWASP Juice Shop challenges.

## Available Solvers

### 1. complete_juice_shop_solver.py
**Purpose:** Real-time automated solver for all 110 challenges with scoreboard verification

**Features:**
- Connects to live Juice Shop instance
- Implements exploit code for each challenge
- Real-time scoreboard verification
- Progress tracking and reporting
- Error handling and retry logic

**Usage:**
```bash
# Default (localhost:3000)
python complete_juice_shop_solver.py

# Custom URL
python complete_juice_shop_solver.py --url http://192.168.1.100:3000

# Verbose mode
python complete_juice_shop_solver.py --verbose
```

**Prerequisites:**
- Running Juice Shop instance
- Python 3.x
- Required packages: `requests`, `pyjwt`

**Install dependencies:**
```bash
pip install requests pyjwt
```

---

### 2. comprehensive_writeup_generator.py
**Purpose:** Generate detailed educational writeups for all 110 challenges

**Features:**
- Automated writeup generation
- CVSS scores and CVE references
- Real-world examples
- Attack diagrams (Mermaid)
- Mitigation strategies
- Discussion questions
- NIST references

**Usage:**
```bash
python comprehensive_writeup_generator.py
```

**Output:**
- Creates `challenge_writeups/` directory
- Generates 79+ individual challenge writeups
- Creates category-organized folders
- Generates index README.md

---

## Challenge Categories

Both solvers handle all 14 vulnerability categories:

1. **Broken Access Control** (11 challenges)
2. **Broken Authentication** (7 challenges)
3. **Sensitive Data Exposure** (7 challenges)
4. **XSS - Cross-Site Scripting** (7 challenges)
5. **Injection** (9 challenges)
6. **Security Misconfiguration** (7 challenges)
7. **Broken Anti Automation** (3 challenges)
8. **Cryptographic Issues** (6 challenges)
9. **Unvalidated Redirects** (2 challenges)
10. **Improper Input Validation** (11 challenges)
11. **Vulnerable Components** (3 challenges)
12. **Security Through Obscurity** (3 challenges)
13. **XXE** (2 challenges)
14. **Insecure Deserialization** (1 challenge)

---

## Solver Implementation Status

### Complete Juice Shop Solver

**Implemented (Level 1-3):**
- ✅ Level 1 (⭐) - 8 challenges
- ✅ Level 2 (⭐⭐) - 6 challenges
- ✅ Level 3 (⭐⭐⭐) - 3 challenges

**To Implement:**
- ⏳ Level 4 (⭐⭐⭐⭐) - 25 challenges
- ⏳ Level 5 (⭐⭐⭐⭐⭐) - 15 challenges
- ⏳ Level 6 (⭐⭐⭐⭐⭐⭐) - 16 challenges

**Total:** 17/110 challenges (15.5% complete)

---

## Example: Running the Complete Solver

```bash
# 1. Start Juice Shop
docker run -d -p 3000:3000 bkimminich/juice-shop

# 2. Run solver
python complete_juice_shop_solver.py

# 3. View results
# Open http://localhost:3000/#/score-board
```

**Expected Output:**
```
================================================================================
  OWASP Juice Shop - Complete Automated Solver
  Solving all 110 challenges with scoreboard verification
================================================================================

[*] Verifying Juice Shop instance...
[+] Juice Shop is running (Version: v15.0.0)

[*] Starting automated solver...
[*] Target: http://localhost:3000
[*] Total challenges: 110

================================================================================
  LEVEL 1 CHALLENGES (⭐) - Trivial
================================================================================

[*] Solving: Score Board (⭐)
    ✅ Verified: Score Board ⭐

[*] Solving: Error Handling (⭐)
    ✅ Verified: Error Handling ⭐

...

================================================================================
  FINAL REPORT
================================================================================

Total Challenges Solved: 17/110
Completion Rate: 15.5%

Successfully Solved: 17
Failed: 0

✅ Solved Challenges:
  - Score Board
  - Error Handling
  - Privacy Policy
  ...
```

---

## Extending the Solvers

### Adding New Challenge Solvers

1. **Implement solver method:**
```python
def solve_new_challenge(self):
    """Challenge: Description"""
    print("\n[*] Solving: New Challenge (⭐⭐)")
    try:
        # Implement exploit code here
        r = self.session.get(f"{self.base_url}/endpoint")

        if self.wait_for_challenge("New Challenge"):
            self.challenges_solved.append("New Challenge")
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        self.challenges_failed.append(("New Challenge", str(e)))
```

2. **Add to level execution:**
```python
def solve_all_level_X(self):
    """Solve all Level X challenges"""
    self.solve_new_challenge()
    # ... other challenges
```

3. **Update main run() method:**
```python
def run(self):
    # ...
    self.solve_all_level_X()
```

---

## Security Notice

⚠️ **IMPORTANT:** These solvers are for **educational purposes only**.

**Authorized Use:**
- Your own local Juice Shop instances
- Authorized penetration testing engagements
- CTF competitions
- Security training labs
- Educational research with permission

**Prohibited Use:**
- Production systems
- Systems you don't own
- Without explicit authorization
- Malicious purposes

---

## Troubleshooting

### Common Issues

**1. Connection Refused**
```
[-] ERROR: Cannot connect to Juice Shop!
```
**Solution:** Make sure Juice Shop is running:
```bash
docker ps  # Check if running
docker run -d -p 3000:3000 bkimminich/juice-shop
```

**2. Challenges Not Verified**
```
⚠️  Challenge may require manual browser access
```
**Solution:** Some challenges require browser interaction. Visit the score board to verify manually.

**3. Import Errors**
```
ModuleNotFoundError: No module named 'jwt'
```
**Solution:** Install dependencies:
```bash
pip install requests pyjwt
```

---

## Contributing

To contribute new solver implementations:

1. Fork the repository
2. Implement solver method
3. Test against live Juice Shop
4. Verify scoreboard integration
5. Submit pull request

---

## Resources

- **OWASP Juice Shop:** https://owasp.org/www-project-juice-shop/
- **Official Solutions:** https://pwning.owasp-juice.shop/
- **API Documentation:** Check `/api-docs` endpoint on Juice Shop

---

**Happy Automated Hacking! 🤖🔓**

*Use responsibly and ethically!*
