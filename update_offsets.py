import os
import json

# Read the specific strings from strings.txt
with open('strings.txt', 'r') as f:
    specific_strings = [line.strip() for line in f]

# Initialize a dictionary to store the variables and their values
variables = {string: 0 for string in specific_strings}  # Default all values to 0

# Load the existing offsets from offsets.json
with open('offsets.json', 'r') as f:
    offsets = json.load(f)

# Get the current dw_build_number from offsets.json and store in a global variable
dw_build_number = offsets.get("dw_build_number", 0)

# Get the current dwBuildNumber from offsets.json
dw_build_number_offset = offsets.get("dwBuildNumber", 0)

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

# Flag to check if dwBuildNumber has changed
dw_build_number_changed = False

# Step 1: Search in non-server files
for filename in os.listdir('../cs2-dumper/output'):
    if filename.endswith('.json') and 'server' not in filename:  # Skip files with 'server' in the name
        with open(os.path.join('../cs2-dumper/output', filename), 'r') as f:
            data = json.load(f)
            # Search the JSON data for specific strings
            search_json(data, specific_strings, client_mode=False)

# Step 2: Search in client files
for filename in os.listdir('../cs2-dumper/output'):
    if filename.endswith('.json') and 'client' in filename:  # Only process files with 'client' in the name
        with open(os.path.join('../cs2-dumper/output', filename), 'r') as f:
            data = json.load(f)
            # Search the JSON data for specific strings
            search_json(data, specific_strings, client_mode=True)
            # Check if dwBuildNumber has changed
            if variables.get("dwBuildNumber", dw_build_number) != dw_build_number_offset:
                dw_build_number_changed = True

# Increment dw_build_number if dwBuildNumber has changed
if dw_build_number_changed:
    dw_build_number += 1

# Update variables with the incremented dw_build_number
variables["dw_build_number"] = dw_build_number

# Ensure dwBuildNumber matches dw_build_number
variables["dwBuildNumber"] = variables.get("dwBuildNumber", dw_build_number)

# Print the variables dictionary before writing to offsets.json
print("Final Variables:")
print(json.dumps(variables, indent=4))

# Dump the variables with their values into offsets.json
with open('offsets.json', 'w') as f:
    json.dump(variables, f, indent=4)
