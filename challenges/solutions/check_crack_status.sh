#!/bin/bash

echo "📊 Checking detailed challenge status..."

curl -s https://juice3.wonkatech.org/api/Challenges | python3 << 'PYTHON'
import json
import sys

data = json.load(sys.stdin)['data']
total = len(data)
solved = [c for c in data if c.get('solved')]
unsolved = [c for c in data if not c.get('solved')]

print(f"\n✅ SOLVED: {len(solved)}/{total} ({len(solved)*100//total}%)")
print("="*50)

# Group solved by difficulty
solved_by_diff = {}
for c in solved:
    diff = c.get('difficulty', 1)
    if diff not in solved_by_diff:
        solved_by_diff[diff] = []
    solved_by_diff[diff].append(c['name'])

for diff in sorted(solved_by_diff.keys()):
    print(f"\nLevel {diff} ({'⭐' * diff}):")
    for name in solved_by_diff[diff]:
        print(f"  ✅ {name}")

print(f"\n\n❌ UNSOLVED: {len(unsolved)}/{total}")
print("="*50)

# Group unsolved by difficulty
unsolved_by_diff = {}
for c in unsolved:
    diff = c.get('difficulty', 1)
    if diff not in unsolved_by_diff:
        unsolved_by_diff[diff] = []
    unsolved_by_diff[diff].append(c['name'])

for diff in sorted(unsolved_by_diff.keys()):
    print(f"\nLevel {diff} ({'⭐' * diff}): {len(unsolved_by_diff[diff])} remaining")
    for i, name in enumerate(unsolved_by_diff[diff][:10], 1):
        print(f"  {i}. {name}")
    if len(unsolved_by_diff[diff]) > 10:
        print(f"  ... and {len(unsolved_by_diff[diff])-10} more")

print(f"\n📈 Progress Summary:")
print(f"  Level 1: {len(solved_by_diff.get(1, []))}/14")
print(f"  Level 2: {len(solved_by_diff.get(2, []))}/15")
print(f"  Level 3: {len(solved_by_diff.get(3, []))}/24")
print(f"  Level 4: {len(solved_by_diff.get(4, []))}/25")
print(f"  Level 5: {len(solved_by_diff.get(5, []))}/20")
print(f"  Level 6: {len(solved_by_diff.get(6, []))}/12")
PYTHON
