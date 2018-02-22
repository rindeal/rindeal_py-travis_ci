#!/bin/bash

set -vue

docker=(
    docker run
    -v "${PWD}:/repo:rw"
    -e "CI=$CI"
    -e "BRANCH_NAME=$TRAVIS_BRANCH"
    "${@}"
    bash -c 'cd /repo && .travis-ci/main.sh'
)
"${docker[@]}"



