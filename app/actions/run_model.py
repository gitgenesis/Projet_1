#Import Modules
from sympy import re
from actions.MCForecastTools import MCSimulation
import pandas as pd
import numpy as np

def MC_run(dataframe,num_simulations, num_of_years):
    
    #to calculate inflation
    dataframe_change = dataframe.pct_change()
    inflation_df = dataframe_change['CPI']

    #calculate Real Rate
    rate_10Y = dataframe['10YBond']
    real_rate_df = pd.concat([inflation_df,rate_10Y],join = 'inner', axis = 1)
    a = real_rate_df['10YBond']
    b = real_rate_df['CPI']
    real_rate_df['real_rate'] = (a - b)
    
    #Real Rate DataFrame
    real_rate_df = pd.DataFrame(real_rate_df['real_rate'])

    #New dataframe
    dataframe = pd.concat([dataframe,real_rate_df], join = 'inner', axis = 1)

    #adapt DataFrame to run MC simulation
    real_rate_df = real_rate_df + 1 
    real_rate_df.columns = ['close']
    real_rate_df = pd.concat([real_rate_df],axis = 1, keys = ['real_rate'])

    #Run MonteCarlo Simulation on real rate
    MC_realrate = MCSimulation(
        portfolio_data = real_rate_df,
        num_simulation = num_simulations,
        num_trading_days = int(round(12*num_of_years,0))
    )

    MC_realrate_data = MC_realrate.calc_cumulative_return()
    real_rate_summary = MC_realrate.summarize_cumulative_return()
    
    #95% Confidence Interval
    ci_lower_rate = round(real_rate_summary[8]*(real_rate_df.iloc[-1]-1),2)
    ci_upper_rate = round(real_rate_summary[9]*(real_rate_df.iloc[-1]-1),2)

    #Run MonteCarlo Simulation on Earnings
    earnings_df = pd.DataFrame(dataframe['earnings'])
    earnings_df.columns = ['close']
    earnings_df = pd.concat([earnings_df],axis =1, keys = ['earnings'])

    MC_earnings = MCSimulation(
    portfolio_data = earnings_df,
    num_simulation = num_simulations,
    num_trading_days = int(round(12*num_of_years,0))
    )

    MC_earnings_data = MC_earnings.calc_cumulative_return();
    earnings_summary = MC_earnings.summarize_cumulative_return()

    #95% Confidence Interval
    ci_lower_earnings = round(earnings_summary[8]*earnings_df.iloc[-1],2)
    ci_upper_earnings = round(earnings_summary[9]*earnings_df.iloc[-1],2)
    mean_earnings = round(earnings_summary[1]*earnings_df.iloc[-1],2)


    def reviewfunc(x):
        a = ci_lower_rate[0]
        b = ci_upper_rate[0]
        if x>= a and x<= b:
            return True
        else:
            return False
    
    dataframe['slice'] = dataframe['real_rate'].apply(reviewfunc)
    dataframe_slice = dataframe[dataframe['slice'] == True]
    PERatio = dataframe_slice['PERatio'].mean()

    #Calculate Price:   
    ci_lower_price = round(PERatio * ci_lower_earnings[0],2)
    ci_upper_price = round(PERatio * ci_upper_earnings[0],2)
    mean_price = round(PERatio * mean_earnings[0],2)

    return ci_lower_price , ci_upper_price, mean_price

