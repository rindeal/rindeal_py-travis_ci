#!/usr/bin/env python3.6
##
# Copyright (C) 2018  Jan Chren (rindeal)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from distutils.core import setup
import sys
import os


# make sure local modules are imported
__DIR__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, __DIR__)
from rindeal.travis_ci.utils._pkg_metadata import metadata


setup(
	# >> required fields
	name=metadata.name,
	version=metadata.version,
	url=metadata.url,

	# >> creator section
	author=metadata.author,
	author_email=metadata.author_email,
	license=metadata.licence_name,

	# >> stuff to actually do
	packages=("rindeal.travis_ci.utils",),
	scripts=("bin/travis-ci-utils",),
)
