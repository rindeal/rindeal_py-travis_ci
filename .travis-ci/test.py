#!/usr/bin/env python

import os
import sys

__DIR__ = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath(os.path.join(__DIR__, "..")))

from rindeal.travis_ci.utils import *


with Fold("fold.tag") as fold:
	with Time():
		fold.desc("Fold Time Description")
	print("content")
	print("content")
	print("content")

with Fold("fold.tag.1") as fold_1:
	with Time():
		fold_1.desc("Fold 1 Description")
		print("content 1\n"*3)
		with Fold("fold.tag.2") as fold_2:
			with Time():
				fold_2.desc("Fold 2 Description")
				print("content 2\n" * 3)
				with Fold("fold.tag.3") as fold_3:
					with Time():
						fold_3.desc("Fold 3 Description")
						print("content 3\n" * 3)
