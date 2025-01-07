import os
import json

# Read the specific strings from strings.txt
with open('strings.txt', 'r') as f:
    specific_strings = [line.strip() for line in f]

# Initialize a dictionary to store the variables and their values
variables = {string: 14057 if string == "dw_build_number" else 0 for string in specific_strings}  # Default dw_build_number to 13984

# Define a recursive function to search for strings inside nested JSON objects
def search_json(data, specific_strings, client_mode=False):
    for key, value in data.items():
        if isinstance(value, (str, int)):  # Check if the value is string or integer
            if key in specific_strings and variables[key] == 0:  # Only update if not already set
                variables[key] = value
                print(f"{'[CLIENT]' if client_mode else '[NON-CLIENT]'} Found: '{key}' with value: {value}")
        elif isinstance(value, dict):  # If the value is a dictionary, search recursively
            search_json(value, specific_strings, client_mode)
        elif isinstance(value, list):  # If the value is a list, iterate through the list
            for item in value:
                if isinstance(item, dict):
                    search_json(item, specific_strings, client_mode)

# Step 1: Search in non-server files
for filename in os.listdir('../cs2-dumper/output'):
    if filename.endswith('.json') and 'server' not in filename:  # Skip files with 'server' in the name
        with open(os.path.join('../cs2-dumper/output', filename), 'r') as f:
            data = json.load(f)
            # Search the JSON data for specific strings
            search_json(data, specific_strings, client_mode=False)

# Step 2: Search in client files (only update variables that are still 0)
for filename in os.listdir('../cs2-dumper/output'):
    if filename.endswith('.json') and 'client' in filename:  # Only process files with 'client' in the name
        with open(os.path.join('../cs2-dumper/output', filename), 'r') as f:
            data = json.load(f)
            # Search the JSON data for specific strings
            search_json(data, specific_strings, client_mode=True)

# Ensure dw_build_number defaults to manula value
variables["dw_build_number"] = variables.get("dw_build_number", 14057)

# Print the variables dictionary before writing to offsets.json
print("Final Variables:")
print(json.dumps(variables, indent=4))

# Dump the variables with their values into offsets.json
with open('offsets.json', 'w') as f:
    json.dump(variables, f, indent=4)
