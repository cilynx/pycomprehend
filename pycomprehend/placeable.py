class Placeable:
    def __init__(self, left, top, width, height, conf):
        # print(f'{type(self)}.__init__{left, top, width, height, conf}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def right(self):
        return self.left + self.width

    @property
    def center(self):
        return (self.right - self.left)/2

    @property
    def bottom(self):
        return self.top - self.height

    @property
    def middle(self):
        return (self.top - self.bottom)/2

    @property
    def x_space_between(self, placeable):
        return max([self.left, placeable.left]) - min([self.right, placeable.right])

    @property
    def y_space_between(self, placeable):
        return max([self.bottom, placeable.bottom]) - min([self.top, placeable.top])

    @property
    def left_aligned(self, placeable):
        return abs(placeable.left - self.left) < max([self.height, placeable.height])/4

    @property
    def right_aligned(self, placeable):
        return abs(placeable.right - self.right) < max([self.height, placeable.height])/4

    @property
    def center_aligned(self, placeable):
        return abs(placeable.center - self.center) < max([self.height, placeable.height])/4
