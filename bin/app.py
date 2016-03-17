import web
import os,sys,inspect,csv
import numpy as np
import matplotlib.pyplot as plt
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from read import writeResult, readCSV
from stream import saveData
urls = ( '/', 'index' )

app = web.application(urls, globals())

render = web.template.render('templates/')

def readData(filename):
	print "Starting read"
	fi = open(filename,'rb')
	reader = csv.reader(fi)
	lst = []
	neu, pos, neg = 0,0,0
	for i in reader:
		respType = i[1]
		if respType == 'neutral': neu += 1
		elif respType == 'positive': pos += 1
		elif respType == 'negative': neg += 1
		lst.append(i)
	return lst, [pos,neg,neu]

class index():
	def GET(self):
		return render.form()

	def POST(self):
		form = web.input(search_term="Donald Trump")
		searchTerm = form.search_term
		numberTweets = form.num
		filename = searchTerm.replace(" ","")+".csv"
		#save tweets to csv file
		saveData(searchTerm, filename, numberTweets)
		#read the saved file
		arr = readCSV(filename)
		#Use Alchemy API to get sentiment and save as csv
		writeResult(arr, "out"+filename, searchTerm)
		arr, info = readData("out"+filename)
		#Save Graph
		keyword = ["Positive","Negative","Neutral"]
		plt.clf()
		ax = plt.subplot(111)
		y = np.arange(len(keyword))
		ax.bar(y[0], info[0], color='g', align='center')
		ax.bar(y[1], info[1], color='r', align='center')
		ax.bar(y[2], info[2], color='b', align='center')
		#plt.bar(y, info, align='center')
		fig = plt.gcf()
		plt.xticks(y, keyword)
		imagePath = "static/"+filename.replace(".csv",".png")
		fig.savefig(imagePath)
		return render.index(arr = arr, imagePath=imagePath)

if __name__ == "__main__":
	app.run()