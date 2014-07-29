# -*- coding: utf-8 -*-

from cpython cimport array
from array import array

cpdef array.array intersect_cython(object x, object y):
    cdef int[:] cx = x
    cdef int[:] cy = y
    cdef int p1, p2
    p1, p2 = 0, 0

    cdef int max_x, max_y
    max_x, max_y = cx.size, cy.size

    cdef array.array int_array_template = array('i', [])
    cdef array.array intersection
    cdef int is_idx
    cdef int is_size
    is_idx = 0
    is_size = max(max_x, max_y)
    intersection = array.clone(int_array_template, is_size, zero=False)

    cdef int a, b
    while p1 < max_x and p2 < max_y:
        a, b = cx[p1], cy[p2]
        if a == b:
            intersection[is_idx] = a
            is_idx += 1
            p1 += 1
            p2 += 1
        elif a < b:
            p1 += 1
        else:
            p2 += 1 
    array.resize(intersection, is_idx)
    return intersection
