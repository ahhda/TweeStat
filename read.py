import csv
import sys
from alchemyapi import AlchemyAPI
try:
	print "File name : "
	fi = open(sys.argv[1],'r')
except Exception as e:
	print e
	print "Provide file"
	sys.exit(0)

alchemyapi = AlchemyAPI()
textRefined = item.text.encode('ascii', 'ignore')
response = alchemyapi.sentiment_targeted('text', textRefined, SEARCHTERM)
reader = csv.reader(fi)
neu,pos,neg = 0,0,0
for i in reader:
	if i != '\n':
		print i
		try:
			arr = i[1]
			if arr == 'neutral':
				neu += 1
			elif arr == 'positive':
				pos +=1
			elif arr == 'negative':
				neg +=1
		except:
			continue
print "Neg ", neg
print "Pos ", pos
print "Neu ", neu