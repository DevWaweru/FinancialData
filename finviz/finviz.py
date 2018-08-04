from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Acquires data from the url by making a HTTP GET request. If the content is in 
    HTML or XML it will return the text content. If the request is invalid, the return will be None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error(f'Error when doing GET request to {url}:{str(e)}')
        return None
    
def good_response(resp):
    '''
    This will return a TRUE if the response comes in HTML
    '''
    content_type = resp.headers['Content-Type'].lower()
    return resp.status_code == 200 and content_type is not None and content_type.find('html') > -1


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)