
# CTFsub, a submit system for A/D CTF

---

```
This is for now a secret repo created for CCIT 2020 A/D final
Here you will find more information about the project 
after the race, so now the project is concentrate for the CCIT and after this become public
and more easly managed for other races
```

---

# Some Helps
## Execution
For run your program as a deamon run ./run.sh after that it will generate the file stop.sh, execute ./stop.sh for kill the CTFsub deamon

## Logs
Watch always the log logs/CTFsub.log for monitoring system status and eventual bugs or teams that have closed the vulnerability used by your attack script.
On logs/flags.log also you can find all taked flags, and in folders you can find your log info of your program and eventualy exception generated in the script that are segnalated on global log and printed with stacktrace and message on the specific attack log

## Attacks
Program your attack using python template attack_template.py, you can run it in the CTF folder and have the same functionaliies of the program when it run in CTFsub, after you confirmed that the script is working, without changing nothing, put it in the attacks folder and it will start to get your flags!

---

# TODO list
```
1- Integrate in attack CONFIG var the possibility to set a custom TIMEOUT for the program (in process_controller dict), making more effincent the entire script but in the same time permitt to run heavy script avoiding that this have killed by CTFsub
2- Test hardly all the implementation on process_controller for be sure that all it's working correctly
3- Create a shell for run time functions and mods:
  functions of the shell{
    1- Modify auto_blacklist status (reset or block a ip on an attack)
    2- Modify config vars like the global timeout, or the thread limit etc...
    3- Manage attacks:{
        1- Create whitelist/blacklist of ip,
        2- Start or stop a specific attack script,
        3- Start a control for an alive service for an attack
        4- Run an attack at one ip or at all ip without following round time
        5- block or start rounds (bypassing of blocking timing)
      }
  }
4- Create a web endpoint for submit easly (also with a simply get request) flags form external scripts (for example with JS)

Example of endpoint:
http://<my_team_ip>:<port_of_webapi>/<string_with_flags>
or
http://<my_team_ip>:<port_of_webapi>/ POST:{'data':<string_with_flags>}
```

---

