"""
Common test runner framework for consistent test output formatting.

Test files should define test functions with names starting with 'test_'.
Each test function should return a tuple: (success: bool, message: str)

Usage:
    from tests.test_runner import run_tests
    
    def test_example():
        # your test code
        return True, "message"
    
    if __name__ == "__main__":
        run_tests()
"""

import inspect
import sys
from pathlib import Path
from typing import Callable, Dict, Tuple
import time

# Try importing directly first (if package is installed)
try:
    from nbody.misc import time_function
    from nbody.constants import GREEN, RED, YELLOW, END
except ImportError:
    # If not installed, add src to path
    test_dir = Path(__file__).parent
    src_dir = test_dir.parent / 'src'
    sys.path.insert(0, str(src_dir))
    from nbody.misc import time_function
    from nbody.constants import GREEN, RED, YELLOW, END


def discover_tests(module=None):
    """
    Discover all test functions in the calling module, preserving definition order.
    
    Args:
        module: The module to search for tests. If None, uses the calling module.
    
    Returns:
        List of (test_name, test_function) tuples, sorted by definition line number.
    """
    if module is None:
        # Get the calling module (the test file that called run_tests)
        frame = inspect.currentframe()
        try:
            # Go back 2 frames: skip discover_tests and run_tests
            caller_frame = frame.f_back.f_back
            module = inspect.getmodule(caller_frame)
        finally:
            del frame
    
    tests = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith('test_'):
            # Get the line number where the function is defined
            line_no = obj.__code__.co_firstlineno
            tests.append((line_no, name, obj))
    
    # Sort by line number to preserve definition order
    tests.sort(key=lambda x: x[0])
    
    # Return list of (name, function) tuples in definition order
    return [(name, func) for _, name, func in tests]


def run_tests(test_name_prefix: str = "Testing", module=None, run_only: list = None) -> Dict[str, bool]:
    """
    Run all test functions discovered in the calling module and format output.
    
    Args:
        test_name_prefix: Prefix for the test suite name in output.
        module: The module to search for tests. If None, uses the calling module.
        run_only: Optional list of test function names to run. If None, runs all tests.
                  Can be specified with or without 'test_' prefix (e.g., ['no_bodies', 'test_one_body']).
    
    Returns:
        Dictionary mapping test names to their success status.
    """
    tests = discover_tests(module)
    
    if not tests:
        print(f"\n{RED}No test functions found!{END}")
        print("Make sure your test functions start with 'test_'")
        return {}
    
    # Filter tests if run_only is specified
    if run_only is not None:
        # Normalize the run_only list: ensure all names start with 'test_'
        normalized_run_only = []
        for name in run_only:
            if name.startswith('test_'):
                normalized_run_only.append(name)
            else:
                normalized_run_only.append(f'test_{name}')
        
        # Filter tests to only include requested ones
        filtered_tests = []
        run_only_set = set(normalized_run_only)
        for test_name, test_func in tests:
            if test_name in run_only_set:
                filtered_tests.append((test_name, test_func))
        
        # Check if any requested tests weren't found
        found_names = {name for name, _ in filtered_tests}
        missing_names = run_only_set - found_names
        if missing_names:
            print(f"\n{YELLOW}Warning: The following tests were requested but not found:{END}")
            for name in sorted(missing_names):
                print(f"  - {name}")
        
        tests = filtered_tests
        
        if not tests:
            print(f"\n{RED}No matching test functions found!{END}")
            return {}
    
    # Get the module name for display
    if module is None:
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            module = inspect.getmodule(caller_frame)
        finally:
            del frame
    
    module_name = module.__name__ if module else "tests"
    test_suite_name = getattr(module, '__doc__', None) or module_name
    
    print("\n")
    print("=" * 60)
    print(test_name_prefix if test_name_prefix != "Testing" else f"Testing {module_name}")
    print("=" * 60)
    
    test_results = {}
    test_order = []  # Preserve the order tests were run
    test_number = 1
    
    # Run each test with timing (tests are already in definition order)
    for test_name, test_func in tests:
        test_order.append(test_name)  # Track order
        # Get test docstring or use function name
        test_description = test_func.__doc__ or test_name.replace('_', ' ').title()
        if test_description:
            test_description = test_description.strip().split('\n')[0]
        
        print(f"\n{test_number}. {test_description}...")
        
        # Run test with timing
        try:
            (result, status), elapsed = time_function(test_func)
            test_results[test_name] = result
            print(f"{status} ran in {elapsed:.4f} seconds")
        except Exception as e:
            test_results[test_name] = False
            print(f"{RED}   ✗ Failed with exception: {e}{END}")
        
        test_number += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    passed_count = sum(1 for result in test_results.values() if result is True)
    failed_count = sum(1 for result in test_results.values() if result is False)
    total_count = len(test_results)
    
    # Iterate in the same order as tests were run (definition order)
    for test_name in test_order:
        result = test_results.get(test_name, False)
        status = f"{GREEN}✓ PASSED{END}" if result is True else f"{RED}✗ FAILED{END}"
        # Clean up test name for display
        display_name = test_name.replace('test_', '').replace('_', ' ')
        print(f"{display_name:.<40} {status}")
    
    print("=" * 60)
    print(f"Total: {total_count} | Passed: {passed_count} | Failed: {failed_count}")
    
    if failed_count == 0:
        print("All tests passed")
    else:
        print(f"{failed_count} test(s) failed")
    print("=" * 60)
    print("\n")
    
    return test_results

