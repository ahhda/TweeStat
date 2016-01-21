import web
import os,sys,inspect,csv

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from read import writeResult

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
		filename = "test.csv"
		arr, info = readData(filename)
		return render.index(arr = arr)

if __name__ == "__main__":
	app.run()