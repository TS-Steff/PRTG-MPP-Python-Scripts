#!/usr/bin/env python3

"""
    wmi_memory

    This Script has to be put into the folder /opt/paessler/share/scripts on the mpp
    Returns installed and free memory in MB received by WMI Query
    The target host has to be in a domain

    Parameters:
    host (str): host to get memory from
    domain (str): domain where the computer belongs to
    username (str): user with WMI Query permissions
    password (str): the users password

    Requirements:
    pywinrm - https://github.com/diyan/pywinrm/    
  
    Note:
    bash - use parameters as normal
    prtg - strings must be blankspace seperated, without parameter name

    Link:
    https://ts-man.ch
    https://github.com/TS-Steff

"""

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

# powershell scrypt to get total memory
ps_mem_tot = """Clear
$CmpSys = WmiObject Win32_ComputerSystem
$MB = 1048576
[int]($CmpSys.TotalPhysicalMemory / $MB) """

# powershell script to get free memory
ps_mem_free = """Clear
$OsSys = WmiObject Win32_OperatingSystem
$MB = 1023
[int]($OsSys.FreePhysicalMemory / $MB) """

# get total memory from system
r = s.run_ps(ps_mem_tot)
MemTot = r.std_out.decode("utf-8").rstrip()

# get free memory from system
r = s.run_ps(ps_mem_free)
#MemFree = r.std_out.rstrip()
MemFree = r.std_out.decode("utf-8").rstrip()

#print(MemTot)
#print(MemFree)

# create json and dump it

print(
	json.dumps(
    	{
        	"version": 2,
            "status": "ok",
            "channels": [
            	{
		    "id": 10,
                    "name": "Total Memory",
                    "type": "integer",
                    "value": int(MemTot),
                },
                {
                    "id": 11,
                    "name": "Free Memory",
                    "type": "integer",
                    "value": int(MemFree),
                },
            ],
        }
    )
)
