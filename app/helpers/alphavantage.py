from alpha_vantage.timeseries import TimeSeries

def ts(api_key):
    return TimeSeries(key=api_key, output_format='pandas', indexing_type='date')

# cc = ForeignExchange(key=api_key, output_format='pandas', indexing_type='date')
# fd = FundamentalData(key=api_key, output_format='pandas')