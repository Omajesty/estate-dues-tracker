CHAIRMAN ADE'S MONEY BOOK

How to start
------------
Open a terminal in this folder and run:

    python main.py

The program creates estate_records.txt and estate_diary.txt on its first run.
The records remain after the program closes. The diary is a plain text file
that can be opened in any text editor.

main.py
    The reception desk. It displays the menu, collects input, and calls the
    appropriate function. It should not contain the data-management rules.

dues_tracker/data_management.py
    Creates, reads, writes, and backs up the text files. It also writes diary
    entries.

dues_tracker/functions.py
    Changes estate data: registering members, recording payments, and importing
    members from a file.

dues_tracker/reports.py
    Reads the saved data and produces payment history and monthly status lists.

dues_tracker/__init__.py
    Marks dues_tracker as a Python package and starts the package data files.

estate_records.txt                    Saved members and payments
estate_diary.txt                      Append-only activity diary
estate_records_backup_YYYY-MM-DD.txt  Dated records snapshot
new_members.txt                       Optional import file, one name and phone
                                      per line: Name, Phone