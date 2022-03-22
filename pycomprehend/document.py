import pdf2image
import pytesseract
from pytesseract import Output

from .page import Page
from .block import Block
from .paragraph import Paragraph
from .line import Line
from .word import Word
from .date import Date

PAGE = 1
BLOCK = 2
PARAGRAPH = 3
LINE = 4
WORD = 5


class Document:
    def __init__(self, filename):
        print(f'Document.__init__({filename})')
        self.filename = filename
        self.raw_text = ''
        self.pages = []
        self.dates = []
        for image in pdf2image.convert_from_path(filename):
            self.raw_text += pytesseract.image_to_string(image)
            data = pytesseract.image_to_data(image, output_type=Output.DICT)
            page = None
            block = None
            paragraph = None
            line = None
            i = 0
            for level in data['level']:
                if level == PAGE:
                    page = Page(data['left'][i],
                                data['top'][i],
                                data['width'][i],
                                data['height'][i],
                                data['conf'][i],
                                data['text'][i])
                    self.pages.append(page)
                elif level == BLOCK:
                    block = Block(data['left'][i],
                                  data['top'][i],
                                  data['width'][i],
                                  data['height'][i],
                                  data['conf'][i],
                                  data['text'][i])
                    page.blocks.append(block)
                elif level == PARAGRAPH:
                    paragraph = Paragraph(data['left'][i],
                                          data['top'][i],
                                          data['width'][i],
                                          data['height'][i],
                                          data['conf'][i],
                                          data['text'][i])
                    block.paragraphs.append(paragraph)
                elif level == LINE:
                    line = Line(paragraph,
                                data['left'][i],
                                data['top'][i],
                                data['width'][i],
                                data['height'][i],
                                data['conf'][i],
                                data['text'][i])
                    paragraph.lines.append(line)
                elif level == WORD:
                    word = Word(line,
                                data['left'][i],
                                data['top'][i],
                                data['width'][i],
                                data['height'][i],
                                data['conf'][i],
                                data['text'][i])
                    line.append(word)
                else:
                    raise Exception(f'Unknown level.  Did Tesseract change their TSV spec?: {level}')
                i += 1
        self.__extract_dates()
        self.__extract_tables()

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def blocks(self):
        return [block for page in self.pages for block in page.blocks]

    @property
    def paragraphs(self):
        return [paragraph for block in self.blocks for paragraph in block.paragraphs]

    @property
    def lines(self):
        return [line for paragraph in self.paragraphs for line in paragraph.lines]

    @property
    def words(self):
        return [word for line in self.lines for word in line.words]

    ###########################################################################
    # Private Methods
    ###########################################################################

    def __extract_dates(self):
        print("\nExtracting Dates...")
        for word in self.words:
            if word.is_date:
                word.date = Date([word])
                self.dates.append(word.date)
            if word.is_year:
                word.date = Date([word.prev.prev, word.prev, word])
                word.prev.date = word.date
                word.prev.prev.date = word.date
                self.dates.append(word.date)

    def __extract_tables(self):
        print("\nExtracting Tables...")
