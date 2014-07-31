rm *.so
rm perftest/*.so
rm perftest/perftest/posting_lists_cython.c
time python3 setup.py build_ext --inplace
cp posting_lists_cython.so perftest
cp posting_lists_extension.so perftest
