#!/bin/bash

set -vue

_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# BEGIN: setup
apt-get -y update
time apt-get -y install python3.6 python3-coverage npm tree

update-alternatives --install /usr/bin/python python /usr/bin/python3.6 0
# END: setup

# BEGIN: test
python3-coverage run --branch --include "rindeal/travis_ci*" setup.py test
python3-coverage report
# END: test

# BEGIN: test install
install_dir="$(mktemp -d)"
./setup.py install --root="${install_dir}" --prefix=""
tree -a "${install_dir}"
# END: test install

# BEGIN: deploy
if [[ "${TRAVIS_BRANCH}" != "master" ]] ; then
    exit 0
fi

coverage_html_dir="$(mktemp -d)"
python3-coverage html -d "${coverage_html_dir}"
#netlify deploy -s rindeal-py-distutils -p "${coverage_html_dir}"
# END: deploy
