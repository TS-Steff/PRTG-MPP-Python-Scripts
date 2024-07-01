#!/usr/bin/env python3

"""
    wmi_services

    This Script has to be put into the folder /opt/paessler/share/scripts on the mpp
    Returns the state of the given services
    The target host has to be in a domain

    Parameters:
    host (str): host to get memory from
    domain (str): domain where the computer belongs to
    username (str): user with WMI Query permissions
    password (str): the users password
    services (str): a comma sperated list of services names (not display name)

    Requirements:
    pywinrm - https://github.com/diyan/pywinrm/    
  
    Note:
    bash - use parameters as normal
    prtg - strings must be blankspace seperated, without parameter name
    services for example TSGateway,TermService

    Link:
    https://ts-man.ch
    https://github.com/TS-Steff

"""

import winrm
import json
import argparse
import sys

services = ['TSGateway','TermService']

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
argparser.add_argument (
     "--services", help="List of services to check", required=False, default="noSvc"
)


# is a terminal?
if sys.stdin.isatty():
    args = argparser.parse_args()
    host = args.host
    domain = args.domain
    user = args.user
    password = args.password
    services = args.services
else:
    (host, domain, user, password, services) = sys.stdin.readline().split()


s = winrm.Session(host, auth=('{}@{}'.format(user,domain), password), transport='ntlm')

prtg_json = {
	"version": 2,
	"status": "ok",
	"channels": [],
	"message": "",
}

services = services.split(",")

query = " OR ".join([f"Name = '{svc}'" for svc in services])
#print (query)
#exit()

ps_test = """Clear
$query = "SELECT * FROM Win32_Service WHERE """ + query + """ "
$result = Get-WmiObject -Query $query

if($result.Count -eq 0){
    write-host "no service found"
    exit(1)
}else{
    $result | Select-Object Name, Status, Started | ConvertTo-Json
}

"""

r = s.run_ps(ps_test)
#strip the output
rstring = r.std_out.decode("utf-8").rstrip()
#print(rstring)

#convert to json
rjson = json.loads(rstring)

id = 10
for entry in rjson:
	prtg_json["channels"].append(
		{
			"id" : id,
			"name" : entry["Name"],
			"type" : "lookup",
			"value" : 1 if entry["Started"] == True else 0,
			"lookup_name": "prtg.standardlookups.boolean.statetrueok",
		}
	)
	id = id+1


# Format the result as JSON and print it to stdout.
print(json.dumps(prtg_json))
exit()


for svc in services:
	print(svc)


# INFO #
ps_mem_tot = """Clear
$CmpSys = WmiObject Win32_ComputerSystem
$MB = 1048576
[int]($CmpSys.TotalPhysicalMemory / $MB) """

r = s.run_ps(ps_mem_tot)
MemTot = r.std_out.decode("utf-8").rstrip()
