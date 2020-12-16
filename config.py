#Inset here the regex for the flag for a better selection, else insert None
FLAG_REGEX = None

#Teams IPs
USE_IP_TEMPLATE = True
#here you can create you template ip for generate address go other teams
#@Team_id will be substituded with a number in TEAM_IP_RANGE
IP_VM_TEMP = "10.10.@team_id.1"
TEAM_IP_RANGE = (1,10)
#Set here your team id for skip the attack
OUR_TEAM_ID = 5
#If you don't use IP TEMPLATE, you can create you custom array of ip
#What is needed is just a list of strings containing the ips of dns,
#These ips will be directly passed into ip paramether in attacks
#You can use also cycles and other functions for create this array
#Remember to skip your team'ip in the list :D
TEAMS_IPS = ["10.10.1.1","10.132.34.65"]

#Set how much time wait from a round to another
TICK_TIME = 1.5 * 60
#Final seconds to wait with a segnalation on Global log
SEC_SECONDS = 3

#Max time for an attack (If not specified on attack config)
TIMEOUT_ATTACK = 40

#Set how many thread activate for the attack
THREADING_LIMIT = 7

#Manage Autoblacklist settings
AUTO_BLACKLIST_ON = True
TIMES_TO_BLACKLIST = 4
TIME_TO_WAIT_IN_BLACKLIST = 6

#This function will be used for submit recived flags so you can adapt this for your A/D gameserver
def flag_submit(flag:bytes):
    import requests # Very usefull library :D
