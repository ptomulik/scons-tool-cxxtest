#! /usr/bin/env python

#
# Copyright (c) 2014-2020 by Paweł Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

# Download local stuff required to generate docs and/or run test suites

import argparse
import os
import sys
import tarfile
import re
import io
import shutil

try:
    # Python 3
    from urllib.request import urlopen, urlretrieve
except ImportError:
    # Python 2
    from urllib2 import urlopen
    from urllib import urlretrieve

def scons_test_version_string(s):
    m = re.match(r'^(?P<maj>\d+)(?:\.(?P<min>\d+))(?:\.(?P<rel>\d+))$', s)
    if not m and s not in _scons_versions:
        raise argparse.ArgumentTypeError('wrong --scons-test-version %r' % s)
    return s

def cxxtest_version_string(s):
    m = re.match(r'^(?P<maj>\d+)(?:\.(?P<min>\d+))(?:\.(?P<rel>\d+))?$', s)
    if not m and s not in _cxxtest_versions:
        raise argparse.ArgumentTypeError('wrong --cxxtest-version %r' % s)
    return s

def untar(tar, **kw):
    # Options
    strip_components = kw.get('strip_components', 0)
    member_name_filter = kw.get('member_name_filter', lambda x: True)
    path = kw.get('path', '.')
    # Download the tar file
    members = [m for m in tar.getmembers() if len(m.name.split('/')) > strip_components]
    if strip_components > 0:
        for m in members:
            m.name = '/'.join(m.name.split('/')[strip_components:])

    members = [m for m in members if member_name_filter(m.name) ]
    tar.extractall(path = path, members = members)

def urluntar(url, **kw):
    # Download the tar file
    tar = tarfile.open(fileobj = io.BytesIO(urlopen(url).read()))
    untar(tar, **kw)
    tar.close()

def info(msg, **kw):
    try: quiet = kw['quiet']
    except KeyError: quiet = False
    if not quiet:
        sys.stdout.write("%s: info: %s\n" % (_script, msg))

def warn(msg, **kw):
    try: quiet = kw['quiet']
    except KeyError: quiet = False
    if not quiet:
        sys.stderr.write("%s: warning: %s\n" % (_script, msg))

def download_cxxtest(**kw):
    """Download cxxtest framework"""
    ver = kw.get('cxxtest_version', _default_cxxtest_version)
    clean = kw.get('clean', False)

    destdir = _topsrcdir

    if clean:
        info("cleaning cxxtest", **kw)
        for f in ['cxxtest']:
            ff = os.path.join(destdir,f)
            if os.path.exists(ff):
                info("removing '%s'" % ff, **kw)
                if os.path.isdir(ff):
                    shutil.rmtree(ff)
                else:
                    os.remove(ff)
        return 0

    url = "https://github.com/ptomulik/cxxtest/archive/%s.tar.gz" % ver
    info("downloading '%s' -> '%s'" % (url, destdir))
    urluntar(url, path = os.path.join(destdir, 'cxxtest'), strip_components = 1)
    return 0

def download_scons_test(**kw):
    """Download scons testing framework"""
    ver = kw.get('scons_test_version', kw.get('scons_version', _default_scons_test_version))
    clean = kw.get('clean', False)

    destdir = _topsrcdir

    if clean:
        info("cleaning scons-test", **kw)
        for f in ['runtest', 'runtest.py', 'testing']:
            ff = os.path.join(destdir,f)
            if os.path.exists(ff):
                info("removing '%s'" % ff, **kw)
                if os.path.isdir(ff):
                    shutil.rmtree(ff)
                else:
                    os.remove(ff)
        return 0

    url = "https://github.com/scons/scons/archive/%s.tar.gz" % ver
    info("downloading '%s' -> '%s'" % (url, destdir))
    member_name_filter = lambda s : re.match('(?:^runtest\.py$|testing/)', s)
    urluntar(url, path = destdir, strip_components = 1, member_name_filter = member_name_filter)
    shutil.move(os.path.join(destdir, 'runtest.py'), os.path.join(destdir, 'runtest'))
    return 0

# The script...
_script = os.path.basename(sys.argv[0])
_scriptabs = os.path.realpath(sys.argv[0])
_scriptdir = os.path.dirname(_scriptabs)
_topsrcdir = os.path.realpath(os.path.join(_scriptdir, '..'))

_all_packages = [ 'scons-test', 'cxxtest' ]

_default_packages = [ 'scons-test', 'cxxtest' ]

# scons versions other than x.y.z
_scons_versions = [
        'master',
        '3.1.2',
        '3.1.1',
        '3.1.0',
        '3.0.5',
        '3.0.4',
        '3.0.3',
        '3.0.2',
        '3.0.1',
        '3.0.0',
        '2.5.1',
        '2.5.0',
        '2.4.1',
        '2.4.0',
        '2.3.1',
        '2.3.0',
        '2.2.0',
        '2.1.0.final.0'
]

if sys.version_info.major == 2:
    _default_scons_version = '3.0.5'
else:
    _default_scons_version = _scons_versions[0]

# cxxtest version other than x.y[.z]
_cxxtest_versions = ['patched', 'master']
_default_cxxtest_version = _cxxtest_versions[0]

# scons-test
_default_scons_test_version = _default_scons_version

_parser = argparse.ArgumentParser(
        prog=_script,
        description="""\
        This tool downloads predefined prerequisites. You may cherry pick what
        to download or simply download all (if you don't specify explicitly
        packages, all predefined packages are being downloaded). The downloaded
        stuff is placed in predefined subdirectories of the source tree such
        that they are later found automatically when the project is being
        built.
        """)

_parser.add_argument('--quiet',
                      action='store_true',
                      help='do not print messages')
_parser.add_argument('--clean',
                      action='store_true',
                      help='clean downloaded package(s)')
_parser.add_argument('--scons-test-version',
                      type=scons_test_version_string,
                      default=_default_scons_test_version,
                      metavar='VER',
                      help='version of SCons test framework to be downloaded')
_parser.add_argument('--cxxtest-version',
                      type=cxxtest_version_string,
                      default=_default_cxxtest_version,
                      metavar='VER',
                      help='version of CxxTest to be downloaded')
_parser.add_argument('packages',
                      metavar='PKG',
                      type=str,
                      nargs='*',
                      default = _default_packages,
                      help='package to download (%s)' % ', '.join(_all_packages))

_args = _parser.parse_args()

def main():
    for pkg in _args.packages:
        if pkg.lower() == 'scons-test':
            download_scons_test(**vars(_args))
        elif pkg.lower() == 'cxxtest':
            download_cxxtest(**vars(_args))
        else:
            warn("unsupported package: %r" % pkg)
            return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
