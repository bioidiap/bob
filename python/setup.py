#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Thu 16 Aug 2012 11:36:19 CEST
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A setup file for Bob Python bindings using Boost.Python
"""

import os
import sys
import platform
from setuptools.command.build_ext import build_ext as build_ext_base
from setuptools import Extension
import subprocess


# ---------------------------------------------------------------------------#
#  various functions and classes to help on the setup                        #
# ---------------------------------------------------------------------------#

def pkgconfig(package):

  def uniq(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

  flag_map = {
      '-I': 'include_dirs',
      '-L': 'library_dirs',
      '-l': 'libraries',
      }

  cmd = [
      'pkg-config',
      '--libs',
      '--cflags',
      package,
      ]

  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)

  output = proc.communicate()[0]

  if proc.returncode != 0: return {}

  kw = {}

  for token in output.split():
    if flag_map.has_key(token[:2]):
      kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])

    else: # throw others to extra_link_args
      kw.setdefault('extra_compile_args', []).append(token)

  for k, v in kw.iteritems(): # remove duplicated
      kw[k] = uniq(v)

  return kw


def bob_variables():

  def get_var(name):
    cmd = [
        'pkg-config',
        '--variable=%s' % name,
        'bob',
        ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    var = proc.communicate()[0].strip()
    if proc.returncode != 0: return None
    return var


  cmd = [
      'pkg-config',
      '--modversion',
      'bob',
      ]

  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)

  output = proc.communicate()[0].strip()

  kw = {}
  kw['version'] = output if proc.returncode == 0 else None

  if kw['version'] is None:
    raise RuntimeError, 'Cannot retrieve Bob version from pkg-config:\n%s' % \
        output

  kw['base_libdir'] = get_var('libdir')
  kw['base_includedir'] = get_var('includedir')

  return kw

# Retrieve central, global variables from Bob's C++ build
BOB = bob_variables()


def uniq(seq, idfun=None):
  """Very fast, order preserving uniq function"""

  # order preserving
  if idfun is None:
      def idfun(x): return x
  seen = {}
  result = []
  for item in seq:
      marker = idfun(item)
      # in old Python versions:
      # if seen.has_key(marker)
      # but in new ones:
      if marker in seen: continue
      seen[marker] = 1
      result.append(item)
  return result


def uniq_paths(seq):
  """Uniq'fy a list of paths taking into consideration their real paths"""
  return uniq([os.path.realpath(k) for k in seq if os.path.exists(k)])


def setup_extension(ext_name, pc_file):
  """Sets up a given C++ extension"""

  import numpy

  pc = pkgconfig(pc_file + '%d%d' % sys.version_info[:2])

  library_dirs=pc.get('library_dirs', [])
  library_dirs=uniq_paths([k for k in library_dirs if os.path.exists(k)])
  include_dirs=pc.get('include_dirs', [])
  include_dirs=uniq_paths([k for k in include_dirs if os.path.exists(k)])
  extra_compile_args=pc.get('extra_compile_args', [])
  extra_compile_args.append('-pthread')

  if platform.system() == 'Darwin':
    sdkroot = os.environ.get('SDKROOT', '/opt/MacOSX10.9.sdk')
    if sdkroot:
      extra_compile_args = ['-isysroot', sdkroot] + extra_compile_args
    extra_compile_args += ['-Wno-#warnings']

  path_to_library = ext_name.rsplit('.', 1)[0]
  path_to_library = path_to_library.replace('.', os.sep)

  return Extension(
      ext_name,
      sources=[os.path.join(path_to_library, 'main.cc')],
      language="c++",
      include_dirs=include_dirs + [numpy.get_include()],
      library_dirs=library_dirs,
      runtime_library_dirs=library_dirs,
      libraries=pc['libraries'],
      extra_compile_args=extra_compile_args,
      )


# ---------------------------------------------------------------------------#
#  setup starts here                                                         #
# ---------------------------------------------------------------------------#

from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()

def load_requirements(f):
  retval = [str(k.strip()) for k in open(f, 'rt')]
  return [k for k in retval if k and k[0] not in ('#', '-')]

setup(

    name='bob',
    version=version,
    description='Bob is a free signal-processing and machine learning toolbox',
    keywords=['signal processing', 'machine learning', 'biometrics'],
    url='https://www.idiap.ch/software/bob',
    license='GPLv3',
    author='Bob Developers',
    author_email='bob-devel@googlegroups.com',

    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=load_requirements('requirements.txt'),

    ext_modules=[
      setup_extension('bob.core._core', 'bob-core-py'),
      setup_extension('bob.core.random._core_random', 'bob-core-random-py'),
      setup_extension('bob.io._io', 'bob-io-py'),
      setup_extension('bob.math._math', 'bob-math-py'),
      setup_extension('bob.measure._measure', 'bob-measure-py'),
      setup_extension('bob.sp._sp', 'bob-sp-py'),
      setup_extension('bob.ip._ip', 'bob-ip-py'),
      setup_extension('bob.ap._ap', 'bob-ap-py'),
      setup_extension('bob.machine._machine', 'bob-machine-py'),
      setup_extension('bob.trainer._trainer', 'bob-trainer-py'),
      ],

    entry_points={
      'console_scripts': [
        'bob_config.py = bob.script.config:main',
        'bob_dbmanage.py = bob.db.script.dbmanage:main',
        'bob_compute_perf.py = bob.measure.script.compute_perf:main',
        'bob_eval_threshold.py = bob.measure.script.eval_threshold:main',
        'bob_apply_threshold.py = bob.measure.script.apply_threshold:main',
        'bob_plot_cmc.py = bob.measure.script.plot_cmc:main',
        'bob_video_test.py = bob.io.script.video_test:main',
        ],
      'bob.db': [
        'iris = bob.db.iris.driver:Interface',
        ],
      },

    classifiers=[
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Software Development :: Libraries :: Python Modules',
      ],

    )
