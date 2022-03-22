import re

class Word:
    def __init__(self, line, left, top, width, height, conf, text):
        # print(f'     Word.__init__{left, top, width, height, conf, text}')
        self.line = line
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        self.text = text
        self.type = None

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def right(self):
        return self.left + self.width

    @property
    def center(self):
        return (self.right - self.left)/2

    @property
    def bottom(self):
        return self.top - self.height

    @property
    def middle(self):
        return (self.top - self.bottom)/2

    @property
    def prev(self):
        index = self.line.words.index(self)
        if index:
            return self.line.words[index-1]

    @property
    def x_space_between(self, word):
        return max([self.left, word.left]) - min([self.right, word.right])

    @property
    def y_space_between(self, word):
        return max([self.bottom, word.bottom]) - min([self.top, word.top])

    @property
    def left_aligned(self, word):
        return abs(word.left - self.left) < max([self.height, word.height])/4

    @property
    def right_aligned(self, word):
        return abs(word.right - self.right) < max([self.height, word.height])/4

    @property
    def center_aligned(self, word):
        return abs(word.center - self.center) < max([self.height, word.height])/4

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
                    self.type == 'year'
                    ppw.type == 'month'
                    pw.type == 'day'
                    return True
        return False
