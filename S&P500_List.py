#Getting S&P 500 list
import bs4 as bs
import numpy as np
import pickle  #To save the python object on disk
import os
import requests
import datetime as dt
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like #Version correction.
import pandas_datareader as web
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text,"lxml")  #Re-arranging the ticker from wikipedia
    table = soup.find('table',{'class':'wikitable sortable'})
    tickers = []  # Storing them in an array
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    with open("sp500tickers.pickle","wb") as f:  #opening folder and writing in the file
        pickle.dump(tickers,f)

    print(tickers)
    return tickers


#Getting the companies data from tickers (SOURCE= Robinhood)
def get_data_from_robinhood(reload_sp500=False):
    if reload_sp500:
        tickers= save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f: #opening folder and reading the file
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):  #Creating the folder and converting the
        os.makedirs('stock_dfs')         #data to csv and saving on the disk.
    start = dt.datetime(2017,8,15)
    end = dt.datetime(2018,8,15)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df= web.DataReader(ticker,'robinhood',start,end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
#get_data_from_robinhood()

#COMPILING ALL THE DATA IN SINGLE DATAFRAME
def compile_data():
    with open("sp500tickers.pickle","rb") as f: #opening folder and reading the file
        tickers = pickle.load(f)
    main_df = pd.DataFrame()

#Taking all the stocks and arranging all accoriding to its closing price.
    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('begins_at',inplace=True)  

        df.rename(columns = {'close_price':ticker},inplace=True) 
        df.drop(['symbol','session','high_price','interpolated','low_price','open_price','volume'], 1,inplace=True) #Dropping all columns except Closing Price.
        

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df,how='outer')

        if(count%10==0):
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

#Creating the correlation table of the dataframe.    

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
##    df['AAPL'].plot()
##    plt.show()
    df_corr = df.corr() #Creating Correlation table for all the dataframe.
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1) #1x1 and plot no.1
    heatmap = ax.pcolor(data,cmap=plt.cm.RdYlGn) #Colors
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False) #arranging ticks at every 1/2 mark
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False) #In both X and Y axes
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)  #No need for this line in case of covariance
    plt.tight_layout()
    plt.show()
    

visualize_data()
