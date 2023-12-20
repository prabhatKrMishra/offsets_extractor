import os
import yaml
import json

# Read the specific strings from strings.txt
with open('strings.txt', 'r') as f:
    specific_strings = [line.strip() for line in f]

# Initialize a dictionary to store the variables and their values
variables = {}

# Read all .yaml files from the 'generated' folder
for filename in os.listdir('../cs2-dumper/generated'):
    if filename.endswith('.yaml'):
        with open(os.path.join('../cs2-dumper/generated', filename), 'r') as f:
            data = yaml.safe_load(f)
            # Get the variable values
            for string in specific_strings:
                for key, value in data.items():
                    if value is not None and string in value:
                        if string not in variables:
                            variables[string] = value[string]
                        elif variables[string] == 0 and value[string] > 0:
                            variables[string] = value[string]

variables["dw_build_number"] = 13982

# Dump the variables with their values into offsets.json
with open('offsets.json', 'w') as f:
    json.dump(variables, f, indent=4)