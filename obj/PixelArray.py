import numpy as np

from PIL import Image

import util.const as const
import util.util as util
import util.txt as txt

from obj.Pixel import Pixel

class PixelArray():

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.arr = [[Pixel(0, 0, 0) for i in range(self.y)] for j in range(self.x)]

    #TODO separate show and save
    def show(self):
        img = Image.new(mode="RGB", size=(self.x, self.y))
        #this is a much faster parse than np.nedumerate?
        for x in range(self.x):
            for y in range(self.y):
                px = self.arr[x][y]
                xy = (x, y)
                rgu = (px.r, px.g, px.u)
                img.putpixel(xy, rgu)
        img.show()
        img_str = const.IMG_SAVE + txt.date_file_str(util.now()) + ".png"
        img.save(img_str)

    def setp(self, x, y, r, g, u):
        try:
            self.arr[x][-1 * y].set_rgu(r, g, u)
        except:
            return
