from os import getenv
from alpha_vantage.timeseries import TimeSeries
# from alpha_vantage.foreignexchange import ForeignExchange
# from alpha_vantage.fundamentaldata import FundamentalData
from os import getenv

class av:
    try:
        ts = TimeSeries(key=getenv('ALPHAVANTAGE_API_KEY'), output_format='pandas', indexing_type='date')
        # cc = ForeignExchange(key=api_key, output_format='pandas', indexing_type='date')
        # fd = FundamentalData(key=api_key, output_format='pandas')
    
    except ValueError:
        print('Please provide a valid AlphaVantage API key.\nGet a free key from https://www.alphavantage.co/support/#api-key')
