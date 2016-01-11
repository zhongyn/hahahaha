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
	NULL = 'NULL'
	NOTRANSACTION = 'NO TRANSACTION'

class SimpleDB(object):
	"""
	@class SimpleDB
	A simple in-memory database, receives commands via standard input and writes response to standard output.
	"""

	def __init__(self):
		self.table = {}
		self.cmd = None


	def run(self, trans_id=0):
		while True:
			self.cmd = self.get_command()
			
			if self.cmd[0] == Command.END:
				return Command.END
			elif self.cmd[0] == Command.SET:
				self.set(self.cmd[1], self.cmd[2], trans_id)
			elif self.cmd[0] == Command.UNSET:
				self.unset(self.cmd[1], trans_id)
			elif self.cmd[0] == Command.GET:
				self.get(self.cmd[1])
			elif self.cmd[0] == Command.BEGIN:
				status = self.run(trans_id + 1)
				if status == Command.END:
					return Command.END
				elif status == Command.ROLLBACK:
					continue
				elif status == Command.COMMIT and trans_id != 0:
					return Command.COMMIT
			elif self.cmd[0] == Command.ROLLBACK:
				if trans_id != 0:
					self.rollback(trans_id)
					return Command.ROLLBACK
				else:
					print Command.NOTRANSACTION
			elif self.cmd[0] == Command.COMMIT:
				if trans_id != 0:
					self.commit()
					return Command.COMMIT
				else:
					print Command.NOTRANSACTION
					
			else:
				print 1


	def get_command(self):
		return raw_input().split()

	def set(self, name, val, trans_id):
		if name in self.table:
			if self.table[name][-1][0] == trans_id:
				self.table[name][-1][1] = val
			else:
				self.table[name].append([trans_id, val])
		else:
			self.table[name] = [[trans_id, val]]

	
	def get(self, name):
		if name in self.table:
			print self.table[name][-1][1]
		else:
			print 'NULL'

	def unset(self, name, trans_id):
		self.set(name, Command.NULL, trans_id)
			
	def numequalto(self):
		pass

	def rollback(self, trans_id):
		for name in self.table.keys():
			if self.table[name][-1][0] == trans_id:
				if len(self.table[name]) == 1:
					del self.table[name]
				else:
					self.table[name].pop()

	def commit(self):
		for name, val in self.table.iteritems():
			self.table[name] = self.table[name][-1]

def main():
	db = SimpleDB()
	db.run()

if __name__ == '__main__':
	main()
