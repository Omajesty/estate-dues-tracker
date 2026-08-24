import os
from datetime import datetime

DB_FILE = "estate_records.txt"
DIARY_FILE = "estate_diary.txt"

def start():
    """Creates the txt files with sections that looks like a database"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            f.write("[Estate Members]\n\n[Payment Records]\n")
        log_event("System Initialized: Created fresh database file.")
        
    if not os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "w", encoding="utf-8") as f:
            f.write("=== ESTATE MANAGEMENT DIARY STARTED ===\n")

def log_event(message):
    """Appends a time-stamped line to the diary."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DIARY_FILE, "a", encoding="utf-8") as f:
        f.write("[" + current_time + "] " + message + "\n")

def load_raw_data():
    """Reads lines from the file and checks if headers are missing."""
    if not os.path.exists(DB_FILE):
        start()
        
    with open(DB_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    
    has_members = False
    has_payments = False
    for line in lines:
        if "[Estate Members]" in line:
            has_members = True
        if "[Payment Records]" in line:
            has_payments = True
            
    if not has_members or not has_payments:
        raise ValueError("The data file headers have been modified or deleted.")
        
    return lines

def save_raw_data(lines):
    """Writes the updated list of lines back to the text file."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)
