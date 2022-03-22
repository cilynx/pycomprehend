class Block:
    def __init__(self, left, top, width, height, conf, text):
        # print(f'  Block.__init__{left, top, width, height, conf, text}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        self.text = text
        self.paragraphs = []

    def __repr__(self):
        return ' '.join([str(paragraph) for paragraph in self.paragraphs])

    @property
    def lines(self):
        return [line for paragraph in self.paragraphs for line in paragraph.lines]

    @property
    def words(self):
        return [word for line in self.lines for word in line.words]
