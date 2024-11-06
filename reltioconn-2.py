import ast
import csv
import pandas as pd
import csv

# Read CSV with dictionaries as rows
with open('outputattributes.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = [row for row in csv_reader]
# Function to extract values from the 'attributes' dictionary
    def extract_values(attributes_dict):
        extracted_data = {}
        for key, attribute_list in attributes_dict.items():
            if isinstance(attribute_list, list) and len(attribute_list) > 0:
                # For nested attributes in Address, flatten the dictionary
                if isinstance(attribute_list[0]['value'], dict):
                    for sub_key, sub_list in attribute_list[0]['value'].items():
                        extracted_data[f"{key}_{sub_key}"] = sub_list[0]['value']
                else:
                    # Extract the main attribute value
                    extracted_data[key] = attribute_list[0]['value']
        return extracted_data

    # List to store all rows of extracted data
    all_extracted_data = []

    # Process each row in data
    for row in data:
        # Convert the 'attributes' value string to a dictionary
        attributes_dict = ast.literal_eval(row['attributes'])
        # Extract values from the attributes dictionary
        extracted_data = extract_values(attributes_dict)
        # Append the extracted data to the list
        all_extracted_data.append(extracted_data)

    # Get headers dynamically from the first row
    headers = all_extracted_data[0].keys() if all_extracted_data else []

    # Write all extracted data to CSV
    with open("outputflattened.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_extracted_data)

    print("Data has been written to outputflattened.csv")
