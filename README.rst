scons-tool-cxxtest
==================

SCons_ tool to compile and run unit tests based on CxxTest_ framework. This tool is extracted from sources found at `CxxTest Repository`_.

Usage example
-------------

First, install CxxTest framework, for example (Debian)::

    sudo apt-get install cxxtest

Git-based projects
^^^^^^^^^^^^^^^^^^

#. Create new git repository::

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-cxxtest`_ as a submodule::

      git submodule add git://github.com/ptomulik/scons-tool-cxxtest.git site_scons/site_tools/cxxtest

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

#. Try it out::

      scons check

LICENSE
-------

See license text in **__init__.py**.

.. _CxxTest: http://cxxtest.com/
.. _CxxTest Repository: https://github.com/CxxTest/cxxtest
.. _scons-tool-cxxtest: https://github.com/ptomulik/scons-tool-cxxtest
.. _SCons: http://scons.org

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
