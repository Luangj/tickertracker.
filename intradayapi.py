import requests

url = 'https://www.alphavantage.co/query?'

## from the url we see that there is a function that directs us to intraday
## then ticker symbol request
## then the interval
#then the api key 
## so i need to make a params 

params = {'function' : 'TIME_SERIES_INTRADAY' , 
          'symbol' : 'IBM',
          'interval' : '5min',
          'apikey' : '9QA2XJU2ZHIRYDEC'
}

response = requests.get(url, params=params)
print(response.text)

