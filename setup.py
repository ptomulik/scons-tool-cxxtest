# -*- coding: utf-8 -*-
"""scons-tool-cxxtest
"""

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
        name='scons-tool-cxxtest',
        version='0.1.2',
        package_dir={'sconstool.cxxtest': '.'},
        packages=['sconstool.cxxtest'],
        namespace_packages=['sconstool'],
        description='SCons tool for building and running unit tests based on CxxTest framework',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/ptomulik/scons-tool-cxxtest',
        author='Paweł Tomulik',
        author_email='ptomulik@meil.pw.edu.pl'
)

# vim: set expandtab tabstop=4 shiftwidth=4:
