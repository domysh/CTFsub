
# CTFsub, a submit system for A/D CTF

---

This tool was used and created for CCIT (Cyberchallenge.IT) 2020 A/D for sending flags and executing attacks during the race. The tool has been designed in such a way as to make the attacks as efficient as possible but also easy to implement and test. In fact, the program try to use all the potential of the computer through multithreading, avoids repeated attacks against teams that have closed the vulnerability through the autoblacklist that after some failed attacks (excluding closed connection) stops the attacks to that specific team (But anyway some times try ro attack again). Everything is controllable at run time through a shell where operations can be carried out quickly and effectively. The code was released publicly after the CCIT A/D. By modifying the config, the system can be configured for any CTF A / D!

# Take this and hack all teams !!!1!

---

# Some Helps
## Execution
To run your program as a deamon run ./run.sh after that it will generate the file stop.sh, execute ./stop.sh for kill the CTFsub deamon

## Logs
Watch always the log logs/CTFsub.log for monitoring system status and eventual bugs or teams that have closed the vulnerability used by your attack script.
On logs/flags.log you can also find all taked flags, and in folders you can find your log info of your program and eventualy exception generated in the script that are segnalated on global log and printed with stacktrace and message on the specific attack log

## Attacks
Program your attack using python template attack_template.py, you can run it in the CTF folder and have the same functionaliies of the program when it run in CTFsub, after you confirmed that the script is working, without changing nothing, put it in the attacks folder and it will start to get your flags!

---

## Poliba team CCIT2020

PizzaOverflow <a href="https://pizzaoverflow.it">Web Site</a> - <a href="mailto:overflowpizza@gmail.com">E-Mail</a><br>
<a href="https://domysh.com">Project by DomySh</a>

---


