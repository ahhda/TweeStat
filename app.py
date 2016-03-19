from flask import Flask, jsonify,request,render_template,send_from_directory
import numpy as np
import matplotlib.pyplot as plt
from read import writeResult, readCSV, threadCaller
from stream import saveData
import os
import csv,sys
import requests
import urllib2
import itertools
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path='/static')

tasks = [
	{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
		'done': False
	},
	{
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web', 
		'done': False
	}
]

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

def getReadings(lst):
	mylst = []
	neu, pos, neg = 0,0,0
	for i in lst:
		respType = i[1]
		if respType == 'neutral': neu += 1
		elif respType == 'positive': pos += 1
		elif respType == 'negative': neg += 1
		mylst.append(i)
	print "Total Final Negative: %s, Positive: %s, Neutral: %s " % (neg, pos, neu)
	return mylst, [pos,neg,neu]

@app.route('/api/tasks/')
def get_tasks():
	print "hahah"
	if 'name' in request.args:
		searchTerm = request.args['name']
		numberTweets = 100
		filename = searchTerm.replace(" ","")+".csv"
		arr = saveData(searchTerm, filename, numberTweets)
		print "Entering writeresult"
		alchemyResult = threadCaller(arr, "out"+filename, searchTerm)
		arr, info = getReadings(alchemyResult)
		print searchTerm
		return jsonify({'Analysis':{'Positive':info[0],'Negative':info[1],'Neutral':info[2]},'Tweets':arr})
	else:
		return jsonify({"test":tasks})

@app.route('/api/')
def index1():
	return "Helloasda"

@app.route('/option/')
def option():
	return render_template("option.html")

@app.route('/corporate/')
def corporate():
	return render_template("corporate.html")

@app.route('/corporate/amazon')
def amazon():
	pageNumber = 1
	max_number = 4
	opener = urllib2.build_opener()
	lst = []
	lst1 = []
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	for number in range(pageNumber, max_number + pageNumber):
		#temp = "http://www.amazon.com/LG-Nexus-5X-Unlocked-Smartphone/product-reviews/B0178GE4FU/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber="
		temp = "http://www.amazon.com/Samsung-Galaxy-SM-G920F-Factory-Unlocked/product-reviews/B00U8KSUIG/ref=cm_cr_dp_see_all_btm?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber="
		#temp = "http://www.amazon.com/Bold-Create-Wealth-Impact-World/product-reviews/1476709580/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber="
		url = opener.open(temp+str(number))
		soup = BeautifulSoup(url)
		Author = soup.findAll('div',id='cm_cr-review_list')
		print("")
		for a in Author:
			names = a.findAll('span','a-size-base review-text')
			for name in names:
				print("")
				print name.renderContents()
				try:
					lst1.append(unicode(name.renderContents(), errors='replace'))
				except Exception,e:
					print "=========================="
					print "probead lst1", e
					print "=========================="
					#lst1.append(str(name.renderContents()))
					continue
		# print("<------- Rating : ------->")
		for a in Author:
			names = a.findAll('span','a-icon-alt')
			for name in names:
				print("")
				print name.renderContents()
				lst.append(name.renderContents())
	newList = []
	print len(lst), len(lst1)
	print lst[0], lst1[0]
	try:
		for i in range(len(lst)):
			newList.append([lst[i], lst1[i]])
	except Exception, e:
		print e
	print newList
	return render_template("amazon.html", lst = newList)


@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		#form = web.input(search_term="Donald Trump")
		searchTerm = request.form['search_term']
		numberTweets = request.form['num']
		filename = searchTerm.replace(" ","")+".csv"
		#save tweets to csv file
		arr = saveData(searchTerm, filename, numberTweets)
		
		#Use Alchemy API to get sentiment and save as csv
		print "Entering writeresult"
		alchemyResult = threadCaller(arr, "out"+filename, searchTerm)
		#alchemyResult = writeResult(arr, "out"+filename, searchTerm)
		arr, info = getReadings(alchemyResult)
		print "after write result"
		# arr, info = readData("out"+filename)
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
		return render_template("index.html",arr = arr, imagePath=imagePath, info=info)
	else:
		return render_template("form.html")

@app.errorhandler(404)
def not_found(error):
	return jsonify({'error': 'Not found'})	

if __name__ == '__main__':
	#app.debug = True
	app.run(host='0.0.0.0',port=8000,debug=True)