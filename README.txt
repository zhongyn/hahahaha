Program written in Python 2.7

----------------
simpleDB
----------------
A simple in-memory database, receives commands via standard input and writes response to standard output.

Data and Transaction commands used in our simple database:

SET name value – Set the variable name to the value value. Neither variable names nor values will contain spaces.
GET name – Print out the value of the variable name, or NULL if that variable is not set.
UNSET name – Unset the variable name, making it just like that variable was never set.
NUMEQUALTO value – Print out the number of variables that are currently set to value. If no variables equal that value, print 0.
END – Exit the program. Your program will always receive this as its last command.
BEGIN – Open a new transaction block. Transaction blocks can be nested; a BEGIN can be issued inside of an existing block.
ROLLBACK – Undo all of the commands issued in the most recent transaction block, and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
COMMIT – Close all open transaction blocks, permanently applying the changes made in them. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.


---------------------------------
Runs the program in terminal
---------------------------------
1) python simpleDB.py < input.txt
or
2) python simpleDB.py


------------
Test
------------
The file test_simpleDB.py was used for unit testing when I created the simpleDB program.
You can add test cases to it and run it. Before using it, make sure mock is installed.
What I did is "pip install mock".


---------------------
Project Design 
---------------------

1. Data Structure

A table uses Python dict to store key_val pair. The key is the variable name, and the value is a list of 
(trans_id, val) pair for each transaction. The latest transaction is added to the end of the list.

table = {name_1: [[trans_id_1, val_1], [trans_id_2, val_2], ...];
         name_2: [[trans_id_1, val_1], [trans_id_2, val_2], ...];
         ...
         ...
        }

For the cmd NUMEQUALTO, a similar structure is used:
counts = {val_1: [[trans_id_1, count_1], [trans_id_2, count_2], ...];
          val_2: [[trans_id_1, count_1], [trans_id_2, count_2], ...];
          ...
          ...
         }

The design of such structures origins from the requirement of multi-level transactions. 
A common solution is recursively calling a new transaction. But we can use a list of (trans_id, val) pairs to 
simulates a stack operation, which saves the recursion stack memory. 

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


2. Command Algorithm

1) UNSET
Unset a variable is treated as setting the variable with the value of NULL.
If UNSET is called before GET in the same transaction for the same variable, and that 
variable is set in the previous transaction, using a var-NULL pair will inform the cmd
GET that the var has been unset.

2) BEGIN
The global variable trans_id in our simpleDB class represents the current transaction id. 
Beginning a new tranction simply increases the current trans_id by one.

3) ROLLBACK
ROLLBACK deletes all the data under current transaction and decreases trans_id by one.

4) COMMIT 
COMMIT only saves the data with the latest transaction id and ends all the transactions by reset trans_id to 0.

5) SET
SET adds or updates the transaction list of the variable name, and updates the counts of the value.


3. Command Validation
A command validation function is included in the class simpleDB. 