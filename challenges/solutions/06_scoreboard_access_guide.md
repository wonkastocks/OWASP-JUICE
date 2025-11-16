# How to Access the Score Board - OWASP Juice Shop

## The Score Board is Hidden! (It's a Challenge)

Finding the Score Board is actually your **first challenge** worth 100 points! Here are multiple ways to find it:

---

## Method 1: Direct URL (Easiest)
Simply add `/#/score-board` to your instance URL:

### For Each Instance:
- **Instance 1:** `http://155.138.197.128:3001/#/score-board`
- **Instance 2:** `http://155.138.197.128:3002/#/score-board`
- **Instance 3:** `http://155.138.197.128:3003/#/score-board`
- **Instance 4:** `http://155.138.197.128:3004/#/score-board`
- **Instance 5:** `http://155.138.197.128:3005/#/score-board`

**Just click any of these links or type them in your browser!**

---

## Method 2: Through the Application (The Challenge Way)

### Option A: Check the Source Code
1. Press **F12** to open DevTools
2. Go to **Sources** tab
3. Navigate to `main.js` or search files
4. Search for "score" (Ctrl+F)
5. You'll find references to `/score-board`

### Option B: Look at Network Traffic
1. Press **F12** → **Network** tab
2. Refresh the page
3. Look for `main.js` file
4. Click it and search for "score-board"

### Option C: Check the About Page
1. Click **OWASP Juice Shop** logo (top-left)
2. Scroll down to **About Us**
3. Look for the link that says **"boring terms of use"**
4. The Lorem Ipsum text contains hints!

### Option D: JavaScript Console
1. Press **F12** → **Console**
2. Type: `window.location = '/#/score-board'`
3. Press Enter

---

## Method 3: Find Hidden Links

### The Admin Page Hint
1. Try going to: `http://155.138.197.128:3003/#/administration`
2. If logged in as admin, you'll see a link to Score Board
3. If not, you'll get an error that reveals its existence!

### The FTP Link
1. The About page mentions `/ftp/legal.md?md_debug=true`
2. This leads to finding the Score Board

---

## What You'll See on the Score Board

```
┌─────────────────────────────────────────┐
│          🏆 Score Board 🏆              │
├─────────────────────────────────────────┤
│                                         │
│  Total Score: X / 13000                │
│  Solved Challenges: X / 110            │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ ✅ Score Board (100 pts)         │  │
│  │ ⬜ Login Admin (200 pts)         │  │
│  │ ⬜ Login Jim (200 pts)           │  │
│  │ ⬜ DOM XSS (100 pts)             │  │
│  │ ⬜ Confidential Document (100)    │  │
│  │ ...                               │  │
│  └──────────────────────────────────┘  │
│                                         │
│  Filter by: [All] [1⭐] [2⭐] [3⭐]     │
│            [4⭐] [5⭐] [6⭐]           │
│                                         │
└─────────────────────────────────────────┘
```

---

## Score Board Features

### 1. Challenge Tracking
- ✅ **Green checkmarks** = Completed challenges
- ⬜ **White boxes** = Unsolved challenges
- **Points** shown for each challenge
- **Difficulty stars** (⭐ to ⭐⭐⭐⭐⭐⭐)

### 2. Categories
Click on category tabs to filter:
- **Injection** (SQL, NoSQL)
- **Broken Authentication**
- **Sensitive Data Exposure**
- **Broken Access Control**
- **Security Misconfiguration**
- **XSS** (Cross-Site Scripting)
- **XXE** (XML External Entities)
- **Improper Input Validation**
- **And more...**

### 3. Difficulty Filters
- ⭐ **1 Star**: Tutorial level
- ⭐⭐ **2 Stars**: Easy
- ⭐⭐⭐ **3 Stars**: Medium
- ⭐⭐⭐⭐ **4 Stars**: Hard
- ⭐⭐⭐⭐⭐ **5 Stars**: Expert
- ⭐⭐⭐⭐⭐⭐ **6 Stars**: Diabolical

### 4. Progress Tracking
- **Total Score**: Your points / Maximum possible
- **Completion %**: How many challenges solved
- **Category Progress**: See which areas you've mastered

---

## Quick Access Links for All Instances

### Copy these URLs:

**Instance 1 (Port 3001):**
```
http://155.138.197.128:3001/#/score-board
```

**Instance 2 (Port 3002):**
```
http://155.138.197.128:3002/#/score-board
```

**Instance 3 (Port 3003):**
```
http://155.138.197.128:3003/#/score-board
```

**Instance 4 (Port 3004):**
```
http://155.138.197.128:3004/#/score-board
```

**Instance 5 (Port 3005):**
```
http://155.138.197.128:3005/#/score-board
```

---

## Pro Tips for Using the Score Board

### 1. Start with 1-2 Star Challenges
- Sort by difficulty
- Complete easy ones first
- Build up your skills

### 2. Use Category Filters
- Focus on one vulnerability type
- Master it before moving on
- SQL Injection has many challenges!

### 3. Read the Hints
- Click on any challenge
- It shows a hint
- Some have tutorial links

### 4. Track Your Progress
- Take screenshots
- Document your solutions
- Compare with other instances

### 5. Challenge Notifications
- Green popup when you solve something
- Shows challenge name and points
- Updates Score Board automatically

---

## Hidden Score Board Variations

### Admin Score Board
If logged in as admin:
```
http://155.138.197.128:3003/#/administration
```
Shows additional admin features!

### API Access
Get scores via API:
```
http://155.138.197.128:3003/api/Challenges
```

### Check Completion Status
```javascript
// Run in console to see your progress
fetch('/api/Challenges')
  .then(r => r.json())
  .then(challenges => {
    const solved = challenges.data.filter(c => c.solved);
    console.log(`Solved: ${solved.length}/110 challenges`);
    console.log(`Points: ${solved.reduce((sum, c) => sum + c.difficulty * 100, 0)}`);
  });
```

---

## First Challenges to Complete from Score Board

Once you access the Score Board, try these easy ones:

### 1. **Score Board** (100 pts) ✅
- Already done by accessing it!

### 2. **DOM XSS** (100 pts)
- Go to search
- Type: `<iframe src="javascript:alert('xss')">`

### 3. **Confidential Document** (100 pts)
- Navigate to: `/ftp/acquisitions.md`

### 4. **Error Handling** (100 pts)
- Go to: `/#/rest/qwertz`
- See the error

### 5. **Privacy Policy** (100 pts)
- Read the privacy policy
- Link in footer

---

## Scoreboard Achievements

### Milestone Rewards
- **First Blood**: First challenge solved
- **10 Challenges**: Novice hacker
- **25 Challenges**: Apprentice
- **50 Challenges**: Journeyman
- **75 Challenges**: Expert
- **100 Challenges**: Master
- **110 Challenges**: JUICE SHOP CHAMPION! 🏆

---

## Remember:
- Each instance has its own Score Board
- Progress is saved per instance
- Finding the Score Board = 100 points instantly!
- The Score Board URL is: `/#/score-board`

**Go check your score now!**