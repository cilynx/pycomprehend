class Placeable:
    def __init__(self, left, top, width, height):
        # print(f'{type(self)}.__init__{left, top, width, height}')
        self.left = left
        self.top = top
        self.width = width
        self.height = height

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
        return (self.top + self.bottom)/2

    ###########################################################################
    # Public Methods
    ###########################################################################

    def x_space_between(self, placeable):
        return max([self.left, placeable.left]) - min([self.right, placeable.right])

    def y_space_between(self, placeable):
        return max([self.bottom, placeable.bottom]) - min([self.top, placeable.top])

    def next_to(self, placeable):
        print(self.middle, placeable.middle, max([self.height, placeable.height]))
        if self.line != placeable.line:
            return False
        return self.x_space_between(placeable) < max([self.height, placeable.height])

    def left_aligned(self, placeable):
        return abs(placeable.left - self.left) < max([self.height, placeable.height])/20

    def right_aligned(self, placeable):
        return abs(placeable.right - self.right) < max([self.height, placeable.height])/4

    def center_aligned(self, placeable):
        return abs(placeable.center - self.center) < max([self.height, placeable.height])/4

    def just_below(self, placeable):
        return self.bottom - placeable.top < max([self.height, placeable.height])/2
