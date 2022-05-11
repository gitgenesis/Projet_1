
#Import Modules
from dataclasses import dataclass
import pandas as pd
from pathlib import Path

def load_data(quandl_key):
    
    #SPY Price Data load
    data_spy_price = pd.read_csv(Path("../data/SPY Data 05.07.22.csv"),
        infer_datetime_format=True,
        parse_dates=['Date'])

    #SPY Price Data Transform
    data_spy_price['Date'] = pd.to_datetime(data_spy_price['Date']).dt.date
    data_spy_price = data_spy_price.set_index('Date')
    data_spy_price['SPY'] = data_spy_price['SPY'].str.replace(",","",regex = True).astype(float)

    #create a DataFrame
    data_spy_price_df = pd.DataFrame(data_spy_price['SPY'])
    data_spy_price_df.columns = ['price']

    #SPY Earnings Data load
    data_spy_earnings= pd.read_csv(Path("../data/S&P PE Ratio.csv"),
            infer_datetime_format=True,
            parse_dates=['Date'])

    #SPY Earnings Data Transform
    data_spy_earnings['Date'] = pd.to_datetime(data_spy_earnings['Date']).dt.date

    #Adjust the correct date from 2030 to 1930
    from datetime import timedelta, date
    col = 'Date'
    future = data_spy_earnings[col] > date(year=2030,month=1,day=1)
    data_spy_earnings.loc[future, col] -= timedelta(days=365.25*100)
    data_spy_earnings = data_spy_earnings.set_index('Date')
    data_spy_earnings['Value'] = data_spy_earnings['Value'].astype(float)

    #create a DataFrame
    data_spy_earnings_df = pd.DataFrame(data_df_earnings_spy['Value'])
    data_spy_earnings_df.columns = ['PERatio']

    #10Y Bond Data load
    data_10year_price = pd.read_csv(Path("../data/10 Year Treasury Rate - Monthly.csv"),
            infer_datetime_format=True,
            parse_dates=['Date'])

    #10Y Bond Data Transform
    data_10year_price['Date'] = pd.to_datetime(data_10year_price['Date']).dt.date
    data_10year_price['Value'] = data_10year_price['Value'].str.replace("%","",regex = True).astype(float)
    data_10year_price = data_10year_price.set_index('Date')

    #Create DataFrame
    data_10year_price_df = pd.DataFrame(data_10year_price['Value'])
    data_10year_price_df.columns = ['10YBond']

    #Load CPI Data
    cpi_code = "RATEINF/CPI_USA"

    #Quandl URL
    cpi_url = f"https://data.nasdaq.com/api/v3/datasets/{cpi_code}.json?api_key={quandl_key}"

    #API Response
    response_cpi_url = requests.get(cpi_url).json()

    #CPI Data Transformation
    df = pd.DataFrame(response_cpi_url)
    cpistart = df["dataset"]['data']
    dates = []
    prices = []
    for info in cpistart:
        dates.append(info[0])
        prices.append(info[1])
    
    #Aggregate all information
    zipped = list(zip(dates,prices))

    #Create DataFrame
    cpi_df = pd.DataFrame(zipped, columns=['Date','CPI'])
    cpi_df.set_index('Date', inplace=True)

    # change in date time format
    cpi_df.index = pd.to_datetime(cpi_df.index, format = '%Y-%m-%d').strftime('%m/%d/%Y')

    #Merge all dataset
    merged_data = pd.concat([data_spy_earnings_df, data_spy_price_df, data_10year_price_df,cpi_df],axis = 1, join = 'inner')
    merged_data['earnings'] = merged_data['price'] / merged_data['PERatio']

    return merged_data
