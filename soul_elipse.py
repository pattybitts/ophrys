
import util.const as const
import util.util as util
import util.calc as calc

from obj.PixelArray import PixelArray
from obj.AngularElipses import AngularElipses

#fyi height is 1000, width is 1618
parr = PixelArray(1000 * const.GOLDEN, 1000)

ae = AngularElipses(parr)

start_time = util.now()
x0 = 500
y0 = 200
x1 = 1500
y1 = 900
k_shift = 15
k = calc.distance(x0, y0, x1, y1) + 15
ae.draw_elipse(x0, y0, x1, y1, k)
parr.show()
render_time = util.now() - start_time
print("Total render time: {r:.1f}".format(r=render_time.total_seconds()))