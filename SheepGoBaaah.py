import tweepy
import os
from dotenv import load_dotenv, find_dotenv
import datetime as dt
import random as rng
import time
import datetime as dt
import calendar as Cal
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

    hours_alive = 0


    RNGMood = {
        "hungry" : 20,
        "interaction" : 20,
        "playful":0
    }



    def __init__(self, api):
        self.api = api
        self.sleeping = False
        self.me = self.api.me()
        self.start = time.time()
        self.moods = []
        self.moods.append("awake",)
        self.switcher = list
        self.switcher = ["Graze","Gather","eat","Scratch",]
        self.wait_timer=0
        self.wait_start = [0,]
        self.wait_time = 0
        

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
        self.switcher[105]=("feeding XD")
        print (self.start)

    def check_tweet_id(self, tweetid):
        logName = "SheepLogs/"+ self.me.name+".txt"
        if os.path.exists(logName):
            with open(logName, "r") as file:
                for line in file.readlines():
                    if  str(tweetid) in line:
                        file.close()
                        return True
                file.close()
        print("no lines found or text file does not exist!!")
        
        return False
    def write_tweet_id(self,tweetid):
        logName = "SheepLogs/"+ self.me.name+".txt"
        if os.path.exists(logName):

            with open (logName, "r") as readFile, open("SheepLogs/"+ self.me.name+".temp", "w") as writeFile:
                writeFile.write(str(tweetid)+"\n")
                for line in readFile:
                    writeFile.write(line)
                print("writing tweet")    
                readFile.close()
                os.remove(logName)
            os.rename("SheepLogs/"+ self.me.name+".temp", logName)


        else:
            with open(logName, "w") as file:
                file.write(str(tweetid) + "\n")

    def mood(self, new_feel, force = False):
        if len(self.moods) != 0 and force == False:
            if new_feel in self.moods[-1] or "Baah " in new_feel:
                #okay so we dont want it to return the same mood over and
                #over again unless its a Baah. this will also work for the ones that are similar
                # ie "scratch" and "scratching"
                new_feel = self.switch(rng.randint(0,100))
                new_feel = self.mood(new_feel) # bit of recursion ftw + smart coding ;)
        elif self.hunger < 15:
            new_feel = self.switch(31)
        else:
            self.moods.append(new_feel)
            return new_feel
        return new_feel

    def switch(self, feelings):
        if feelings >= 30 and feelings < 45 :
            self.hunger += 5
        return self.switcher[feelings] + " " + "".join(rng.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))


