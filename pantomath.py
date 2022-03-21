#!/usr/bin/env python3

import sys
from tabulate import tabulate
from pycomprehend import Document

document = Document(sys.argv[1])

print(tabulate([[date.string, date.dt, date.left, date.right, date.top, date.bottom] for date in document.dates]))
