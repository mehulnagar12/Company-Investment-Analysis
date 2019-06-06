## 1. DataViz: The first script of the project.
	It's just the test of how to download and read the csv using Pandas Data reader.

## 2. S&P500_List: The script is explained as follows:
	1.	Saving the Tickers:
	Tickers are the company’s name in short. We are exploring the Wikipedia website and getting all the tickers and extracting the name of all the tickers from the website and saving them in one pickle file.

	2.	Getting the data from RobinHood:
	Robinhood is the data source from which we are extracting the data of the company which includes the high price, low price, volume, closing price, volume of the particular day. After extracting the data, it is stored in one CSV format.

	3.	Compiling the data:
	After storing the data we want all the data in one csv according to the closing price so in this function we drop all the unnecessary columns from each csv(of the data) and then store the closing price of each company in one CSV file according to the date.

	4.	Visualizing the data:
	in this function we find the correlation of each company with each other companies and save those value in another CSV file, and after executing the function a heat map of the table is drawn.

## 3. Buy_Sell: The script is explained as follows:

	1.	Process data from labels:
	In this function we are selecting our feature set as the pricing changes for the particular day of all the companies. We will take into the account all the companies percent changes that day, and our label will be whether or not the price rose by ‘x%’ within next n days then according to that we will buy or sell the stock.

	2.	Buy Sell Hold:
	In this function we are creating our labels and there are two choices buy or sell or hold, but basically buy and sell. If the price rises by more than ‘x%’ in next ’n’ days then it is but and if it drops less than ‘x%’ then it is sold, otherwise hold. This function will be mapped to the pandas data frame.
		RETURN 1: BUY
		RETURN -1: SELL
		RETURN 0: HOLD

	3.	Extract feature sets:
	The function will take any ticker, create the needed data set and create our target column which will be our label. The target column for now will return 1, -1, 0 values for each row based on the function. 
 


	4.	Do ml:
	In this we will perform the machine learning techniques using the sklearn and Voting Classifier. The voting classifier is the classifier that let us combine many classifiers and allow them to each get the vote on what they think the class of the feature set should be.
	On the above classifier we train and test our data, we use this because it shuffles the data and creates the training and the testing samples. 
	Then we’ve calculated the accuracy and printed the predicted spread.
 
## 4. TRADE.IPYNB: 
   To perform the backtesting process and analyze the amount of money that a person has invested, i.e. performing the company investment analysis we have used
   the zipline library. It is an inbulit library in python to perform the finanace operations and do the backtesting process. We have used IPyNotebook (Anaconda)
   Jupyter notebook to perform the further operation with the data set that is extracted and trained by us in the above 3 steps.
  
