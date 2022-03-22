from dateutil.parser import parse


class Date:
    def __init__(self, words):
        self.words = words
        self.string = ' '.join([word.text for word in self.words])
        self.dt = parse(self.string)

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
