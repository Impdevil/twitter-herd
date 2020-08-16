import tweepy
import os
from dotenv import load_dotenv, find_dotenv
import datetime as dt
import random as rng
import time
import string
import json
load_dotenv(find_dotenv())



'''
API_KEY
API_SECRET_KEY
BEARER_TOKEN
ACCESS_TOKEN
ACCESS_T_SECRET
'''

herd_names = {"electricsheep02","electricsheep03"}
herd_accounts= list()
print(os.environ.get("Test"))

if os.environ.get("API_KEY") != None:
    print("potato")
else:
    print("something went wrong! lol")

apis = list()
auth = tweepy.OAuthHandler(os.environ.get("API_KEY"),os.environ.get("API_SECRET_KEY"))
print("grass?")
auth.set_access_token(os.environ.get("ACCESS_TOKEN"),os.environ.get("ACCESS_T_SECRET"))
api_1 = tweepy.API(auth)
apis.append(api_1)
print("grass!!!")
auth_2 = tweepy.OAuthHandler(os.environ.get("API_KEY_2"), os.environ.get("API_SECRET_KEY_2"))
auth_2.set_access_token(os.environ.get("ACCESS_TOKEN_2"),os.environ.get("ACCESS_T_SECRET_2"))
api_2 = tweepy.API(auth_2)
apis.append(api_2)



for i in range(0,1):
    try:
        api.verify_credentials()
        print("Baaah "  + str(dt.datetime.timestamp(dt.datetime.now())))
    except:
        print("baah!?!?!!?"+ str(dt.datetime.timestamp(dt.datetime.now())))




#api.update_status("Baah! at " + str(dt.datetime.timestamp(dt.datetime.now())))
#print("first tweet!")
###LE Sigh


#api.update_status("Wake up at " + str(dt.datetime.timestamp(dt.datetime.now())))

class sheepie:
    moods = []
    hours_alive = 0
    def __init__(self, api):
        self.api = api
        self.sleeping = False
        self.me = self.api.me()
        self.start = time.time()
        print (self.start)

    def mood(self, new_feel, force = False):
        if len(self.moods) != 0 and force == False:
            if new_feel in self.moods[-1] and "Baah " not in new_feel:
                #okay so we dont want it to return the same mood over and
                #over again unless its a Baah. this will also work for the ones that are similar
                # ie "scratch" and "scratching"
                new_feel = switch(rng.randint(0,100))
                new_feel = mood(new_feel) # bit of recursion ftw + smart coding ;)

        else:
            self.moods.append(new_feel)
            return new_feel
        return new_feel

    def switch(self, feelings):
        switcher = list
        switcher = ["Graze","Gather","eat","Scratch",]
        for i in range(3,110):
            if i < 10:
                switcher.append("Baah ")
            if i >= 10 and i < 20:
                switcher.append("Grazing")
            if i >= 20 and i < 40:
                switcher.append("eating")
            if i >= 40 and i < 50 :
                switcher.append( "Scratching")
            if i >= 50 and i < 60:
                switcher.append("Gather")
            if i >= 60 and i < 100:
                switcher.append("Baah ")
            if i > 99:
                switcher.append("baah")

        switcher[100]=("Sleep")
        switcher[101]=("Paralyze")
        switcher[102]=( "Wolf!!")
        switcher[103]=("Run!")
        switcher[109]=("Waking up")

        return switcher[feelings] + " " + "".join(rng.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))



    def living(self):    
        sleep_hours=0
        awake_hours = 0
        if self.sleeping == False:
            dtime = time.time()
            curr_time = dtime - self.start
            print(curr_time)
            if curr_time > 3600: #1hour
                self.hours_alive += 1
                awake_hours +=1
                print("awake for "+ str(awake_hours))
                self.start = 0
                if awake_hours > 16:
                    self.sleeping = True
                    try:
                        self.api.update_status(self.switch(100))
                    except:
                        print("dup error again")
                        self.api.update_status(self.switch(100) + "...")
                    return
            feeling = rng.randint(0,99)
            try:
                self.api.update_status(self.mood(self.switch(feeling)))
                print(str(feeling)+" " + self.switch(feeling))
            except:
                print( str(feeling)+" " + self.switch(feeling))
                print("dup error")
            wait_time = 23 + rng.randint(7,97)
            print("Waiting "+str(wait_time))
            time.sleep(wait_time)
        #What to do with this thing hmmm
        if self.sleeping:
            dtime = time.time()
            curr_time = dtime - self.start
            if curr_time > 3600: #1hour
                self.sleep_hours += 1
                self.hours_alive += 1
                self.start = 0
                print("sleeping for " + sleep_hours)
            if self.sleep_hours > 8:
                self.moods = []
                self.sleeping = False
                return
    
    def herd_call(self):
        global herd_names
        global herd_accounts
        try:
            followers = tweepy.Cursor(self.api.followers).items()
            for following in followers:
                if following.name in herd_names:
                    print("     fellowSheep")
                    herd_accounts.append(following)
                    
        except:
            print("BAAah? (where is everyone)")


    def herd_interact(self):
        pasture = tweepy.Cursor(self.api.home_timeline).items(2)

        for baah in pasture:
            print("tweet: "+baah.user.name + " "+ baah.text)
            if baah.user.name != self.me.name:
                if "Gather" in baah.text:
                    self.api.update_status( "@" + baah.user.screen_name  + " " + self.mood(self.switch(1),force = True), in_reply_to_status_id=baah.id)
                    print(self.me.name + " spoke to " + baah.user.name)
                    break
                else:
                    print("listening to self")
        #except:

        time.sleep(2)
                

herd_bots = list()
herd_bots.append(sheepie(apis[0]))
herd_bots.append(sheepie(apis[1]))
for i in range(0,len(herd_bots)):
    print("finding eachother")
    herd_bots[i].herd_call()

while True:
    for i in range(0,len(herd_bots)):

        print("switching to " + herd_bots[i].api.me().name)
        if rng.randint(0,5) == 1:
            herd_bots[i].herd_interact()
        herd_bots[i].living()


