#!/usr/bin/env python
#
# Copyright (c) 2014-2018 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
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
import re

_exe = TestSCons._exe
test = TestSCons.TestSCons()

##if not test.where_is('cxxtest'):
##    test.skip_test("Could not find 'clang', skipping test.\n")

test.file_fixture('../../../__init__.py', 'site_scons/site_tools/cxxtest/__init__.py')
test.dir_fixture('../../../cxxtest', 'cxxtest')

test.write('SConstruct', """
DefaultEnvironment(tools=[])
env = Environment(tools=['default', 'cxxtest'])
env.CxxTest('MyTestSuite1')
""")

test.write('MyTestSuite1.t.h', """\
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

test.run(['check'])

test.must_contain_all_lines(test.stdout(), ['MyTestSuite1', 'OK!'])
test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
