#! python3
# mapIt.py - Launches a map in the browser using an web address from the command line or clipboard

import webbrowser
import pyperclip
import sys
if len(sys.argv) > 1:
    # Get address from command line
    address = ' '.join(sys.argv[1:])
else:
    # Get address form the clipboard
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address)
