import dues_tracker
from dues_tracker import functions
import dues_tracker.reports as report_engine

from dues_tracker.data_management import create_backup

def run_menu():
    try:
        dues_tracker.start()
    except Exception as err:
        print("\n[System Error] " + str(err))
        print("Please fix the file structure manually before starting.")
        return

    while True:
        print("\n==========================================")
        print("       ESTATE MANAGEMENT SYSTEM           ")
        print("==========================================")
        print("1. Register New Member")
        print("2. Record Dues Payment")
        print("3. Check Dues Status (Paid vs Owing)")
        print("4. View Member Full Payment History")
        print("5. Create Dated Data Backup (Snapshot)")
        print("6. Import Members from new_members.txt")
        print("7. Exit System")
        print("==========================================")
        
        choice = input("Select an option (1-7): ").strip()
        
        try:
            if choice == "1":
                name = input("Enter Member Full Name: ")
                success, response = functions.add_member(name)
                if success:
                    print("\nSuccess: Member registered with ID: " + response)
                else:
                    print("\nError: " + response)

            elif choice == "2":
                m_id = input("Enter Member ID (e.g., EST-001): ")
                amt = input("Enter Amount Paid: ")
                mth = input("Enter Billing Month (e.g., January 2026): ")
                success, response = functions.record_payment(m_id, amt, mth)
                if success:
                    print("\n" + response)
                else:
                    print("\nError: " + response)

            elif choice == "3":
                target_month = input("Enter Month & Year to audit (e.g., January 2026): ")
                paid, owing = report_engine.generate_monthly_status(target_month)
                
                print("\nDUES REPORT FOR: " + target_month.upper())
                print("\nUP TO DATE:")
                for item in paid:
                    print("  - [" + item['id'] + "] " + item['name'])
                if len(paid) == 0:
                    print("  (No payments recorded)")
                    
                print("\nOWING / DEBTORS:")
                for item in owing:
                    print("  - [" + item['id'] + "] " + item['name'])
                if len(owing) == 0:
                    print("  (No debtors tracked for this period)")

            elif choice == "4":
                search_id = input("Enter Member ID (e.g., EST-001): ")
                data, error = report_engine.fetch_history(search_id)
                if error:
                    print("\nError: " + error)
                else:
                    print("\nPayment Statement: " + data['name'] + " (" + search_id.upper() + ")")
                    for r in data['records']:
                        print("  - " + r['month'] + " | Amount: " + r['amount'] + " | Paid")
                    if len(data['records']) == 0:
                        print("  No transactions posted for this profile.")

            elif choice == "5":
                success, response = create_backup()
                if success:
                    print("\nSuccess: Backup file created -> " + response)
                else:
                    print("\nError: Could not back up data. " + response)

            elif choice == "6":
                print("\nAttempting to import from 'new_members.txt'...")
                success, response = functions.import_members_from_file("new_members.txt")
                if success:
                    print("\nSuccess! " + response)
                else:
                    print("\nError: " + response)

            elif choice == "7":
                print("\nGoodbye")
                break
            else:
                print("\nInvalid selection. Please choose an option from 1 to 7.")
                
        except ValueError as file_error:
            print("\n[File Corruption Detected] " + str(file_error))
            print("The program stopped to prevent losing data layout records.")

if __name__ == "__main__":
    run_menu()
