# PRTG-MPP-Python-Scripts
 Python Scripts for the Paessler PRTG Multi-Platform Probe  
   
 A collection of skripts to monitor different sytems

## info

### parameters
most scripts support parameters. While in bash, these are standard like ```<script> -param value -param2 value2``` in the sensor settings you have to add the parameters seperated by a whitespace like ```value value2```.  
This will not allow you to add parameters with whitespaces!!!

## skripts
### wmi_services.py
This scipts gets a list of windows services

#### requirements
https://github.com/diyan/pywinrm/

#### paramters
| parameters | note
|:-----------|:---
| host |
| domain |
| username |
| password |
| services | commasperated ex. TSGateway,TermService