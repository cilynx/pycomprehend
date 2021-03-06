from dateutil.parser import parse

from .bagofwords import BagOfWords

class Date(BagOfWords):
    def __init__(self, words):
        super().__init__(words)
        self.dt = parse(self.text)
        self.range = None
        for word in self.words:
            word.date = self


class DateRange(BagOfWords):
    def __init__(self, start, end):
        super().__init__([start, end])
        self.start = parse(start.text)
        self.end = parse(end.text)
        start.range = self
        end.range = self
