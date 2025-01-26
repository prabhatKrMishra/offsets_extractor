import os
import re
import json

# Read the specific strings from strings.txt
with open('strings.txt', 'r') as f:
    specific_strings = [line.strip() for line in f]

# Initialize a dictionary to store the variables and their values
variables = {string: "0x0" for string in specific_strings}  # Default all values to "0x0"

# Load the existing offsets from offsets.json
with open('offsets.json', 'r') as f:
    offsets = json.load(f)

# Get the current dw_build_number from offsets.json and store in a global variable
dw_build_number = offsets.get("dw_build_number", "0x0")

# Get the current dwBuildNumber from offsets.json
dw_build_number_offset = offsets.get("dwBuildNumber", "0x0")

# Function to parse .hpp files and extract hex values
def parse_hpp(file_path, specific_strings, client_mode=False):
    with open(file_path, 'r') as f:
        content = f.read()

    # Regular expression to match variables with hexadecimal offsets
    pattern = r"constexpr std::ptrdiff_t (\w+) = (0x[0-9A-Fa-f]+);"
    matches = re.findall(pattern, content)

    for name, hex_value in matches:
        if name in specific_strings and variables[name] == "0x0":  # Only update if not already set
            variables[name] = hex_value  # Directly store the hex value
            print(f"{'[CLIENT]' if client_mode else '[NON-CLIENT]'} Found: '{name}' with value: {hex_value}")

# Flag to check if dwBuildNumber has changed
dw_build_number_changed = False

# Step 1: Search in non-server .hpp files
for filename in os.listdir('../cs2-dumper/output'):
    if filename.endswith('.hpp') and 'server' not in filename:  # Skip files with 'server' in the name
        file_path = os.path.join('../cs2-dumper/output', filename)
        parse_hpp(file_path, specific_strings, client_mode=False)

# Step 2: Search in client .hpp files
for filename in os.listdir('../cs2-dumper/output'):
    if filename.endswith('.hpp') and 'client' in filename:  # Only process files with 'client' in the name
        file_path = os.path.join('../cs2-dumper/output', filename)
        parse_hpp(file_path, specific_strings, client_mode=True)
        # Check if dwBuildNumber has changed
        if variables.get("dwBuildNumber", dw_build_number) != dw_build_number_offset:
            dw_build_number_changed = True

# Increment dw_build_number if dwBuildNumber has changed
if dw_build_number_changed:
    dw_build_number = dw_build_number + 1

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
