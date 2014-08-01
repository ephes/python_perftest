# -*- encoding: utf-8 -*-

import random
import numpy as np

from array import array
from timeit import Timer
from numba import jit as numba_jit

try:
    # python 2
    from itertools import izip
except ImportError as err:
    # python 3
    izip = zip

from .posting_lists_cython import intersect_2cython
from .posting_lists_cython import intersect_lists_cython
from .posting_lists_extension import intersect_lists_extension

def get_random_ints(sample_size=5000, a=0, b=10000):
    return sorted(random.sample(range(b), sample_size))


class IntersectBase(object):
    def __init__(self, lists):
        self.lists = lists

    def timeit(self):
        t = Timer(self)
        print(self.timeit_string.format(round(min(t.repeat(3, 10)), 6)))
    
    def intersection_as_list(self):
        return self()


class IntersectBaseArray(IntersectBase):
    def __init__(self, lists):
        super(IntersectBaseArray, self).__init__(lists)
        self.array_lists = []
        for posting_list in self.lists:
            self.array_lists.append(array("i", posting_list))

    def intersection_as_list(self):
        return list(self())


class PythonListIntersect(IntersectBase):
    timeit_string = "naive python list intersection        : {0:.5f}s"

    def __call__(self):
        lists = self.lists
        if len(lists) == 1:
            return lists[0]
        pointers = [0 for l in lists]
        intersection = []
        list_lens = [len(l) for l in lists]
        not_finished = len([(i, j) for i, j in zip(pointers, list_lens) if i >= j]) == 0
        while not_finished:
            values = [l[p] for l, p in izip(lists, pointers)]
            if len(set(values)) == 1:
                intersection.append(values[0])
                for i, p in enumerate(pointers):
                    pointers[i] += 1
                    if pointers[i] >= list_lens[i]:
                        not_finished = False
            else:
                min_val, min_num = min([(j, i) for i, j in enumerate(values)])
                pointers[min_num] += 1
                if pointers[min_num] >= list_lens[min_num]:
                    not_finished = False
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

numba_list_intersect = numba_jit()(list_intersect)


class NumbaListIntersect(IntersectBase):
    timeit_string = "list intersection with numba @jit     : {0:.5f}s"

    def __call__(self):
        lists = self.lists
        if len(lists) == 1:
            return lists[0]
        else:
            tmp_intersection = numba_list_intersect(lists[0], lists[1])
            for new_list in lists[2:]:
                tmp_intersection = numba_list_intersect(tmp_intersection, new_list)
            return tmp_intersection


class NumpyArrayIntersect(IntersectBase):
    timeit_string = "numpy array intersection              : {0:.5f}s"
    
    def __init__(self, lists):
        super(NumpyArrayIntersect, self).__init__(lists)
        self.array_lists = []
        for posting_list in self.lists:
            self.array_lists.append(np.array(posting_list))

    def __call__(self):
        lists = self.lists
        if len(lists) == 1:
            return lists[0]
        else:
            tmp_intersection = np.intersect1d(self.array_lists[0],
                self.array_lists[1])
            for new_list in self.array_lists[2:]:
                tmp_intersection = np.intersect1d(tmp_intersection, new_list)
            return tmp_intersection

    def intersection_as_list(self):
        return list(self())


class PythonSetIntersect(IntersectBase):
    timeit_string = "python set intersection               : {0:.5f}s"
    
    def __init__(self, lists):
        super(PythonSetIntersect, self).__init__(lists)
        self.set_lists = []
        for posting_list in self.lists:
            self.set_lists.append(set(posting_list))
    
    def __call__(self):
        return set.intersection(*self.set_lists)

    def intersection_as_list(self):
        return sorted(list(self()))


class PythonArrayIntersect(IntersectBaseArray):
    timeit_string = "python array intersection             : {0:.5f}s"

    def __call__(self):
        lists = self.array_lists
        pointers = array("i", [0 for l in lists])
        intersection = array("i")
        array_lens = [len(ar) for ar in lists]
        not_finished = len([(i, j) for i, j in zip(pointers, array_lens) if i >= j]) == 0
        while not_finished:
            values = [l[p] for l, p in izip(lists, pointers)]
            if len(set(values)) == 1:
                intersection.append(values[0])
                for i, p in enumerate(pointers):
                    pointers[i] += 1
                    if pointers[i] >= array_lens[i]:
                        not_finished = False
            else:
                min_val, min_num = min([(j, i) for i, j in enumerate(values)])
                pointers[min_num] += 1
                if pointers[min_num] >= array_lens[min_num]:
                    not_finished = False
        self.intersection = intersection
        return intersection


class CythonArrayIntersect(IntersectBaseArray):
    timeit_string = "cython intersection of multiple arrays: {0:.5f}s"

    def __call__(self):
        #return intersect_2cython(self.xar, self.yar)
        return intersect_lists_cython(self.array_lists)

    
class CythonArrayIntersect2(IntersectBaseArray):
    timeit_string = "cython intersection of 2 arrays       : {0:.5f}s"

    def __call__(self):
        lists = self.lists
        if len(lists) == 1:
            return lists[0]
        else:
            tmp_intersection = intersect_2cython(self.array_lists[0], self.array_lists[1])
            for new_list in self.array_lists[2:]:
                tmp_intersection = intersect_2cython(tmp_intersection, new_list)
            return tmp_intersection


class ExtensionArrayIntersect(IntersectBaseArray):
    timeit_string = "c extension array intersection        : {0:.5f}s"

    def __call__(self):
        return intersect_lists_extension(self.array_lists)

    
def run_timeit():
    posting_lists = [get_random_ints() for i in range(5)]
    test_classes = [
        PythonArrayIntersect,
        PythonListIntersect,
        NumbaListIntersect,
        NumpyArrayIntersect,
        ExtensionArrayIntersect,
        CythonArrayIntersect,
        CythonArrayIntersect2,
        PythonSetIntersect,
    ]
    for TestClass in  test_classes:
        test_instance = TestClass(posting_lists)
        test_instance.timeit()
