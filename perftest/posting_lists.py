# -*- encoding: utf-8 -*-

import random
import numpy as np

from numba import jit
from array import array
from timeit import Timer

from .posting_lists_cython import intersect_cython

def get_random_ints(sample_size=50000, a=1, b=500000):
    return sorted(random.sample(range(b), sample_size))


class IntersectBase(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def timeit(self):
        t = Timer(self)
        print(self.timeit_string.format(round(t.timeit(number=10), 5)))
    

class PythonListIntersect(IntersectBase):
    timeit_string = "naive python list intersection    : {:>30}s"

    def __call__(self):
        x, y = self.x, self.y
        p1, p2 = 0, 0
        intersection = []
        max_x, max_y = len(x), len(y)
        while p1 < max_x and p2 < max_y:
            a, b = x[p1], y[p2]
            if a == b:
                intersection.append(a)
                p1 += 1
                p2 += 1
            elif a < b:
                p1 += 1
            else:
                p2 += 1
        self.intersection = intersection
        return intersection


def list_intersect(x, y):
    p1, p2 = 0, 0
    intersection = []
    max_x, max_y = len(x), len(y)
    # numba does not support while conditions
    # or while True :/
    #while p1 < max_x and p2 < max_y:
    while 1:
        if not (p1 < max_x and p2 < max_y):
            break
        a, b = x[p1], y[p2]
        if a == b:
            intersection.append(a)
            p1 += 1
            p2 += 1
        elif a < b:
            p1 += 1
        else:
            p2 += 1
    return intersection

numba_list_intersect = jit()(list_intersect)


class NumbaListIntersect(IntersectBase):
    timeit_string = "python list intersection with @jit: {:>30}s"

    def __call__(self):
        self.intersection = numba_list_intersect(self.x, self.y)
        return self.intersection


class NumpyArrayIntersect(IntersectBase):
    timeit_string = "numpy array intersection          : {:>30}s"
    
    def __init__(self, x, y):
        super(NumpyArrayIntersect, self).__init__(x, y)
        self.xa = np.array(self.x)
        self.ya = np.array(self.y)

    def __call__(self):
        self.intersection = np.intersect1d(self.xa, self.ya)
        return self.intersection


class PythonSetIntersect(IntersectBase):
    timeit_string = "python set intersection           : {:>30}s"
    
    def __init__(self, x, y):
        super(PythonSetIntersect, self).__init__(x, y)
        self.xs = set(self.x)
        self.ys = set(self.y)
    
    def __call__(self):
        self.intersection = self.xs.intersection(self.ys)


class PythonArrayIntersect(IntersectBase):
    timeit_string = "python array intersection         : {:>30}s"

    def __init__(self, x, y):
        super(PythonArrayIntersect, self).__init__(x, y)
        self.xar = array("i", self.x)
        self.yar = array("i", self.y)

    def __call__(self):
        x, y = self.xar, self.yar
        p1, p2 = 0, 0
        intersection = array("i")
        max_x, max_y = len(x), len(y)
        while p1 < max_x and p2 < max_y:
            a, b = x[p1], y[p2]
            if a == b:
                intersection.append(a)
                p1 += 1
                p2 += 1
            elif a < b:
                p1 += 1
            else:
                p2 += 1
        self.intersection = intersection
        return intersection


class CythonArrayIntersect(IntersectBase):
    timeit_string = "cython array intersection         : {:>30}s"

    def __init__(self, x, y):
        super(CythonArrayIntersect, self).__init__(x, y)
        self.xar = array("i", self.x)
        self.yar = array("i", self.y)

    def __call__(self):
        self.intersection = intersect_cython(self.xar, self.yar)
        return self.intersection
    

def run_timeit():
    x, y = get_random_ints(), get_random_ints()
    test_classes = [
        NumbaListIntersect,
        PythonArrayIntersect,
        PythonListIntersect,
        NumpyArrayIntersect,
        PythonSetIntersect,
        CythonArrayIntersect,
    ]
    for TestClass in  test_classes:
        test_instance = TestClass(x, y)
        test_instance.timeit()
