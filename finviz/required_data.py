from finviz import simple_get
from bs4 import BeautifulSoup

get_rows = 1
count=0
all_tds=[]
stock_data=[]

def get_all(start_point):
    html = simple_get(f'https://finviz.com/screener.ashx?v=111&r={start_point}')
    data = BeautifulSoup(html, 'html.parser')
    return data

def stored_data():
    get=1
    while get<62:
        get_page=get_all(get)
        for td in get_page.select('td'):
            all_tds.append(td.text)
        get+=20
    return all_tds    

def return_stock_data():
    stored = stored_data()
    while count<len(stored):
        if stored[count]==str(get_rows):
            get_details = {'ticker':stored[count+1],'company':stored[count+2], 'sector':stored[count+3], 'industry':stored[count+4], 'country':stored[count+5], 'market_cap':stored[count+6], 'price':stored[count+8], 'change':stored[count+9], 'volume':stored[count+10]}
            get_rows+=1
            stock_data.append(get_details)
        count+=1
        
    return stock_data