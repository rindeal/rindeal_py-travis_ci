#!/usr/bin/env python3

import os
import sys

__DIR__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__DIR__, "..")))

from rindeal.travis_ci.utils import *


with Fold("fold.tag") as fold:
	with Time():
		fold.desc("Fold Time Description")
		print("content\n" * 3)

with TimedFold("fold.tag.1", "Fold 1 Description"):
	print("content 1\n" * 3)
	with TimedFold("fold.tag.2", "Fold 2 Description"):
		print("content 2\n" * 3)
		with TimedFold("fold.tag.3", "Fold 3 Description"):
			print("content 3\n" * 3)
