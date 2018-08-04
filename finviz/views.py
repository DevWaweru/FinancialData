from django.shortcuts import render
from .required_data import stock_data
from .models import Market
import json
from threading import Timer
from datetime import time,date
# Drawing graphs on the chart
from .fusioncharts import FusionCharts

# Create your views here.
def home(request):
    # Get the stock data and save it in our database
    sectors, industries, countries, top_earners = [],[],[], []
    get_day = date.today()
    #Get single portfolio
    try:
        single_portfolio = Market.get_all().last()
        day = single_portfolio.date.date()
    except:
        pass
    
    if day == get_day:
        pass
    else:
        stocks = stock_data()
        for stock in stocks:
            volume = stock['volume'].replace(',','')
            change = stock['change'].replace('%','')
            market = Market(ticker=stock['ticker'], company=stock['company'], sector=stock['sector'], industry=stock['industry'], country=stock['country'], price=float(stock['price']), change=float(change), volume=int(volume))
            market.save()
    
    # Feeds the navbar
    portfolios = Market.get_today(get_day)
    for portfolio in portfolios:
        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)
    
    earners = Market.get_top_earners(get_day)
    for earner in earners:
        top_earners.append({'label':f'{earner.company}', 'value':f'{earner.change}'})

    # Data responsible for charting the graph
    data = {'chart': {'caption':'Top earners for today','subCaption':' ','numberSuffix':'%','theme':'ocean'},'data': top_earners}
    
    # converting the json data to string
    chart_data = json.dumps(data)
	# Create an object for the column2d chart using the FusionCharts class constructor
    market_graph = FusionCharts("column2d", "ex1" , "100%", "600", "chart-1", "json", chart_data)

    return render(request, 'index.html', {
        'portfolios':portfolios,
        'countries':countries,
        'output':market_graph.render(),
        'earners':earners,
    })

def country(request, country):
    # Get the stock data and save it in our database
    sectors, industries, countries, top_earners = [],[],[], []
    get_day = date.today()
    # Feeds the navbar
    portfolios = Market.get_all()
    for portfolio in portfolios:
        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)

    country_portfolios = Market.get_by_country(country, get_day)

    earners = Market.get_earners_by_country(country,get_day)
    for earner in earners:
        if earner.change>0:
            top_earners.append({'label':f'{earner.company}', 'value':f'{earner.change}'})

    # Data responsible for charting the graph
    data = {'chart': {'caption':'Top earners for today','subCaption':' ','numberSuffix':'%','theme':'ocean'},'data': top_earners}
    
    # converting the json data to string
    chart_data = json.dumps(data)
	# Create an object for the column2d chart using the FusionCharts class constructor
    market_graph = FusionCharts("column2d", "ex1" , "100%", "600", "chart-1", "json", chart_data)
    
    return render(request, 'country.html',{
        'country':country,
        'countries':countries,
        'portfolios':country_portfolios,
        'earners':earners,
        'output':market_graph.render(),
    })

# def get_data():
#     print('hello, world')

# Timer(30, get_data).start()