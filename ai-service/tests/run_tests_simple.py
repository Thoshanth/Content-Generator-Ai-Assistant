#!/usr/bin/env python3
"""
Simple test runner for Windows compatibility
Runs all test suites without Unicode characters
"""

import subprocess
import sys
import os
from datetime import datetime

def run_test(test_file, test_name):
    """Run a single test file"""
    print(f"\n[TEST] Running: {test_name}")
    print(f"   File: {test_file}")
    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr and "UnicodeEncodeError" not in result.stderr:
            print(f"STDERR: {result.stderr[:500]}")
        
        success = result.returncode == 0
        
        if success:
            print(f"[PASS] {test_name}")
        else:
            print(f"[FAIL] {test_name} (exit code: {result.returncode})")
        
        return success
    
    except subprocess.TimeoutExpired:
        print(f"[FAIL] {test_name} - TIMEOUT")
        return False
    
    except Exception as e:
        print(f"[FAIL] {test_name} - ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("AI Service v5.0 - Test Suite")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    # Get test directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define all tests
    tests = [
        (os.path.join(test_dir, "test_v5_features.py"), "v5.0 Features Test"),
        (os.path.join(test_dir, "test_four_emails.py"), "Four Emails Test"),
    ]
    
    # Check which tests exist
    available_tests = []
    for test_file, test_name in tests:
        if os.path.exists(test_file):
            available_tests.append((test_file, test_name))
    
    if not available_tests:
        print("[ERROR] No tests found!")
        return False
    
    print(f"Available Tests: {len(available_tests)}")
    for i, (test_file, test_name) in enumerate(available_tests, 1):
        print(f"  {i}. {test_name}")
    
    # Run all tests
    print("\n" + "=" * 70)
    print("Running Tests")
    print("=" * 70)
    
    results = {}
    start_time = datetime.now()
    
    for test_file, test_name in available_tests:
        success = run_test(test_file, test_name)
        results[test_name] = success
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Duration: {duration:.1f}s")
    print()
    
    # Detailed results
    print("Detailed Results:")
    for test_name, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {status} - {test_name}")
    
    print()
    
    # Final verdict
    if passed == total:
        print("[SUCCESS] All tests passed!")
        return True
    elif passed > 0:
        print(f"[INFO] {passed}/{total} tests passed")
        return False
    else:
        print("[ERROR] All tests failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Tests interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"[ERROR] Test runner failed: {str(e)}")
        sys.exit(1)
