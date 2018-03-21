#!/usr.bin/env python

import os
import sys

__DIR__ = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath(os.path.join(__DIR__, "..")))

from rindeal.travis_ci.utils import *


with Fold("fold tag") as fold:
	with Time():
		fold.desc("Fold Time Description")
	print("content")
	print("content")
	print("content")
