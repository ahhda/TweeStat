import csv
import sys
from alchemyapi import AlchemyAPI
import threading
def readCSV(inFile):
	fi = open(inFile,'rb')
	reader = csv.reader(fi)
	lst = []
	for i in reader:
		lst.append(i[0])
	return lst

class alchemyThread (threading.Thread):
    def __init__(self, threadID, apiKey, arr, search, resultsArray):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.apiKey = apiKey
        self.arr = arr
        self.search = search
        self.resultsArray = resultsArray
    def run(self):
        print "Starting " + str(self.threadID)
        analyzeTweets(self.apiKey, self.arr, self.search, self.resultsArray)
        print "Exiting " + str(self.threadID)

def analyzeTweets(apiKey, arr, search, resultsArray):
	alchemyapi = AlchemyAPI(apiKey)
	SEARCHTERM = search.lower()
	neg, pos, neu = 0,0,0

	for item in arr:
		#print item
		response = alchemyapi.sentiment_targeted('text', item[0], SEARCHTERM)
		print "maine response",response

		try:
			respType = response['docSentiment']['type']
			#print "Response ",respType
		except Exception, e:
			#print e
			continue
		if respType == 'neutral': neu += 1
		elif respType == 'positive': pos += 1
		elif respType == 'negative': neg += 1
		lst = [item[0],respType, item[1],item[2]]
		resultsArray.append(lst)
	print "Tried ",len(arr), " got ", (neg+pos+neu)
	print "Negative: %s, Positive: %s, Neutral: %s " % (neg, pos, neu)

def threadCaller(arr, outFile, search):
	if len(arr) == 0:
		return []
	resultsArray = []
	keys = ["ae38cefaec63a572c9c29594a2642c5286d668ff","89e395ea07490a40a55ccf241612724f80827956",
	"f7e81de9b04fcb1eadc9469800a86a15bffd8ec3","d3547d0e12ac5425b57cf1d2e05280525224a109","6d03602e012eca8b7ab3ac92e37327950b1caa78"]
	threads = []
	try:
		arrPart = [arr[i:i+len(keys)] for i in range(0, len(arr), len(arr)/len(keys))]
	except Exception, e:
		arrPart = [arr]
	for count, array in enumerate(arrPart):
		t = alchemyThread(count, keys[count%len(keys)], arrPart[count], search, resultsArray)
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	fi = open(outFile,'wb')
	writer = csv.writer(fi)
	for item in resultsArray:
		writer.writerow(item)
	fi.close()
	return resultsArray

def writeResult(arr, outFile, search):
	alchemyapi = AlchemyAPI(apiKey)
	#alchemyapi = AlchemyAPI("89e395ea07490a40a55ccf241612724f80827956")
	#alchemyapi = AlchemyAPI("f7e81de9b04fcb1eadc9469800a86a15bffd8ec3")
	#alchemyapi = AlchemyAPI("d3547d0e12ac5425b57cf1d2e05280525224a109")
	#alchemyapi = AlchemyAPI("6d03602e012eca8b7ab3ac92e37327950b1caa78")
	#print "In write ",len(arr)
	fi = open(outFile,'wb')
	SEARCHTERM = search.lower()
	writer = csv.writer(fi)
	neg, pos, neu = 0,0,0
	results = []
	print "Starting AlchemyAPI"
	for item in zip(*arr)[0]:
		#print item
		response = alchemyapi.sentiment_targeted('text', item, SEARCHTERM)
		#print "maine response",response
		try:
			respType = response['docSentiment']['type']
			#print "Response ",respType
		except Exception, e:
			#print e
			continue
		if respType == 'neutral': neu += 1
		elif respType == 'positive': pos += 1
		elif respType == 'negative': neg += 1
		lst = [item,respType]
		writer.writerow(lst)
		results.append(lst)
	print "Negative: %s, Positive: %s, Neutral: %s " % (neg, pos, neu)
	fi.close()
	print "AlchemyAPI Complete"
	return results

#alchemyapi = AlchemyAPI("a2fa1280d81edd71204346e0df887fb6926ad33b")

if __name__ == "__main__":
	if len(sys.argv) <= 3:
		print "usage: .py <readfilename> <writefilename> <search term>"
		sys.exit(0)
	#print sys.argv[2]
	inFile = sys.argv[1]
	outFile = sys.argv[2]
	SEARCHTERM = sys.argv[3]
	arr = readCSV(inFile)
	writeResult(arr, outFile, SEARCHTERM)