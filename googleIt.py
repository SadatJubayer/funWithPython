#! python3
# googleIt.py - Launches a google search in the browser using data from the command line or clipboard

import webbrowser
import pyperclip
import sys
if len(sys.argv) > 1:
    # Get address from command line
    address = ' '.join(sys.argv[1:])
else:
    # Get address form the clipboard
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/search?q=' + address)
