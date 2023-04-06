# meraki_wanmon
Basic script created by ChatGPT which monitors all WAN interface statuses of Meraki MX devices and sends an email should a change occur using gmail email address

DISCLAIMER = script has not been fully tested and is given as is, I would advise against running in production environment before stress testing / optimisation and security hardening is first done on the script.

make sure you first update your API and Org ID within wanmon.py file and email details for gmail within alert.py section

to run this script you must run both files

python3 wanmon.py &
python3 alert.py
