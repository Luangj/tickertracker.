from tkinter import *

root = Tk()
root.geometry("480x320")

#background color of all of it
root.config(bg = '#f0f0f0')

# create the 1day, week, month , YTD, Max
lastdaybutton = Button(root, text = '24h' , bg='#0d3273' ,fg='white', relief= SUNKEN, padx = 2 , pady=1 , width = 4)
lastdaybutton.place(x=10, y=75)

weekbutton = Button(root, text = '7D' , bg= '#0d3273' ,fg='white', relief= SUNKEN, padx = 2 , pady=1 , width = 4)
weekbutton.place(x=50, y=75)

monthbutton = Button(root, text = '1M' , bg='#0d3273' ,fg='white', relief= SUNKEN, padx = 2 , pady=1 , width = 4)
monthbutton.place(x=90, y=75)

ytdbutton = Button(root, text = 'YTD' , bg='#0d3273' ,fg='white', relief= SUNKEN, padx = 2 , pady=1 , width = 4)
ytdbutton.place(x=130, y=75)

maxbutton = Button(root, text = 'Max' , bg='#0d3273' ,fg='white', relief= SUNKEN, padx = 2 , pady=1 , width = 4)
maxbutton.place(x=170, y=75 )

# now to create the search bar , gonna have to create a functino that incorporates intraday.py

label1=  Label(root, text= 'Ticker' , relief = RAISED)
entry1 = Entry(root, bg = '#FFFFFF')
label1.grid(row=0 , column=0)
entry1.grid(row = 0 , column=1)

import tkinter.messagebox
import requests
from tkinter import entry

root.title('search tab')

url = 'https://www.alphavantage.co/query?'
API_KEY = '9QA2XJU2ZHIRYDEC'

def fetch_stock_data(ticker_symbol, time_range):
   
        '24h': ('TIME_SERIES_INTRADAY', '5min'),
        '7D': ('TIME_SERIES_DAILY', None),
        '1M': ('TIME_SERIES_DAILY', None),
        'YTD': ('TIME_SERIES_DAILY', None),
        'Max': ('TIME_SERIES_MONTHLY', None)}

    function, interval = time_functions[time_range]
    params = { 
       'function': function,
        'symbol': ticker_symbol,
        'apikey': API_KEY 
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Check for API errors
            if "Error Message" in data:
                messagebox.showerror('Error', f'Invalid ticker: {ticker_symbol}')
                return None

            # Extract time series data
            if function == 'TIME_SERIES_INTRADAY':
                time_series = data.get('Time Series (5min)')
            elif function == 'TIME_SERIES_DAILY':
                time_series = data.get('Time Series (Daily)')
            else:
                time_series = data.get('Monthly Time Series')

            if not time_series:
                messagebox.showerror('Error', f'No data found for {ticker_symbol}')
                return None

            # Get the latest and previous prices based on the time range
            dates = sorted(time_series.keys(), reverse=True)
            if time_range == '24h':
                latest = time_series[dates[0]]
                previous = time_series[dates[1]]  # 5 minutes earlier
            elif time_range == '7D':
                latest = time_series[dates[0]]
                previous = time_series[dates[7]]  # 7 days earlier
            elif time_range == '1M':
                latest = time_series[dates[0]]
                previous = time_series[dates[20]]  # ~1 month (20 trading days)
            elif time_range == 'YTD':
                latest = time_series[dates[0]]
                current_year = datetime.datetime.now().year
                ytd_date = None
                for date in dates:
                    if date.startswith(str(current_year)):
                        ytd_date = date
                    else:
                        break
                previous = time_series[ytd_date] if ytd_date else time_series[dates[-1]]
            else:  # Max
                latest = time_series[dates[0]]
                previous = time_series[dates[-1]]  # Earliest available

            # Calculate price and percentage change
            latest_price = float(latest['4. close'])
            previous_price = float(previous['4. close'])
            percentage_change = ((latest_price - previous_price) / previous_price) * 100

            return latest_price, percentage_change
        else:
            messagebox.showerror('Error', f'API request failed, Code: {response.status_code}')
            return None
    except Exception as e:
        messagebox.showerror('Error', f'Failed to fetch data: {str(e)}')
        return None
params = {
        'function' : 'TIME_SERIES_INTRADAY' , 
        'symbol' : ticker_symbol,
        'interval' : '5min',
        'apikey' : '9QA2XJU2ZHIRYDEC'
    }

def search_ticker(ticker_symbol):
    params = {
        'function' : 'TIME_SERIES_INTRADAY' , 
        'symbol' : ticker_symbol,
        'interval' : '5min',
        'apikey' : '9QA2XJU2ZHIRYDEC'
    }

    try:
        response = requests.get(url,params=params)
        if response.status_code == 200:
            data = response.json()
            if 'times series(5min)' in data:
                tkinter.messagebox.showinfo('success', f'Data retrieved for {ticker_symbol}')
                print(data['Time Series (5min)'])
            else:
                tkinter.messagebox.showerror('error', f'Failure in retrieving data for {ticker_symbol}')
        else:
            tkinter.messagebox.showerror('error',f'API request failed, Code:{response.status_code}')
    except Exception as e:
        tkinter.messagebox.showerror('error', f'Failed to search for {str(e)}')

def search():
    ticker = entry1.get().strip() #this will remove whitespace
    if ticker:
        search_ticker(ticker)
    else:
        tkinter.messagebox.showwarning('input error', 'enter a ticker symbol')
