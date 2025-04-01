"""Main entry point for the pyonacci package.

This module serves as the entry point for the pyonacci package when run as a script.
It imports and executes the main CLI function from the cli module.

Example:
    To run the package from command line:
        $ python -m pyonacci

"""
from pyonacci.cli import main as cli_main

if __name__ == "__main__":
    cli_main()
