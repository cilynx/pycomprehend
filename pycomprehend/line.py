class Line:
    def __init__(self, left, top, width, height, conf, text):
        # print(f'    Line.__init__{left, top, width, height, conf, text}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        self.words = []
        self.breaks = []
        if text:
            raise Exception(f'Line should never be passed text directly: {text}')

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def text(self):
        return ' '.join([word.text for word in self.words])


    ###########################################################################
    # Public Methods
    ###########################################################################

    def append(self, word):
        self.words.append(word)
        self.breaks.extend([word.left, word.right])
