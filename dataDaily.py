import streamlit as st
from Functions.functions import *
from Functions.mylibraries import *

#Market Index
masi = tv.get_hist(symbol='MASI',exchange='CSEMA',interval=Interval.in_daily,n_bars=70000)

#High Cap
attijari = tv.get_hist(symbol='ATW',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
iam = tv.get_hist(symbol='IAM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
bcp = tv.get_hist(symbol='BCP',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
lafarge = tv.get_hist(symbol='LHM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
boa = tv.get_hist(symbol='BOA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
taqa = tv.get_hist(symbol='TQM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
managem = tv.get_hist(symbol='MNG',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
ciment= tv.get_hist(symbol='CMA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
marsa = tv.get_hist(symbol='MSA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

#Middle Cap
cosumar = tv.get_hist(symbol='CSR',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
wafa = tv.get_hist(symbol='WAA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
afriqia = tv.get_hist(symbol='GAZ',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
label = tv.get_hist(symbol='LBV',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
total = tv.get_hist(symbol='TMA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
cih = tv.get_hist(symbol='CIH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
addouha = tv.get_hist(symbol='ADH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
akdital =  tv.get_hist(symbol='AKT',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

#Low Cap
tgcc = tv.get_hist(symbol='TGC',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
cdm = tv.get_hist(symbol='CDM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
bmci =  tv.get_hist(symbol='BCI',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
sanlam =  tv.get_hist(symbol='SAH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
atlanta = tv.get_hist(symbol='ATL',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
cristal = tv.get_hist(symbol='LES',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
aradei = tv.get_hist(symbol='ARD',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
cfg = tv.get_hist(symbol='CFG',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
aliance = tv.get_hist(symbol='ADI',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
delta = tv.get_hist(symbol='DHO',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
hps = tv.get_hist(symbol='HPS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
risma = tv.get_hist(symbol='RIS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
auto =  tv.get_hist(symbol='ATH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
sonasid = tv.get_hist(symbol='SID',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
saada = tv.get_hist(symbol='RDS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
jet = tv.get_hist(symbol='JET',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
stok = tv.get_hist(symbol='SNA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)


ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
dataframes = [masi,attijari,iam,bcp,lafarge,boa,taqa,managem,ciment,marsa,cosumar,wafa,afriqia,label,total,cih,addouha,akdital,tgcc,cdm,bmci,sanlam,atlanta,cristal,aradei,cfg,aliance,delta,hps,risma,auto,sonasid,saada,jet,stok]


# Save each DataFrame to disk
for i, df in zip(ticker, dataframes):
    df.to_pickle(f'dataframe_{i}.pkl')
