scons-tool-cxxtest
==================

.. image:: https://travis-ci.org/ptomulik/scons-tool-cxxtest.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-cxxtest
    :alt: Travis CI build status

SCons_ tool to compile and run unit tests based on CxxTest_ framework. This tool is extracted from sources found at `CxxTest Repository`_.

Installation
------------

First, install CxxTest framework, for example (Debian)::

    sudo apt-get install cxxtest

Installing with pipenv
^^^^^^^^^^^^^^^^^^^^^^

You should use this in projects using pipenv

.. code-block:: shell

      pipenv install --dev scons-tool-cxxtest

Alternativelly, you may add the following snippet to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-cxxtest = "*"


Installing as a git submodule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Create new git repository::

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-cxxtest`_ as a submodule::

      git submodule add git://github.com/ptomulik/scons-tool-cxxtest.git site_scons/site_tools/cxxtest

Usage example
-------------

#. Create simple test file

   .. code-block:: cpp

      // MyTestSuite1.t.h
      #include <cxxtest/TestSuite.h>
      class MyTestSuite1 : public CxxTest::TestSuite
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
      env = Environment(tools = ['default', 'cxxtest'])
      env.CxxTest('MyTestSuite1')

#. Try it out:

   .. code-block:: shell

      scons check

LICENSE
-------

See license text in **__init__.py**.

.. _CxxTest: http://cxxtest.com/
.. _CxxTest Repository: https://github.com/CxxTest/cxxtest
.. _scons-tool-cxxtest: https://github.com/ptomulik/scons-tool-cxxtest
.. _SCons: http://scons.org

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
