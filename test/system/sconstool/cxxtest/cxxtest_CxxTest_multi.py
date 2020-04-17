#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import TestSCons
import sys
import os

_exe = TestSCons._exe
_obj = TestSCons._obj

if sys.platform == 'win32':
    test = TestSCons.TestSCons(program='scons.bat', interpreter=None)
else:
    test = TestSCons.TestSCons()

test.subdir('cxxtest')
try:
    test.dir_fixture('../../../../cxxtest', 'cxxtest')
except OSError:
    # test with other cxxtest, if there is no cxxtest in project tree
    pass

def find_line(content, line):
    return line in [s.strip() for s in content.splitlines()]

test.file_fixture('../../../../__init__.py', 'site_scons/site_tools/cxxtest/__init__.py')
test.file_fixture('../../../../about.py', 'site_scons/site_tools/cxxtest/about.py')

test.write('MyTestSuite1.t.h', r"""\
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
""")

test.write('MyTestSuite2.t.h', r"""\
// MyTestSuite2.t.h
#include <cxxtest/TestSuite.h>
class MyTestSuite2 : public CxxTest::TestSuite
{
public:
void testAddition(void)
{
  TS_ASSERT(2 + 2 > 2);
  TS_ASSERT_EQUALS(2 + 2, 4);
}
};
""")

test.write('MyTestSuite3.t.h', r"""\
// MyTestSuite2.t.h
#include <cxxtest/TestSuite.h>
class MyTestSuite3 : public CxxTest::TestSuite
{
public:
void testAddition(void)
{
  TS_ASSERT(3 + 3 > 3);
  TS_ASSERT_EQUALS(3 + 3, 6);
}
};
""")

#
# Without specifying target name
#

test.write('SConstruct', r"""\
import sconstool.loader
sconstool.loader.extend_toolpath(transparent=True)
env = Environment(tools=['default', 'cxxtest'])
env.CxxTest(['MyTestSuite1.t.h', 'MyTestSuite2.t.h'])
""")

test.run()  # nothing should happen .. but it happens unfortunatelly
test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_not_exist('MyTestSuite1.t.cpp')
test.must_not_exist('MyTestSuite2.t.cpp')
test.must_not_exist('MyTestSuite1.t%s' % _obj)
test.must_not_exist('MyTestSuite2.t%s' % _obj)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)

test.run(['check'])
test.must_contain_all_lines(test.stdout(), [test.workpath('MyTestSuite1'), test.workpath('MyTestSuite2')], find_line)

test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_exist('MyTestSuite1.t.cpp')
test.must_exist('MyTestSuite2.t.cpp')
test.must_exist('MyTestSuite1.t%s' % _obj)
test.must_exist('MyTestSuite2.t%s' % _obj)
test.must_exist('MyTestSuite1%s' % _exe)
test.must_exist('MyTestSuite2%s' % _exe)

test.run(['check'])
test.must_contain_all_lines(test.stdout(), [test.workpath('MyTestSuite1'), test.workpath('MyTestSuite2')], find_line)

test.run()
test.must_not_contain_any_line(test.stdout(), [test.workpath('MyTestSuite1'), test.workpath('MyTestSuite2')], find_line)

test.run(['-c'])
test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_not_exist('MyTestSuite1.t.cpp')
test.must_not_exist('MyTestSuite2.t.cpp')
test.must_not_exist('MyTestSuite1.t%s' % _obj)
test.must_not_exist('MyTestSuite2.t%s' % _obj)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)

#
# Without specified target name
#

test.write('SConstruct', r"""\
import sconstool.loader
sconstool.loader.extend_toolpath(transparent=True)
env = Environment(tools=['default', 'cxxtest'])
env.CxxTest('MyTestSuite', ['MyTestSuite1.t.h', 'MyTestSuite2.t.h', 'MyTestSuite3.t.h'])
""")

test.run()  # nothing should happen .. but it happens unfortunatelly
test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_not_exist('MyTestSuite.t.cpp')
test.must_not_exist('MyTestSuite1.t.cpp')
test.must_not_exist('MyTestSuite2.t.cpp')
test.must_not_exist('MyTestSuite3.t.cpp')
test.must_not_exist('MyTestSuite.t%s' % _obj)
test.must_not_exist('MyTestSuite1.t%s' % _obj)
test.must_not_exist('MyTestSuite2.t%s' % _obj)
test.must_not_exist('MyTestSuite3.t%s' % _obj)
test.must_not_exist('MyTestSuite%s' % _exe)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)
test.must_not_exist('MyTestSuite3%s' % _exe)

