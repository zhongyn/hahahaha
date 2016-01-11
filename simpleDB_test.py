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

	@patch('simpleDB.SimpleDB.get_command')
	@patch('sys.stdout', new_callable=StringIO)
	def test_set_var_get_var(self, mock_output, mock_command):
		mock_command.side_effect = [self.set_a_10, self.get_a, self.end]
		self.db.run()
		self.assertEqual('10\n', mock_output.getvalue())

	@patch('simpleDB.SimpleDB.get_command')
	@patch('sys.stdout', new_callable=StringIO)
	def test_get_var_no_exist(self, mock_output, mock_command):
		mock_command.side_effect = [self.get_a, self.end]
		self.db.run()
		self.assertEqual('NULL\n', mock_output.getvalue())

	@patch('simpleDB.SimpleDB.get_command')
	@patch('sys.stdout', new_callable=StringIO)
	def test_set_var_unset_var_get_var(self, mock_output, mock_command):
		mock_command.side_effect = [self.set_a_10, self.unset_a, self.get_a, self.end]
		self.db.run()
		self.assertEqual('NULL\n', mock_output.getvalue())


if __name__ == '__main__':
	unittest.main()
