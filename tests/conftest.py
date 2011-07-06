from __future__ import print_function

import urllib2
import functools

import pytest

def throws_exception(call, exceptions=[Exception]):
	"""
	Invoke the function and return True if it raises any of the
	exceptions provided. Otherwise, return False.
	"""
	try:
		call()
	except tuple(exceptions):
		return True
	except Exception, e:
		pass
		#print("Unexpected exception", e)
	return False

def pytest_namespace():
	has_internet = pytest.mark.skipif('not pytest.config.has_internet')
	return vars()

def pytest_configure(config):
	open_google = functools.partial(urllib2.urlopen, 'http://www.google.com')
	config.has_internet = not throws_exception(open_google, [Exception, urllib2.URLError])