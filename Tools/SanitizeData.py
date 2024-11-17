import pandas as pd
import random
import string
import os
import json
from dotenv import load_dotenv
import sys
import uuid

# Load environment variables
load_dotenv()

# Environment-based replacements
LOCATION_REPLACEMENT = os.getenv("LOCATION_REPLACEMENT")
EMPLOYEE_MAPPING = json.loads(os.getenv("EMPLOYEE_MAPPING", "{}"))

# Random value generation functions
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

# Helper function for employee mapping with error handling and format reversal
def map_employee(value, column_name):
    if pd.notna(value):
        if value in EMPLOYEE_MAPPING:
            return EMPLOYEE_MAPPING[value]
        else:
            raise ValueError(f"Error: '{value}' in column '{column_name}' is not found in EMPLOYEE_MAPPING.")
    return value

def map_employee_reverse_format(value, column_name):
    if pd.notna(value):
        # Convert "lastname, firstname" to "firstname lastname" for lookup
        reversed_name = ' '.join(value.split(", ")[::-1])
        if reversed_name in EMPLOYEE_MAPPING:
            # Convert the mapped "firstname lastname" back to "lastname, firstname"
            mapped_name = EMPLOYEE_MAPPING[reversed_name]
            return ', '.join(mapped_name.split(" ")[::-1])
        else:
            raise ValueError(f"Error: '{value}' in column '{column_name}' is not found in EMPLOYEE_MAPPING.")
    return value

# Function to randomize the link after the base URL
def randomize_link(url):
    base_url = "http://www.toasttab.com/receipts/"
    if url.startswith(base_url):
        random_part = generate_random_string(16) + "/" + generate_random_string(16)
        return base_url + random_part
    return url

# Individual sanitization functions
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

# Main function to process all files in the input directory in the specified order
def main(input_directory):
    date_dir_name = os.path.basename(os.path.normpath(input_directory))
    root_directory = os.path.abspath(os.path.join(input_directory, "../../.."))
    output_directory = os.path.join(root_directory, "SampleData", date_dir_name)
    os.makedirs(output_directory, exist_ok=True)

    file_processors = [
        ("AllItemsReport.csv", sanitize_all_items_report),
        ("CashEntries.csv", sanitize_cash_entries),
        ("CheckDetails.csv", sanitize_check_details),
        ("ItemSelectionDetails.csv", sanitize_item_selection_details),
        ("KitchenTimings.csv", sanitize_kitchen_timings),
        ("ModifiersSelectionDetails.csv", sanitize_modifiers_selection_details),
        ("OrderDetails.csv", sanitize_order_details),
        ("PaymentDetails.csv", sanitize_payment_details),
        ("TimeEntries.csv", sanitize_time_entries)
    ]

    for file_name, processor in file_processors:
        input_file = os.path.join(input_directory, file_name)
        output_file = os.path.join(output_directory, file_name)
        if os.path.isfile(input_file):
            try:
                sanitized_data = processor(input_file)
                if sanitized_data is not None:
                    sanitized_data.to_csv(output_file, index=False)
                    print(f"Sanitized {file_name} saved to {output_file}")
            except ValueError as e:
                print(f"Sanitization error in {file_name}: {e}")
        else:
            print(f"File '{file_name}' not found in directory '{input_directory}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python SanitizeData.py <input_directory>")
        sys.exit(1)
    input_directory = sys.argv[1]
    main(input_directory)
