# PRTG-MPP-Python-Scripts
 Python Scripts for the Paessler PRTG Multi-Platform Probe  
   
 A collection of skripts to monitor different sytems

## info

### parameters
most scripts support parameters. While in bash, these are standard like ```<script> -param value -param2 value2``` in the sensor settings you have to add the parameters seperated by a whitespace like ```value value2```.  
This will not allow you to add parameters with whitespaces!!!  

## Known Issues
- PRTG varialbes like ```%windowsuser``` do not work


## requirements
for wmi skritps https://github.com/diyan/pywinrm/


## skripts
### powershell
| name                      | purpose
|:--------------------------|:---
| win_rebootReq.py          | returns if there is a windows update reboot pending 
| win_totUserSessions.py    | returns the number of active User Sessions
| win_upd.py                | returns the windows update state (updates hidden, optional, critical and days since last updatescan)

### wmi
| name                      | purpose
|:--------------------------|:---
| wmi_services.py           | get the state of a services list
| wmi_memory.py             | returns available and free memory

### mpp-local
| name                      | purpose
|:--------------------------|:---
| apt-update-count.py       | returns number of upgradable packages

### OVL
Contains the Lookups for various sensors
| name                               | purpose
|:-----------------------------------|:---
| ts.WinCheckRebootPending.ovl       | OK if no reboot pending, ERROR if reboot pending
