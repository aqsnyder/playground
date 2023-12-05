import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the ticker symbol
tickerSymbol = 'BTC-USD'

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Get historical data for this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical prices for this ticker
# Using the current date as the end date
tickerDf = tickerData.history(period='1d', start='2014-9-17', end=current_date)

# Save to CSV
tickerDf.to_csv('BTC-USD.csv')
