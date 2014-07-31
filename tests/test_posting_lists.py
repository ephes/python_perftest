# -*- encoding: utf-8 -*-

import pytest

from perftest.posting_lists import ExtensionArrayIntersect
from perftest.posting_lists import CythonArrayIntersect
from perftest.posting_lists import PythonArrayIntersect
from perftest.posting_lists import PythonListIntersect
from perftest.posting_lists import NumpyArrayIntersect
from perftest.posting_lists import NumbaListIntersect
from perftest.posting_lists import PythonSetIntersect
from perftest.posting_lists import get_random_ints

TEST_CLASSES = [
    NumbaListIntersect,
    PythonArrayIntersect,
    PythonListIntersect,
    NumpyArrayIntersect,
    PythonSetIntersect,
#    CythonArrayIntersect,
    ExtensionArrayIntersect,
]

def test_simple_intersection():
    a, b, c = [1, 2, 3, 4], [4, 5, 6, 7], [4, 9, 10, 11]
    result = [4]
    for TestClass in TEST_CLASSES:
        test_instance = TestClass([a, b, c])
        assert test_instance.intersection_as_list() == result

def test_random_intersection():
    sample_size, low, high = 500, 0, 5000
    ilists = []
    for i in range(3):
        ilists.append(get_random_ints(sample_size=sample_size, a=low, b=high))
    result = PythonSetIntersect(ilists).intersection_as_list()
    print(result)
    for TestClass in TEST_CLASSES:
        test_instance = TestClass(ilists)
        assert test_instance.intersection_as_list() == result

def test_empty_intersection():
    a, b, c = [1, 2, 3], [5, 6, 7], [8, 9, 10]
    result = []
    for TestClass in TEST_CLASSES:
        test_instance = TestClass([a, b, c])
        assert test_instance.intersection_as_list() == result

def test_full_intersection():
    a, b, c = [1, 2, 3], [1, 2, 3], [1, 2, 3]
    result = a
    for TestClass in TEST_CLASSES:
        test_instance = TestClass([a, b, c])
        assert test_instance.intersection_as_list() == result

def test_one_empty_list_intersection():
    a, b, c = [], [4, 5, 6], [4, 5, 6]
    result = a
    for TestClass in TEST_CLASSES:
        test_instance = TestClass([a, b, c])
        assert test_instance.intersection_as_list() == result

def test_all_lists_empty_intersection():
    a, b, c = [], [], []
    result = a
    for TestClass in TEST_CLASSES:
        test_instance = TestClass([a, b, c])
        assert test_instance.intersection_as_list() == result
