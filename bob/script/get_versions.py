# Andre Anjos <andre.anjos@idiap.ch>
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Amir Mohammadi <amir.mohammadi@idipa.ch>
# Mon 20 Jul 17:30:00 CEST 2015

# Lists the final version of a given package in PyPI

import pkg_resources  # for bob import to work properly
import sys
import os


def main():

  from bob.utils import get_releases, get_max_version

  if len(sys.argv) != 2:
    print("usage: %s <requirements.txt>" % os.path.basename(sys.argv[0]))
    sys.exit(1)

  dependencies = [l.rstrip("\n") for l in open(sys.argv[1], 'r').readlines()]
  for d in dependencies:
    d = d.split("==")[0].strip()
    versions = get_releases(d)
    print("{0} == {1}".format(
        d, '{}.{}.{}'.format(*get_max_version(versions).version)))


if __name__ == '__main__':
  main()
