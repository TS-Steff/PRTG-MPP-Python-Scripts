# PRTG-MPP-Python-Scripts
 Python Scripts for the Paessler PRTG Multi-Platform Probe  
   
 A collection of skripts to monitor different sytems

## info

### parameters
most scripts support parameters. While in bash, these are standard like ```<script> -param value -param2 value2``` in the sensor settings you have to add the parameters seperated by a whitespace like ```value value2```.  
This will not allow you to add parameters with whitespaces!!!


## requirements
for wmi skritps https://github.com/diyan/pywinrm/


## skripts
### wmi
| name                      | purpose
|:--------------------------|:---
| wmi_services.py           | get the state of a services list
| wmi_memory.py             | returns available and free memory
| wmi_totUserSessions.py    | returns the number of active User Sessions

### mpp-local
| name                      | purpose
|:--------------------------|:---
| apt-update-count.py       | returns number of upgradable packages