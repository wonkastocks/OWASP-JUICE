#!/bin/bash

# Auto-crack all remaining challenges in background

echo "=========================================="
echo "🚀 AUTO-CRACK ALL CHALLENGES"
echo "=========================================="

BASE_URL="https://juice3.wonkatech.org"

# Function to check current status
check_status() {
    curl -s "$BASE_URL/api/Challenges" | python3 -c "
import json, sys
data = json.load(sys.stdin)['data']
solved = len([c for c in data if c.get('solved')])
total = len(data)
print(f'Status: {solved}/{total} solved ({solved*100//total}%)')
"
}

# Run all Python solvers in parallel
echo "📊 Initial status:"
check_status

echo -e "\n🔥 Running all solvers in parallel..."

# Run each solver in background
(timeout 30 python3 complete_solver.py > /tmp/complete.log 2>&1) &
(timeout 30 python3 advanced_solver.py > /tmp/advanced.log 2>&1) &
(timeout 30 python3 ultimate_solver.py > /tmp/ultimate.log 2>&1) &
(timeout 30 python3 level4_solver.py > /tmp/level4.log 2>&1) &
(timeout 30 python3 level5_solver.py > /tmp/level5.log 2>&1) &
(timeout 30 python3 level6_solver.py > /tmp/level6.log 2>&1) &
(timeout 30 python3 remaining_challenges_solver.py > /tmp/remaining.log 2>&1) &
(timeout 30 python3 aggressive_solver.py > /tmp/aggressive.log 2>&1) &
(timeout 30 python3 final_completion_solver.py > /tmp/final.log 2>&1) &
(timeout 30 python3 ultimate_completion.py > /tmp/ultimate_completion.log 2>&1) &
(timeout 30 python3 documented_automation.py > /tmp/documented.log 2>&1) &

# Wait for all background jobs
wait

echo -e "\n✅ All solvers completed"

# Show success messages from logs
echo -e "\n📋 Successful challenges:"
grep -h "✅" /tmp/*.log 2>/dev/null | head -50

echo -e "\n📊 Final status:"
check_status

echo -e "\n✅ AUTO-CRACK COMPLETE"
