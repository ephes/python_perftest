# -*- coding: utf-8 -*-
import os
import sys

from Cython.Build import cythonize

from distutils.core import setup, Extension

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

extensions = [
    Extension("posting_lists_extension",
        ["perftest/posting_lists_extension.c"]),
    Extension("posting_lists_cython",
        ["perftest/posting_lists_cython.pyx"]),
]

setup(
    name='python_perftest',
    version='0.0.1',
    author='Jochen Wersdörfer',
    author_email='jochen-perftest@wersdoerfer.de',
    include_package_data=True,
    install_requires = [''],
    ext_modules = cythonize(extensions),
    packages=['python_perftest'],
    url='https://github.com/ephes/python_perftest',
    license='BSD licence, see LICENCE.txt',
    description='Some performance tests comparing cpython with numba, cython etc.',
    long_description=open('README.md').read(),
)
