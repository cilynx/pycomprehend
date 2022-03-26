import PIL
import os

class Image():
    def __init__(self, arg=None):
        self.pil_image = None
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
            else:
                raise Exception("Image.__init__(arg): Argument was not a string")
        else:
            print("No argument passed")

    ###########################################################################
    # Send anything we don't recognize through to PIL
    ###########################################################################

    def __getattr__(self, name):
        return self.pil_image.__getattribute__(name)

    ###########################################################################
    # Add a somewhat useful title to show() when none is provided
    ###########################################################################

    def show(self, *args, **kwargs):
        if len(args) == 0 and not 'title' in kwargs:
            kwargs['title'] = os.path.basename(self.path)
        self.pil_image.show(*args, **kwargs)

    def threshold(self, thresh=127):
        return self.point(lambda p: 255 if p > thresh else 0)
