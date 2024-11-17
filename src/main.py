import os
import sys
from dotenv import load_dotenv
from data_processor import (
    sanitize_all_items_report,
    sanitize_cash_entries,
    sanitize_check_details,
    sanitize_item_selection_details,
    sanitize_kitchen_timings,
    sanitize_modifiers_selection_details,
    sanitize_order_details,
    sanitize_payment_details,
    sanitize_time_entries
)

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
        print("Usage: python main.py <input_directory>")
        sys.exit(1)
    input_directory = sys.argv[1]
    main(input_directory)
