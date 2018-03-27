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

import os
import sys
import time
import typing
import uuid
import re


class AnsiEscSeq:
	"""
	@link http://www.termsys.demon.co.uk/vtansi.htm
	@link http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-048.pdf
	@link https://github.com/travis-ci/travis-web/blob/cf9ead330bd9eddb2a834646198dee27e420ce95/app/styles/app/layouts/ansi.scss
	@link https://github.com/travis-ci/travis-web/blob/cf9ead330bd9eddb2a834646198dee27e420ce95/app/styles/app/vars.scss
	@link https://github.com/travis-ci/travis-web/blob/4d89a80318fa1a4f1ba2c31a39b818563eff5e9f/app/utils/log.js
	@link https://github.com/mmalecki/ansiparse/blob/master/lib/ansiparse.js
	"""

	# taken from `Log.Deansi` module in `app/utils/log.js`
	__CLEAR_ANSI = r"""
	(?:
		\033  # ESC
	)
	(?:
		## 1. variant
		## - `Query Device Code`
		## - `Report Device Code`
		\[  # CSI
		0?c
		|  # or

		## 2. variant
		## - `Report Device OK`
		## - `Report Device Failure`
		## - `Query Device Status`
		## - `Query Cursor Position`
		\[  # CSI
		[0356]n
		|  # or

		## 3. variant
		## - `Disable Line Wrap`
		## - `Enable Line Wrap`
		\[  # CSI
		7[lh]
		|  # or

		## 4. variant
		## - `Text Cursor Enable Mode Hide`
		## - `Text Cursor Enable Mode Show`
		\[  # CSI
		\?25[lh]
		|  # or

		## 5. variant
		## - `Designate Character Set – US ASCII`
		\(B
		|  # or

		## 6. variant
		## - `Horizontal Tab Set`
		H
		|  # or

		## 7. variant
		## - `Cursor Horizontal Absolute`
		\[  # CSI
		(?:
			\d+
			(
				;\d+
			)
			{, 2}
		)?
		G
		|  # or

		## 8. variant
		## - `Erase in Display`
		## - `Erase in Line`
		\[  # CSI
		(?:
			[12]
		)?
		[JK]
		|  # or

		## 9. variant
		## - `Cursor Backward (Left) by 1`
		## - `Reverse Index`
		[DM]
		|  # or

		## 10. variant
		## - clear
		\[  # CSI
		0K
	)
	"""

	ESC: str = "\x1B"
	"""
	Escape character
	"""
	CSI: str = ESC + "["
	"""
	Control Sequence Introducer
	"""

	CONTROL_FUNCTIONS = {

	}

	FG_BLACK = "30"
	FG_RED = "31"
	FG_GREEN = "32"
	FG_YELLOW = "33"
	FG_BLUE = "34"
	FG_MAGENTA = "35"
	FG_CYAN = "36"
	FG_WHITE = "37"
	FG_BRIGHT_BLACK = "90"

	FG_DEFAULT = "39"

	FG_COLOURS = {
		"black":    {"open": FG_BLACK,      "rgb": "", "close": FG_DEFAULT},
		"red":      {"open": FG_RED,        "close": FG_DEFAULT},
		"green":    {"open": FG_GREEN,      "close": FG_DEFAULT},
		"yellow":   {"open": FG_YELLOW,     "close": FG_DEFAULT},
		"blue":     {"open": FG_BLUE,       "close": FG_DEFAULT},
		"magenta":  {"open": FG_MAGENTA,    "close": FG_DEFAULT},
		"cyan":     {"open": FG_CYAN,       "close": FG_DEFAULT},
		"white":    {"open": FG_WHITE,      "close": FG_DEFAULT},
		"grey":     {"open": FG_BRIGHT_BLACK, "close": FG_DEFAULT},
	}
	"""
	@link https://github.com/mmalecki/ansiparse/blob/master/lib/ansiparse.js#L154
	"""

	BG_BLACK = "40"
	BG_RED = "41"
	BG_GREEN = "42"
	BG_YELLOW = "43"
	BG_BLUE = "44"
	BG_MAGENTA = "45"
	BG_CYAN = "46"
	BG_WHITE = "47"

	BG_DEFAULT = "49"

	BG_COLOURS = {
		"black":    {"open": BG_BLACK,      "close": BG_DEFAULT},
		"red":      {"open": BG_RED,        "close": BG_DEFAULT},
		"green":    {"open": BG_GREEN,      "close": BG_DEFAULT},
		"yellow":   {"open": BG_YELLOW,     "close": BG_DEFAULT},
		"blue":     {"open": BG_BLUE,       "close": BG_DEFAULT},
		"magenta":  {"open": BG_MAGENTA,    "close": BG_DEFAULT},
		"cyan":     {"open": BG_CYAN,       "close": BG_DEFAULT},
		"white":    {"open": BG_WHITE,      "close": BG_DEFAULT},
	}
	"""
	@link https://github.com/mmalecki/ansiparse/blob/master/lib/ansiparse.js#L166
	"""

	BOLD_OR_INTENSE = "1"
	ITALIC = "3"
	SINGLY_UNDERLINED = "4"

	NORMAL_COLOUR_OR_INTENSITY = "22"
	NOT_ITALIC = "23"
	NOT_UNDERLINED = "24"

	STYLES = {
		"bold":         {"open": BOLD_OR_INTENSE,   "close": NORMAL_COLOUR_OR_INTENSITY},
		"italic":       {"open": ITALIC,            "close": NOT_ITALIC},
		"underline":    {"open": SINGLY_UNDERLINED, "close": NOT_UNDERLINED},
	}
	"""
	@link https://github.com/mmalecki/ansiparse/blob/master/lib/ansiparse.js#L177
	"""

	@classmethod
	def sgr(cls, *args: typing.Optional[typing.Sequence[typing.Union[str, int]]]):
		"""
		SGR (Select Graphic Rendition)

		:param args: sequence of strings or integers representing SGR parameters
		:return:
		"""
		params = ";".join(str(x) for x in args)
		return f'{cls.CSI}{params}m'

	@classmethod
	def colour(cls, text: str, fg: str= "", bg: str= "", style: str= "") -> str:
		"""
		Colourize string

		:param text:
		:param fg: foreground colour;
				possible values: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` and `grey`
		:param bg: background colour;
				possible values: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` and `white`
		:param style: plus(`+`)-delimited string; possible values: `bold`, `italic` and `underline`
		:return: colourized string
		"""
		codes = []
		str_out = ""

		if fg:
			codes.append(cls.FG_COLOURS[fg])
		if bg:
			codes.append(cls.BG_COLOURS[bg])
		if style:
			styles = style.split('+')
			for s in styles:
				if s not in cls.STYLES:
					raise Exception('invalid style')
				codes.append(cls.STYLES[s])

		for c in codes:
			str_out += cls.sgr(c['open'])

		str_out += text

		while codes:
			str_out += cls.sgr(codes.pop()['close'])

		return str_out

	@classmethod
	def el(cls, param: typing.Union[int, str] ="", selective: bool =False) -> str:
		"""
		EL (Erase in Line)

		One of the "control functions".

		::

			| Oct Hex  *  	(* marks function used in DEC VT series or LA series terminals)
			| --- -- - - --------------------------------------------------------------------
			| 113 4B K * EL  - Erase in Line (cursor does not move)
			|          *      [K = [0K = Erase from current position to end (inclusive)
			|          *      [1K = Erase from beginning to current position
			|          *      [2K = Erase entire current line
			|          *      [?0K = Selective erase to end of line ([?1K, [?2K similar)

		:return:
		"""
		param = str(param)
		if param not in {"", "0", "1", "2"}:
			raise Exception("invalid param")

		return f"{cls.CSI}{'?' if selective else ''}{param}K"

	@staticmethod
	def enabled() -> bool:
		"""
		Are both standard output and standard error TTYs?

		Taken from https://github.com/naftulikay/travis-pls

		:return:
		"""
		return os.isatty(sys.stdout.fileno()) and os.isatty(sys.stderr.fileno())


