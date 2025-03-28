from tkinter import *
import requests
import webbrowser
import tkinter.messagebox

root= Tk()
root.title('stock ticker search ')
root.geometry('300x200')


url = 'https://www.alphavantage.co/query?'

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
                print(data['Time series (5min)'])
            else:
                tkinter.messagebox.showerror('error', f'Failure in retrieving data for {ticker_symbol}')
        else:
            tkinter.messagebox.showerror('error',f'API request failed, Code:{response.status_code}')
    except Exception as e:
        tkinter.messagebox.showerror('error', f'Failed to search for {str(e)}')

def search():
    ticker = entry.get().strip() #this will remove whitespace
    if ticker:
        search_ticker(ticker)
    else:
        tkinter.messagebox.showinfo('input error', 'enter a ticker symbol')
