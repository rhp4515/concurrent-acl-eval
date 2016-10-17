# Scalable and Secure Concurrent Evaluation of History-based Access Control Policies
	- This code base contains implementation of the algorithm described in the
	  above paper authored by Maarten Decat, Bert Lagaisse, Wouter Joosen
	- Pseudo code of the algortihm is inside pseudo code folder


# Instructions
 - Compile master.da from the ./src/ folder as the main config file contains
   path specified based on src folder
 - Run the below commands from the base folder
 	- cd src
 	- python -m da master.da

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

# Bugs, Limitations, Assumption
- Assumption 1:
	- Only one rule from the policy list will evaluate to True

- Limitation 1:
	- Rule match from the policy list happen one after another in the order

- Bug 1:
	- In few rare cases attributes updates are inconsistent. Hard to debug and
	find the cause for the bug

# Contributions
	- Hari implemented policy evaluation logic
	- Arvind implemented db emulator logic
	- We pair programmed the main logic and involved in healthy discussion about
	  implementation design based on the pseudo code