"""
Command-line interface for Cheta, allowing users to access features directly from the terminal.
"""
import sys
from cheta.gui import get_reactions

def main() -> None:
    """Main function to handle command-line arguments and execute corresponding functions."""
    if len(sys.argv) > 1 and sys.argv[1] == "reactions":
        get_reactions()
    else:
        print("Usage: cheta reactions")
