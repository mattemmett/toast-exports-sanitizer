import pandas as pd
import random
import string
import json
import uuid

def sanitize_all_items_report(file_path):
    data = pd.read_csv(file_path)
    if 'Item Qty (incl voids)' in data.columns:
        data = data[data['Item Qty (incl voids)'] != 0.0]
    return data

def sanitize_cash_entries(file_path):
    data = pd.read_csv(file_path)
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT
    for column in ['Employee', 'Employee 2']:
        if column in data.columns:
            data[column] = data[column].apply(lambda x: map_employee(x, column) if pd.notna(x) else x)
    return data

def sanitize_check_details(file_path):
    data = pd.read_csv(file_path)
    for column in ['Customer Id', 'Location Code']:
        if column in data.columns and data[column].notna().any():
            raise ValueError(f"Error: '{column}' field is unexpectedly populated. Please open an issue with the developer.")
    if 'Customer' in data.columns:
        data['Customer'] = data['Customer'].apply(lambda x: generate_random_name() if pd.notna(x) else x)
    if 'Customer Phone' in data.columns:
        data['Customer Phone'] = data['Customer Phone'].apply(lambda x: generate_random_phone() if pd.notna(x) else x)
    if 'Customer Email' in data.columns:
        data['Customer Email'] = data['Customer Email'].apply(lambda x: generate_random_email() if pd.notna(x) else x)
    if 'Server' in data.columns:
        data['Server'] = data['Server'].apply(lambda x: map_employee(x, 'Server') if pd.notna(x) else x)
    if 'Link' in data.columns:
        data['Link'] = data['Link'].apply(lambda x: randomize_link(x) if pd.notna(x) else x)
    return data

def sanitize_item_selection_details(file_path):
    data = pd.read_csv(file_path)
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT
    if 'Server' in data.columns:
        data['Server'] = data['Server'].apply(lambda x: map_employee(x, 'Server') if pd.notna(x) else x)
    if 'Tab Name' in data.columns:
        data['Tab Name'] = data['Tab Name'].apply(lambda x: generate_random_name() if pd.notna(x) else x)
    return data

def sanitize_kitchen_timings(file_path):
    data = pd.read_csv(file_path)
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT
    if 'Server' in data.columns:
        data['Server'] = data['Server'].apply(lambda x: map_employee(x, 'Server') if pd.notna(x) else x)
    if 'Fulfilled By' in data.columns:
        data['Fulfilled By'] = data['Fulfilled By'].apply(lambda x: map_employee(x, 'Fulfilled By') if pd.notna(x) else x)
    return data

def sanitize_modifiers_selection_details(file_path):
    data = pd.read_csv(file_path)
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT
    if 'Server' in data.columns:
        data['Server'] = data['Server'].apply(lambda x: map_employee(x, 'Server') if pd.notna(x) else x)
    return data

def sanitize_order_details(file_path):
    data = pd.read_csv(file_path)
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT
    if 'Server' in data.columns:
        data['Server'] = data['Server'].apply(lambda x: map_employee(x, 'Server') if pd.notna(x) else x)

    if 'Tab Names' in data.columns:
        def randomize_tab_names(tab_names):
            if pd.notna(tab_names):
                tab_list = tab_names.split(", ") if tab_names.startswith('"') and tab_names.endswith('"') else [tab_names]
                randomized_tabs = [generate_random_name() for _ in tab_list]
                return f'"{", ".join(randomized_tabs)}"' if len(randomized_tabs) > 1 else randomized_tabs[0]
            return tab_names

        data['Tab Names'] = data['Tab Names'].apply(randomize_tab_names)

    return data

def sanitize_payment_details(file_path):
    data = pd.read_csv(file_path)
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT
    if 'Tab Name' in data.columns:
        data['Tab Name'] = data['Tab Name'].apply(lambda x: generate_random_name() if pd.notna(x) else x)
    for column in ['Server', 'Void User', 'Void Approver']:
        if column in data.columns:
            data[column] = data[column].apply(lambda x: map_employee(x, column))
    if 'Email' in data.columns:
        data['Email'] = data['Email'].apply(lambda x: generate_random_email() if pd.notna(x) else x)
    if 'Phone' in data.columns:
        data['Phone'] = data['Phone'].apply(lambda x: generate_random_phone() if pd.notna(x) else x)
    if 'Last 4 Card Digits' in data.columns:
        data['Last 4 Card Digits'] = data['Last 4 Card Digits'].apply(lambda x: "XXXX" if pd.notna(x) else x)
    if 'Receipt' in data.columns:
        data['Receipt'] = data['Receipt'].apply(lambda x: generate_random_string(13) if pd.notna(x) else x)
    return data

def sanitize_time_entries(file_path):
    data = pd.read_csv(file_path)
    
    if 'Location' in data.columns:
        data['Location'] = LOCATION_REPLACEMENT

    if 'Employee GUID' in data.columns:
        data['Employee GUID'] = data['Employee GUID'].apply(lambda x: generate_random_guid() if pd.notna(x) else x)

    if 'Employee External Id' in data.columns:
        data['Employee External Id'] = data['Employee External Id'].apply(lambda x: generate_random_external_id() if pd.notna(x) else x)

    if 'Employee' in data.columns:
        data['Employee'] = data['Employee'].apply(lambda x: map_employee_reverse_format(x, 'Employee') if pd.notna(x) else x)

    return data

def map_employee(value, column_name):
    if pd.notna(value):
        if value in EMPLOYEE_MAPPING:
            return EMPLOYEE_MAPPING[value]
        else:
            raise ValueError(f"Error: '{value}' in column '{column_name}' is not found in EMPLOYEE_MAPPING.")
    return value

def map_employee_reverse_format(value, column_name):
    if pd.notna(value):
        reversed_name = ' '.join(value.split(", ")[::-1])
        if reversed_name in EMPLOYEE_MAPPING:
            mapped_name = EMPLOYEE_MAPPING[reversed_name]
            return ', '.join(mapped_name.split(" ")[::-1])
        else:
            raise ValueError(f"Error: '{value}' in column '{column_name}' is not found in EMPLOYEE_MAPPING.")
    return value

def randomize_link(url):
    base_url = "http://www.toasttab.com/receipts/"
    if url.startswith(base_url):
        random_part = generate_random_string(16) + "/" + generate_random_string(16)
        return base_url + random_part
    return url

def generate_random_name():
    first_names = ["Alex", "Chris", "Jordan", "Taylor", "Morgan", "Casey"]
    last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_email():
    domains = ["example.com", "email.com", "mail.com"]
    return f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@{random.choice(domains)}"

def generate_random_phone():
    return ''.join(random.choices(string.digits, k=10))

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_guid():
    return str(uuid.uuid4())

def generate_random_external_id():
    return ''.join(random.choices(string.digits, k=4))
