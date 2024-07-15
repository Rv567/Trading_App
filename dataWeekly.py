import streamlit as st
from Functions.functions import *
from Functions.mylibraries import *

#Market Index
masiwk = tv.get_hist(symbol='MASI',exchange='CSEMA',interval=Interval.in_weekly,n_bars=70000)

#High Cap
attijariwk = tv.get_hist(symbol='ATW',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
iamwk = tv.get_hist(symbol='IAM',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
bcpwk = tv.get_hist(symbol='BCP',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
lafargewk = tv.get_hist(symbol='LHM',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
boawk = tv.get_hist(symbol='BOA',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
taqawk = tv.get_hist(symbol='TQM',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
cimentwk= tv.get_hist(symbol='CMA',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)

#Middle Cap
totalwk = tv.get_hist(symbol='TMA',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
addouhawk = tv.get_hist(symbol='ADH',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
tgccwk = tv.get_hist(symbol='TGC',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
cdmwk = tv.get_hist(symbol='CDM',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
atlantawk = tv.get_hist(symbol='ATL',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
bmciwk =  tv.get_hist(symbol='BCI',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
akditalwk =  tv.get_hist(symbol='AKT',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
sanlamwk =  tv.get_hist(symbol='SAH',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)

#Low Cap
cfgwk = tv.get_hist(symbol='CFG',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
aradeiwk = tv.get_hist(symbol='ARD',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
aliancewk = tv.get_hist(symbol='ADI',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
distywk = tv.get_hist(symbol='DYT',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
autowk =  tv.get_hist(symbol='ATH',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
saadawk = tv.get_hist(symbol='RDS',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
deltawk = tv.get_hist(symbol='DHO',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)
feniewk =  tv.get_hist(symbol='FBR',exchange='CSEMA',interval=Interval.in_weekly,n_bars=60000)

ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM","CMA","TMA","ADH","TGC","CDM","ATL","BCI","AKT","SAH","CFG","ARD","ADI","DYT","ATH","RDS","DHO","FBR"]
dataframes = [masiwk,attijariwk,iamwk,bcpwk,lafargewk,boawk,taqawk,cimentwk,totalwk,addouhawk,tgccwk,cdmwk,atlantawk,bmciwk,akditalwk,sanlamwk,cfgwk,aradeiwk,aliancewk,distywk,autowk,saadawk,deltawk,feniewk]


# Save each DataFrame to disk
for i, df in zip(ticker, dataframes):
    df.to_pickle(f'dataframe_weekly_{i}.pkl')