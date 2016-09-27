#!/usr/bin/env bash
# Wed 21 Sep 2016 13:08:05 CEST

source $(dirname ${0})/functions.sh

run_cmd cd ${PREFIX}

# The tests:
run_cmd ${PREFIX}/bin/python ${BOB_PREFIX_PATH}/bin/coverage run --source=${CI_PROJECT_NAME} ${BOB_PREFIX_PATH}/bin/nosetests -sv ${CI_PROJECT_NAME}
run_cmd ${PREFIX}/bin/python ${BOB_PREFIX_PATH}/bin/coverage report

run_cmd cd ${CI_PROJECT_DIR}
