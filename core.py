import disk
from math import sqrt
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from resizeimage import resizeimage


def is_file(filename):
    return disk.is_file(filename)


class FilterPhoto:
    def __init__(self, filename):
        self.filename = self.clean_filename(filename)
        self.image = disk.open(filename)
        self.size = self.image.size
        self.colors = len(self.image.getcolors())
        self.filters = [
            {'name': 'No Filters', 'filter': self.no_filter},
            {'name': 'Square Blocks', 'filter': self.filter_squareblocks},
            {'name': 'Circle Dots', 'filter': self.filter_circledots},
            {'name': 'Black Out Text', 'filter': self.filter_lettertext},
            {'name': 'Black Out Inverse', 'filter': self.filter_inversetext}
        ]

    def __str__(self):
        return "FilterPhoto Object\n  Filename: '{}'\n  Size: {}\n  Colors: {}".format(self.filename, self.size, self.colors)

    def __repr__(self):
        return "FilterPhoto(filename='{}',size={},colors={})".format(self.filename, self.size, self.colors)

    def clean_filename(self, filename):
        if '/' in filename:
            filename = filename.split('/')[-1]
        filename = filename.replace('.', '_filtered.')
        return filename

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
            return x

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
        return image

    def filter_circledots(self, size=1024, colors=16, circles=16, color=(255, 255, 255)):
        # image properties
        colors = min(256, colors)
        r, g, b = color
        color = (min(255, r), min(255, g), min(255, b))
        size = size - (size % circles)
        d = size // circles  # pixel diameter of individual circles
        r = d // 2

        # helper functions
        def is_color(i):
            val = abs(r - (i % d))
            x = (i // size) % d
            y = int(sqrt(r**2 - (x - r)**2))
            return val <= y

        def color_index(i):
            row = i // (size * d)
            col = (i % size) // d
            x = row * circles + col
            return x

        # load image into memory
        image = self.image
        image = image.filter(
            ImageFilter.SMOOTH_MORE).quantize(colors).convert('RGB')
        image = resizeimage.resize_cover(
            image, [circles, circles], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')
        img_data = image.getdata()  # get image data

        # generate pixel data for new image
        data = map(lambda i: img_data[color_index(i)]
                   if is_color(i) else color, range(size**2))

        image = Image.new('RGB', (size, size))
        image.putdata(list(data))
        return image

    def filter_lettertext(self, text="Base Camp Coding Academy", fontsize=256, size=1024, colors=256, color=(255, 255, 255), padding=64):
        # image properties
        colors = min(256, colors)
        r, g, b = color
        color = (min(255, r), min(255, g), min(255, b))

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [size, size, ], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')
        data = image.getdata()

        # create text image
        text_image = Image.new('RGB', (size, size))
        text_image.putdata([color for _ in range(size**2)])
        text_image = text_image.convert('RGB')

        # draw on text_image
        font = disk.get_font(fontsize)
        draw = ImageDraw.Draw(text_image, mode='RGB')
        c = 0
        for word in text.split():
            draw.text((padding // 2, padding + c), word +
                      '_', font=font, fill=(0, 0, 0))
            c += size // len(text.split())

        # get data from text image
        text_image = text_image.convert('RGB')
        text_image = resizeimage.resize_cover(
            text_image, [size, size, ], validate=False).convert('RGB')
        text_data = text_image.getdata()

        # make new data
        new_data = [color if text_data[i] == color else data[i]
                    for i in range(size**2)]

        image = Image.new('RGB', (size, size))
        image.putdata(new_data)
        return image

    def filter_inversetext(self, text="Base Camp Coding Academy", fontsize=256, size=1024, colors=256, color=(255, 255, 255), padding=64):
        # image properties
        colors = min(256, colors)
        r, g, b = color
        color = (min(255, r), min(255, g), min(255, b))

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [size, size, ], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')
        data = image.getdata()

        # create text image
        text_image = Image.new('RGB', (size, size))
        text_image.putdata([color for _ in range(size**2)])
        text_image = text_image.convert('RGB')

        # draw on text_image
        font = disk.get_font(fontsize)
        draw = ImageDraw.Draw(text_image, mode='RGB')
        c = 0
        for word in text.split():
            draw.text((padding // 2, padding + c), word +
                      '_', font=font, fill=(0, 0, 0))
            c += size // len(text.split())

        # get data from text image
        text_image = text_image.convert('RGB')
        text_image = resizeimage.resize_cover(
            text_image, [size, size, ], validate=False).convert('RGB')
        text_data = text_image.getdata()

        # make new data
        new_data = [color if text_data[i] != color else data[i]
                    for i in range(size**2)]

        image = Image.new('RGB', (size, size))
        image.putdata(new_data)
        return image

    def no_filter(self, size=1024):
        image = self.image
        image = resizeimage.resize_cover(
            image, [size, size], validate=False).convert('RGB')
        return image

    def save(self):
        disk.save_image(self)
