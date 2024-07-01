#!/usr/bin/env python3
"""
    apt-update-count

    Returns the number of upgradable packages
    This Script has to be put into the folder /opt/paessler/share/scripts on the mpp itself
    
    Note:
    This script may run on other linux machines with the skript sensor too. Not yet tested

    Link:
    https://ts-man.ch
    https://github.com/TS-Steff

"""

import subprocess
import re
import json

# Define the maximum warning and error counts
maxWrn = 1
maxErr = 3

# Initialize the count
count = 0

# Run the apt-get update command
subprocess.run(['apt-get', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Get the list of upgradable packages
result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)

# Count the number of upgradable packages
count = len(re.findall(r'upgradable', result.stdout))

#print(f"Number of upgradable packages: {count}")


# Use the count to determine warnings or errors
if count > maxErr:
    status = "error"
    message = "more then 3 packages upgradable"
    #print(f"Error: {count} packages are upgradable. This exceeds the maximum error threshold of {maxErr}.")
elif count > maxWrn:
    status = "warning"
    message = "more then 1 package upradable"
    #print(f"Warning: {count} packages are upgradable. This exceeds the maximum warning threshold of {maxWrn}.")
else:
    status = "ok"
    message = "All packages up to date"
    #print(f"All is good. Only {count} packages are upgradable.")
print(
    json.dumps(
        {
            "version": 2,
            "status": status,
            "message": message,
            "channels":[
                {
                    "id": 10,
                    "name": "Upgradable packages",
                    "type": "integer",
                    "value": int(count),
                },
            ],
        }
    )
)
