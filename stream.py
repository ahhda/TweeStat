from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
#print "hello"

access_token = "2895960169-Q8hQuNMLpybYSMgRba9g1hfS6gL5XGzzpCdt305"
access_token_secret = "CNFM2jQpqmOYcf4F8jhFa89jvGEKYdkIsVC0ZPKqrL1FY"
consumer_key = "Ucgj0ZotxSKez6fecx1FkbRQp"
consumer_secret = "ITKErjm9dGCVBIZmgL3fujzc1lpSMyztXbWfy8AsBonZEEtzxG"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#pub = api.home_timeline()

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
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
    #readHome(10)
    print "Enter Search Term\n"
    HASHTAG = raw_input()
    print "Enter File Name\n"
    FILE = raw_input()
    #stream = Stream(auth, l)
    #stream.filter(track=[HASHTAG])
    fi = open(FILE,'w')
    arr = tweepy.Cursor(api.search, q=HASHTAG).items(500)
    for item in arr:
    	print item.text
    	fi.write(item.text.encode('ascii', 'ignore')+'\n\n')
    	#decoded = json.loads(item)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
    fi.close()
    #print HASHTAG