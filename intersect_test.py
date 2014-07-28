# -*- encoding: utf-8 -*-

import sys
import numpy as np

from timeit import Timer

from perftest.posting_lists import list_intersect, get_random_ints, numba_list_intersect

def main(args):
    x, y = get_random_ints(), get_random_ints()
    xa = np.array(x)
    ya = np.array(y)
    print(len(list_intersect(x, y)))
    print(len(numba_list_intersect(x, y)))
    setup = '''
import numpy as np
from perftest.posting_lists import list_intersect, get_random_ints, numba_list_intersect
x, y = get_random_ints(), get_random_ints()
xa = np.array(x)
ya = np.array(y)
    '''
    tl = Timer('list_intersect(x, y)', setup)
    tn = Timer('numba_list_intersect(x, y)', setup)
    ta = Timer('np.intersect1d(xa, ya)', setup)
    print("list intersection:\t %s%s" % (round(min(tl.repeat(5, 10)), 6), "s"))
    print("numba list intersection:\t %s%s" % (round(min(tn.repeat(5, 10)), 6), "s"))
    print("numpy array intersection:\t %s%s" % (round(min(ta.repeat(5, 10)), 6), "s"))

if __name__ == "__main__":
    main(sys.argv)
