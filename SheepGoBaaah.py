import tweepy
import os
from dotenv import load_dotenv, find_dotenv
import datetime as dt
import random as rng
import time
import datetime as dt
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



for api in apis:
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
    hunger= 25;
    moods = []
    hours_alive = 0
    def __init__(self, api):
        self.api = api
        self.sleeping = False
        self.me = self.api.me()
        self.start = time.time()
        self.sleep_hours=0
        self.awake_hours = 0
        self.switcher = list
        self.switcher = ["Graze","Gather","eat","Scratch",]
        for i in range(3,111):
            if i < 10:
                self.switcher.append("Baah")
            if i >= 10 and i < 30:
                self.switcher.append("Grazing")
            if i >= 30 and i < 45 :
                self.switcher.append( "Scratching")
            if i >= 50 and i < 60:
                self.switcher.append("Group up")
            if i >= 60 and i < 100:
                self.switcher.append("Baah ")
            if i > 99:
                self.switcher.append("baah")

        self.switcher[100]=("Sleep")
        self.switcher[101]=("Paralyze")
        self.switcher[102]=( "Wolf!!")
        self.switcher[103]=("Run!")
        self.switcher[104]=("Waking up")
        self.switcher[105]=("feed")
        print (self.start)


    def check_tweet_id(self, tweetid):
        logName = "SheepLogs/"+ self.me.name+".txt"
        if os.path.exists(logName):
            print(logName)
            with open(logName, "r") as file:
                for line in file.readlines():
                    if line == str(tweetid):
                        return True
                        file.close()
        print("no lines found or text file does not exist!!")
        return False

    def write_tweet_id(self,tweetid):
        logName = "SheepLogs/"+ self.me.name+".txt"
        if os.path.exists(logName):
            print("potato")
            with open (logName, "r") as readFile, open("SheepLogs/"+ self.me.name+".temp", "w") as writeFile:
                writeFile.write(str(tweetid)+"\n")
                for line in readFile:
                    writeFile.write(line)
                    
                readFile.close()
                os.remove(logName)
            os.rename("SheepLogs/"+ self.me.name+".temp", logName)


        else:
            with open(logName, "w") as file:
                file.write(str(tweetid) + "\n")


                



    def mood(self, new_feel, force = False):
        if len(self.moods) != 0 and force == False:
            if new_feel in self.moods[-1] and "Baah " not in new_feel:
                #okay so we dont want it to return the same mood over and
                #over again unless its a Baah. this will also work for the ones that are similar
                # ie "scratch" and "scratching"
                new_feel = self.switch(rng.randint(0,100))
                new_feel = self.mood(new_feel) # bit of recursion ftw + smart coding ;)
        elif self.hunger < 15:
            new_feel = self.switch(21)
        else:
            self.moods.append(new_feel)
            return new_feel
        return new_feel

    def switch(self, feelings):
        if feelings >= 10 and feelings <=20:
            self.hunger += 5
        return self.switcher[feelings] + " " + "".join(rng.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))



    def living(self):    

        if self.sleeping == False:
            dtime = time.time()
            curr_time = dtime - self.start
            print("timeAlive "+str(curr_time))
            if curr_time > 10: #1hour
                self.hours_alive += 1
                self.awake_hours += 1
                print("awake for "+ str(self.hours_alive))

                if self.awake_hours > 10:
                    self.sleeping = True
                    self.awake_hours = 0
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
                if "eat" in self.moods[-1]:
                    self.hunger = self.hunger + 15

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
            if curr_time > 10: #1hour
                self.sleep_hours += 1
                self.hours_alive += 1

                print("sleeping for " + str(self.sleep_hours)  + str(self.start))
            if self.sleep_hours > 10:
                self.moods = []
                self.sleeping = False
                self.sleep_hours = 0
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

    def feed_sheep(self):
        searchingforfood ="#f33dth3sh33p"
        if(True):
        #try:
            feedStock = tweepy.Cursor(self.api.search, q=searchingforfood, lang="en").items(5)
            print("looking for food")
            for tweet in feedStock:
                print(tweet.text)
                if self.check_tweet_id(tweet.id) !=True:
                    self.write_tweet_id(tweet.id)
                    self.api.update_status( "@" + tweet.user.screen_name  + " " + self.mood(self.switch(105),force = True), in_reply_to_status_id=tweet.id)

        else:
        #except:
            print("no feed so far")

    def herd_interact(self):
        pasture = tweepy.Cursor(self.api.home_timeline).items(2)

        for baah in pasture:
            print("tweet: "+baah.user.name + " "+ baah.text)
            if baah.user.name != self.me.name:
                if "Group up" in baah.text:
                    self.api.update_status( "@" + baah.user.screen_name  + " " + self.mood(self.switch(1),force = True), in_reply_to_status_id=baah.id)
                    print(self.me.name + " spoke to " + baah.user.name)
                    break
                else:
                    print("listening to self")

        
    
                    

                

herd_bots = list()
herd_bots.append(sheepie(apis[0]))
herd_bots.append(sheepie(apis[1]))
for i in range(0,len(herd_bots)):
    print("finding eachother")
    herd_bots[i].herd_call()
    herd_bots[i].feed_sheep()
while True:
    for i in range(0,len(herd_bots)):

        print("switching to " + herd_bots[i].api.me().name)
        if rng.randint(0,5) == 1:
            herd_bots[i].herd_interact()
        herd_bots[i].living()


