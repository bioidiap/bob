#!/usr/bin/env bash
# Wed 21 Sep 2016 13:08:05 CEST

source $(dirname ${0})/functions.sh

run_cmd ./bin/buildout

if [ -x ./bin/bob_dbmanage.py ]; then
  run_cmd ./bin/bob_dbmanage.py all download --force;
fi

if [ -d ./doc ]; then
  run_cmd ./bin/sphinx-build doc sphinx
fi

if [ -z "${WHEEL_TAG}" ]; then
  # C/C++ extensions
  run_cmd ./bin/python setup.py bdist_wheel
else
  # Python-only packages
  run_cmd ./bin/python setup.py bdist_wheel --python-tag ${WHEEL_TAG}
fi
