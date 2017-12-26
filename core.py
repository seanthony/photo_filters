import disk


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
