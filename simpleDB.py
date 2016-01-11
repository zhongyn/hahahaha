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
    zero_arg_cmds = [BEGIN, ROLLBACK, COMMIT, END]
    one_arg_cmds = [UNSET, GET, NUMEQUALTO]
    two_arg_cmds = [SET]


class SimpleDB(object):
    """
    @class SimpleDB
    A simple in-memory database, receives commands via standard input and writes response to standard output.
    Data structure for storing (name, val) and (val, count) pairs:

    table = {name_1: [[trans_id_1, val_1], [trans_id_2, val_2], ...];
             name_2: [[trans_id_1, val_1], [trans_id_2, val_2], ...];
             ...
             ...
            }
    counts = {val_1: [[trans_id_1, count_1], [trans_id_2, count_2], ...];
              val_2: [[trans_id_1, count_1], [trans_id_2, count_2], ...];
              ...
              ...
             }

    The design of such structures origins from the requirement of multi-level transactions. 
    A common solution is recursively calling new transaction. But we can use a list of (trans_id, val) pairs to 
    simulates a stack operation, which saves the recursion stack memory. 
    Begining a new transaction simply increases the current trans_id by 1.
    Using python dict here gives us runtime of O(1) for the commands GET,SET,UNSET,NUMEQUALTO.

    Example:
    table = {a: [[0, 2], [3, 5], [4, 10]];
             b: [[2, 5], [3, 88]]
            }
    The corresponding counts:
    counts = {2: [[0, 1]];
              5: [[2, 1], [3, 2]];
              10: [[4, 1]];
              88: [[3, 1]]
             }
    """


    def __init__(self):
        self.table = {}
        self.counts = {}
        self.trans_id = 0

    def run(self):
        """
        @fn run
        Receives standard input and process commands.
        """
        while True:
            cmd = self.get_command()
            # if not self.is_valid_cmd(cmd):
            #     print "Invalid command"
            #     continue
            if cmd[0] == Command.END:
                break
            elif cmd[0] == Command.SET:
                self.set(cmd[1], cmd[2])
            elif cmd[0] == Command.UNSET:
                self.unset(cmd[1])
            elif cmd[0] == Command.GET:
                self.get(cmd[1])
            elif cmd[0] == Command.NUMEQUALTO:
                self.numequalto(cmd[1])
            elif cmd[0] == Command.BEGIN:
                self.trans_id += 1
            elif cmd[0] == Command.ROLLBACK:
                self.rollback()
            elif cmd[0] == Command.COMMIT:
                self.commit()

    def get_command(self):
        """
        @fn get_command
        Receives a string from std, split it and returns a list.
        """
        return raw_input().split()

    def set(self, name, val):
        """
        @fn set
        Adds or updates name-val pair in database table. Also updates the value counts.
        """
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
        """
        @fn get
        Print out the value of the variable name, or NULL if the variable is not set.
        """
        if name in self.table:
            print self.table[name][-1][1]
        else:
            print Command.NULL

    def unset(self, name):
        """
        @fn unset
        Unset a variable is treated as setting the variable with the value of NULL.
        If UNSET is called before GET in the same transaction for the same variable, and that 
        variable is set in the previous transaction, using a var-NULL pair will inform the cmd
        GET that the var has been unset.
        """
        self.set(name, Command.NULL)

            
    def numequalto(self, val):
        """
        @fn numequalto
        Print out the count of val in the latest transaction, or 0 if val does not exist.
        """
        if val in self.counts:
            print self.counts[val][-1][1]
        else:
            print 0

    def update_counts(self, val, change):
        """
        @fn update_counts
        Adds or updates val-count in counting table. The change can be positive or negative.
        """
        if val in self.counts:
            if self.trans_id == self.counts[val][-1][0]:
                self.counts[val][-1][1] += change
            else:
                self.counts[val].append([self.trans_id, self.counts[val][-1][1]+change])
        else:
            self.counts[val] = [[self.trans_id, change]]

    def rollback(self):
        """
        @fn rollback
        Deletes the data of the last transaction, decreases the trans_id by 1, if the current trans_id != 0.
        """
        if self.trans_id != 0:
            self.del_last_trans(self.table)
            self.del_last_trans(self.counts)
            self.trans_id -= 1
        else:
            print Command.NOTRANSACTION

    def del_last_trans(self, data):
        """
        @fn del_last_trans
        Deletes the last transaction data.
        """
        for name in data.keys():
             if data[name][-1][0] == self.trans_id:
                 if len(data[name]) == 1:
                     del data[name]
                 else:
                     data[name].pop()
        
    def commit(self):
        """
        @fn commit
        Saves the latest data and ends all the transactions.
        """
        if self.trans_id != 0:
            self.save_latest_data(self.table)
            self.save_latest_data(self.counts)
            self.trans_id = 0
        else:
            print Command.NOTRANSACTION

    def save_latest_data(self, data):
        """
        @fn save_latest_data
        Save the latest data, called by @fn commit.
        """
        for name, val in data.iteritems():
            data[name] = val[-1:]

    def is_valid_cmd(self, cmd):
        """
        @fn is_valid_cmd
        Validates the standard input.
        """
        if (cmd[0] in Command.zero_arg_cmds and len(cmd) == 1) or (cmd[0] in Command.one_arg_cmds and len(cmd) == 2) or (cmd[0] in Command.two_arg_cmds and len(cmd) == 3):
            return True
        return False


def main():
    db = SimpleDB()
    db.run()

if __name__ == '__main__':
    main()
