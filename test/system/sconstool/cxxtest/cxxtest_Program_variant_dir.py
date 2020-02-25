# -*- coding: utf-8 -*-
#!/usr/bin/env python3
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

test.file_fixture('../../../../__init__.py', 'site_scons/site_tools/cxxtest/__init__.py')
test.file_fixture('../../../../about.py', 'site_scons/site_tools/cxxtest/about.py')

test.subdir('src')

test.write('SConstruct', r"""\
import sconstool.loader
sconstool.loader.extend_toolpath(transparent=True)
env = Environment(tools=['default', 'cxxtest'])
SConscript('src/SConscript', variant_dir='build', src_dir='src', duplicate=0, exports={'env': env})
""")

test.write(['src', 'SConscript'], r"""\
Import('env')
env.Program('MyTestSuite1.t.h')
""")

test.write(['src', 'MyTestSuite1.t.h'], """\
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

test.run()

test.must_exist(['build', 'MyTestSuite1.t.cpp'])
test.must_exist(['build', 'MyTestSuite1.t%s' % _obj])
test.must_exist(['build', 'MyTestSuite1.t%s' % _exe])

test.run(program=test.workpath('build/MyTestSuite1.t%s' % _exe),
         stdout='Running cxxtest tests (1 test)',
         match=lambda a,e: a.find(e) != -1)

test.run(['-c'])
test.must_not_exist(['build', 'MyTestSuite1.t.cpp'])
test.must_not_exist(['build', 'MyTestSuite1.t%s' % _obj])
test.must_not_exist(['build', 'MyTestSuite1.t%s' % _exe])

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
