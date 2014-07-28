# -*- encoding: utf-8 -*-

import random

from numba import jit

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

def get_random_ints(sample_size=10000, a=1, b=100000):
    return sorted(random.sample(range(b), sample_size))
