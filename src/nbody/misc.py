"""
Miscellaneous utility functions for the n-body simulation package.
"""
import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Any, Tuple


def timer(func: Callable = None, *, print_result: bool = True) -> Callable:
    """
    A decorator to time how long a function takes to execute.
    
    Args:
        func: The function to be timed (used when decorator is called without parentheses).
        print_result: Whether to print the execution time. Defaults to True.
    
    Returns:
        The wrapped function that times execution.
    
    Examples:
        Basic usage:
        >>> @timer
        ... def my_function():
        ...     time.sleep(1)
        ...     return "done"
        >>> result = my_function()  # Prints: "my_function took 1.00 seconds"
        
        Without printing:
        >>> @timer(print_result=False)
        ... def my_function():
        ...     return "done"
        
        Accessing the elapsed time:
        >>> @timer
        ... def my_function():
        ...     return "done"
        >>> result, elapsed = my_function()
        >>> print(f"Took {elapsed:.2f} seconds")
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = f(*args, **kwargs)
            elapsed_time = time.perf_counter() - start_time
            
            if print_result:
                print(f"{f.__name__} took {elapsed_time:.4f} seconds")
            
            # Store elapsed time as an attribute for later access
            wrapper.last_time = elapsed_time
            return result
        return wrapper
    
    # Support both @timer and @timer() syntax
    if func is None:
        return decorator
    else:
        return decorator(func)


@contextmanager
def timer_context(name: str = "Code block"):
    """
    A context manager to time a block of code.
    
    Args:
        name: A name to identify the timed code block. Defaults to "Code block".
    
    Examples:
        >>> with timer_context("my calculation"):
        ...     result = sum(range(1000000))
        # Prints: "my calculation took 0.0234 seconds"
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed_time = time.perf_counter() - start_time
        print(f"{name} took {elapsed_time:.4f} seconds")


def time_function(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Time a function call and return both the result and elapsed time.
    
    Args:
        func: The function to time.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    
    Returns:
        A tuple of (function_result, elapsed_time_in_seconds).
    
    Examples:
        >>> def calculate_sum(n):
        ...     return sum(range(n))
        >>> result, elapsed = time_function(calculate_sum, 1000000)
        >>> print(f"Result: {result}, Time: {elapsed:.4f}s")
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_time = time.perf_counter() - start_time
    return result, elapsed_time