######## AI systems
    
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
        print("looking for food")
        #if(True):
        try:
            feedStock = tweepy.Cursor(self.api.search, q=searchingforfood, lang="en").items(5)

            for tweet in feedStock:
                print(tweet.user.screen_name + " " + tweet.text)
                if self.check_tweet_id(tweet.id) != True:
                    self.write_tweet_id(tweet.id)
                    self.api.update_status( "@" + tweet.user.screen_name  + " " + self.mood(self.switch(105),force = True), in_reply_to_status_id=tweet.id)
                    self.hunger -= rng.randint(20,80)
                    self.RNGMood["interaction"] += 10
                    return
        
            print("here we goooo")
            searchingforfood= "#feedthesheep"
            feedStock = tweepy.Cursor(self.api.search, q=searchingforfood, lang="en").items(10)

            tweet = feedStock(rng.randint(0,feedStock.num_tweets))
            print(tweet.text)
            if self.check_tweet_id(tweet.id) !=True:
                self.write_tweet_id(tweet.id)
                self.api.update_status( "@" + tweet.user.screen_name  + " " + self.mood(self.switch(105),force = True), in_reply_to_status_id=tweet.id)
                self.hunger -= 40
                self.RNGMood["interaction"] += 20
                return
        except:
            print("no feed so far")

    def herd_interact(self):
        print("needing interaction")
        pasture = tweepy.Cursor(self.api.home_timeline).items(10)
        for baah in pasture:
            if baah.user.name != self.me.name and self.check_tweet_id(baah.id) != True:
                print("tweet: "+baah.user.name + " "+ baah.text)
                if "Group up" in baah.text:
                    self.write_tweet_id(baah.id)
                    
                    self.api.update_status( "@" + baah.user.screen_name  + " " + self.mood(self.switch(1),force = True), in_reply_to_status_id=baah.id)
                    print(self.me.name + " spoke to " + baah.user.name)
                    self.RNGMood["interaction"] -= 10
                    break
                else:
                    print("listening to self")
        if self.RNGMood["interaction"] > 40:
            self.api.update_status(self.mood(self.switch(61)))

    def is_awake_action(self, currTime):    
        feeling = rng.randint(0,99)
        try:
                self.api.update_status(self.mood(self.switch(feeling)))
                print(str(feeling)+" " + self.switch(feeling))
                if "eat" in self.moods[-1]:
                    self.hunger = self.hunger -15

        except:
                print( str(feeling)+" " + self.switch(feeling))
                print("dup error")


    ###
    #
    ###
    def ai_algo(self):

        dtime = time.time()
        curr_time = dtime - self.start
        #print("time alive " + str(curr_time))
        hours = dt.datetime.now().hour;mins= dt.datetime.now().minute
        if hours > 7 and hours < 23:            #check if sheep should be asleep next run through
            self.sleeping = False
        else: 
            print("going to sleep now")
            self.sleeping = True


        if self.sleeping != True:
            self.wait_timer = dtime - self.wait_start[0]
            
            if self.wait_timer > self.wait_time:
                print(self.api.me().name +" is awake!!")          
                self.RNGMood["hungry"] = self.RNGMood["hungry"] + self.hunger 
                totalrange = 0
                print("Hunger: "+str(self.hunger))
                print("Hungry level : " + str(self.RNGMood["hungry"]))
                print("interaction: " + str(self.RNGMood["interaction"]))

                for i in self.RNGMood.values():
                    totalrange += i
                print("mood range: "+ str(totalrange))
                if totalrange < 1:
                    x = rng.randint(0,1)
                    if x == 1:
                        self.is_awake_action(curr_time)
                    if x == 0:
                        self.herd_interact()
                else:
                    moodint = rng.randint(0, int(totalrange))
                    print("mood choice: " + str(moodint))
                    if  moodint > self.RNGMood["interaction"] and moodint <= self.RNGMood["interaction"] + self.RNGMood["hungry"]:
                        self.feed_sheep()
                    elif moodint < self.RNGMood["interaction"]:
                        x = rng.randint(0,self.RNGMood["interaction"])
                        if x < self.RNGMood["interaction"]/4:
                            self.is_awake_action(curr_time)
                        if x > self.RNGMood["interaction"]/4:
                            self.herd_interact()
                
                
                self.wait_timer = 0
                self.wait_start = [time.time(),]
                self.wait_time = 50 + rng.randint(7,123)
                self.hunger = self.hunger + rng.randint(-5, 5)
                if self.RNGMood["hungry"] < 500:
                    self.RNGMood["hungry"] += int(rng.randint(0, self.wait_time)/4)
                    self.RNGMood["hungry"] = self.RNGMood["hungry"] + self.hunger 
                self.RNGMood["interaction"] += int(rng.randint(0,self.wait_time)/5)

                print("Waiting: "+str(self.wait_time) + " seconds")
            



herd_bots = list()
herd_bots.append(sheepie(apis[0]))
herd_bots.append(sheepie(apis[1]))
for i in range(0,len(herd_bots)):
    print("finding eachother")
    herd_bots[i].herd_call()
while True:
    for i in range(0,len(herd_bots)):

        #print("switching to " + herd_bots[i].api.me().name)
        herd_bots[i].ai_algo()
 

