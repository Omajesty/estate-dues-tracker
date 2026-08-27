from dues_tracker.data_management import backup_records
from dues_tracker.functions import (
    import_members,
    record_payment,
    register,
)
from dues_tracker.reports import (
    show_all_members,
    show_all_payments,
    show_member,
    show_payment_status,
)


def show_menu():
    """Display the main menu."""

    print("\n")
    print("=" * 50)
    print("       CHAIRMAN ADE'S MONEY BOOK")
    print("=" * 50)
    print("1. Register new member")
    print("2. Record payment")
    print("3. View member")
    print("4. View all members")
    print("5. Check payment status")
    print("6. View all payments")
    print("7. Backup records")
    print("8. Import members")
    print("0. Exit")
    print("=" * 50)


def main():

    while True:

        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            print("\n--- REGISTER MEMBER ---")

            name = input(
                "Enter member name: "
            )

            house_no = input(
                "Enter house number: "
            )

            success, message = register(
                name,
                house_no
            )

            print(message)

        elif choice == "2":

            print("\n--- RECORD PAYMENT ---")

            house_no = input(
                "Enter house number: "
            )

            amount = input(
                "Enter amount paid: "
            )

            month = input(
                "Enter month paid for: "
            )

            success, message = record_payment(
                house_no,
                amount,
                month
            )

            print(message)

        elif choice == "3":

            print("\n--- VIEW MEMBER ---")

            house_no = input(
                "Enter house number: "
            )

            show_member(house_no)

        elif choice == "4":

            show_all_members()

        elif choice == "5":

            print("\n--- PAYMENT STATUS ---")

            month = input(
                "Enter month to check: "
            )

            show_payment_status(month)

        elif choice == "6":

            show_all_payments()

        elif choice == "7":

            print("\n--- BACKUP RECORDS ---")

            success, message = backup_records()

            print(message)

        elif choice == "8":

            print("\n--- IMPORT MEMBERS ---")

            filename = input(
                "Enter filename "
                "(press Enter for new_members.txt): "
            ).strip()

            if not filename:
                filename = "new_members.txt"

            success, message = import_members(
                filename
            )

            print(message)

        elif choice == "0":

            print(
                "\nChairman Ade's Money Book closed."
            )
            print(
                "All records have been saved."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select a valid menu option."
            )


if __name__ == "__main__":
    main()