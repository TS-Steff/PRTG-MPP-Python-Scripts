#!/usr/bin/env python3

###
# .DESCRIPTION
#  Returns if there is a WindwosUpdate reboot required
#
# .LINKS
#  https://github.com/diyan/pywinrm/

import argparse
import winrm
import json
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

ps_reqReboot = """Clear
$rebootPending = 0

# check if reboot is pending
if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired"){
    $rebootPending = 1
}

$rebootPending
"""

r = s.run_ps(ps_reqReboot)
rebootRequired = r.std_out.decode("utf-8").rstrip()

print(
	json.dumps(
    	{
        	"version": 2,
            "status": "ok",
            "channels": [
            	{
                	"id": 10,
                    "name": "Reboot Pending",
                    "type": "integer",
                    "value": int(rebootRequired),
                },
            ],
        }
    )
)
