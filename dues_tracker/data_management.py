import json
import shutil
from datetime import datetime
from pathlib import Path


# Files are located in the main project folder.
BASE_DIR = Path(__file__).resolve().parent.parent

RECORDS_FILE = BASE_DIR / "estate_records.txt"
DIARY_FILE = BASE_DIR / "estate_diary.txt"


def check_db():
    """Check whether the estate records file exists."""

    return RECORDS_FILE.exists()


def create_db():
    """Create a new empty estate records file."""

    data = {
        "members": []
    }

    try:
        with open(RECORDS_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:
        raise ValueError(
            "The estate records file could not be created."
        )


def load_raw_data():
    """
    Load the estate records.

    If no records file exists, create a fresh one.

    If the existing file contains invalid JSON or has
    an invalid structure, return a human-readable error.
    """

    if not check_db():
        create_db()

    try:
        with open(RECORDS_FILE, "r") as file:
            data = json.load(file)

    except json.JSONDecodeError:
        raise ValueError(
            "The estate records file is damaged or contains "
            "invalid data."
        )

    except OSError:
        raise ValueError(
            "The estate records file could not be opened."
        )

    # Check that the main structure is correct.
    if not isinstance(data, dict):
        raise ValueError(
            "The estate records have an invalid format."
        )

    if "members" not in data:
        raise ValueError(
            "The estate records are missing the members section."
        )

    if not isinstance(data["members"], list):
        raise ValueError(
            "The members section must be a list."
        )

    # Validate each member's basic structure.
    for member in data["members"]:

        if not isinstance(member, dict):
            raise ValueError(
                "The estate records contain an invalid member."
            )

        required_fields = [
            "name",
            "house_no",
            "dor",
            "payments"
        ]

        for field in required_fields:
            if field not in member:
                raise ValueError(
                    f"A member record is missing '{field}'."
                )

        if not isinstance(member["payments"], list):
            raise ValueError(
                "A member's payments must be stored as a list."
            )

    return data


def save_raw_data(data):
    """Save estate records to the records file."""

    try:
        with open(RECORDS_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:
        raise ValueError(
            "The estate records could not be saved."
        )


def get_timestamp():
    """Return the current date and time."""

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def log_event(message):
    """
    Add an event to the estate diary.

    'a' means append, so old diary entries are preserved.
    """

    try:
        with open(DIARY_FILE, "a") as file:
            file.write(
                f"[{get_timestamp()}] {message}\n"
            )

    except OSError:
        print(
            "Warning: The estate diary could not be updated."
        )


def backup_records():
    """
    Create a dated backup of estate_records.txt.
    """

    if not RECORDS_FILE.exists():
        return False, (
            "There are no estate records to back up."
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        BASE_DIR /
        f"estate_records_backup_{timestamp}.txt"
    )

    try:
        shutil.copy2(
            RECORDS_FILE,
            backup_file
        )

    except OSError:
        return False, (
            "The estate records backup could not be created."
        )

    return True, (
        f"Backup created successfully:\n"
        f"{backup_file.name}"
    )