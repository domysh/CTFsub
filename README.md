# CTFsub, a submit system for A/D CTF

---

This tool was used and created for CCIT (Cyberchallenge.IT) 2020 A/D for sending flags and executing attacks during the race. The tool has been designed in such a way as to make the attacks as efficient as possible but also easy to implement and test. In fact, the program try to use all the potential of the computer through multithreading, avoids repeated attacks against teams that have closed the vulnerability through the autoblacklist that after some failed attacks (excluding closed connection) stops the attacks to that specific team (But anyway some times try ro attack again). Everything is controllable at run time through a shell where operations can be carried out quickly and effectively. The code was released publicly after the CCIT A/D. By modifying the config, the system can be configured for any CTF A / D!

---

# How to Use

## Install

Install all requirements with pip for make runnable this program with

```bash
pip install -r requirements.txt
```

## Configuration

First of all we need to change some configurations on config.py file.

#### FLAG_REGEX

If not setted to None, this paramether will be used to filter the result of all the attacks submitted using the regex for take the flag, setting this we can return from the attack also an entire webpage, and in this case CTFsub will search the flags and submit it.

### Targets IP Configuration

#### USE_IP_TEMPLATE

With this we can choose if select all teams IP with a particular template of only with a list of IPs

### IP Template

If  USE_IP_TEMPLATE is setted to true, we can set IP_VM_TEMP that is the template to use for generate the IPs of terget machines: We can write the ip and instead of a decimal number, we can put @team_id.

Example: "10.10.@team_id.10"

CTFsub will substitute @team_id with a team ip range setted with TEAM_IP_RANGE. With this we can set a tuple with a range of number to set to team_id (will be taked all number including extremes), and also we can skip our team setting OUR_TEAM_ID to our team id.

### Ip list

We can set TEAMS_IPS to a list of IP to attack when have strage IPs

#### TICK_TIME

CTFsub try to avoid useless attacks, so setting the TICK time, if attacks are faster than this time, CTFsub will wait for next round and retry attacks following the regenetarion of flags in targets machines (The time is in seconds)

#### SEC_SECONDS

Before starting the round, if SEC_SECONDS is > 0, CTFsub will send a message to global logs every second before starting next round attack for avoid to make strange changes to attacks file during the attacks execution

#### TIMEOUT_ATTACK

This is the time limit for a single attack to a machine. If the execution of an attack go over this time, the attacker process will be killed (But we can also choose a custom time for every attack, this is a global and general time limit)

#### THREADING_LIMIT

CTFsub create a thread for every attack to do, this variable limit the creation of threads, so you can choose this according to the platform specifics

#### Flag submit method

```python
def flag_submit(flag:bytes):
    #Do some stuff for submit the flag to gameserver
```

this method will be used for submit flags to the game server. Flags will be saved in a database and repeted flags will be not submited. Also if this function faise an exception this will be catched and segnataled in CTFsub logs

### Auto Blacklist System

There is an autoesclusion systrem that CTFsub can use to avoid to attack machines that have closed vulnerabilities. We can enable this automatic system setting AUTO_BLACKLIST_ON to true. This system will count the number of times when the attack failed for a closed vulnerability (not for a closed connection!).
When for TIMES_TO_BLACKLIST consecutive timess the attack fails because the vulnerability is closed, the attack for that specific team ip will be putted in a blacklist. But, for avoid to lost some flags because of for example the team have resetted the service and haven't closed the vulnerability yet, every TIME_TO_WAIT_IN_BLACKLIST rounds CTFsub will retry to attack the team. If the attack is completed successfully, CTFsub will remove this IP attack from the auto blacklist.

## How to Run

We can execute ./CTFsub python script, this will spawn a shell, and we will use only this shell for do everything. If CTFsub is not started, running the shell we will able to choose if run CTFsub. Once runned CTFsub, this will be a totaly indipendent program, for this you can close the shell and CTFsub will continue to run. Running again the CTFsub shell, this will be attached to the running CTFsub service.

## how_attack.py

This file is a template of a python script for create an attack to give to CTFsub that will run this for every team. Using CTFsub attack template we have some special functionalities, and also we can set custom settings for this attack

#### Attack Template Configs

PORT: If the target service have a TCP port open. we can set this PORT as a global variable. Before the starting of the attack, CTFsub will check if the connection is open, if  the connection isn't open the attack will be skipped for a connection error

TIMEOUT: If the global timeout is too much or too less for this attack, we can set this variable for have a custom TIMEOUT for this kind of attacks

