class Line:
    def __init__(self, left, top, width, height, conf, text):
        print(f'    Line.__init__{left, top, width, height, conf, text}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        self.text = text
        self.words = []

    def __repr__(self):
        return ' '.join([str(word) for word in self.words])
