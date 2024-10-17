#!/usr/bin/env python3

###
# .DESCRIPTION
#  Returns Windows Update State
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


ps_winupd_hidden="""clear
$ignoreKBs = @('2267602')
$updateSession = New-Object -com "Microsoft.Update.Session"
$updates=$updateSession.CreateupdateSearcher().Search(("IsInstalled=0 and Type='Software'")).Updates

$updHid = 0
$updCri = 0
$updOpt = 0

foreach ($update in $updates){

    if ($update.IsHidden){
        $updHid += 1
    }elseif($update.AutoSelectOnWebSites){
        if($ignoreKBs -contains $update.KBArticleIDs -eq $false){
            write-verbose "no ignores"
            $updCri += 1
            $updCriText += "KB" + $update.KBArticleIDs + " "
        }else{
            $verbosMsg = "KB" + $update.KBArticleIDs + " will be ignored"
            write-verbose "$verbosMsg"
        }

    }else{
        $updOpt += 1
    }
}

# Create a hashtable with the data to output
$result = @{
    hidden    = $updHid
    critical  = $updCri
    optional  = $updOpt
    criticalText = $updCriText.Trim()
}

# Get days since last update
$KeyValue = get-hotfix | sort-object -Descending -Property InstalledOn -ErrorAction SilentlyContinue | Select-Object -First 1
$LastUpdate = $KeyValue.InstalledOn
$LastUpdateDate = Get-Date $LastUpdate -Format "yyyy-MM-dd"
$now = (Get-Date).toString("yyyy-MM-dd")
$diffSinceLastUpdate = New-TimeSpan -Start $LastUpdateDate -End $now
$diffSinceLastUpdate = $diffSinceLastUpdate.Days

$result += @{
	lastUpd 	= $diffSinceLastUpdate
}

# Convert the hashtable to JSON and output it
$result | ConvertTo-Json
"""

r = s.run_ps(ps_winupd_hidden)
result = r.std_out.decode("utf-8").rstrip()

parsed_data = json.loads(result)

# Access the values in the parsed JSON
#hidden_updates = parsed_data["hidden"]
#critical_updates = parsed_data["critical"]
#optional_updates = parsed_data["optional"]
#critical_text = parsed_data["criticalText"]
#daysLastUpdate = parsed_data["lastUpd"]

# Print or use the parsed values
#print(f"Hidden Updates: {hidden_updates}")
#print(f"Critical Updates: {critical_updates}")
#print(f"Optional Updates: {optional_updates}")
#print(f"Critical Update Text: {critical_text}")
#print(f"Days since last upd: {daysLastUpdate}")

# create and dump json
print(
	json.dumps(
		{
			"version": 2,
			"status": "ok",
			"message": parsed_data["criticalText"],
			"channels":[
				{
					"id":		10,
					"name":		"Hidden Updates",
					"type": 	"integer",
					"value":	int(parsed_data["hidden"]),
				},
				{
					"id":		11,
					"name":		"Critical Updates",
					"type":		"integer",
					"value":	int(parsed_data["critical"]),
				},
				{
					"id":		12,
					"name":		"Optional Updates",
					"type":		"integer",
					"value":	int(parsed_data["optional"]),
				},
				{
					"id":		13,
					"name":		"Days since last update",
					"type":		"integer",
					"value":	int(parsed_data["lastUpd"]),
				},
			],
		}
	)
)
