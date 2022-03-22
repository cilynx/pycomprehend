from dateutil.parser import parse

from .placeable import Placeable

class Date(Placeable):
    def __init__(self, words):
        left = min([word.left for word in words])
        top = max([word.top for word in words])
        width = max([word.right for word in words]) - left
        height = top - min([word.bottom for word in words])
        super().__init__(left, top, width, height, words[0].conf)

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
    def first_word(self):
        return self.words[0]

    @property
    def last_word(self):
        return self.words[-1]


class DateRange(Placeable):
    def __init__(self, start, end):
        self.words = [start, end]

        left = min([word.left for word in self.words])
        top = max([word.top for word in self.words])
        width = max([word.right for word in self.words]) - left
        height = top - min([word.bottom for word in self.words])
        super().__init__(left, top, width, height, start.conf)

        self.start = parse(start.text)
        self.end = parse(end.text)
        start.range = self
        end.range = self
