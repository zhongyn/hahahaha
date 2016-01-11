import unittest
from mock import patch
from StringIO import StringIO
from simpleDB import SimpleDB

class SimpleDBTestCase(unittest.TestCase):
    """
    @class SimpleDBTestCase
    Test each data and transaction command and their combinations work correctly in SimpleDB. 
    """

    def setUp(self):
        """
        @fn setUp
        Creates variables used by the test cases.
        """
        self.db = SimpleDB()
        self.set_a_10 = ['SET', 'a', '10']
        self.set_a_20 = ['SET', 'a', '20']
        self.set_a_30 = ['SET', 'a', '30']
        self.set_b_10 = ['SET', 'b', '10']
        self.set_b_30 = ['SET', 'b', '30']
        self.unset_a = ['UNSET', 'a']
        self.get_a = ['GET', 'a']
        self.numequalto_10 = ['NUMEQUALTO', '10']
        self.numequalto_20 = ['NUMEQUALTO', '20']
        self.numequalto_30 = ['NUMEQUALTO', '30']
        self.begin = ['BEGIN']
        self.rollback = ['ROLLBACK']
        self.commit = ['COMMIT']
        self.end = ['END']

        # Mock the func get_command() and std output
        self.patcher_get_cmd = patch('simpleDB.SimpleDB.get_command')
        self.patcher_output = patch('sys.stdout', new_callable=StringIO)
        self.mock_cmd = self.patcher_get_cmd.start()
        self.mock_output = self.patcher_output.start()
    
    def tearDown(self):
        self.patcher_get_cmd.stop()
        self.patcher_output.stop()
    
    def test_set_get(self):
        """
        SET a 10
        GET a       => 10
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.get_a, self.end]
        self.db.run()
        self.assertEqual('10\n', self.mock_output.getvalue())

    def test_get_var_no_exist(self):
        """
        GET a       => NULL
        END
        """
        self.mock_cmd.side_effect = [self.get_a, self.end]
        self.db.run()
        self.assertEqual('NULL\n', self.mock_output.getvalue())

    def test_unset_var_get_NULL(self):
        """
        SET a 10
        UNSET a
        GET a       => NULL
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.unset_a, self.get_a, self.end]
        self.db.run()
        self.assertEqual('NULL\n', self.mock_output.getvalue())

    def test_unset_var_no_exist(self):
        """
        UNSET a
        END
        """
        self.mock_cmd.side_effect = [self.unset_a, self.end]
        self.db.run()
        self.assertEqual('', self.mock_output.getvalue())

    def test_numequalto_after_set(self):
        """
        SET a 10
        SET b 10
        NUMEQUALTO 10   => 2
        NUMEQUALTO 20   => 0
        SET b 30        
        NUMEQUALTO 10   => 1
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.set_b_10, self.numequalto_10, self.numequalto_20, self.set_b_30, self.numequalto_10, self.end]
        self.db.run()
        self.assertEqual('2\n0\n1\n', self.mock_output.getvalue())

    def test_numequalto_after_unset(self):
        """
        SET a 10
        NUMEQUALTO 10   => 1
        UNSET a
        NUMEQUALTO 10   => 0
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.numequalto_10, self.unset_a, self.numequalto_10, self.end]
        self.db.run()
        self.assertEqual('1\n0\n', self.mock_output.getvalue())

    def test_begin_rollback_twice(self):
        """
        BEGIN
        SET a 10
        GET a       => 10
        BEGIN
        SET a 20
        GET a       => 20
        ROLLBACK
        GET a       => 10
        ROLLBACK
        GET a       => NULL
        END
        """
        self.mock_cmd.side_effect = [self.begin, self.set_a_10, self.get_a, self.begin, self.set_a_20, self.get_a, self.rollback, self.get_a, self.rollback, self.get_a, self.end]
        self.db.run()
        self.assertEqual('10\n20\n10\nNULL\n', self.mock_output.getvalue())


    def test_begin_commit_rollback(self):
        """
        BEGIN
        SET a 10
        BEGIN
        SET a 20
        COMMIT
        GET a       => 20
        ROLLBACK    => NO TRANSACTION
        END
        """
        self.mock_cmd.side_effect = [self.begin, self.set_a_10, self.begin, self.set_a_20, self.commit, self.get_a, self.rollback, self.end]
        self.db.run()
        self.assertEqual('20\nNO TRANSACTION\n', self.mock_output.getvalue())

    def test_commit_no_transaction(self):
        """
        SET a 10
        COMMIT      => NO TRANSACTION
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.commit, self.end]
        self.db.run()
        self.assertEqual('NO TRANSACTION\n', self.mock_output.getvalue())

    def test_unset_rollback_commit(self):
        """
        SET a 10
        BEGIN
        GET a       => 10
        SET a 20
        BEGIN
        UNSET a
        GET a       => NULL
        ROLLBACK
        GET a       => 20
        COMMIT
        GET a       => 20
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.begin, self.get_a, self.set_a_20, self.begin, self.unset_a, self.get_a, self.rollback, self.get_a, self.commit, self.get_a, self.end]
        self.db.run()
        self.assertEqual('10\nNULL\n20\n20\n', self.mock_output.getvalue())

    def test_numequalto_after_unset_rollback(self):
        """
        SET a 10
        BEGIN
        NUMEQUALTO 10   => 1
        BEGIN
        UNSET a
        NUMEQUALTO 10   => 0
        ROLLBACK
        NUMEQUALTO 10   => 1
        COMMIT
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.begin, self.numequalto_10, self.begin, self.unset_a, self.numequalto_10, self.rollback, self.numequalto_10, self.commit, self.end]
        self.db.run()
        self.assertEqual('1\n0\n1\n', self.mock_output.getvalue())

    def test_numequalto_after_commit(self):
        """
        SET a 10
        BEGIN
        SET a 20
        BEGIN
        SET a 30
        COMMIT
        NUMEQUALTO 10   => 0
        NUMEQUALTO 20   => 0
        NUMEQUALTO 30   => 1
        END
        """
        self.mock_cmd.side_effect = [self.set_a_10, self.begin, self.set_a_20, self.begin, self.set_a_30, self.commit, self.numequalto_10, self.numequalto_20, self.numequalto_30, self.end]
        self.db.run()
        self.assertEqual('0\n0\n1\n', self.mock_output.getvalue())



if __name__ == '__main__':
    unittest.main()
