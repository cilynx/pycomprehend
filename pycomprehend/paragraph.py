class Paragraph:
    def __init__(self, left, top, width, height, conf, text):
        print(f'   Paragraph.__init__{left, top, width, height, conf, text}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        self.text = text
        self.lines = []

    def __repr__(self):
        return ' '.join([str(line) for line in self.lines])

    @property
    def words(self):
        return [word for line in self.lines for word in line.words]