def colour(*args, **kwargs):
	return AnsiEscSeq.colour(*args, **kwargs)


class _FoldTimeBase:
	_stream: typing.Optional[typing.TextIO]
	_MaybeStreamType = typing.Union[int, str]

	def __init__(self, stream: typing.TextIO =sys.stdout):
		self._stream = stream

	def start(self) -> _MaybeStreamType:
		raise NotImplementedError

	def end(self) -> _MaybeStreamType:
		raise NotImplementedError

	def _maybe_stream_write(self, str_out: str) -> _MaybeStreamType:
		return self._stream.write(str_out) if self._stream else str_out

	def __enter__(self):
		if not self._stream:
			raise Exception("invalid use, stream must be provided when using as a context manager")
		self.start()
		return self

	def __exit__(self, *_) -> None:
		self.end()


class Fold(_FoldTimeBase):
	"""
	::

		| travis_fold() {
		|     local action=$1
		|     local name=$2
		|     echo -en "travis_fold:${action}:${name}\\r${ANSI_CLEAR}"
		| }

	"""

	_tag: str
	_desc: str
	_started: bool

	# https://github.com/travis-ci/travis-web/blob/4d89a80/app/utils/log.js#L30
	_re_tag = re.compile(r"^([\w_\-\.]+)$")

	def __init__(self, tag: str, desc: str ="", stream: typing.TextIO =sys.stdout, started: bool =False):
		super().__init__(stream)

		self._tag = tag
		if self._re_tag.search(self._tag) is None:
			raise ValueError("Invalid tag name")
		self._desc = desc
		self._started = started

	def _action(self, action: str) -> str:
		tmpl = 'travis_fold:{action}:{tag}\r{clear}'
		return tmpl.format(action=action, tag=self._tag, clear=AnsiEscSeq.el())

	def desc(self, text: str) -> _FoldTimeBase._MaybeStreamType:
		"""
		Yellow is the colour Travis CI uses for this purpose.
		Examples are: `Build system information`, `Worker information`, ...
		"""
		str_out = AnsiEscSeq.colour(text, fg='yellow') + "\n"
		return self._maybe_stream_write(str_out)

	def start(self) -> _FoldTimeBase._MaybeStreamType:
		"""
		@link https://github.com/travis-ci/worker/blob/a8bdf4846ac390bba372d3f56ff0552a025da4af/package.go

		:return: Number of bytes written
		"""
		if self._started:
			raise Exception("travis fold already started")
		self._started = True

		str_action = self._action('start')
		out = self._maybe_stream_write(str_action)

		if self._desc:
			out += self.desc(self._desc)

		return out

	def end(self) -> _FoldTimeBase._MaybeStreamType:
		if not self._started:
			raise Exception("travis fold not started yet")

		str_out = self._action('end')

		return self._maybe_stream_write(str_out)


