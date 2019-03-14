#! python3
# RenameDates.py - Renames filenames with American MM-DD-YYYY date format
# to European DD-MM-YYYY.

import shutil
import os
import re

# Create a regex that matches files with the American date format.

datePattern = re.compile(r"""^(.*?)  # all text before the date
   ((0|1)?\d)-                     # one or two digits for the month
       ((0|1|2|3)?\d)-                 # one or two digits for the day
       ((19|20)\d\d)                   # four digits for the year
       (.*?)$                          # all text after the date
     """, re.VERBOSE)

# TODO: Loop over the files in the working directory.

for fileNames in os.listdir('.'):
    mo = datePattern.search(fileNames)

    # Skip files without a date
    if mo == None:
        continue

    # Get the different parts of the filename.
    beforePart = mo.group(1)
    monthPart = mo.group(2)
    dayPart = mo.group(4)
    yearPart = mo.group(6)
    afterPart = mo.group(8)


# TODO: Form the European-style filename.

    euroFileName = beforePart + dayPart + '-' + \
        monthPart + '-' + yearPart + afterPart

# TODO: Get the full, absolute file paths.
    absWorkingDir = os.path.abspath('.')
    fileNames = os.path.join(absWorkingDir, fileNames)
    euroFileName = os.path.join(absWorkingDir, euroFileName)

# TODO: Rename the files.
    print('Renaming "%s" to "%s"...' % (fileNames, euroFileName))
    shutil.move(fileNames, euroFileName)
