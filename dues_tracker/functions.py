from .data_management import load_raw_data, save_raw_data, log_event

def add_member(member_name):
    """A function to count current members, create a new sequential ID, and add them."""
    try:
        lines = load_raw_data()
    except ValueError as e:
        return False, str(e)

    name_clean = member_name.strip()
    if name_clean == "":
        return False, "Member name cannot be empty."

    
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


    next_id = "EST-" + str(member_count + 1).zfill(3)
    

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
    
    
    try:
        amount_num = float(amount)
        if amount_num <= 0:
            return False, "Payment amount must be greater than zero."
    except ValueError:
        return False, "Amount must be a number."


    id_exists = False
    for line in lines:
        if line.strip().startswith("ID: " + id_upper + " |"):
            id_exists = True
            break

    if not id_exists:
        return False, "Member ID " + id_upper + " is not registered."


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

def import_members_from_file(import_filename="new_members.txt"):
    """Reads a text file line-by-line and imports members dynamically."""
    import os
    if not os.path.exists(import_filename):
        return False, "Import file '" + import_filename + "' not found. Create it first."

    try:
        with open(import_filename, "r", encoding="utf-8") as f:
            lines_to_import = f.readlines()
    except Exception as e:
        return False, "Failed to read import file: " + str(e)

    success_count = 0
    skipped_count = 0

    for line in lines_to_import:
        cleaned_line = line.strip()
        
        
        if cleaned_line == "":
            continue
            
        
        try:
            if "," not in cleaned_line:
                
                skipped_count = skipped_count + 1
                continue
                
            parts = cleaned_line.split(",")
            name = parts[0].strip()
            phone = parts[1].strip()
            
            
            if name == "" or phone == "":
                skipped_count = skipped_count + 1
                continue
                
            
            member_details = name + " (Phone: " + phone + ")"
            
            
            success, result = add_member(member_details)
            
            if success:
                success_count = success_count + 1
            else:
                skipped_count = skipped_count + 1
                
        except Exception:
            
            skipped_count = skipped_count + 1
            continue

    from .data_management import log_event
    log_event("IMPORT COMPLETED: Successfully added " + str(success_count) + " members. Skipped " + str(skipped_count) + " bad lines.")
    
    summary = "Import complete. Added: " + str(success_count) + " | Skipped/Bad format: " + str(skipped_count)
    return True, summary

