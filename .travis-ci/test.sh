#!/usr/bin/env bash

set -ue

__DIR__="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


CMD=./bin/travis-ci-utils


echo "======= Test Fold =========="

$CMD fold -start --desc "Fold Description" fold.tag
echo "inside fold"
$CMD fold -end fold.tag

echo "============ Test Timer ================="

$CMD time -start timer.id
echo "inside timer 1"
echo "inside timer 2"
echo "inside timer 3"
$CMD time -end timer.id

echo "=========== Test Fold With Timer ================"

$CMD fold -start --desc "Fold With Timer Description" fold.timer.tag
echo "inside fold before timer"
$CMD time -start fold.timer.id
echo "inside fold with timer 1"
echo "inside fold with timer 2"
echo "inside fold with timer 3"
$CMD time -end fold.timer.id
echo "inside fold after timer"
$CMD fold -end fold.timer.tag


echo "=========== Test Fold With Timer 2 ================"

$CMD fold -start fold.timer.tag2
$CMD time -start fold.timer.id2
$CMD fold -desc "Fold Timer Description"
echo '$ command'
$CMD time -end fold.timer.id2
$CMD fold -end fold.timer.tag2

echo "=========== Test Python Lib ================"

"${__DIR__}/test.py"
