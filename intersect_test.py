# -*- encoding: utf-8 -*-

import sys
import numpy as np

from timeit import Timer

from perftest.posting_lists import list_intersect, get_random_ints, numba_list_intersect

def foobar():
    for i in range(100000):
        pass

def main(args):
    x, y = get_random_ints(), get_random_ints()
    xa = np.array(x)
    ya = np.array(y)
    print(len(list_intersect(x, y)))
    print(len(numba_list_intersect(x, y)))
    setup = '''
import numpy as np
from array import array
from perftest.posting_lists import list_intersect, get_random_ints, numba_list_intersect
from perftest.posting_lists_cython import intersect_cython
x, y = get_random_ints(), get_random_ints()
sx, sy = set(x), set(y)
xa = np.array(x)
ya = np.array(y)
xar = array("i", x)
yar = array("i", y)
    '''
    tl = Timer('list_intersect(x, y)', setup)
    tn = Timer('numba_list_intersect(x, y)', setup)
    ta = Timer('np.intersect1d(xa, ya)', setup)
    tr = Timer('intersect_cython(xar, yar)', setup)
    ts = Timer('sx.intersection(sy)', setup)
    tz = Timer(foobar, setup)
    print("list intersection:\t %s%s" % (round(min(tl.repeat(5, 10)), 6), "s"))
    print("numba list intersection:\t %s%s" % (round(min(tn.repeat(5, 10)), 6), "s"))
    print("numpy array intersection:\t %s%s" % (round(min(ta.repeat(5, 10)), 6), "s"))
    print("cython array intersection:\t %s%s" % (round(min(tr.repeat(5, 10)), 6), "s"))
    print("python set intersection:\t %s%s" % (round(min(ts.repeat(5, 10)), 6), "s"))
    print("python timeit callable:\t %s%s" % (round(min(tz.repeat(5, 10)), 6), "s"))

if __name__ == "__main__":
    main(sys.argv)
