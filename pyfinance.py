import pandas as pd
import numpy as np

#for Importing Data
import pandas_datareader.data as pdr

np.random.seed(1234)
pd.options.display.max_rows = 10
pd.options.display.max_columns=8

#Main
def main():
    #df = create_data(['AMZN','GOOGL','FB','NFLX','INTC'])
    #df.index.name = 'date'
    #save_to_file(df)
    #print(read_quotes())
    #print(reshape_quotes(read_quotes()))
    #save_data()
    print(load_reshape_ratings())
#------------------------------------------------------------------------------------------
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

def save_to_file(df):
    #output = StringIO.StringIO()
    writer = pd.ExcelWriter('ratings.xlsx')
    df.to_excel(writer,sheet_name ='Sheet1')
    writer.save()
#End of Data Preparation
#------------------------------------------------------------------------------------------

# Importing Data

def read_quotes():
    r = pd.read_excel('ratings.xlsx',index_col=0)
    p = pdr.get_data_yahoo(r.columns,'20160101','20161231')
    #Indexing
    #p.loc[:,:,'AMZN']
    p.loc['Adj Close']
    return p.to_frame()
    
def reshape_quotes(df):
    p = df[['Adj Close','Volume']]
    p.index.names=['date','stock']
    p.columns=['close','volume']
    p.columns.names = ['field']
    p = p.swaplevel('date','stock').sort_index()
    return p.assign(ret=100 * p.groupby(level='stock').close.pct_change())
    
def save_data():
    data = reshape_quotes(read_quotes())
    # Save as .hdf
    data.to_hdf('quotes.hdf','df',format='table')
    #Save as .csv
    for g,grp in data.groupby(level='stock'):
        grp.to_csv('quotes/{}.csv'.format(g))
        print(g + '.csv created')

#-------------------------------------------------------------------------------------------
#Clean Data
def load_reshape_ratings():
    r = pd.read_excel('ratings.xlsx',index_col=0)
    r = r.stack().to_frame('ratings')
    r.index.names=['date','stock']
    r = r.swaplevel('date','stock').sort_index()
    return r

if __name__ == '__main__': main()

