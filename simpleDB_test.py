import unittest
from mock import patch
from StringIO import StringIO
from simpleDB import SimpleDB, Command

class SimpleDBTestCase(unittest.TestCase):
	"""
	@class SimpleDBTestCase
	Test each data and transaction command and their combinations work correctly in SimpleDB. 
	"""

	def setUp(self):
		self.db = SimpleDB()
		self.set_a_10 = ['SET', 'a', '10']
		self.unset_a = ['UNSET', 'a']
		self.get_a = ['GET', 'a']
		self.numequalto_10 = ['NUMEQUALTO', '10']
		self.end = ['END']

		self.patcher_get_cmd = patch('simpleDB.SimpleDB.get_command')
		self.patcher_output = patch('sys.stdout', new_callable=StringIO)
		self.mock_command = self.patcher_get_cmd.start()
		self.mock_output = self.patcher_output.start()
	
	def tearDown(self):
		self.patcher_get_cmd.stop()
		self.patcher_output.stop()
	
	def test_set_var_get_var(self):
		self.mock_command.side_effect = [self.set_a_10, self.get_a, self.end]
		self.db.run()
		self.assertEqual('10\n', self.mock_output.getvalue())

	def test_get_var_no_exist(self):
		self.mock_command.side_effect = [self.get_a, self.end]
		self.db.run()
		self.assertEqual('NULL\n', self.mock_output.getvalue())

	def test_set_var_unset_var_get_var(self):
		self.mock_command.side_effect = [self.set_a_10, self.unset_a, self.get_a, self.end]
		self.db.run()
		self.assertEqual('NULL\n', self.mock_output.getvalue())


if __name__ == '__main__':
	unittest.main()
