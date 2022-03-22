from dateutil.parser import parse


class Date:
    def __init__(self, words):
        self.words = words
        self.text = ' '.join([word.text for word in self.words])
        self.dt = parse(self.text)
        self.range = None
        for word in self.words:
            word.date = self

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def left(self):
        return min([word.left for word in self.words])

    @property
    def right(self):
        return max([word.right for word in self.words])

    @property
    def top(self):
        return max([word.top for word in self.words])

    @property
    def bottom(self):
        return min([word.bottom for word in self.words])

    @property
    def first_word(self):
        return self.words[0]

    @property
    def last_word(self):
        return self.words[-1]


class DateRange:
    def __init__(self, start, end):
        start.range = self
        end.range = self
        self.words = [start, end]
        self.start = parse(start.text)
        self.end = parse(end.text)
