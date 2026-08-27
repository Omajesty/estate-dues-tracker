CHAIRMAN ADE'S MONEY BOOK
=========================

ABOUT
-----

Chairman Ade's Money Book is a Python application for
managing estate members and their monthly dues.

The application allows the Chairman to:

1. Register new members.
2. Record payments.
3. Check who has paid for a particular month.
4. Check who is owing for a particular month.
5. View a member's complete payment history.
6. View all estate members.
7. View all recorded payments.
8. Keep a dated activity diary.
9. Create backups of estate records.
10. Import members from a text file.


PROJECT STRUCTURE
-----------------

main.py
--------
This is the reception desk.

It displays the menu, receives input from the Chairman,
and sends each request to the appropriate module.

It does not contain the application's main business logic.


dues_tracker/
-------------

This is the main Python package containing the different
rooms of the application.


__init__.py
-----------
Marks dues_tracker as a Python package.


data_management.py
------------------
Handles data storage and file operations.

It is responsible for:

- Creating estate_records.txt when it does not exist.
- Loading saved records.
- Saving records.
- Handling damaged record files.
- Writing events to estate_diary.txt.
- Creating dated backups.


functions.py
------------
Contains the main business logic.

It is responsible for:

- Registering members.
- Recording payments.
- Validating input.
- Finding members.
- Checking payment status.
- Retrieving member information.
- Importing members.


reports.py
----------
Handles the presentation of information.

It displays:

- Individual member details.
- Payment history.
- All members.
- Payment status.
- All payments.


DATA FILES
----------

estate_records.txt
------------------
Stores the permanent member and payment information
in JSON format.

estate_diary.txt
----------------
Stores a dated record of important events.

estate_records_backup_...
-------------------------
Contains dated copies of the estate records.


PAYMENT RULE
------------

There is no fixed dues amount in this application.

The Chairman only records a payment when a member has
brought their complete dues.

Therefore:

- A recorded payment means the member is PAID for that month.
- No payment record means the member is OWING for that month.

The amount paid is still recorded for the Chairman's records.


FIRST RUN
---------

The first time the program is run, estate_records.txt
may not exist.

The program detects this and creates a new empty database
automatically.


RUNNING THE PROGRAM
-------------------

Open a terminal in the estate_dues_manager folder.

Run:

python main.py


PERSISTENCE
-----------

All member and payment information is saved to
estate_records.txt.

The records therefore remain available after the program
is closed and started again.


ERROR HANDLING
--------------

If estate_records.txt does not exist, the program creates
it automatically.

If the file contains invalid JSON or an invalid structure,
the program reports the problem using a human-readable
message rather than exposing a Python traceback.


DIARY
-----

Every important event is recorded in estate_diary.txt
with its date and time.

The diary uses append mode so previous entries are never
deleted when new events occur.


BONUS FEATURES
--------------

The application includes:

1. A dated backup option.

2. An import option for new_members.txt.

The import file contains one member name per line.
Empty or invalid lines are rejected without crashing
the program.