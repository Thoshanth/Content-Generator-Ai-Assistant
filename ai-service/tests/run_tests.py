#!/usr/bin/env python3
"""
Test runner for AI Service
Runs all tests in the correct order
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def run_test(test_file, description):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"File: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, 
                              text=True, 
                              cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

def main():
    """Run all AI service tests"""
    print("🧪 AI Service Test Suite")
    print("=" * 60)
    
    tests = [
        ("test_complexity_analysis.py", "Complexity Analysis"),
        ("test_providers.py", "Provider Testing"),
        ("test_fallback.py", "Fallback Mechanism"),
        ("test_service.py", "Service Endpoints"),
        ("test_four_emails.py", "Email Generation"),
        ("test_intelligent_routing.py", "Intelligent Routing"),
        ("test_final_routing_demo.py", "Routing Demo")
    ]
    
    results = []
    
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())