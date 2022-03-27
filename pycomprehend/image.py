import PIL
import os

class Image():
    def __init__(self, arg=None):
        self.pil_image = None
        self.pixels = []
        self.path = None

        if arg:
            if type(arg) == str:
                if os.path.isfile(arg):
                    print("Path is a file")
                    self.path = arg
                    self.pil_image = PIL.Image.open(self.path)
                elif os.path.isdir(arg):
                    print("Path is a dir")
                else:
                    raise FileNotFoundError("Path is not a file or a dir")
            elif type(arg) == PIL.Image.Image:
                self.pil_image = arg
            else:
                raise Exception("Image.__init__(arg): Argument was not a path or PIL image")
        else:
            print("No argument passed")

    ###########################################################################
    # Send anything we don't recognize through to PIL
    ###########################################################################

    def __getattr__(self, name):
        return self.pil_image.__getattribute__(name)

    ###########################################################################
    # Simple binary threshold
    ###########################################################################

    def threshold(self, thresh=127):
        return Image(self.point(lambda p: 255 if p > thresh else 0))

    ###########################################################################
    # Parse through all pixels to prepare for deeper comprehension
    ###########################################################################

    def parse_pixels(self):
        for i in range(self.width):
            for j in range(self.height):
                self.pixels.append(Pixel(i, j, self.getpixel((i,j))))

    ###########################################################################
    # Pixel collections
    ###########################################################################

    def pixels_by_value(self, value):
        if not self.pixels:
            self.parse_pixels()
        return [pixel for pixel in self.pixels if pixel.value == value]

    @property
    def black_pixels(self):
        return self.pixels_by_value((0, 0, 0))

    @property
    def white_pixels(self):
        return self.pixels_by_value((255, 255, 255))

    @property
    def border_pixels(self):
        return [pixel for pixel in self.pixels if pixel.x == 0 or pixel.x == self.width or pixel.y == 0 or pixel.y == self.height]

    ###########################################################################
    # Oddly specific properties
    ###########################################################################

    @property
    def border_is_white(self):
        for pixel in self.border_pixels:
            if pixel.value != (255, 255, 255):
                return False
        return True
    ###########################################################################
    # Get the bounding box regardless of if the background is black or white
    ###########################################################################

    def getbbox(self):
        if self.border_is_white:
            return PIL.ImageOps.invert(self).getbbox()
        return self.pil_image.getbbox()

    ###########################################################################
    # Crop to content
    ###########################################################################

    def autocrop(self):
        return Image(self.crop(self.getbbox()))


class Pixel():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
