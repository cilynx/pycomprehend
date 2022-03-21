#!/usr/bin/env python3

import sys
import re
import pytesseract

from tabulate import tabulate
from dateutil.parser import parse
from pdf2image import convert_from_path

images = convert_from_path(sys.argv[1])

text = ''
for image in images:
    text += pytesseract.image_to_string(image)
#    print(pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT))

print(text)

months = '(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'

date_formats = [
    months + r' \d{1,2}, \d{2,4}',  # Mar 20, 2022
    r'\d{1,2}/\d{1,2}/\d{2,4}'      # 3/20/2022
]

dates = '|'.join('(?:{0})'.format(x) for x in date_formats)

rows = []

matches = re.findall(dates, text, re.IGNORECASE)

print(tabulate([[match, parse(match)] for match in matches]))
