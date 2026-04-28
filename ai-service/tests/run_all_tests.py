#!/usr/bin/env python3
"""
Master test runner for all AI Service tests
Runs all test suites and provides comprehensive report
"""

import subprocess
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}")
    print(f"{text.center(70)}")
    print(f"{'='*70}{Colors.END}\n")

def print_section(text):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'-'*70}{Colors.END}")

def run_test(test_file, test_name):
    """Run a single test file"""
    print(f"\n{Colors.YELLOW}🧪 Running: {test_name}{Colors.END}")
    print(f"   File: {test_file}")
    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"{Colors.RED}STDERR:{Colors.END}")
            print(result.stderr)
        
        success = result.returncode == 0
        
        if success:
            print(f"{Colors.GREEN}✅ {test_name} PASSED{Colors.END}")
        else:
            print(f"{Colors.RED}❌ {test_name} FAILED (exit code: {result.returncode}){Colors.END}")
        
        return success
    
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ {test_name} TIMEOUT (exceeded 5 minutes){Colors.END}")
        return False
    
    except Exception as e:
        print(f"{Colors.RED}❌ {test_name} ERROR: {str(e)}{Colors.END}")
        return False

def main():
    """Run all tests"""
    print_header("AI Service v5.0 - Complete Test Suite")
    
    # Get test directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define all tests
    tests = [
        (os.path.join(test_dir, "test_v5_features.py"), "v5.0 Features Test"),
        (os.path.join(test_dir, "test_four_emails.py"), "Four Emails Test"),
        (os.path.join(test_dir, "test_fallback.py"), "Fallback Mechanism Test"),
        (os.path.join(test_dir, "test_intelligent_routing.py"), "Intelligent Routing Test"),
        (os.path.join(test_dir, "test_service.py"), "Service Test"),
    ]
    
    # Check which tests exist
    available_tests = []
    missing_tests = []
    
    for test_file, test_name in tests:
        if os.path.exists(test_file):
            available_tests.append((test_file, test_name))
        else:
            missing_tests.append((test_file, test_name))
    
    if missing_tests:
        print_section("Missing Tests")
        for test_file, test_name in missing_tests:
            print(f"  ⚠️  {test_name}: {test_file}")
    
    if not available_tests:
        print(f"{Colors.RED}❌ No tests found!{Colors.END}")
        return False
    
    print_section("Available Tests")
    for i, (test_file, test_name) in enumerate(available_tests, 1):
        print(f"  {i}. {test_name}")
    
    # Run all tests
    print_section("Running Tests")
    
    results = {}
    start_time = datetime.now()
    
    for test_file, test_name in available_tests:
        success = run_test(test_file, test_name)
        results[test_name] = success
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {Colors.GREEN}{passed}{Colors.END}")
    print(f"Failed: {Colors.RED}{total - passed}{Colors.END}")
    print(f"Duration: {duration:.1f}s")
    print()
    
    # Detailed results
    print_section("Detailed Results")
    
    for test_name, success in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if success else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {status} - {test_name}")
    
    print()
    
    # Final verdict
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.END}")
        return True
    elif passed > 0:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {passed}/{total} tests passed{Colors.END}")
        return False
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ All tests failed{Colors.END}")
        return False

if __name__ == "__main__":
    print("AI Service v5.0 - Complete Test Suite Runner")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    try:
        success = main()
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Tests interrupted by user{Colors.END}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n{Colors.RED}❌ Test runner failed: {str(e)}{Colors.END}")
        sys.exit(1)
