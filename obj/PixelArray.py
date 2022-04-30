from PIL import Image

from obj.Pixel import Pixel

class PixelArray():

    def __init__(self, rows, cols):
        self.rows = int(rows)
        self.cols = int(cols)
        self.arr = [[Pixel(0, 0, 0) for i in range(self.cols)] for j in range(self.rows)]

    def show(self):
        img = Image.new(mode="RGB", size=(self.cols, self.rows))
        img.show()