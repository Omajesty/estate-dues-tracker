# Estate Dues Management System

A modular, lightweight Python package designed to help housing estate residents' associations track membership registrations, monthly dues payments, ledger statements, and account auditing status securely.

This project was built strictly using custom text-file parsing structures to guarantee permanent data storage across application restarts, alongside a background activity log diary.

## Features

- **Permanent File Registry:** Stores estate membership data and accounting sheets in `estate_records.txt` to ensure records survive local application closures.
- **Automated Identifier Sequence:** Automatically generates clean structural tracking references (e.g., `EST-001`, `EST-002`) during student/resident onboarding processes.
- **Historical Payment Logs:** Collects financial profiles specifying member IDs, numeric targets, billing month cycles, and updates transaction registers.
- **Dues Status Auditing:** Filters entire account ledgers to separate profiles instantly into **Up To Date** or **Owing / Debtors** lists for any chosen month.
- **Activity Log Diary:** Appends timestamped, human-readable audit lines to `estate_diary.txt` whenever profiles update, ensuring readable historical data outside the program.

## How to Set Up and Run

### 1. Prerequisites
Ensure you have Python 3 installed on your system. This application relies purely on standard Python built-in modules and does not require external library configurations or `pip` dependencies.

### 2. Cloned Folder Preparation
Ensure your target workspace reflects the package setup exactly:
- `main.py` sits directly in the root workspace directory.
- `dues_tracker/` exists as a subfolder directly next to `main.py`.

### 3. Running the Program
Open your system command prompt or terminal window, navigate into the root directory containing `main.py`, and run the following command:

```bash
python main.py
```
