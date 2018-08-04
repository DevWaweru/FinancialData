from django.shortcuts import render
from .required_data import stock_data
from .models import Market

# Create your views here.
def home(request):
    # Get the stock data and save it in our database
    sectors, industries, countries = [],[],[]

    # stocks = stock_data()
    # for stock in stocks:
    #     volume = stock['volume'].replace(',','')
    #     change = stock['change'].replace('%','')
    #     market = Market(ticker=stock['ticker'], company=stock['company'], sector=stock['sector'], industry=stock['industry'], country=stock['country'], price=float(stock['price']), change=float(change), volume=int(volume))
    #     market.save()
    
    portfolios = Market.get_all()

    for portfolio in portfolios:
        # Getting listed sectors
        if portfolio.sector in sectors:
            pass
        else:
            sectors.append(portfolio.sector)

        # Getting listed industries
        if portfolio.industry in industries:
            pass
        else:
            industries.append(portfolio.industry)

        # Getting listed countries
        if portfolio.country in countries:
            pass
        else:
            countries.append(portfolio.country)
    
    print(sectors)
    print(countries)
    print(industries)

    return render(request, 'index.html', {
        'portfolios':portfolios,
        'countries':countries,
        'industries':industries,
        'sectors':sectors,
    })