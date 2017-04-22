import pandas as pd
import numpy as np

np.random.seed(1234)
pd.options.display.max_rows = 10

#Main
def main():
    df = create_data(['AMZN','GOOGL','FB','NFLX','INTC'])
    df.index.name = 'date'
    print(df)

#Data Preparation
def create_data(stocks):
    dates = pd.date_range('20160101','20161231',freq='B')
    ratings = np.array(list('ABCDE'))
    n = 10
    l = []
    for s in stocks:
        dates_indexer = np.unique(np.random.randint(0,len(dates),size=n))
        ratings_indexer = np.random.randint(0,len(ratings),size=len(dates_indexer))
        l.append(pd.Series(ratings[ratings_indexer],index=dates[dates_indexer],name=s))
    return pd.concat(l,axis=1)

    

if __name__ == '__main__': main()