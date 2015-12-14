# Milestone project for Data Incubator

The project allows the user to display the 30-day price history for a stock.  The user can input any value into the 'ticker' field, and select any particular price option.  The program then displays the data.


## index.html
There are safeguards in place to handle user error.  
The "ticker" field is text.  If the stock is not found, an error is reported to the user.
Radio buttons allow for one of four price options.


## plot.html
Plot is displayed.  The name of the company is shown.  A "back" button returns the user to the main/index page.


## app.py
This accepts the user ticker value, formats into an API string, and sends a request to Quandl.  The API key is kept hidden.  The request is returned in .json format, which is then read into pandas.  The company name is extracted as well.
The relevant columns are extracted from pandas, and a plot is calculated using bokeh.  The plot data and compnay name are fed to plot.html.


