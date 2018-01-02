import disk
from math import sqrt
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from resizeimage import resizeimage
from random import randint, choice


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
            {'name': 'Black Out Inverse', 'filter': self.filter_inversetext},
            {'name': 'Andy Warhol', 'filter': self.filter_warhol},
            {'name': 'Color Swap', 'filter': self.filter_colorswap},
            {'name': 'Color Scale', 'filter': self.filter_colorscale},
            {'name': 'Minimalist', 'filter': self.filter_minimalist},
            {'name': 'Minimalist Wave', 'filter': self.filter_minimalistwave}
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

    def no_filter(self, size=1024):
        image = self.image
        image = resizeimage.resize_cover(
            image, [size, size], validate=False).convert('RGB')
        return image

    def filter_squareblocks(self, size=1024, colors=16, blocks=16, color=(255, 255, 255)):
        # image properties
        colors = max(1, min(256, colors))
        size = size - (size % blocks)
        w = size // blocks  # block width
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

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
        colors = max(1, min(256, colors))
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
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
        colors = max(1, min(256, colors))
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

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
        colors = max(1, min(256, colors))
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

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

    def filter_warhol(self, size=1024, colors=4, color=(0, 0, 0), padding=24, smooths=8):
        # image properties
        colors = max(1, min(256, colors))
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        q_size = (size - (3 * padding)) // 2
        size = size - (size % (q_size * 2 + padding * 3))

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [q_size, q_size, ], validate=False).convert('RGB')
        # smooth image
        for _ in range(smooths):
            image = image.filter(ImageFilter.SMOOTH_MORE).convert(
                'RGB').quantize(colors).convert('RGB')

        # get image data
        data = list(image.getdata())

        # get colors in picture
        def sum_tuple(t):
            r, g, b = t
            return r + g + b

        def random_color():
            return (randint(0, 255), randint(0, 255), randint(0, 255))

        colors_in_picture = sorted(list(set(data)), key=sum_tuple)
        k = str(colors_in_picture[0])
        warhol = []

        # generate lists of data with new colors
        for _ in range(4):
            d = {str(v): random_color() for v in colors_in_picture[1:]}
            d[k] = (0, 0, 0)
            warhol.append([d.get(str(px)) for px in data])

        data = []
        long_pad = [color for _ in range(size)]
        short_pad = [color for _ in range(padding)]
        for r in range(2):
            for _ in range(padding):
                data.extend(long_pad)
            for i in range(0, q_size**2, q_size):
                data.extend(short_pad)
                data.extend(warhol[2 * r][i:i + q_size])
                data.extend(short_pad)
                data.extend(warhol[2 * r + 1][i:i + q_size])
                data.extend(short_pad)
        for _ in range(padding):
            data.extend(long_pad)

        image = Image.new('RGB', (size, size))
        image.putdata(data)
        return image

    def filter_colorswap(self, size=1024, color=(0, 0, 0), padding=24):
        # image properties
        colors = 256
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        q_size = (size - (4 * padding)) // 3
        size = size - (size % (q_size * 3 + padding * 4))
        height = size - (q_size + padding)

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [q_size, q_size, ], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')

        # get image data
        px_data = []
        # rgb
        rgb = list(image.getdata())
        for r in range(3):
            for g in range(3):
                for b in range(3):
                    if ((r + g + b) == 3) and ((r**2 + b**2 + g**2) == 5):
                        px_data.append(
                            list(map(lambda t: (t[r], t[g], t[b]), rgb)))

        px_data[3], px_data[1], px_data[5], px_data[2] = px_data[1], px_data[2], px_data[3], px_data[5]

        data = []
        long_pad = [color for _ in range(size)]
        short_pad = [color for _ in range(padding)]
        for r in range(2):
            for _ in range(padding):
                data.extend(long_pad)
            for i in range(0, q_size**2, q_size):
                data.extend(short_pad)
                data.extend(px_data[3 * r][i:i + q_size])
                data.extend(short_pad)
                data.extend(px_data[3 * r + 1][i:i + q_size])
                data.extend(short_pad)
                data.extend(px_data[3 * r + 2][i:i + q_size])
                data.extend(short_pad)
        for _ in range(padding):
            data.extend(long_pad)

        image = Image.new('RGB', (size, height))
        image.putdata(data)
        return image

    def filter_colorscale(self, size=1024, color=(255, 255, 255), padding=16):
        # image properties
        colors = 256
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        q_size = (size - (4 * padding)) // 3
        size = size - (size % (q_size * 3 + padding * 4))

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [q_size, q_size], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')

        # get image data
        px_data = []
        # rgb
        rgb = list(image.getdata())
        for r in range(3):
            for g in range(3):
                for b in range(3):
                    if ((r + g + b) == 3) and ((r**2 + b**2 + g**2) == 5):
                        px_data.append(
                            list(map(lambda t: (t[r], t[g], t[b]), rgb)))

        # r g b only
        px_data.append(list(map(lambda t: (t[0], 0, 0), rgb)))
        px_data.append(list(map(lambda t: (0, t[1], 0), rgb)))
        px_data.append(list(map(lambda t: (0, 0, t[2]), rgb)))

        px_data[3], px_data[7], px_data[6], px_data[2], px_data[5] = px_data[2], px_data[3], px_data[5], px_data[6], px_data[7]

        data = []
        long_pad = [color for _ in range(size)]
        short_pad = [color for _ in range(padding)]
        for r in range(3):
            for _ in range(padding):
                data.extend(long_pad)
            for i in range(0, q_size**2, q_size):
                data.extend(short_pad)
                data.extend(px_data[3 * r][i:i + q_size])
                data.extend(short_pad)
                data.extend(px_data[3 * r + 1][i:i + q_size])
                data.extend(short_pad)
                data.extend(px_data[3 * r + 2][i:i + q_size])
                data.extend(short_pad)
        for _ in range(padding):
            data.extend(long_pad)

        image = Image.new('RGB', (size, size))
        image.putdata(data)
        return image

    def filter_minimalist(self, size=1024, colors=4, color=(255, 255, 255), padding=128):
        # image properties
        colors = max(1, min(256, colors))
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        height = (size - ((colors + 1) * padding)) // colors
        size = size - (size % ((height * colors) + (colors + 1) * padding))
        width = size - (2 * padding)

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [size, size], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')

        # get image data
        colors_in_picture = list(set(list(image.getdata())))

        # padding data sets
        long_pad = [color for _ in range(padding * size)]
        short_pad = [color for _ in range(padding)]

        data = long_pad[:]
        for unique_color in colors_in_picture:
            for i in range(height):
                data.extend(short_pad)
                data.extend([unique_color for _ in range(width)])
                data.extend(short_pad)
            data.extend(long_pad)

        image = Image.new('RGB', (size, size))
        image.putdata(data)
        return image

    def filter_minimalistwave(self, size=1024, color=(255, 255, 255), padding=32, jump=1, step=1):
        # image properties
        colors = 2
        r, g, b = color
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        size = size - ((size - (2 * padding)) % step)
        inner = size - (2 * padding)

        # load image into memory
        image = self.image
        image = resizeimage.resize_cover(
            image, [size, size], validate=False).convert('RGB')
        image = image.quantize(colors).convert('RGB')

        # get image data
        color_a, color_b = tuple(set(list(image.getdata())))

        # padding data sets
        long_pad = [color for _ in range(padding * size)]
        short_pad = [color for _ in range(padding)]

        c = inner // 2
        data = long_pad[:]
        for a in range(0, inner, step):
            for b in range(step):
                data.extend(short_pad)
                data.extend([color_a for _ in range(c)])
                data.extend([color_b for _ in range(c, inner)])
                data.extend(short_pad)
            c = min(inner, max(c + choice([-jump, 0, jump]), 0))
        data.extend(long_pad)

        image = Image.new('RGB', (size, size))
        image.putdata(data)
        return image

    def save(self):
        disk.save_image(self)
