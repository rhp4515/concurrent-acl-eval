**********************************************************************************
Scalable and Secure Concurrent Evaluation of History-based Access Control Policies
**********************************************************************************
	- Pseudo code of the algortihm is inside pseudo code folder

************
Instructions
************
 - Compile master.da from the ./src/ folder as the main config file contains
   path specified based on src folder
 - Run the below commands from the base folder
 	- cd src
 	- python -m da --message-buffer-size=$((16*1024)) master.da

******
Design
******

------------------
#1 DB SYNC LATENCY
------------------

Once the attr updates are ready to be commited into the db,

1. We add them to the attr_cache
2. Start a new timer process to wait for a randomly selected time based on min and
   max latency. The timer process waits for the specified duration and pings the
   process started it.
3. Receive the timer response and initiate the DB_WRITE_REQUEST.

This design hides the updates from other process to mimic the latency. The
current process can piggy back on the attr updates from the attr_cache.

---------------------
#2 PREVENT STARVATION
---------------------

To prevent write request starvation, we can await for all the previous read 
requests to complete. But this blocks the current thread and we could not
continue to process the COORDW_RESPONSE in this process. Therefore, we
transformed this wait condition to an event based model. This does not involve
continuous polling.

-------------------------------
#3 WAIT FOR PENDING MIGHT READS
-------------------------------

To wait for the all the pending might read to be empty, we can await for all 
depndent request to complete. This will result in a blocking state as explained 
in the previous case. Therefore, we transformed this wait condition to an event 
based model. This does not involve continuous polling. 
Therefore, we introduced a new map called res_commit_q. This map contains
eval_id as key and all its dependant_eval_ids as value.

************
Instructions
************

Compile master.da from the ./src/ folder as the main config file contains
path specified based on src folder

**********
Main Files
**********

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
	- Rule match from the policy list happen one after another in order given in
	policy-list.xml file

*************
Contributions
*************

* Hari implemented policy evaluation logic
* Arvind implemented db emulator logic
* We pair programmed the main logic and involved in healthy discussion about
  implementation design based on the pseudo code

