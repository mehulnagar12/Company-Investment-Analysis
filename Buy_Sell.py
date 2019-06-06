from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn import svm, cross_validate, neighbors  
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

#SVM: Support Vector Machine
#Cross-Validation: Creates shuffled training and testing samples
#K-nearest Neighbours is for neighbouring data.





#Model is per company basis which is compared with all other companies

def process_data_for_labels(ticker):        #Labels are the target
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv',index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1,hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker])/df[ticker]
    df.fillna(0,inplace=True)
    #print(df.head())
    return tickers,df
    


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02 #Stock Price change by 2% in 7 days (hm_days)
    for col in cols:
        if(col>requirement):
            return 1         #BUY
        if(col<-requirement):
            return -1       #SELL
    return 0


def extract_featuresets(ticker):
    tickers,df= process_data_for_labels(ticker)
    df['{}_target'.format(ticker)]= list(map(buy_sell_hold,
                                             df['{}_1d'.format(ticker)],
                                             df['{}_2d'.format(ticker)],
                                             df['{}_3d'.format(ticker)],
                                             df['{}_4d'.format(ticker)],
                                             df['{}_5d'.format(ticker)],
                                             df['{}_6d'.format(ticker)],
                                             df['{}_7d'.format(ticker)],
                                             ))
    vals = df['{}_target'.format(ticker)].values.tolist()  #removed tolist
    str_vals = [str(i) for i in vals]
    print('Data Spread: ',Counter(str_vals))  #Distribution of the data

    df.fillna(0,inplace=True)
    df= df.replace([np.inf, -np.inf],np.nan)  #Replaceing Large changing with nan
    df.dropna(inplace=True)

    df_vals= df[[ticker for ticker in tickers]].pct_change() #Normalized(% change)
    df_vals= df_vals.replace([np.inf,-np.inf],0)  
    df_vals.fillna(0,inplace=True)

    X= df_vals.values
    y= df['{}_target'.format(ticker)].values

    return X, y, df


#Testing the algorithm on the random data.
def do_ml(ticker):
    X,y,df= extract_featuresets(ticker)
#test against 25% of sample data
    X_train,X_test,y_train,y_test= cross_validate.train_test_split(X,y,test_size=0.25)

    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())]) 
    clf.fit(X_train,y_train)
    confidence= clf.score(X_test,y_test)
    print('Accurancy: ',confidence)
    predictions= clf.predict(X_test)
    print('Predicted spread: ',Counter(predictions))
    print()
    

    

do_ml('AAPL')










