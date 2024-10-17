#!/usr/bin/env python3

###
# .DESCRIPTION
#  Returns Current CPU Usage for all Cores incl. _Total
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

ps_cpu = """Clear
$cpuUsages = Get-WmiObject Win32_PerfFormattedData_PerfOS_Processor | select PSComputerName,Name,PercentProcessorTime

# Create an empty hashtable
$cpuUsageHashtable = @{}

foreach($cpu in $cpuUsages){
     $cpuUsageHashtable[$cpu.Name] = $cpu.PercentProcessorTime
}

# Output JSON
$cpuUsageHashtable | ConvertTo-Json -Depth 3
"""

r = s.run_ps(ps_cpu)
CPUUsage = r.std_out.decode("utf-8").rstrip()

cpu_json = json.loads(CPUUsage)



prtg_json = {
	"version": 2,
	"status": "ok",
	"channels": [],
	"message": "",
}

id = 10

for core, usage in cpu_json.items():
	prtg_json["channels"].append(
		{
			"id": id,
			"name": f"Core {core}",
			"type": "integer",
			"kind": "percent",
			"value": int(usage),
		}
	)
	id = id+1

print(json.dumps(prtg_json))
