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

def getMeTweets(temp, NUM, SEARCHTERM, sincedate,untildate):
	last_id = -1
	while len(temp) < NUM:
		print "in loop"
		count = NUM - len(temp)
		try:
			new_tweets = api.search(q=SEARCHTERM,lang="en", count=count,since=sincedate,until=untildate, max_id=str(last_id - 1))
			if not new_tweets:
				print "not found"
				break
			#print last_id
			last_id = new_tweets[-1].id
			#print last_id
			print "after api search"
			twetext = []
			#print dir(new_tweets[0])
			for item in new_tweets:
				z = re.sub(r"http\S+", "", item.text)
				lst = [z, item.created_at]
				try:
					if z not in zip(*twetext)[0]:
						twetext.append(lst)
				except Exception, e:
					twetext.append(lst)
			#twetext = [re.sub(r"http\S+", "", item.text) for item in new_tweets if re.sub(r"http\S+", "", item.text) not in twetext]
			temp.extend(twetext)
		except tweepy.TweepError as e:
			print e
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
	arr = tweepy.Cursor(api.search, q=SEARCHTERM, lang="en").items(NUM)
	print "Tweets collected"
	temp = []
	threads = []
	sttime = time.time()
	thread1 = myThread(1,temp, NUM, SEARCHTERM, "2016-03-15","2016-03-16")
	thread2 = myThread(2,temp, NUM, SEARCHTERM, "2016-03-16","2016-03-17")
	thread3 = myThread(3,temp, NUM, SEARCHTERM, "2016-03-17","2016-03-18")
	thread4 = myThread(4,temp, NUM, SEARCHTERM, "2016-03-14","2016-03-15")
	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	threads.append(thread1)
	threads.append(thread2)
	threads.append(thread3)
	threads.append(thread4)
	for t in threads:
		t.join()
	#temp = [item for item in arr]
	print "array made"
	print time.time()-sttime
	print len(temp)
	print "adding to file"
	for item in temp:
		item[0] = item[0].lower().encode('ascii', 'ignore')
		fi.writerow([item[0], item[1]])
	print "done"
	#print temp[0]
	# for item in arr:
	# 	try:
	# 		item.text = item.text.lower().encode('ascii', 'ignore')
	# 		# Remove reduntant retweets and only check English tweets
	# 		if (item.retweeted == False) and ("rt " not in item.text):
	# 			item.text = item.text.replace(HASHTAG,SEARCHTERM)
	# 			fi.writerow([item.text])
	# 		# if ((SEARCHTERM in item.text) or HASHTAG in item.text):
	# 		# item.text = item.text.replace(HASHTAG,SEARCHTERM)
	# 		# fi.writerow([item.text])
	# 			#print item.text+'\n'
	# 		# textRefined = item.text.encode('ascii', 'ignore')
	# 		# response = alchemyapi.sentiment_targeted('text', textRefined, SEARCHTERM)
	# 		# print textRefined, response["docSentiment"]["type"]
	# 		#fi.writerow([textRefined,response["docSentiment"]["type"]])
	# 	except Exception as e:
	# 		print e
	# 		continue
	# 	#decoded = json.loads(item)
	# 	# Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
	# 	#print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
	FILE.close()

access_token = "2895960169-Q8hQuNMLpybYSMgRba9g1hfS6gL5XGzzpCdt305"
access_token_secret = "CNFM2jQpqmOYcf4F8jhFa89jvGEKYdkIsVC0ZPKqrL1FY"
consumer_key = "Ucgj0ZotxSKez6fecx1FkbRQp"
consumer_secret = "ITKErjm9dGCVBIZmgL3fujzc1lpSMyztXbWfy8AsBonZEEtzxG"
alchemyapi = AlchemyAPI()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if __name__ == "__main__":
	if len(sys.argv) <= 3:
		print "usage: .py <search_term> <filename> <number_tweets>"
		sys.exit(0)
	saveData(sys.argv[1],sys.argv[2],sys.argv[3])