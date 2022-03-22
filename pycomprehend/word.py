import re

from .placeable import Placeable


class Word(Placeable):
    def __init__(self, line, left, top, width, height, conf, text):
        super().__init__(left, top, width, height, conf)
        self.line = line
        self.text = text
        self.type = None
        self.date = None

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def prev(self):
        index = self.line.words.index(self)
        if index:
            return self.line.words[index-1]

    @property
    def next(self):
        index = self.line.words.index(self)
        if index+1 < len(self.line.words):
            return self.line.words[index+1]

    @property
    def is_date(self):
        if self.type == 'date':
            return True
        elif self.type:
            return False

        # 03/21/2022
        matches = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', self.text)
        if matches:
            self.type = 'date'
            return True
        else:
            return False

    @property
    def is_year(self):
        if self.type == 'year':
            return True
        elif self.type:
            return False

        months = '(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*'

        # 2 or 4-digit year?
        if re.search(r'\d{2,4}', self.text):
            # 1 or 2-digit day followed by comma?
            pw = self.prev
            if pw and re.search(r'\d{1,2}\,', pw.text):
                # Month?
                ppw = pw.prev
                if ppw and re.search(months, ppw.text, re.IGNORECASE):
                    self.type = 'year'
                    ppw.type = 'month'
                    pw.type = 'day'
                    return True
        return False
