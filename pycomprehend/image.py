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
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    self.pixels[y].append(Pixel(x, y, self.getpixel((x,y))))
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
    # Pixel collections
    ###########################################################################

    def pixels_by_value(self, value):
        pixels = [pixel for row in self.pixels for pixel in row]
        return [pixel for pixel in pixels if pixel.value == value]

    @property
    def black_pixels(self):
        return self.pixels_by_value((0, 0, 0))

    @property
    def white_pixels(self):
        return self.pixels_by_value((255, 255, 255))

    @property
    def border_pixels(self):
        pixels = [pixel for row in self.pixels for pixel in row]
        return [pixel for pixel in pixels if pixel.x == 0 or pixel.x == self.width-1 or pixel.y == 0 or pixel.y == self.height-1]

    ###########################################################################
    # Oddly specific properties
    ###########################################################################

    @property
    def border_is_white(self):
        white = 0
        not_white = 0
        for pixel in self.border_pixels:
            if pixel.value == (255, 255, 255):
                white += 1
            else:
                not_white += 1
        return white/(white+not_white) >= 0.9

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
