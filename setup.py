# -*- coding: utf-8 -*-
import os
import sys

from Cython.Build import cythonize

from distutils.core import setup, Extension

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='python_perftest',
    version='0.0.1',
    author='Jochen Wersdörfer',
    author_email='jochen-perftest@wersdoerfer.de',
    include_package_data=True,
    install_requires = [''],
    ext_modules = cythonize("perftest/posting_lists_cython.pyx"),
#    ext_modules = [
        #Extension("postings", sources=["postings/postings.c"])
        #Extension("postings_new", sources=["postings/postings_new.c"])
        #Extension("postings_new", sources=["postings/postings_new3.c"])
#    ],
    packages=['python_perftest'],
    url='https://github.com/ephes/python_perftest',
    license='BSD licence, see LICENCE.txt',
    description='Some performance tests comparing cpython with numba, cython etc.',
    long_description=open('README.md').read(),
)
