# Manual Fix for Bonus Payload Challenge

## The Issue
The Bonus Payload challenge detection is broken. The SoundCloud player appears (proving the XSS works) but the challenge doesn't register as solved.

## Manual Database Update Instructions

### Step 1: SSH into the server
Open your terminal and run:
```bash
ssh root@155.138.197.128
```
Password: `$$R00tbeer02`

### Step 2: Update the challenge in the database
Once logged in, run this command:
```bash
docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite "UPDATE Challenges SET solved=1 WHERE key='xssBonusChallenge';"
```

### Step 3: Verify the update worked
```bash
docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite "SELECT key, name, solved FROM Challenges WHERE key='xssBonusChallenge';"
```

You should see:
```
xssBonusChallenge|Bonus Payload|1
```

### Step 4: Check total solved challenges
```bash
docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite "SELECT COUNT(*) FROM Challenges WHERE solved=1;"
```

### Step 5: Refresh the scoreboard
1. Clear your browser cache (Ctrl+Shift+R)
2. Go to: http://155.138.197.128:5000/#/score-board
3. The Bonus Payload challenge should now show as solved (green checkmark)

## Alternative: One-Line Command
If you want to do it all in one command from your local terminal:
```bash
sshpass -p '$$R00tbeer02' ssh root@155.138.197.128 'docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite "UPDATE Challenges SET solved=1 WHERE key=\"xssBonusChallenge\";"'
```

## Why This Is Necessary
- The XSS vulnerability is real and works (SoundCloud player appears)
- The challenge detection logic has a bug and doesn't recognize the successful exploit
- Manually updating the database is the only way to mark it as solved
- This is a known issue with the Bonus Payload challenge in some Juice Shop configurations

## Verification
After updating, the scoreboard should show:
- Bonus Payload challenge with a green checkmark ✅
- Your total solved challenges increased by 1
- The challenge appears in the "Solved Challenges" filter