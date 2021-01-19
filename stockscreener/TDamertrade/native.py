import time
import urllib
import requests
from splinter import Browser
from config import password, account_number, client_id

# define the location of the Chrome Driver - CHANGE THIS!!!!!
executable_path = {'executable_path': r'C:\Users\Alex\Desktop\chromedriver_win32\chromedriver'}

# Create a new instance of the browser, make sure we can see it (Headless = False)
browser = Browser('chrome', **executable_path, headless=False)

# define the components to build a URL
method = 'GET'
url = 'https://auth.tdameritrade.com/auth?'
client_code = client_id + '@AMER.OAUTHAP'
payload = {'response_type':'code', 'redirect_uri':'http://localhost/test', 'client_id':client_code}