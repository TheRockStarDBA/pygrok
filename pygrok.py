__author__ = 'drathier'

import re
import patterns

# TODO: make % escapes possible
# TODO: let Pygrok() take any number of parameters, joining them using (?:.|\n)* to avoid re-parsing the whole string


class Pygrok():
	def __init__(self, *pattern):
		self.pattern = self._pattern_parser(r"(?:.|\n)*".join(pattern))
		print pattern
		print r"(?:.|\n)*".join(pattern)
		print self.pattern

	def _pattern_parser(self, pattern):
		matches = re.sub(r'%{(?:(\w+)\.)?(\w+)(?::(\w+))?}', lambda m: self._parser(m), pattern)
		return matches

	def _parser(self, matches):
		pattern_group, pattern_key, result_key = matches.groups()

		if pattern_group == "cisco":
			pattern_dict = patterns.cisco
		elif pattern_group == "whitespace":
			pattern_dict = patterns.whitespace
		else:
			pattern_dict = patterns.base

		pattern = self._pattern_parser(pattern_dict[pattern_key])

		if result_key:
			return "(?P<" + result_key + ">" + pattern + ")"
		else:
			return "(?:" + pattern + ")"

	def _strip_none_values(self, inputdict):
		retdict = {}
		for elem in inputdict:
			if inputdict[elem] is not None:
				retdict[elem] = inputdict[elem]
		return retdict

	def search(self, input):
		#print "pattern", self.pattern
		ret = re.search(self.pattern, input)
		if ret:
			return self._strip_none_values(ret.groupdict())
		else:
			return {}

	def multisearch(self, inputList):
		ret = []
		for row in inputList:
			ret.append(self.search(row))
		return ret