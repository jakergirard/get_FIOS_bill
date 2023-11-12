#!/bin/bash
#run_fios_script.sh is used to run the cron jobh
# Source your .bash_profile or .bashrc
source /home/dbelle/.script_secure.sh

# Run your Python script
/usr/bin/python3 /home/dbelle/scripts/get_FIOS_bill/getfile_FIOS.py
