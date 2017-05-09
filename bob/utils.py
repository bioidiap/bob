#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Wed 05 Aug 11:36 2015 CEST
#
# Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland

import distutils.version
import pkg_resources
import pkgtools.pypi
import re


def get_config():
  """
  Returns a string containing the configuration information.
  """
  import bob.extension
  return bob.extension.get_config(__name__)


def get_releases(package):
  """
  Given a package name, get the release versions
  """
  try:
    return pkgtools.pypi.PyPIJson(package).retrieve()['releases'].keys()
  except Exception:
    return []


def get_max_version(versions):

  try:
    v = list(reversed(sorted([distutils.version.StrictVersion(k)
                              for k in versions])))
    final = [k for k in v if not k.prerelease]
    if final:
      return final[0]
    return v[0]
  except Exception:
    v = list(reversed(sorted([distutils.version.LooseVersion(k)
                              for k in versions])))
    final = [k for k in v if not re.search(r'[a-z]', k.vstring)]
    if final:
      return final[0]
    return v[0]


def get_dependencies(pkg_name="bob"):
  """
  Given a package name, get the dependency list
  """
  package = pkg_resources.working_set.by_key[pkg_name]
  return [str(r) for r in package.requires()]