test.run(['check'])
test.must_contain_all_lines(test.stdout(), [test.workpath('MyTestSuite')], find_line)
test.must_not_contain_any_line(test.stdout(), [test.workpath('MyTestSuite1'), test.workpath('MyTestSuite2')], find_line)

test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_exist('MyTestSuite3.t.h')
test.must_not_exist('MyTestSuite.t.cpp')
test.must_exist('MyTestSuite1.t.cpp')
test.must_exist('MyTestSuite2.t.cpp')
test.must_exist('MyTestSuite3.t.cpp')
test.must_not_exist('MyTestSuite.t%s' % _obj)
test.must_exist('MyTestSuite1.t%s' % _obj)
test.must_exist('MyTestSuite2.t%s' % _obj)
test.must_exist('MyTestSuite3.t%s' % _obj)
test.must_exist('MyTestSuite%s' % _exe)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)

test.run(['-c'])
test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_not_exist('MyTestSuite.t.cpp')
test.must_not_exist('MyTestSuite1.t.cpp')
test.must_not_exist('MyTestSuite2.t.cpp')
test.must_not_exist('MyTestSuite3.t.cpp')
test.must_not_exist('MyTestSuite.t%s' % _obj)
test.must_not_exist('MyTestSuite1.t%s' % _obj)
test.must_not_exist('MyTestSuite2.t%s' % _obj)
test.must_not_exist('MyTestSuite3.t%s' % _obj)
test.must_not_exist('MyTestSuite%s' % _exe)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)
test.must_not_exist('MyTestSuite3%s' % _exe)

#
# Without CXXTESTROOT
#

test.write('SConstruct', r"""\
import sconstool.loader
sconstool.loader.extend_toolpath(transparent=True)
env = Environment(tools=['default', 'cxxtest'])
env.CxxTest('MyTestSuite', ['MyTestSuite1.t.h', 'MyTestSuite2.t.h', 'MyTestSuite3.t.h'], 'MyTestSuite.t.cpp')
""")

test.run()  # nothing should happen .. but it happens unfortunatelly
test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_not_exist('MyTestSuite.t.cpp')
test.must_not_exist('MyTestSuite1.t.cpp')
test.must_not_exist('MyTestSuite2.t.cpp')
test.must_not_exist('MyTestSuite3.t.cpp')
test.must_not_exist('MyTestSuite.t%s' % _obj)
test.must_not_exist('MyTestSuite1.t%s' % _obj)
test.must_not_exist('MyTestSuite2.t%s' % _obj)
test.must_not_exist('MyTestSuite3.t%s' % _obj)
test.must_not_exist('MyTestSuite%s' % _exe)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)
test.must_not_exist('MyTestSuite3%s' % _exe)

test.run(['check'])
test.must_contain_all_lines(test.stdout(), [test.workpath('MyTestSuite')], find_line)
test.must_not_contain_any_line(test.stdout(), [test.workpath('MyTestSuite1'), test.workpath('MyTestSuite2')], find_line)

test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_exist('MyTestSuite3.t.h')
test.must_exist('MyTestSuite.t.cpp')
test.must_exist('MyTestSuite1.t.cpp')
test.must_exist('MyTestSuite2.t.cpp')
test.must_exist('MyTestSuite3.t.cpp')
test.must_exist('MyTestSuite.t%s' % _obj)
test.must_exist('MyTestSuite1.t%s' % _obj)
test.must_exist('MyTestSuite2.t%s' % _obj)
test.must_exist('MyTestSuite3.t%s' % _obj)
test.must_exist('MyTestSuite%s' % _exe)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)

test.run(['-c'])
test.must_exist('MyTestSuite1.t.h')
test.must_exist('MyTestSuite2.t.h')
test.must_not_exist('MyTestSuite.t.cpp')
test.must_not_exist('MyTestSuite1.t.cpp')
test.must_not_exist('MyTestSuite2.t.cpp')
test.must_not_exist('MyTestSuite3.t.cpp')
test.must_not_exist('MyTestSuite.t%s' % _obj)
test.must_not_exist('MyTestSuite1.t%s' % _obj)
test.must_not_exist('MyTestSuite2.t%s' % _obj)
test.must_not_exist('MyTestSuite3.t%s' % _obj)
test.must_not_exist('MyTestSuite%s' % _exe)
test.must_not_exist('MyTestSuite1%s' % _exe)
test.must_not_exist('MyTestSuite2%s' % _exe)
test.must_not_exist('MyTestSuite3%s' % _exe)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
