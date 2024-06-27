#!/usr/bin/env python3

###
# .DESCRIPTION
#  Returns installed memory and free memory in MB
#
# .LINKS
#  https://github.com/diyan/pywinrm/

import winrm
import json
import argparse
import sys

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "host", help="Win host to check", default="noHost"
)
argparser.add_argument(
    "--domain", help="Domain the host belongs to", required=False, default="noDomain"
)
argparser.add_argument(
    "--user", help="User with admin priviledges", required=False, default="noUser"
)
argparser.add_argument(
    "--password", help="The users password", required=False, default="noPassword"
)

# is a terminal?
if sys.stdin.isatty():
    args = argparser.parse_args()
    host = args.host
    domain = args.domain
    user = args.user
    password = args.password
else:
    (host, domain, user, password) = sys.stdin.readline().split()


s = winrm.Session(host, auth=('{}@{}'.format(user,domain), password), transport='ntlm')

# powershell scrypt to get total memory
ps_cnt_users = """Clear
$result = (((quser) -replace '^>', '') -replace '\s{2,}', ',').Trim() | ForEach-Object {
    if ($_.Split(',').Count -eq 5) {
        Write-Output ($_ -replace '(^[^,]+)', '$1,')
    } else {
        Write-Output $_
    }
} | ConvertFrom-Csv

#$result
$result.Count 
"""

r = s.run_ps(ps_cnt_users)
totUsers = r.std_out.decode("utf-8").rstrip()


if not totUsers:
	totUsers = 0

totUsers = int(totUsers)

#print(totUsers)


# create json and dump it

print(
	json.dumps(
    	{
        	"version": 2,
            "status": "ok",
            "channels": [
            	{
                	"id": 10,
                    "name": "Total user sessions active",
                    "type": "integer",
                    "value": totUsers,
                },
            ],
        }
    )
)
