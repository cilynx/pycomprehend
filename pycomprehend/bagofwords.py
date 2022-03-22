from .placeable import Placeable


class BagOfWords(Placeable):
    def __init__(self, words):
        self.words = words

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def left(self):
        return min([word.left for word in self.words])

    @property
    def top(self):
        return max([word.top for word in self.words])

    @property
    def width(self):
        return max([word.right for word in self.words]) - self.left

    @property
    def height(self):
        return self.top - min([word.bottom for word in self.words])

    @property
    def text(self):
        return ' '.join([word.text for word in self.words])
