import sys
from cheta.gui import open_gui

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "hello":
        open_gui()
    else:
        print("Usage: cheta hello")