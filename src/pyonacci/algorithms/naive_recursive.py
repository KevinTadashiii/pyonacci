"""The Naive Recursive Algorithm module.

This module provides an implementation of the Fibonacci sequence using the naive
recursive algorithm. The naive recursive algorithm is a simple recursive
implementation of the Fibonacci sequence. It has a time complexity of O(2^n) and
a space complexity of O(n). This algorithm is not efficient for large values of
`n`.
"""

def naive_recursive_algorithm(n: int) -> list:
    """Returns a list of the first `n` Fibonacci numbers using the naive recursive algorithm.

    The naive recursive algorithm is a simple recursive implementation of the Fibonacci
    sequence. It has a time complexity of O(2^n) and a space complexity of O(n).
    This algorithm is not efficient for large values of `n`.

    Args:
        n (int): The number of Fibonacci numbers to generate.

    Returns:
        list: A list of the first `n` Fibonacci numbers.
    """
    def fib(n: int) -> int:
        if n <= 1:
            return n
        return fib(n-1) + fib(n-2)

    return [fib(i) for i in range(n)]
