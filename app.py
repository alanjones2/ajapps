from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
import feedparser as fp

app = Flask(__name__)


# Define the root route

@app.route('/')
def index():
    return "Try '/yfin'"
    
#############################
@app.route('/yfin/')
def fin():
    return render_template('yfinance.html')

@app.route('/yfin/callback/<endpoint>')
def cb(endpoint):   
    if endpoint == "getStock":
        return gm(request.args.get('data'),request.args.get('period'),request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph
def gm(stock,period, interval):
    st = yf.Ticker(stock)
  
    # Create a line graph
    df = st.history(period=(period), interval=interval)
    df=df.reset_index()
    df.columns = ['Date-Time']+list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
        hover_data=("Open","Close","Volume"), 
        range_y=(min,max), template="seaborn" )

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

#####################################

@app.route('/weather/')
def weatherindex():
    return render_template('weatherindex.html', weatherData = getWeather("5128581"))

@app.route('/fetchweather/')
def fetchweather():
    return json.dumps(getWeather(request.args.get('city')))
    #return app.response_class(getWeather(request.args.get('city')), content_type='application/json')

def getWeather(city):

    url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{city}"
    w = fp.parse(url)

    allData = {'feed':w.feed,
               'forecast':w.entries}
    return  allData

###################################