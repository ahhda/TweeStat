from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy
import json
import csv,sys
import matplotlib.pyplot as plt
from alchemyapi import AlchemyAPI
import time
import re
import threading
import datetime
from difflib import SequenceMatcher
#pub = api.home_timeline()
class StdOutListener(StreamListener):
	#Prints received tweets to stdout.
	def on_data(self, data):
		# print(data)
		# return True
		decoded = json.loads(data)

		# Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
		print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
		#print decoded

		def on_error(self, status):
			print(status)

			def readHome(n):
				for status in tweepy.Cursor(api.home_timeline).items(n):
					print status.user.screen_name, status.text
					print "\n"

					if __name__ == '__main__':
						l = StdOutListener()

class myThread (threading.Thread):
    def __init__(self, threadID, temp, NUM, SEARCHTERM, sincedate, untildate):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.temp = temp
        self.NUM = NUM
        self.SEARCHTERM = SEARCHTERM
        self.sincedate = sincedate
        self.untildate = untildate
    def run(self):
        print "Starting " + str(self.threadID)
        getMeTweets(self.temp, self.NUM, self.SEARCHTERM, self.sincedate, self.untildate)
        print "Exiting " + str(self.threadID)

def similar(a,b):
	return SequenceMatcher(None, a, b).ratio()

def getMeTweets(temp, NUM, SEARCHTERM, sincedate,untildate):
	last_id = -1
	print "Temp length ",len(temp)
	while len(temp) < NUM:
		#print "in loop"
		count = NUM - len(temp)
		try:
			if len(temp) >= NUM:
				return
			new_tweets = api.search(q=SEARCHTERM,lang="en", count=count,since=sincedate,until=untildate, max_id=str(last_id - 1))
			if not new_tweets:
				print "not found"
				break
			#print last_id
			if len(temp) >= NUM:
				return
			print dir(new_tweets[0])
			tweetdata.append(new_tweets)
			last_id = new_tweets[-1].id
			#print last_id
			#print "after api search"
			twetext = []
			#print dir(new_tweets[0])
			prevTweet = ""
			ignoreList = [':','(',')','#','@','!','*','[',']',';','?','|','/','\\']
			for item in new_tweets:
				z = re.sub(r"http\S+", "", item.text).rstrip().encode('ascii', 'ignore')
				z = z.translate(None, ''.join(ignoreList))

				if similar(prevTweet, z) > 0.8:
					prevTweet = z
					continue
				prevTweet = z
				lst = [z, item.created_at, item.id]
				try:
					if z not in zip(*twetext)[0]:
						twetext.append(lst)
				except Exception, e:
					twetext.append(lst)
				
			#twetext = [re.sub(r"http\S+", "", item.text) for item in new_tweets if re.sub(r"http\S+", "", item.text) not in twetext]
			if len(twetext) < NUM-len(temp):
				temp.extend(twetext)
			else:
				temp.extend(twetext[:NUM-len(temp)])
			print "After extend", len(temp)
		except tweepy.TweepError as e:
			print "no tweets",e
			break

def saveData(SEARCHTERM,FILE,NUM):
	print "Entering Twitter API "
	SEARCHTERM = SEARCHTERM.lower()
	#print "Enter File Name "
	FILE = FILE
	#print "Enter number of tweets "
	NUM = int(NUM)
	#stream = Stream(auth, l)
	#stream.filter(track=[HASHTAG])
	FILE = open(FILE,'wb')
	fi = csv.writer(FILE)
	HASHTAG = SEARCHTERM.replace(" ","")
	print "Starting tweet collection"
	# arr = tweepy.Cursor(api.search, q=SEARCHTERM, lang="en").items(NUM)
	# print "Tweets collected"
	global temp
	#temp = []
	threads = []
	sttime = time.time()
	x = datetime.datetime.now()
	for i in xrange(1,5):
		datenew = str(x.year)+"-"+str(x.month)+"-"+str(x.day-i+1)
		dateold = str(x.year)+"-"+str(x.month)+"-"+str(x.day-i)
		print dateold, datenew
		t = myThread(i,temp, NUM, SEARCHTERM, dateold, datenew)
		threads.append(t)
		t.start()
	
	while (len(temp) < NUM):
		flag = False
		for i in threads:
			if i.isAlive():
				flag = True
		if flag == False:
			break
		continue

	# for t in threads:
	# 	t.join()
	#temp = [item for item in arr]
	print "array made"
	print time.time()-sttime
	print len(temp)
	print "adding to file"
	for item in temp:
		item[0] = item[0].lower().encode('ascii', 'ignore')
		fi.writerow([item[0], item[1]])
	print "done"
	FILE.close()
	return temp

access_token = "2895960169-Q8hQuNMLpybYSMgRba9g1hfS6gL5XGzzpCdt305"
access_token_secret = "CNFM2jQpqmOYcf4F8jhFa89jvGEKYdkIsVC0ZPKqrL1FY"
consumer_key = "Ucgj0ZotxSKez6fecx1FkbRQp"
consumer_secret = "ITKErjm9dGCVBIZmgL3fujzc1lpSMyztXbWfy8AsBonZEEtzxG"
#alchemyapi = AlchemyAPI("a2fa1280d81edd71204346e0df887fb6926ad33b")
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
tweetdata = []
temp = []
if __name__ == "__main__":
	if len(sys.argv) <= 3:
		print "usage: .py <search_term> <filename> <number_tweets>"
		sys.exit(0)
	saveData(sys.argv[1],sys.argv[2],sys.argv[3])