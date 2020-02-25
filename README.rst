scons-tool-cxxtest
=====================

.. image:: https://badge.fury.io/py/scons-tool-cxxtest.svg
    :target: https://badge.fury.io/py/scons-tool-cxxtest
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-cxxtest.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-cxxtest
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-cxxtest?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-cxxtest

SCons_ tool to compile and run unit tests based on cxxtest_ framework.

Installation
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add cxxtest tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-cxxtest

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-cxxtest

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-cxxtest = "*"


The tool will be installed as a namespaced package ``sconstool.cxxtest``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-cxxtest`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-cxxtest.git site_scons/site_tools/cxxtest

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.cxxtest`` (this may be required by other tools).

Usage example
-------------

#. Create simple test file

   .. code-block:: cpp

      // MyTestSuite.t.h
      #include <cxxtest/TestSuite.h>
      class MyTestSuite : public CxxTest::TestSuite
      {
      public:
        void testAddition(void)
        {
          TS_ASSERT(1 + 1 > 1);
          TS_ASSERT_EQUALS(1 + 1, 2);
        }
      };

#. Create simple SConstruct file

   .. code-block:: python

      # SConstruct
      # TODO: uncomment following lines if the tool is installed via pip/pipenv
      # import sconstool.loader
      # sconstool.loader.extend_toolpath(transparent=True)
      env = Environment(tools = ['default', 'cxxtest'])
      env.CxxTest('MyTestSuite')

#. Try it out:

   .. code-block:: shell

      scons

Builders
--------

- ``CxxTestObject([target], source, **kw)``,
- ``CxxTestProgram([target], source, **kw)``,
- ``CxxTest([target], source, [root], **kw)``.

Construction variables used
---------------------------

The following SCons construction variables might be used to customize the
**cxxtest** tool. In addition to these, a ``$CXXTESTGENSUFFIX`` is used as
the source suffix for ``CxxTestObject`` builder, see scons-tool-cxxtestgen_.

+------------------------+---------------------------------------------------+-----------------------------------------+
|        Name            |                      Description                  |               Default Value             |
+========================+===================================================+=========================================+
| CXXTESTCCFLAGS         | Options for C and C++ compilers.                  | ``"$CCFLAGS"``                          |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTCPPDEFINES      | C preprocessor definitions.                       | ``"$CPPDEFINES"``                       |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTCPPFLAGS        | C preprocessor options.                           | ``"$CPPFLAGS"``                         |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTCPPPATH         | List of C/C++ include directories.                | ``["$CXXTESTINCLUDEPATH", "$CPPPATH"]`` |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTCXX             | The C++ compiler.                                 | ``"$CXX"``                              |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTCXXFLAGS        | Options for C++ compiler.                         | ``"$CXXFLAGS"``                         |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTINCLUDEPATH     | Extra include path to be prepended to CPPPATH.    | Determined automatically.               |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTLIBPATH         | List of directories to be searched for libraries. | ``"$LIBPATH"``                          |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTLIBPREFIX       | The prefix used for (static) library names.       | ``"$LIBPREFIX"``                        |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTLIBS            | A list of libraries to be linked with executable. | ``"$LIBS"``                             |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTLIBSUFFIX       | The suffix used for (static) library names.       | ``"$LIBSUFFIX"``                        |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTLINK            | The linker.                                       | ``"$LINK"``                             |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTLINKFLAGS       | General user options passed to the linker.        | ``"$LINKFLAGS"``                        |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTOBJPREFIX       | The prefix used for (static) object file names.   | ``"$OBJPREFIX"``                        |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTOBJSUFFIX       | The suffix used for (static) object file names.   | ``"$OBJSUFFIX"``                        |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTPROGPREFIX      | The prefix used for executable file names.        | ``"$PROGPREFIX"``                       |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTPROGSUFFIX      | The suffix used for executable file names.        | ``"$PROGSUFFIX"``                       |
+------------------------+---------------------------------------------------+-----------------------------------------+
| CXXTESTRUNFLAGS        | Options for test runner.                          | ``[]``                                  |
+------------------------+---------------------------------------------------+-----------------------------------------+


LICENSE
-------

Copyright (c) 2018-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _scons-tool-cxxtest: https://github.com/ptomulik/scons-tool-cxxtest
.. _scons-tool-cxxtestgen: https://github.com/ptomulik/scons-tool-cxxtestgen
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader
.. _SCons: http://scons.org
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
.. _cxxtest: http://cxxtest.com/

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
