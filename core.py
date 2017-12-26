import disk
from math import sqrt
from PIL import Image, ImageFilter
from resizeimage import resizeimage


def first_val(t):
    a, b = t
    return a


class FilterPhoto:
    def __init__(self, filename):
        self.filename = filename.replace('.', '_filtered.')
        self.image = disk.open(filename)
        self.size = self.image.size
        self.colors = len(self.image.getcolors())

    def __str__(self):
        return "FilterPhoto Object\n  Filename: '{}'\n  Size: {}\n  Colors: {}".format(self.filename, self.size, self.colors)

    def __repr__(self):
        return "FilterPhoto(filename='{}',size={},colors={})".format(self.filename, self.size, self.colors)

    def filter_squareblocks(self, size=1024, colors=16, blocks=16, color=(255, 255, 255)):
        # image properties
        colors = min(256, colors)
        size = size - (size % blocks)
        w = size // blocks  # block width
        r, g, b = color
        color = (min(255, r), min(255, g), min(255, b))

        # helper functions
        def color_index(i):
            row = i // (size * w)
            col = (i % size) // w
            x = row * blocks + col
            return min(x, 255)

        # load image into memory
        image = self.image
        image = image.filter(
            ImageFilter.SMOOTH_MORE).quantize(colors).convert('RGB')
        image = resizeimage.resize_cover(
            image, [blocks, blocks], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')
        img_data = image.getdata()  # get image data

        # generate pixel data for new image
        data = map(lambda i: img_data[color_index(i)], range(size**2))

        image = Image.new('RGB', (size, size))
        image.putdata(list(data))
        image.show()

    # def filter_circle_dots(self, size=1024, colors=16, circles=16, color=(255, 255, 255)):
    #     # image properties
    #     colors = min(256, colors)
    #     size = size - (size % circles)
    #     d = size // circles  # pixel diameter of individual circles
    #     r, g, b = color
    #     color = (min(255, r), min(255, g), min(255, b))

    #     # helper functions
    #     def is_color(i):
    #         w = r - int(sqrt(r**2 - (i % px - r)**2))
    #         return None

    #     def color_index(i):
    #         return i // size**2 * circles + i % circles

    #     # load image into memory
    #     image = self.image
    #     image = image.filter(
    #         ImageFilter.SMOOTH_MORE).quantize(colors).convert('RGB')
    #     image = resizeimage.resize_cover(
    #         image, [circles, circles], validate=False).convert('RGB')
    #     image = image.quantize(colors).convert('RGB')
    #     img_data = image.getdata()  # get image data

    #     # generate pixel data for new image
    #     data = map(lambda i: img_data[color_index(i)], range(size**2))

    #     image = Image.new('RGB', (size, size))
    #     image.putdata(list(data))
    #     image.show()
