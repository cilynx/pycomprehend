from .bagofwords import BagOfWords


class Contig(BagOfWords):
    def __init__(self, words):
        super().__init__(words)
        for word in words:
            word.contig = self

    ###########################################################################
    # Public Methods
    ###########################################################################

    def append(self, word):
        self.words.append(word)
        word.contig = self
