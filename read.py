import csv
import sys
from alchemyapi import AlchemyAPI

def readCSV(inFile):
	fi = open(inFile,'rb')
	reader = csv.reader(fi)
	lst = []
	for i in reader:
		lst.append(i[0])
	return lst

def writeResult(arr, outFile, search):
	fi = open(outFile,'wb')
	SEARCHTERM = search.lower()
	writer = csv.writer(fi)
	neg, pos, neu = 0,0,0
	for item in arr:
		response = alchemyapi.sentiment_targeted('text', item, SEARCHTERM)
		try:
			respType = response['docSentiment']['type']
		except:
			continue
		if respType == 'neutral': neu += 1
		elif respType == 'positive': pos += 1
		elif respType == 'negative': neg += 1
		lst = [item,respType]
		writer.writerow(lst)
	print "Negative: %s, Positive: %s, Neutral: %s " % (neg, pos, neu)
	fi.close()

alchemyapi = AlchemyAPI()

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