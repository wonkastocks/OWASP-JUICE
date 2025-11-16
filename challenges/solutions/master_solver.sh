#!/bin/bash

# Master Solver - Run all Python solvers in sequence

echo "====================================="
echo "🚀 MASTER JUICE SHOP SOLVER"
echo "====================================="

BASE_URL="https://juice3.wonkatech.org"

# Check initial status
echo "📊 Checking initial status..."
curl -s "$BASE_URL/api/Challenges" | python3 -c "
import json, sys
data = json.load(sys.stdin)['data']
solved = len([c for c in data if c.get('solved')])
total = len(data)
print(f'Initial: {solved}/{total} solved ({solved*100//total}%)')
"

# Run all solvers in sequence
echo -e "\n🎯 Running complete_solver.py..."
timeout 30 python3 complete_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running advanced_solver.py..."
timeout 30 python3 advanced_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running ultimate_solver.py..."
timeout 30 python3 ultimate_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running level4_solver.py..."
timeout 30 python3 level4_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running level5_solver.py..."
timeout 30 python3 level5_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running level6_solver.py..."
timeout 30 python3 level6_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running remaining_challenges_solver.py..."
timeout 30 python3 remaining_challenges_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running aggressive_solver.py..."
timeout 30 python3 aggressive_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running final_completion_solver.py..."
timeout 30 python3 final_completion_solver.py 2>/dev/null | grep "✅" | head -20

echo -e "\n🎯 Running ultimate_completion.py..."
timeout 30 python3 ultimate_completion.py 2>/dev/null | grep "✅" | head -20

# Check final status
echo -e "\n====================================="
echo "📊 Checking final status..."
curl -s "$BASE_URL/api/Challenges" | python3 -c "
import json, sys
data = json.load(sys.stdin)['data']
solved = len([c for c in data if c.get('solved')])
total = len(data)
print(f'Final: {solved}/{total} solved ({solved*100//total}%)')
print()
unsolved = [c['name'] for c in data if not c.get('solved')]
print(f'Remaining {len(unsolved)} unsolved challenges:')
for i, name in enumerate(unsolved[:20], 1):
    print(f'{i}. {name}')
if len(unsolved) > 20:
    print(f'... and {len(unsolved)-20} more')
"

echo -e "\n====================================="
echo "✅ MASTER SOLVER COMPLETE"
echo "====================================="
