#Inset here the regex for the flag for a better selection, else insert None
FLAG_REGEX = 'flg\\{[A-Za-z0-9]{25}\\}'

#here you can create you template ip for generate address go other teams
#@Team_id will be substituded with a number in TEAM_IP_RANGE
IP_VM_TEMP = "10.10.@team_id.1"
TEAM_IP_RANGE = (1,28)
#Set here your team id for skip the attack
OUR_TEAM_ID = 5
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
def flag_submit(flag:str):
    import requests
    requests.post('https://finals.cyberchallenge.it/submit',
        data={'team_token': '461KEFD3kfscDZPx', 'flag': flag},timeout=3)
