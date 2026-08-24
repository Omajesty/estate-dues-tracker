from .data_management import load_raw_data, save_raw_data, log_event

def add_member(member_name):
    """Counts current members, creates a new sequential ID, and adds them."""
    try:
        lines = load_raw_data()
    except ValueError as e:
        return False, str(e)

    name_clean = member_name.strip()
    if name_clean == "":
        return False, "Member name cannot be empty."

    # Count how many members are already registered to decide the next ID
    member_count = 0
    counting = False
    for line in lines:
        if "[Estate Members]" in line:
            counting = True
            continue
        if "[Payment Records]" in line:
            break
        if counting and line.strip().startswith("ID:"):
            member_count = member_count + 1

    # Formats number into simple ID style (e.g., EST-001)
    next_id = "EST-" + str(member_count + 1).zfill(3)
    
    # Locate the member section index to insert the new line right under it
    target_index = -1
    for i, line in enumerate(lines):
        if line.strip() == "[Estate Members]":
            target_index = i
            break

    if target_index != -1:
        new_record = "ID: " + next_id + " | Name: " + name_clean + "\n"
        lines.insert(target_index + 1, new_record)
        save_raw_data(lines)
        log_event("REGISTERED MEMBER: Added " + next_id + " - " + name_clean)
        return True, next_id
    
    return False, "Could not find Member section structure."

def record_payment(member_id, amount, month):
    """Checks if ID exists before adding a payment entry."""
    try:
        lines = load_raw_data()
    except ValueError as e:
        return False, str(e)

    id_upper = member_id.strip().upper()
    month_clean = month.strip()
    
    # Ensure amount is valid text that can be a number
    try:
        amount_num = float(amount)
        if amount_num <= 0:
            return False, "Payment amount must be greater than zero."
    except ValueError:
        return False, "Amount must be a number."

    # Look through the file to verify if this member ID exists
    id_exists = False
    for line in lines:
        if line.strip().startswith("ID: " + id_upper + " |"):
            id_exists = True
            break

    if not id_exists:
        return False, "Member ID " + id_upper + " is not registered."

    # Locate the payment section index
    payment_index = -1
    for i, line in enumerate(lines):
        if line.strip() == "[Payment Records]":
            payment_index = i
            break

    if payment_index != -1:
        record_line = "ID: " + id_upper + " | Month: " + month_clean + " | Amount: " + str(amount_num) + " | Status: Paid\n"
        lines.insert(payment_index + 1, record_line)
        save_raw_data(lines)
        log_event("PAYMENT RECORDED: ID " + id_upper + " paid " + str(amount_num) + " for " + month_clean)
        return True, "Payment recorded successfully."

    return False, "Payment Records section header is missing."
