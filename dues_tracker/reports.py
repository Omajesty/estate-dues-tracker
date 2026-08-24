from .data_management import load_raw_data

def parse_database():
    """A helper function to break plain lines into lists for names and payments."""
    members = {}
    payments = []
    
    lines = load_raw_data()
    current_section = None
    
    for line in lines:
        cleaned = line.strip()
        if cleaned == "":
            continue
        if cleaned == "[Estate Members]" or cleaned == "[Payment Records]":
            current_section = cleaned
            continue

        if current_section == "[Estate Members]" and cleaned.startswith("ID:"):
            # Splits "ID: EST-001 | Name: John" into pieces
            parts = cleaned.split("|")
            m_id = parts[0].replace("ID:", "").strip()
            name = parts[1].replace("Name:", "").strip()
            members[m_id] = name

        elif current_section == "[Payment Records]" and cleaned.startswith("ID:"):
            parts = cleaned.split("|")
            m_id = parts[0].replace("ID:", "").strip()
            month = parts[1].replace("Month:", "").strip()
            amount = parts[2].replace("Amount:", "").strip()
            
            payment_dictionary = {"id": m_id, "month": month, "amount": amount}
            payments.append(payment_dictionary)

    return members, payments

def fetch_history(member_id):
    """Finds all payment lines matching a specific member ID."""
    id_upper = member_id.strip().upper()
    members, payments = parse_database()
    
    if id_upper not in members:
        return None, "Member ID " + id_upper + " does not exist."
        
    user_payments = []
    for payment in payments:
        if payment["id"] == id_upper:
            user_payments.append(payment)
            
    result = {"name": members[id_upper], "records": user_payments}
    return result, None

def generate_monthly_status(target_month):
    """Sorts all estate members into paid lists or owing lists for a specific month."""
    members, payments = parse_database()
    month_query = target_month.strip().lower()
    
   
    paid_ids = []
    for payment in payments:
        if payment["month"].lower() == month_query:
            paid_ids.append(payment["id"])
            
    up_to_date = []
    owing = []
    
   
    for m_id, name in members.items():
        member_data = {"id": m_id, "name": name}
        if m_id in paid_ids:
            up_to_date.append(member_data)
        else:
            owing.append(member_data)
            
    return up_to_date, owing
