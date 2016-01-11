# -*- coding: utf-8 -*-

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
    
    Data structure for storing (name, val) and (val, count):
    table = {name_1: [[trans_id_1, val_1], [trans_id_2, val_2], ...];
             name_2: [[trans_id_1, val_1], [trans_id_2, val_2], ...];
             ...
             ...
             ...
            }
            
    counts = {val_1: [[trans_id_1, count_1], [trans_id_2, count_2], ...];
              val_2: [[trans_id_1, count_1], [trans_id_2, count_2], ...];
              ...
              ...
              ...
             }
    
    For example:
    table = {a: [[0, 2], [3, 5], [4, 10]];
             b: [[2, 5], [2, 88]]
            }

    The corresponding counts:
    counts = {2: [[0, 1]];
              5: [[2, 1], [3, 2]];
              10: [[4, 1]];
              88: [[2, 1]]
             }

    """

    def __init__(self):
        self.table = {}
        self.counts = {}
        self.cmd = None
        self.trans_id = 0

    def run(self):
        while True:
            self.cmd = self.get_command()
            
            if self.cmd[0] == Command.END:
                break
            elif self.cmd[0] == Command.SET:
                self.set(self.cmd[1], self.cmd[2])
            elif self.cmd[0] == Command.UNSET:
                self.unset(self.cmd[1])
            elif self.cmd[0] == Command.GET:
                self.get(self.cmd[1])
            elif self.cmd[0] == Command.NUMEQUALTO:
                self.numequalto(self.cmd[1])
            elif self.cmd[0] == Command.BEGIN:
                self.trans_id += 1
            elif self.cmd[0] == Command.ROLLBACK:
                self.rollback()
            elif self.cmd[0] == Command.COMMIT:
                self.commit()
            else:
                print 1


    def get_command(self):
        return raw_input().split()

    def set(self, name, val):
        if name in self.table:
            self.update_counts(self.table[name][-1][1], -1)
            if self.table[name][-1][0] == self.trans_id:
                self.table[name][-1][1] = val
            else:               
                self.table[name].append([self.trans_id, val])
        else:
            self.table[name] = [[self.trans_id, val]]
        
        self.update_counts(val, 1)

    
    def get(self, name):
        if name in self.table:
            print self.table[name][-1][1]
        else:
            print Command.NULL

    def unset(self, name):
        self.set(name, Command.NULL)

            
    def numequalto(self, val):
        if val in self.counts:
            print self.counts[val][-1][1]
        else:
            print 0

    def update_counts(self, val, change):
        if val in self.counts:
            if self.trans_id == self.counts[val][-1][0]:
                self.counts[val][-1][1] += change
            else:
                self.counts[val].append([self.trans_id, self.counts[val][-1][1]+change])
        else:
            self.counts[val] = [[self.trans_id, change]]

    def rollback(self):
        if self.trans_id != 0:
            self.del_last_trans(self.table)
            self.del_last_trans(self.counts)
            self.trans_id -= 1
        else:
            print Command.NOTRANSACTION

    def del_last_trans(self, data):
        for name in data.keys():
             if data[name][-1][0] == self.trans_id:
                 if len(data[name]) == 1:
                     del data[name]
                 else:
                     data[name].pop()
        
    def commit(self):
        if self.trans_id != 0:
            self.save_latest_data(self.table)
            self.save_latest_data(self.counts)
            self.trans_id = 0
        else:
            print Command.NOTRANSACTION

    def save_latest_data(self, data):
        for name, val in data.iteritems():
            data[name] = val[-1:]
        

def main():
    db = SimpleDB()
    db.run()

if __name__ == '__main__':
    main()
