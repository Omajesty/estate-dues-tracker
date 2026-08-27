from .functions import (
    check_payment_status,
    get_all_members,
    get_all_payments,
    get_member,
)


def show_member(house_no):
    """Display one member's complete details."""

    success, member = get_member(house_no)

    if not success:
        print(member)
        return

    print("\n" + "=" * 60)
    print("MEMBER DETAILS")
    print("=" * 60)

    print(f"Name: {member['name']}")
    print(f"House Number: {member['house_no']}")
    print(f"Date Registered: {member['dor']}")

    print("\nPAYMENT HISTORY")
    print("-" * 60)

    if not member["payments"]:
        print("No payments recorded.")

    else:
        for payment in member["payments"]:

            print(
                f"Month: {payment['month']} | "
                f"Amount: {payment['amount']:.2f} | "
                f"Date: {payment['date']}"
            )

    print("=" * 60)


def show_all_members():
    """Display all registered members."""

    success, members = get_all_members()

    if not success:
        print(members)
        return

    print("\n" + "=" * 60)
    print("ALL ESTATE MEMBERS")
    print("=" * 60)

    if not members:
        print("No members have been registered.")
        return

    for member in members:

        print(
            f"House {member['house_no']} | "
            f"{member['name']} | "
            f"Payments: {len(member['payments'])}"
        )

    print("=" * 60)


def show_payment_status(month):
    """Display who has paid and who is owing."""

    success, results = check_payment_status(month)

    if not success:
        print(results)
        return

    print("\n" + "=" * 60)
    print(f"PAYMENT STATUS — {month}")
    print("=" * 60)

    if not results:
        print("No members have been registered.")
        return

    for result in results:

        print(
            f"House {result['house_no']} | "
            f"{result['name']} | "
            f"{result['status']}"
        )

    print("=" * 60)


def show_all_payments():
    """Display all payments in the estate."""

    success, payments = get_all_payments()

    if not success:
        print(payments)
        return

    print("\n" + "=" * 75)
    print("ALL PAYMENTS")
    print("=" * 75)

    if not payments:
        print("No payments have been recorded.")
        return

    for payment in payments:

        print(
            f"{payment['name']} | "
            f"House {payment['house_no']} | "
            f"{payment['month']} | "
            f"{payment['amount']:.2f} | "
            f"{payment['date']}"
        )

    print("=" * 75)