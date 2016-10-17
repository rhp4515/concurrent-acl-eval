# concurrent-acl-eval

# Instructions
 - Compile master.da from the ./src/ folder as the main config file contains
   path specified based on src folder

# Main Files

- config/main-config.json
	- contains the parameters used by main process and other processes
	- contains paths to the log files

- config/db-config.xml
	- contains the data for initial state of database

- config/policy-list.xml
	- contains the rules to be evaluated

- src/master.da
	- contains main process
	- main process initiates and sets up application process, db emulater process,
	subject coordinators, resource coordinators and workers
	- number of processes are read from main-config.json file

- src/policy.py
	- contains logic for evaluating the policy

- src/constants.py
	- contains few constant declarations

# Bugs and Limitations


# Contributions
	- Hari implemented policy evaluation logic
	- Arvind implemented db emulator logic
	- We pair programmed the main logic and involved in healthy discussion about
	  implementation design based on the pseudo code