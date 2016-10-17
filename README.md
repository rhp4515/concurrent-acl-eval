**********************************************************************************
Scalable and Secure Concurrent Evaluation of History-based Access Control Policies
**********************************************************************************
	- This code base contains implementation of the algorithm described in the
	  above paper authored by Maarten Decat, Bert Lagaisse, Wouter Joosen
	- Pseudo code of the algortihm is inside pseudo code folder

************
Instructions
************
 - Compile master.da from the ./src/ folder as the main config file contains
   path specified based on src folder
 - Run the below commands from the base folder
 	- cd src
 	- python -m da master.da

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

------------------------------------
#2 WAIT FOR PREVIOUS EVALS TO COMMIT
------------------------------------

To wait for all the previous evals to commit, we can await for all the
previous requests to commit. But this blocks the current thread and we could not
continue to process the RES_COMMIT_RESPONSE in this process. Therefore, we
transformed this wait condition to an event based model. This does not involve
continuous polling.

Whenever a process receives a RES_COMMIT_RESPONSE and it has no res conflict,

1. Update the eval with PENDING_ATTR_DB_UPDATE status in eval_cache
2. Send a RES_COMMIT_DONE msg to self
3. On receiving the RES_COMMIT_DONE, sort eval_cache based on requests received
   (fairly simple with pandas dataframes) and send APP_EVALUATION_RESPONSE to
   all the process with PENDING_ATTR_DB_UPDATE status till you see a process
   with WORKER_COMPLETE status.

When you see a process with WORKER_COMPLETE status, it indicates the evaluation
is RES_COMMIT phase and you should not send response to evaluations following
that. So we break there.

-------------------------------------
#3 WAIT FOR TENTATIVE EVALS TO COMMIT
-------------------------------------

To wait for the all the tentaive evals to commit, we can await for all of them
to commit resulting in a blocking state as explained in the previous case.
Therefore, we transformed this wait condition to an event based model.
This does not involve continuous polling. However, here we need a new data
structure to track the dependent requests without affecting the main eval_cache.

Therefore, we introduced a new map called res_commit_q. This map contains
eval_id as key and all its dependant_eval_ids as value.

When a WORKER_EVALUATION_REQUEST comes and there is no subject attr conflict,

Get dependant_eval_ids for eval_id
if dependant_eval_ids is not empty
	Set res_commit_q[eval_id] = dependant_eval_ids
else:
	Send RES_COMMIT_REQ to ResCoord
	Send RES_COMMIT_REQ_DONE, curr_eval_id to self
	On receiving RES_COMMIT_REQ_DONE,
		get all the evals_dependent_on the current
		for each eval_id in evals_dependent_on:
   			remove curr_eval_id from res_commit_q[eval_id]
   			if res_commit_q[eval_id]:
   				send RES_COMMIT_REQ to ResCoord

This will ensure that, this dependent check is triggered only when any one of
the evals receives a RES_COMMIT_RESPONSE, so its dependent evals can initiate
RES_COMMIT_REQ if its dependent_eval_ids list is empty.

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

