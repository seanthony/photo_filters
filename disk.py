from PIL import Image, ImageFont
from resizeimage import resizeimage
from os.path import isfile, join


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
    return isfile(filename)


def save_image(image_obj):
    fp = join('.', 'filtered_photos', image_obj.filename)
    image_obj.image.save(fp)


def get_font(fontsize):
    # I had to link directly to the file on my hard drive in fonts because of windows permissions
    try:
        return ImageFont.truetype('./Fonts/Blackout-2am_0.ttf', fontsize)
    except OSError:
        return ImageFont.truetype('C:\\Windows\\Fonts\\Blackout-2am_0.ttf', fontsize)
