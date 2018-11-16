# -*- coding: utf-8 -*-
"""sconstool.cxxtest

Tool-specific initialization for cxxtest.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

#
# Copyright (c) 2018 Paweł Tomulik
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

from .about import __version__

import SCons.Tool
import SCons.Defaults
import SCons.Util
import SCons.Action
import os

try:
    import site_tools.cxxtestgen as cxxtestgen
except ImportError:
    import sconstool.cxxtestgen as cxxtestgen
try:
    from site_tools.util import Selector, \
                                Replacements, \
                                ReplacingBuilder, \
                                ReplacingAction
except ImportError:
    from sconstool.util import Selector, \
                               Replacements, \
                               ReplacingBuilder, \
                               ReplacingAction


CxxTestVars = [
    'OBJPREFIX',
    'OBJSUFFIX',
    'CXX',
    'CCFLAGS',
    'CXXFLAGS',
    'CPPFLAGS',
    'CPPDEFINES',
    'CPPPATH',
    'LINK',
    'LINKFLAGS',
    'LIBPATH',
    'LIBS',
    'LIBPREFIX',
    'LIBSUFFIX',
    'PROGPREFIX',
    'PROGSUFFIX',
]


CxxTestReplacements = Replacements({k: 'CXXTEST%s' % k for k in CxxTestVars})

class TestRunnerAction(object):
    def __init__(self, action):
        self.action = action

    def __getattr__(self, name):
        return getattr(self.action, name)

    def __setattr__(self, name, value):
        if name in ('action',):
            super(TestRunnerAction, self).__setattr__(name, value)
        else:
            setattr(self.action, name, value)

    def __call__(self, target, source, env, *args, **kw):
        result = 0
        for src in source:
            r = self.action(target, [src], env, *args, **kw)
            if r != 0 and result in (0, 2):
                result = r
        return result


class CxxTestLinkingBuilder(ReplacingBuilder):
    def __call__(self, env, target, source, *args, **kw):
        # preserve LIBPREFIXES and LIBSUFFIXES, so we'll still be able to
        # link agains libraries with original $LIBPREFIX, $LIBSUFFIX etc.,
        # even if someone sets $CXXTESTLIBPREFIX, $CXXTESTLIBSUFFIX, etc.
        ovr = {'LIBPREFIXES': [env.subst(x) for x in env['LIBPREFIXES']],
               'LIBSUFFIXES': [env.subst(x) for x in env['LIBSUFFIXES']]}
        return ReplacingBuilder.__call__(self, env, target, source, *args, **dict(ovr, **kw))


CxxTestCXXAction = ReplacingAction(SCons.Defaults.CXXAction, CxxTestReplacements)
runAction = TestRunnerAction(SCons.Action.Action("$CXXTESTRUNCOM", "$CXXTESTRUNCOMSTR"))


def createCxxTestObjBuilder(env):
    try:
        obj = env['BUILDERS']['CxxTestStaticObject']
    except KeyError:
        obj = SCons.Builder.Builder(action=SCons.Defaults.CXXAction,
                                    emitter={},
                                    prefix='$OBJPREFIX',
                                    suffix='$OBJSUFFIX',
                                    src_builder=['CxxTestGen'],
                                    src_suffix='$CXXTESTGENSUFFIX',
                                    source_scanner=SCons.Tool.SourceFileScanner,
                                    single_source=1)
        obj = ReplacingBuilder(obj, CxxTestReplacements)
        env['BUILDERS']['CxxTestStaticObject'] = obj
        env['BUILDERS']['CxxTestObject'] = obj
    return obj


def createCxxTestProgBuilder(env):
    try:
        prog = env['BUILDERS']['CxxTestProgram']
    except KeyError:
        prog = SCons.Builder.Builder(action=SCons.Defaults.LinkAction,
                                     emitter='$PROGEMITTER',
                                     prefix='$PROGPREFIX',
                                     suffix='$PROGSUFFIX',
                                     src_suffix='$OBJSUFFIX',
                                     src_builder='CxxTestObject',
                                     target_scanner=SCons.Tool.ProgramScanner)
        prog = CxxTestLinkingBuilder(prog, CxxTestReplacements)
        env['BUILDERS']['CxxTestProgram'] = prog
    return prog


def createCxxTestBuilder(env):
    try:
        return env['BUILDERS']['CxxTest']
    except KeyError:
        env['BUILDERS']['CxxTest'] = _CxxTestWrapper
        return _CxxTestWrapper


def _list_sources(nodes):
    sources = []
    for node in nodes:
        sources += node.sources
    return sources


def _CxxTestWrapper(env, target, source=None, root=[], **kw):
    if root:
        root = env.CxxTestGenRoot(root, **kw)

    if target is None:
        prgs = []
        for src in source:
            prgs += env.CxxTestProgram([src] + root, **kw)
    else:
        if root:
            parts = source
        else:
            root = env.CxxTestGen(source[0], **kw)
            parts = source[1:]
        cxxs = []
        for part in parts:
            cxxs += env.CxxTestGenPart(part, **kw)
        prgs = env.CxxTestProgram(target, root + cxxs, **kw)

    if kw.get('CXXTESTALIAS', env.get('CXXTESTALIAS')):
        # Alias takes ownership over the nodes
        alias = env.Alias('$CXXTESTALIAS', prgs, runAction, **kw)
        env.AlwaysBuild(alias)

        # Do not build nodes by default
        objs = _list_sources(prgs)
        cxxs = _list_sources(objs)
        for node in (prgs + objs + cxxs):
            env.Ignore(node.dir, node)
            env.Clean(node.dir, node)
        return alias
    return prgs


def extendObjBuilders(env):
    obj, _ = SCons.Tool.createObjBuilders(env)
    src_suffix = env.subst('$CXXTESTGENSUFFIX') or '.t.cpp'
    obj.add_action(src_suffix, CxxTestCXXAction)
    if SCons.Util.is_Dict(obj.suffix):
        obj.set_suffix(Selector(obj.suffix))
    else:
        obj.set_suffix(Selector({None: obj.suffix}))
    obj.suffix['$CXXTESTGENSUFFIX'] = '$CXXTESTOBJSUFFIX'


def extendProgBuilder(env):
    # Seems, we can't do anything usefull here... The default program builder
    # has fixed action and single suffix, independent on source suffix. That's
    # ok, it's not single source builder. It will still work, but will not use
    # our CXXTESTxxx variables and will probably append suffix ".t" to the
    # generated executables.
    pass


def findCxxTestIncludePath(env):
    def _p(p):
        return os.path.join(*(p.split('/')))

    script = env.subst('$CXXTESTGEN')
    if not script or not os.path.isfile(script):
        return []
    script = os.path.realpath(script)  # resolve symlinks

    scriptdir = os.path.dirname(script)
    for reldir in [_p('..'), _p('../..'), _p('../../..')]:
        incdir = os.path.join(scriptdir, reldir)
        if os.path.isfile(os.path.join(incdir, 'cxxtest', 'TestSuite.h')):
            return [os.path.normpath(incdir)]
    return []


def setCxxTestDefaults(env):
    env.SetDefault(CXXTESTOBJSUFFIX='.t$OBJSUFFIX')
    env.SetDefault(CXXTESTINCLUDEPATH=findCxxTestIncludePath(env))
    env.SetDefault(CXXTESTCPPPATH=['$CXXTESTINCLUDEPATH', '$CPPPATH'])
    env.SetDefault(CXXTESTALIAS='check')
    env.SetDefault(CXXTESTRUNFLAGS=[])
    env.SetDefault(CXXTESTRUNCOM='$SOURCE.abspath $CXXTESTRUNFLAGS')
    env.SetDefault(CXXTESTRUNCOMSTR='$CXXTESTRUNCOM')
    CxxTestReplacements.inject(env, 'SetDefault')


def generate(env):
    cxxtestgen.generate(env)
    extendObjBuilders(env)
    extendProgBuilder(env)
    createCxxTestObjBuilder(env)
    createCxxTestProgBuilder(env)
    createCxxTestBuilder(env)
    setCxxTestDefaults(env)


def exists(env):
    return cxxtestgen.exists(env)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
