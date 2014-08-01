rm perftest/*.so
rm perftest/perftest/posting_lists_cython.c
time python3 setup.py build_ext --inplace
