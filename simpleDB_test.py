from unittest import TestCase

class SimpleDBTestCase(TestCase):
	"""
	@class SimpleDBTestCase
	Test each data and transaction command and their combinations work correctly in SimpleDB.

	"""
	
	def __init__(self, arg):
		super(SimpleDBTestCase, self).__init__()
		self.arg = arg