class Time(_FoldTimeBase):

	_id: str
	_start_time: int

	# https://github.com/travis-ci/travis-web/blob/4d89a80/app/utils/log.js#L31
	_re_id = re.compile(r"^([\w_\-\.]+)$")

	def __init__(self, stream: typing.TextIO =sys.stdout, timer_id: str =None, start_time: int =0):
		super().__init__(stream)

		self._id = timer_id if timer_id else str(uuid.uuid4())
		if self._re_id.search(self._id) is None:
			raise ValueError("invalid timer id")
		self._start_time = start_time

	def get_id(self) -> str:
		return self._id

	def get_start_time(self) -> int:
		return self._start_time

	@staticmethod
	def _nanoseconds():
		return int(time.time()*1e9)

	def start(self) -> _FoldTimeBase._MaybeStreamType:
		"""
		Start timer

		::

			| travis_time_start() {
			|     travis_timer_id=$(printf %08x $(( RANDOM * RANDOM )))
			|     travis_start_time=$(travis_nanoseconds)
			|     echo -en "travis_time:start:$travis_timer_id\\r${ANSI_CLEAR}"
			| }

		:return: Number of bytes written
		"""
		if self._start_time:
			raise Exception("already started")

		tmpl = 'travis_time:start:{id}\r{clear}'
		str_out = tmpl.format(id=self._id, clear=AnsiEscSeq.el())

		self._start_time = self._nanoseconds()

		return self._maybe_stream_write(str_out)

	def end(self) -> _FoldTimeBase._MaybeStreamType:
		"""
		End timer and write result

		::

			| travis_time_finish() {
			|     local result=$?
			|     travis_end_time=$(travis_nanoseconds)
			|     local duration=$(($travis_end_time-$travis_start_time))
			|     echo -en "\\ntravis_time:end:$travis_timer_id:start=$travis_start_time,finish=$travis_end_time,duration=$duration\\r${ANSI_CLEAR}"
			|     return $result
			| }

		:return: Number of bytes written
		"""
		if not self._start_time:
			raise Exception("not yet started")

		end_time = self._nanoseconds()
		duration = end_time - self._start_time

		tmpl = 'travis_time:end:{id}:start={start_time},finish={end_time},duration={duration}\r{clear}'
		str_out = tmpl.format(
			id=self._id,
			start_time=self._start_time,
			end_time=end_time,
			duration=duration,
			clear=AnsiEscSeq.el()
		)

		return self._maybe_stream_write(str_out)


class TimedFold(_FoldTimeBase):
	_fold: Fold
	_time: Time
	_fold_desc: str

	def __init__(
			self,
			tag,
			desc: str = "",
			stream: typing.TextIO =sys.stdout,
			fold_kwargs: dict ={},
			time_kwargs: dict ={}
	):
		super().__init__(stream)

		self._fold = Fold(tag, stream=stream, **fold_kwargs)
		self._time = Time(stream=stream, **time_kwargs)
		self._fold_desc = desc

	def start(self):
		self._fold.start()
		self._time.start()
		if self._fold_desc:
			self._fold.desc(self._fold_desc)

	def end(self):
		self._time.end()
		self._fold.end()
