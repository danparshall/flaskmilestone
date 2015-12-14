from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from pandas import DataFrame,Series
import datetime as dt
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
import os


################################################################################
# secret data kept in separate file
def loadApiKey( keyFile, keyName ) :
	with open(keyFile) as f:
		fromFile = {}
		for line in f:
			line = line.split() # to skip blank lines
			if len(line)==3 :			# 
				fromFile[line[0]] = line[2]			
	f.close()
	apiKey = fromFile[keyName]
	return apiKey

################################################################################

def fetch_quandl(ticker, apiKey) :

	if not ticker.isalpha():
#		print "ticker must contain only letters, defaulting to AAPL"
#		ticker = "AAPL"
		return df=None
	else :
		ticker = ticker.upper()


	now = dt.datetime.now().date()
	then = now - dt.timedelta(days=30)
	then = "&start_date=" + then.strftime("%Y-%m-%d")
	now  = "&end_date=" + now.strftime("%Y-%m-%d")

	reqUrl = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + \
					'/data.json?api_key=' + apiKey + now + then

	r = requests.get(reqUrl)
#	r.raise_for_status()	# throws HTTPError if ticker not valid

	if r.status_code < 400 :
		dat = r.json()['dataset_data']
		df = DataFrame(dat['data'], columns=dat['column_names'] )
		df = df.set_index(pd.DatetimeIndex(df['Date']))

	else :
		print "Stock ticker not valid"
		df = None

	return df

################################################################################

def make_figure(df, priceReq, tickerText ):

	print "priceReq : ", priceReq, type(priceReq)

	p = figure(x_axis_type="datetime", width=800, height=600)
	#p.line(df.index, df['Close'], color='#000000', legend=ticker, line_width='10')


	if type(priceReq) == list :
		for req in priceReq:
			p.line(df.index, df[priceReq[req]], legend=req, line_width='3')
	else :
		p.line(df.index, df[priceReq], legend=priceReq, line_width='3')

	p.title = tickerText + " Prices"

	p.grid.grid_line_alpha=0.3
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Price'
	p.legend.orientation = "top_left"

	if 0:
		bokeh.io.output_file('templates/plotstock.html')
		bokeh.io.save(p)

	script, div = components(p)
	return script, div

################################################################################

app = Flask(__name__)

# init
app.vars = {}
keyFile = 'API_KEYS'
keyName = 'quandl'
app.vars['apiKey'] = loadApiKey( keyFile, keyName)


@app.route('/')
def main():
	return redirect('/index')

@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/plotpage', methods=['POST'])
def plotpage():
	tickStr = request.form['tickerText']
	reqList = request.form['priceCheck'] # checkboxes

	app.vars['ticker'] = tickStr.upper()
	app.vars['priceReqs'] = reqList

	df = fetch_quandl(app.vars['ticker'], app.vars['apiKey'])


	# if the stock ticker isn't valid, reload with warning message
	if not type(df) == DataFrame :
		msg = "Sorry, that ticker isn't valid. Please try again."
		return render_template('index.html', msg=msg)
	else:
		script, div = make_figure(df, app.vars['priceReqs'], app.vars['ticker'] )
		return render_template('plot.html', script=script, div=div, ticker=tickStr)


if __name__ == '__main__':
	port=int(os.environ.get("PORT",5000))

	if port==5000 :
		app.run(port=port,host='0.0.0.0')
	else :
		app.run(port=port)