We can set also a static IP filtering for every kind of attack. (You can set only one of this filter, if are setted all this 2 ip filter, CTFsub will ignore ip filters)

BLACKLIST: list of Ip to exclude for this kind of attack

WHITELIST: list of IP to attack (Others IP will be not attacked)

#### Attack template run functionalities

```python
def run(ip,g_var):
    return "Text with the flag"
    #return ["Array","With","Flags"]
```

CTFsub will start the attack running run function. Here we can set the main program to run for make an attack. We have as paramether from CTFsub the ip to attack (as string value), so we have to integrate it with our code, and also we have a particular paramether called g_var that will be explained later. From the run function we return a list of flags of a string with a flag that will be elaborated according to the configs and submitted using the method gived in the config.

#### g_var functionalities

g_var give as a method for save an information that are usefull to save for an attack during the rounds. G_var is a python dictionary that will be saved in a json file and also loaded from a json file for every execution of the attack. The information saved in this dictionary are different for every attack and for every ip targeted

For set a g_var variable we can use g_var_set function

```python
g_var_set(g_var_object,'dict variable name',first_value)
```

### Test a attack template

For test an attack template, we can put the python script in the root folder of the CTFsub project and run it as a common python script, using as a test ip TEST_IP_TARGET that will be used for the test. During the test will be generate a temp json file that simulate the g_var functionalities. TEST_IP_TARGET will be passed to run function that will run the attack. The results of run function will be printed but the flags will be not submitted or filtered. This will happen when the script will be integrated with CTFsub.

## Run an attack

For start a attack script you need only to move the script in the attacks folder generated form CTFsub. At the start of a new round the attack will start.

You can change the python file script of the attack, changes will be instantly ready.

### Monitoring, Logging and debugging

CTFsub during the execution create a log folder.

Here you can find some data file as json file and database. CTFsub.log is the global log that we can view also from the shell. Here there are the informations of the state of the CTFsub service. CTFsub also will create a subfolder in the logs folder for every attack in attacks folder. in this folder there is a log file for every team attacked containing the stdin and the stderr produced during the execution of the attack script for that team

All fails and success and skip of the attacks for every team will be segnalated in the global log.ù

## CTFsub shell

Running ./CTFsub we can run a shell that have some functionalities for edit the behavior of CTFsub during the execution: CTFsub will never be killed during the race!

Now I will explain some function of CTFsub shell, using TAB in CTFsub you will have some hints

### Process command

```bash
process @list
```

give a list of attacks gived to CTFsub

```bash
process attack_name <function>
```

writing the attack name (The attack name is the name of the python attack template without .py extension) we have a lot of functionalities for see the attack status and edit the attck behavior.

#### g_var

with this function we can set/get/remove a g_var for a specific information saved for a specific ip var, the changes are avaiable during the execution

#### enable

With this you can enable or disable an attack 

#### filter

with this command you can set a static filter to set what team attack and what team not attack setting WHITELIST and BLACKLIST (This setting will override default setting setted in the attack template)

#### status

See the status of the attack process

#### timeout

Set the a custom timeout for the attack (This setting will override default setting setted in the attack template)

#### autoblacklist

Here we can see the status of the autoblacklist for a specific ip attacked and also force to exit from the autoblacklist or instead force to enter in the autoblacklist

The autoblacklist is totaly different from static blacklist.

#### alive-ctrl

with this we can see/edit/disable the control for verify if the targeted TCP service is enabled or not (This setting will override default setting setted in the attack template)

### Config command

With this command we can change the values setted during the execution of some variables in config.py and see also the actual values

### Log command

With the log command we can see and monitoring the global log file (the equivalent of ""tail -f logs/CTFsub.log")

### ShellRequest command

shellreq is an importanto command that enable to change the status of the round and wait times

#### shellreq break-wait-time

With this command, next time and only for one time that CTFsub have to wait the next round, CTFsub will bypass the wait time and start attacks immediatly!

#### shellreq stop-attacks

With this command, all attacks that are in execution will be blocked and others attacks will be immediatly skipped.

#### shellreq force-remove-req

Shell request communicate with CTFsub with a file. If there are problems with a shell request that block the execution of CTFsub use this command for clear the requests

### Stop/Restart command

If you need to stop CTFsub deamon or restart it, you can use these command for do that

## Clear CTFsub project

Once finished the race, if you want keep CTFsub ready for next A/D CTF run (In the normal shell)

```bash
./CTFsub clear
```

this will clear all generate files, logs and attacks. So the project will return back to the inital state ready for another CTF

---

<a href="https://domysh.com">Project by DomySh</a>

---
