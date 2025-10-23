#!/usr/bin/env python3
"""
Test runner for the data analyzer project.
Run all tests or specific test modules.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def run_all_tests():
    """Run all tests in the tests directory."""
    loader = unittest.TestLoader()
    start_dir = str(src_path / "tests")
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run a specific test module."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{test_module}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test module
        test_module = sys.argv[1]
        if not test_module.startswith('test_'):
            test_module = f'test_{test_module}'
        
        print(f"Running {test_module}...")
        success = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests...")
        success = run_all_tests()
    
    sys.exit(0 if success else 1)