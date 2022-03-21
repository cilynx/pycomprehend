import json

class Word:
    def __init__(self, left, top, width, height, conf, text):
        # print(f'     Word.__init__{left, top, width, height, conf, text}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        self.text = text

    @property
