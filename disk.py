from PIL import Image
from resizeimage import resizeimage
from os.path import isfile


def open(filename):
    image = Image.open(filename)
    w, h = image.size
    s = min([w, h])
    box = ((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)
    image = image.crop(box=box).quantize(256).convert('RGB')
    image = resizeimage.resize_cover(
        image, [s, s], validate=False).convert('RGB')
    return image


def is_file(filename):
    return isfile(fname)
