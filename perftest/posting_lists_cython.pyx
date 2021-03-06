# -*- coding: utf-8 -*-
cimport cython

from cpython cimport array
from array import array

from cpython cimport Py_INCREF, Py_DECREF
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

cpdef array.array intersect_2cython(object x, object y):
    cdef int[:] cx = x
    cdef int[:] cy = y
    cdef int p1, p2
    p1, p2 = 0, 0

    cdef int size_x = cx.size, size_y = cy.size

    cdef array.array int_array_template = array('i', [])
    cdef array.array intersection
    cdef int is_idx
    cdef int is_size
    is_idx = 0
    is_size = min(size_x, size_y)
    intersection = array.clone(int_array_template, is_size, zero=False)

    cdef int a, b
    while p1 < size_x and p2 < size_y:
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

cpdef array.array intersect_lists_cython(lists):
    cdef int lists_len = len(lists)

    cdef int **my_arrays = <int **>PyMem_Malloc(lists_len * cython.sizeof(Py_ssize_t))
    if not my_arrays:
        raise MemoryError()

    cdef int *pointers = <int *>PyMem_Malloc(lists_len * cython.sizeof(Py_ssize_t))
    if not pointers:
        raise MemoryError()

    cdef int *list_lens = <int *>PyMem_Malloc(lists_len * cython.sizeof(Py_ssize_t))
    if not list_lens:
        raise MemoryError()

    cdef array.array int_array_template = array('i', [])
    cdef array.array intersection
    cdef int intersection_idx = 0, min_size, i_len_list

    cdef int[:] tmp_array

    for i in range(lists_len):
        i_len_list = len(lists[i])
        if i_len_list > 0:
            tmp_array = lists[i]
            my_arrays[i] = &tmp_array[0]
            pointers[i] = 0
            list_lens[i] = i_len_list
            if i == 0:
                min_size = i_len_list
            elif i_len_list < min_size:
                min_size = i_len_list
        else:
            PyMem_Free(my_arrays)
            PyMem_Free(pointers)
            PyMem_Free(list_lens)
            # one of the lists is empty, return empty intersection
            return array.clone(int_array_template, 0, zero=False)

    intersection = array.clone(int_array_template, min_size, zero=False)

    cdef int min_val = -1, max_val = -1, max_idx = -1
    cdef int min_idx = -1, tmp_val = -1, all_same = -1

    cdef int not_finished = 1
    while not_finished:
        all_same = 1
        for i in range(lists_len):
            tmp_val = my_arrays[i][pointers[i]]
            if i > 0:
                if tmp_val < min_val:
                    min_val = tmp_val
                    min_idx = i
                    all_same = 0
                elif tmp_val > min_val:
                    all_same = 0
                if tmp_val > max_val:
                    max_val = tmp_val
                    max_idx = i
            else:
                min_val = tmp_val
                min_idx = i
                max_val = tmp_val
                max_idx = i
        if all_same == 1:
            intersection[intersection_idx] = min_val
            intersection_idx += 1
            for i in range(lists_len):
                pointers[i] += 1
                if pointers[i] >= list_lens[i]:
                    not_finished = 0
        else:
            pointers[min_idx] += 1
            if pointers[min_idx] >= list_lens[min_idx]:
                not_finished = 0
#            for i in range(lists_len):
#                while pointers[i] < max_val and pointers[i] < list_lens[i]:
#                    pointers[i] += 1
#                if pointers[i] >= list_lens[i]:
#                    not_finished = 0
#                    break

    PyMem_Free(my_arrays)
    PyMem_Free(pointers)
    PyMem_Free(list_lens)

    array.resize(intersection, intersection_idx)
    return intersection
