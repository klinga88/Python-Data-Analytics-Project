
# coding: utf-8

# In[101]:


# 1. open individual file
# 2. iterate over days and update min close price, max close price, max and max difference
# 3. for each new day that has a lower min start calculating the max difference again
# 4. if max difference is ever larger than the previous, save that instead
# 5. Now you have this for one stock, do it for all the stocks!!!!

import pandas as pd
import numpy as np
import time
import json
import random
import requests
import os
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

#import  plotly.plotly as py
#import plotly.graph_objs as go

#read in the first file
input_folder = os.path.join("..","Data","Test_stock")
#input_folder = os.path.join("..","Data","Stocks")
output_file = os.path.join("Combined Stock Data.csv")

#plotly.tools.set_credentials_file(username='klinga88', api_key='r4j4H1eCCeIYTpmYRxx5')
#plotly.tools.set_config_file(world_readable=True)


# In[102]:


#function: Determines the largest difference between close prices given a stock's daily historical dataframe
#input: historical daily stock data in the form of a pandas dataframe
#output: Largest difference between two close prices, minimum close date, minimum close price,maximum close date,
#        maximum close price

def maxChange(data_df):
    min_close = data_df.iloc[0,4] #initiliaze first close price in the list
    min_date = data_df.iloc[0,0] #initiliaze first close price in the list
    max_close = None
    max_date = None
    biggest_diff = data_df.iloc[1,4] - data_df.iloc[0,4] # initialize to the price difference from first day to second in list



    for index, row in data_df.iterrows():
        if (row["Close"] - min_close) > biggest_diff:
            biggest_diff = row["Close"] - min_close
            max_close = row["Close"]
            max_date = row["Date"]

        if (row["Close"] < min_close):  
            min_close = row["Close"]
            min_close_Date = row["Date"]

    #print(f"Biggest Change: {biggest_diff}, from:{min_date} to {max_date}")
    
    return biggest_diff, min_date, min_close, max_date, max_close


# In[103]:


combined_ticker = []
combined_biggest_diff = []
combined_min_date = []
combined_min_close = []
combined_max_date = []
combined_max_close = []
counter = 0
#Iterate over each stock in the input folder
for filename in os.listdir(input_folder):
    try:
        ticker = filename.split(".")[0]
        input_file = os.path.join(input_folder,filename)
        data_df = pd.read_csv(input_file)
        biggest_diff, min_date, min_close, max_date, max_close = maxChange(data_df)
        combined_ticker.append(ticker)
        combined_biggest_diff.append(biggest_diff)
        combined_min_date.append(min_date)
        combined_min_close.append(min_close)
        combined_max_date.append(max_date)
        combined_max_close.append(max_close)
    except:
        print(f"Could not retrieve {filename}")
    counter +=1
    print(f'counter: {counter}')
combined_df = pd.DataFrame({"Ticker":combined_ticker,
                           "Biggest Difference":combined_biggest_diff,
                           "Minimum Close Date":combined_min_date,
                           "Minimum Close":combined_min_close,
                           "Maximum Close Date":combined_max_date,
                           "Maximum Close":combined_max_close})


# In[104]:


combined_df.head(20)


# In[97]:


combined_df["Minimum Close Date"] =  pd.to_datetime(combined_df["Minimum Close Date"])
combined_df["Maximum Close Date"] =  pd.to_datetime(combined_df["Maximum Close Date"])

combined_df.to_csv(output_file)


# In[98]:


#create range of dates for min and max dates from dataset
datelist = pd.date_range(start=combined_df["Minimum Close Date"].min(), end=combined_df["Maximum Close Date"].max())

datelist_df = pd.DataFrame({"Date":datelist})

#get value counts for min close day and max close day
min_close_dates_df = combined_df["Minimum Close Date"].value_counts().to_frame()
max_close_dates_df = combined_df["Maximum Close Date"].value_counts().to_frame()


min_close_dates_df = min_close_dates_df.reset_index()
max_close_dates_df = max_close_dates_df.reset_index()

min_close_dates_df = min_close_dates_df.rename(columns={"index":"Date","Minimum Close Date":"Min Count"})
max_close_dates_df = max_close_dates_df.rename(columns={"index":"Date","Maximum Close Date":"Max Count"})

min_close_dates_df

#create the dataframe containing number of min days and max days for all days in time period.  We will trim date range after
min_max_df = datelist_df.merge(min_close_dates_df,how="left",on="Date")
min_max_df = min_max_df.merge(max_close_dates_df,how="left",on="Date")

min_max_df = min_max_df.fillna(value=0)
min_max_df

