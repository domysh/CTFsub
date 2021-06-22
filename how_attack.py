#This is a template for attack file in CTFsub
#Use this to learn how build a CTFsub compatible attack
#and learn how to do a test doing a test attack
from utils.classes import *

#This is the address that the program use while testing
TEST_IP_TARGET = "10.10.1.1" #DON'T USE THIS IN run FUNCTION!

#CTFsub configs
#This settings doesn't work while running as test

#Following variables are READED from CTFsub
#These variables are optional, you can remove variables
#you don't Use, Thay will take the default value

PORT = None, #Insert the number of the port for see 
            #if the service is on before start the attack
                
TIMEOUT = None #Every instace of the attack have a timeout setted in configs
            #Set here a custom timeout for this process
            #None = Use Global Timeout

#Filter option (Use only one of these vars)
#If you define all this 2 variables, CTFsub will ignore it

#BLACKLIST = ['127.0.0.1'] # List of ip to skip
#WHITELIST = ['127.0.0.1'] # Only this list of IP will be attacked


#Set a custom flag regex for this attack
#You can use the global configuration not defining this variable
#Instead set FLAG_REGEX
#FLAG_REGEX = None # This will deactivate the regex filter for this attack... you must return just filtered flags
#FLAG_REGEX = "flg\\{[A-Za-z]{10}\\}" # set a different regex to use for this attack 

# Special Exceptions to use
# 1. raise AttackFailed() -> say to CTFsub that the vuln is closed
# 2. raise AttackRequestRefused() -> say to CTFsub that the service is not responding
# 3. every other Error will be logged and CTFsub take it as a Failed Attack
# Write here the "main" function of the attack
def run(ip,g_var):
    # ip = use this variable to set the ip to attack... CTFsub will change it for every team
    # g_var = this dict don't change for attacks with the same type of attack and IP
            #It is saved in a json file by CTFsub, only with a clear operation 
            #The Values are resetted, you can change these values with the CTFsub shell

    #Create a variable in g_var with an initial value
    #for every variable you use in g_var call this function first
    g_var_set(g_var,'count',0)
    
    #print information (Redirected to log)
    print(f"Success! Test g_var status: {g_var['count']}")

    #g_var use example
    g_var['count'] +=1
    
    #Return a flag or an array of flags (types accepted str,bytes,list)
    #If in config is setted a FLAG_REGEX, CTFsub will automatically filter this/these string/s
    return ['flag1','flag2']

#For test this program, put this program in CTFsub 
#directory (not the attack directory) and run it with python3
#When you put this script in attack folder, CTFsub will automaticaly run this.
if __name__ == '__main__': run_test_case(run,TEST_IP_TARGET)
