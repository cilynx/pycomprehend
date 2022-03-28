import PIL
import os

from PIL import ImageFilter, ImageOps

class Image():
    def __init__(self, arg=None):
        self.pil_pixels = []
        self.pil_image = None
        self.pixel = []
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
                self.pixel.append([])
                for x in range(self.width):
                    pixel = Pixel(self, x, y)
                    if y:
                        pixel.neighbors['n'] = self.pixel[y-1][x]
                        self.pixel[y-1][x].neighbors['s'] = pixel
                        if x:
                            pixel.neighbors['nw'] = self.pixel[y-1][x-1]
                            self.pixel[y-1][x-1].neighbors['se'] = pixel
                        if x < self.width - 1:
                            pixel.neighbors['ne'] = self.pixel[y-1][x+1]
                            self.pixel[y-1][x+1].neighbors['sw'] = pixel
                    if x:
                        pixel.neighbors['w'] = self.pixel[y][x-1]
                        self.pixel[y][x-1].neighbors['e'] = pixel
                    self.pixel[y].append(pixel)
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

    @property
    def pixels(self):
        return [pixel for row in self.pixel for pixel in row]

    def pixels_by_value(self, value):
        return [pixel for pixel in self.pixels if pixel.value == value]

    @property
    def black_pixels(self):
        return self.pixels_by_value((0, 0, 0))

    @property
    def white_pixels(self):
        return self.pixels_by_value((255, 255, 255))

    @property
    def border_pixels(self):
        return [pixel for pixel in self.pixels if pixel.x == 0 or pixel.x == self.width-1 or pixel.y == 0 or pixel.y == self.height-1]

    @property
    def edge_pixels(self):
        return [pixel for pixel in self.pixels if pixel.is_edge]

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
            return ImageOps.invert(self).getbbox()
        return self.pil_image.getbbox()

    ###########################################################################
    # Crop to content
    ###########################################################################

    def autocrop(self):
        return Image(self.crop(self.getbbox()))

    ###########################################################################
    # Skew
    ###########################################################################

    def get_skew(self, min=-45, max=45, step=1):
        guess = 0
        dir = 1
        prev_image = self.copy()
        left, upper, right, lower = prev_image.getbbox()
        prev_area = (lower-upper)*(right-left)
        while min <= guess <= max:
            guess += step*dir
            image = self.rotate(guess)
            left, upper, right, lower = image.getbbox()
            area = (lower-upper)*(right-left)
            if area > prev_area:
                dir *= -1
                step = step/2
            elif area == prev_area:
                return guess
            prev_image = image
            prev_area = area

    def deskew(self, min=-45, max=45, step=1):
        return Image(self.rotate(self.get_skew()))

    ###########################################################################
    # Edges
    ###########################################################################

    def highlight_edges(self, color=None):
        if not color:
            color = (255, 0, 0)
        copy = Image(self.copy())
        for pixel in copy.edge_pixels:
            pixel.value = color
        return copy

    def show_edges(self, color=None):
        self.highlight_edges(color=color).show()

    def edges(self):
        if self.border_is_white:
            return Image(ImageOps.invert(self).filter(ImageFilter.FIND_EDGES))
        return Image(self.filter(ImageFilter.FIND_EDGES))

class Pixel():
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.neighbors = {}

    @property
    def value(self):
        return self.image.getpixel((self.x, self.y))

    @value.setter
    def value(self, value):
        self.image.putpixel((self.x, self.y), value)

    @property
    def is_edge(self):
        for neighbor in self.neighbors.values():
            if neighbor.value != self.value:
                return True
        return False
