#!/bin/bash

# OWASP Juice Shop Master Challenge Solver
# Target: http://155.138.197.128:5000

BASE_URL="http://155.138.197.128:5000"
API_URL="${BASE_URL}/rest"
SCORE_URL="${BASE_URL}/#/score-board"

echo "========================================="
echo " OWASP Juice Shop - Master Solver v1.0"
echo " Target: $BASE_URL"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print challenge
challenge() {
    echo -e "${YELLOW}🎯 $1${NC}"
}

# Function to print error
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Create results directory
mkdir -p juice_shop_writeups
cd juice_shop_writeups

# Start the writeup
echo "# OWASP Juice Shop - Complete Challenge Writeup" > WRITEUP.md
echo "## Target: $BASE_URL" >> WRITEUP.md
echo "## Date: $(date)" >> WRITEUP.md
echo "" >> WRITEUP.md

# Track solved challenges
SOLVED_COUNT=0

echo "Starting automated challenge solver..."
echo ""

# Call the Python solver
python3 ../juice_solver.py

echo ""
echo "========================================="
echo " Challenge solving complete!"
echo " Check WRITEUP.md for full documentation"
echo " Score Board: $SCORE_URL"
echo "========================================="