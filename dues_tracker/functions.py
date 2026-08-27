from .data_management import (
    load_raw_data,
    save_raw_data,
    log_event,
    get_timestamp,
)


def validate_name(name):
    """Validate a member's name."""

    name = name.strip()

    if name == "":
        return False, "Member name cannot be empty."

    return True, name


def validate_house_number(house_no):
    """Validate a house number."""

    try:
        house_no = int(house_no)

    except (ValueError, TypeError):
        return False, "House number must be a number."

    if house_no <= 0:
        return False, (
            "House number must be greater than zero."
        )

    return True, house_no


def validate_amount(amount):
    """
    Validate a payment amount.

    There is intentionally no fixed dues amount.
    The Chairman only records complete payments.
    """

    try:
        amount = float(amount)

    except (ValueError, TypeError):
        return False, (
            "Payment amount must be a number."
        )

    if amount <= 0:
        return False, (
            "Payment amount must be greater than zero."
        )

    return True, amount


def validate_month(month):
    """Validate a payment month."""

    month = month.strip()

    if month == "":
        return False, "Payment month cannot be empty."

    return True, month


def find_member(data, house_no):
    """Find a member using their house number."""

    for member in data["members"]:

        if member["house_no"] == house_no:
            return member

    return None


def register(member_name, house_no):
    """
    Register a new estate member.
    """

    valid, member_name = validate_name(member_name)

    if not valid:
        return False, member_name

    valid, house_no = validate_house_number(house_no)

    if not valid:
        return False, house_no

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    # Prevent duplicate house numbers.
    if find_member(data, house_no) is not None:
        return False, (
            f"House number {house_no} is already registered."
        )

    details = {
        "name": member_name,
        "house_no": house_no,
        "dor": get_timestamp(),
        "payments": []
    }

    data["members"].append(details)

    try:
        save_raw_data(data)

    except ValueError as error:
        return False, str(error)

    log_event(
        f"New member registered: "
        f"{member_name}, House {house_no}"
    )

    return True, (
        f"{member_name} registered successfully."
    )


def record_payment(house_no, amount, month):
    """
    Record a complete payment for a particular month.

    There is no fixed dues amount. Once the Chairman
    records a payment, that member is considered paid
    for that month.
    """

    valid, house_no = validate_house_number(house_no)

    if not valid:
        return False, house_no

    valid, amount = validate_amount(amount)

    if not valid:
        return False, amount

    valid, month = validate_month(month)

    if not valid:
        return False, month

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    member = find_member(data, house_no)

    if member is None:
        return False, (
            f"No member found for house {house_no}."
        )

    # Do not record the same month twice.
    for payment in member["payments"]:

        if payment["month"].lower() == month.lower():
            return False, (
                f"{member['name']} already has a payment "
                f"recorded for {month}."
            )

    payment = {
        "month": month,
        "amount": amount,
        "date": get_timestamp()
    }

    member["payments"].append(payment)

    try:
        save_raw_data(data)

    except ValueError as error:
        return False, str(error)

    log_event(
        f"Payment recorded: "
        f"{member['name']}, "
        f"House {house_no}, "
        f"Amount {amount:.2f}, "
        f"Month {month}"
    )

    return True, (
        f"Payment for {month} recorded successfully "
        f"for {member['name']}."
    )


def check_payment_status(month):
    """
    Determine who has paid and who is owing for a month.

    A payment record means PAID.
    No payment record means OWING.
    """

    valid, month = validate_month(month)

    if not valid:
        return False, month

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    results = []

    for member in data["members"]:

        paid = False

        for payment in member["payments"]:

            if payment["month"].lower() == month.lower():
                paid = True
                break

        status = "PAID" if paid else "OWING"

        results.append({
            "name": member["name"],
            "house_no": member["house_no"],
            "status": status
        })

    return True, results


def get_member(house_no):
    """
    Retrieve one member and their complete payment history.
    """

    valid, house_no = validate_house_number(house_no)

    if not valid:
        return False, house_no

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    member = find_member(data, house_no)

    if member is None:
        return False, (
            f"No member found for house {house_no}."
        )

    return True, member


def get_all_members():
    """Return all estate members."""

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    return True, data["members"]


def get_all_payments():
    """Return every payment recorded in the estate."""

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    payments = []

    for member in data["members"]:

        for payment in member["payments"]:

            payments.append({
                "name": member["name"],
                "house_no": member["house_no"],
                "month": payment["month"],
                "amount": payment["amount"],
                "date": payment["date"]
            })

    return True, payments


def import_members(filename="new_members.txt"):
    """
    Import members from a text file.

    Each non-empty line is treated as one member name.
    A new sequential house number is assigned.

    Invalid/empty lines are rejected without crashing.
    """

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

    except FileNotFoundError:
        return False, (
            f"The file '{filename}' could not be found."
        )

    except OSError:
        return False, (
            f"The file '{filename}' could not be opened."
        )

    try:
        data = load_raw_data()

    except ValueError as error:
        return False, str(error)

    imported = 0
    rejected = 0

    # Determine the next house number.
    house_numbers = [
        member["house_no"]
        for member in data["members"]
    ]

    if house_numbers:
        next_house = max(house_numbers) + 1
    else:
        next_house = 1

    for line in lines:

        name = line.strip()

        # Empty/nonsense lines are rejected.
        if not name:
            rejected += 1
            continue

        valid, name = validate_name(name)

        if not valid:
            rejected += 1
            continue

        # Avoid importing the same name twice.
        duplicate_name = False

        for member in data["members"]:

            if member["name"].lower() == name.lower():
                duplicate_name = True
                break

        if duplicate_name:
            rejected += 1
            continue

        member = {
            "name": name,
            "house_no": next_house,
            "dor": get_timestamp(),
            "payments": []
        }

        data["members"].append(member)

        log_event(
            f"New member imported: "
            f"{name}, House {next_house}"
        )

        imported += 1
        next_house += 1

    try:
        save_raw_data(data)

    except ValueError as error:
        return False, str(error)

    return True, (
        f"Import complete. "
        f"Imported: {imported}. "
        f"Rejected: {rejected}."
    )