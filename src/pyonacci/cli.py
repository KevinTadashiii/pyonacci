"""Generate Fibonacci sequences using different algorithms.

Usage:
    pyonacci [-n <elements>] [-a <algorithm>]
    pyonacci -h | --help
    pyonacci -l | --list-algorithms

Options:
    -n --elements <elements>    Number of elements in the Fibonacci sequence
    -a --algorithm <algorithm>  Algorithm to use for generation (can use prefix)
    -h --help                   Show this help message
    -l --list-algorithms        Show list of available algorithms
"""

import importlib
import os
from pathlib import Path

from docopt import docopt


def get_algorithm_function(algorithm_name: str) -> callable:
    """Dynamically imports and returns the requested algorithm function.

    Args:
        algorithm_name: Name of the algorithm function to import

    Returns:
        The algorithm function if found, None otherwise
    """
    for file in os.listdir(Path(__file__).parent / 'algorithms'):
        if file.endswith('.py') and not file.startswith('__'):
            module_name = file[:-3]
            try:
                module = importlib.import_module(f'.algorithms.{module_name}', package='pyonacci')
                if hasattr(module, algorithm_name):
                    return getattr(module, algorithm_name)
            except ImportError:
                continue
    return None


def get_available_algorithms() -> list[str]:
    """Gets a list of available Fibonacci sequence generation algorithms.

    Scans the algorithms directory for Python files containing functions that end
    with '_algorithm' and returns their names as a sorted list.

    Returns:
        list[str]: A sorted list of algorithm function names found in the algorithms
            directory.

    Note:
        Algorithm functions must end with '_algorithm' to be detected.
        Files starting with '__' are ignored.
    """
    algorithms_dir = Path(__file__).parent / 'algorithms'
    algorithm_files = [f for f in os.listdir(algorithms_dir)
                      if f.endswith('.py') and not f.startswith('__')]

    algorithms = []
    for file in algorithm_files:
        module_name = file[:-3]
        try:
            module = importlib.import_module(f'.algorithms.{module_name}', package='pyonacci')
            for attr in dir(module):
                if attr.endswith('_algorithm'):
                    algorithms.append(attr)
        except ImportError:
            continue

    return sorted(algorithms)


def match_algorithm_by_prefix(prefix: str, available_algorithms: list[str]) -> str:
    """Matches an algorithm by prefix.

    Args:
        prefix: The prefix or partial name to match
        available_algorithms: List of available algorithm names

    Returns:
        The full algorithm name if a unique match is found, None otherwise
    """
    matches = [algo for algo in available_algorithms if algo.startswith(prefix)]

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Ambiguous algorithm prefix '{prefix}'. Matching algorithms:")
        for match in matches:
            print(f"  - {match}")
        return None
    else:
        return None


def main() -> None:
    """Main entry point for the CLI application.

    This function handles command line argument parsing and orchestrates the
    Fibonacci sequence generation process. It supports listing available algorithms,
    matching algorithm names by prefix, and generating sequences using the selected
    algorithm.

    Returns:
        None

    Example:
        When run from command line:
            $ pyonacci -n 10 -a recursive
            Using algorithm: recursive_algorithm
            Fibonacci sequence (recursive_algorithm):
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    args = docopt(__doc__)

    if args["--list-algorithms"]:
        print("Available algorithms:")
        for algo in get_available_algorithms():
            print(f"  - {algo}")
        return

    num_elements = int(args["--elements"])
    algorithm_input = args["--algorithm"]
    available_algorithms = get_available_algorithms()

    if algorithm_input in available_algorithms:
        algorithm = algorithm_input
    else:
        algorithm = match_algorithm_by_prefix(algorithm_input, available_algorithms)
        if algorithm is None:
            print(f"Error: No algorithm matching '{algorithm_input}' found.")
            return
        print(f"Using algorithm: {algorithm}")

    algorithm_func = get_algorithm_function(algorithm)
    if algorithm_func is None:
        print(f"Error: Could not load algorithm '{algorithm}'.")
        return

    result = algorithm_func(num_elements)
    print(f"Fibonacci sequence ({algorithm}):")
    print(result)
