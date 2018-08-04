from django.shortcuts import render
from .required_data import stock_data
from .models import Market
import json
from threading import Timer
from datetime import time,date, timedelta
# Drawing graphs on the chart
from .fusioncharts import FusionCharts

# Create your views here.
def home(request):
    title = 'Home'
    # Get the stock data and save it in our database
    sectors, industries, countries, top_earners = [],[],[], []
    get_day = date.today()
    #Get single portfolio
    try:
        single_portfolio = Market.get_all().last()
        day = single_portfolio.date.date()
    except:
        day = get_day-timedelta(days=1)
    
    if day == get_day:
        pass
    else:
        stocks = stock_data()
        for stock in stocks:
            sector=stock['sector'].replace(' ','_')
            industry=stock['industry']
            country=stock['country'].replace(' ','_')
            volume = stock['volume'].replace(',','')
            change = stock['change'].replace('%','')
            market = Market(ticker=stock['ticker'], company=stock['company'], sector=sector, industry=industry, country=country, price=float(stock['price']), change=float(change), volume=int(volume))
            market.save()
    
    # Feeds the navbar
    portfolios = Market.get_today(get_day)
    for portfolio in portfolios:
        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)
        # Getting listed sectors
        if portfolio.sector in sectors:
            pass
        else:
            sectors.append(portfolio.sector)
    
    
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
        'title':title,
        'portfolios':portfolios,
        'countries':countries,
        'sectors':sectors,
        'output':market_graph.render(),
        'earners':earners,
    })

def country(request, country):
    title = f'{country}'
    # Get the stock data and save it in our database
    countries, sectors, top_earners = [],[],[]
    get_day = date.today()
    # Feeds the navbar
    portfolios = Market.get_all()
    for portfolio in portfolios:
        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)
        # Getting listed sectors
        if portfolio.sector in sectors:
            pass
        else:
            sectors.append(portfolio.sector)

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
        'title':title,
        'country':country,
        'countries':countries,
        'sectors':sectors,
        'portfolios':country_portfolios,
        'earners':earners,
        'output':market_graph.render(),
    })

def sector(request, sector):
    title = f'{sector}'
    # Get the stock data and save it in our database
    countries, sectors, top_earners = [],[],[]
    get_day = date.today()
    # Feeds the navbar
    portfolios = Market.get_all()
    for portfolio in portfolios:
        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)
        # Getting listed sectors
        if portfolio.sector in sectors:
            pass
        else:
            sectors.append(portfolio.sector)

    sector_portfolios = Market.get_by_sector(sector, get_day)

    earners = Market.get_earners_by_sector(sector,get_day)
    for earner in earners:
        if earner.change>0:
            top_earners.append({'label':f'{earner.company}', 'value':f'{earner.change}'})

    # Data responsible for charting the graph
    data = {'chart': {'caption':f'Top earners in {sector}','subCaption':' ','numberSuffix':'%','theme':'ocean'},'data': top_earners}
    
    # converting the json data to string
    chart_data = json.dumps(data)
	# Create an object for the column2d chart using the FusionCharts class constructor
    market_graph = FusionCharts("column2d", "ex1" , "100%", "600", "chart-1", "json", chart_data)
    
    return render(request, 'sector.html',{
        'title':title,
        'country':country,
        'countries':countries,
        'sectors':sectors,
        'portfolios':sector_portfolios,
        'earners':earners,
        'output':market_graph.render(),
    })

def single_company(request, company):
    title = f'{company} Data'
    countries, sectors, company_data = [],[],[]
    all_days=0
    get_day=date.today()
    # Feeds the navbar
    portfolios = Market.get_all()
    for portfolio in portfolios:
        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)
        # Getting listed sectors
        if portfolio.sector in sectors:
            pass
        else:
            sectors.append(portfolio.sector)
    
    company_portfolios = Market.get_by_ticker(company)

    # Gets data by date
    while all_days < 6:
        day = get_day - timedelta(days=all_days)
        try:
            portfolio = Market.get_by_ticker_date(company, day)
            portfolio_change = portfolio.change
        except:
            portfolio_change = 0

        if day == date.today():
            day='Today'
        elif day == date.today() - timedelta(days=1):
            day='Yesterday'

        company_data.append({'label':f'{day}', 'value':f'{portfolio_change}'})
        all_days+=1

    # Data responsible for charting the graph
    data = {'chart': {'caption':f'{company} Earnings for the last 5 days','subCaption':' ','numberSuffix':'%','theme':'ocean'},'data': company_data}
    
    # converting the json data to string
    chart_data = json.dumps(data)
	# Create an object for the column2d chart using the FusionCharts class constructor
    market_graph = FusionCharts("column2d", "ex1" , "100%", "600", "chart-1", "json", chart_data)

    return render(request, 'single_company.html',{
        'title':title,
        'company':company,
        'countries':countries,
        'sectors':sectors,
        'portfolios':company_portfolios,
        'output':market_graph.render(),
    })