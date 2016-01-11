# -*- coding: utf-8 -*-

from sys import stdin


class Command(object):
	"""
	@class Command
	Define the Data and Transaction commands used in our simple database.

	SET name value – Set the variable name to the value value. Neither variable names nor values will contain spaces.
	GET name – Print out the value of the variable name, or NULL if that variable is not set.
	UNSET name – Unset the variable name, making it just like that variable was never set.
	NUMEQUALTO value – Print out the number of variables that are currently set to value. If no variables equal that value, print 0.
	END – Exit the program. Your program will always receive this as its last command.
	BEGIN – Open a new transaction block. Transaction blocks can be nested; a BEGIN can be issued inside of an existing block.
	ROLLBACK – Undo all of the commands issued in the most recent transaction block, and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
	COMMIT – Close all open transaction blocks, permanently applying the changes made in them. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
	"""

	SET = 'SET'
	GET = 'GET'
	UNSET = 'UNSET'
	NUMEQUALTO = 'NUMEQUALTO'
	END = 'END'
	BEGIN = 'BEGIN'
	ROLLBACK = 'ROLLBACK'
	COMMIT = 'COMMIT'


class SimpleDB(object):
	"""
	@class SimpleDB
	A simple in-memory database, receives commands via standard input and writes response to standard output.
	"""

	def __init__(self):
		self.table = {}
		self.cmd = None

	def run(self):
		local_table = {}
		while True:
			self.cmd = self.get_command()
			
			if self.cmd[0] == Command.END:
				break;
			elif self.cmd[0] == Command.SET:
				self.set(local_table, self.cmd[1], self.cmd[2])
			elif self.cmd[0] == Command.UNSET:
				self.unset(local_table, self.cmd[1])
			elif self.cmd[0] == Command.GET:
				self.get(local_table, self.cmd[1])
			else:
				print 1


	def get_command(self):
		return raw_input().split()

	def set(self, table, name, val):
		table[name] = val
	
	def get(self, table, name):
		if name in table:
			print table[name]
		else:
			print 'NULL'

	def unset(self, table, name):
		table.pop(name, None)

	def numequalto(self):
		pass

	def end(self):
		pass

	def begin(self):
		pass

	def rollback(self):
		pass

	def commit(self):
		pass

def main():
	db = SimpleDB()
	db.run()

if __name__ == '__main__':
	main()
