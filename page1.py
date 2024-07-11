from Functions.functions import *
from Functions.mylibraries import *


def app():
    st.header("Introduction to the Data page")
    st.write("Welcome to the Data Management page. Here, you update stock dataframes with real-time data.")
    st.subheader("Update Real-Time Data")
    st.write("Initiate the update the stock dataframes with real-time data")

    if st.button('Update stock dataframes ..'):
        with st.spinner('In progress...'):
            time.sleep(1)
            #Market Index
            masi = tv.get_hist(symbol='MASI',exchange='CSEMA',interval=Interval.in_daily,n_bars=70000)

            #High Cap
            attijari = tv.get_hist(symbol='ATW',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            iam = tv.get_hist(symbol='IAM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            bcp = tv.get_hist(symbol='BCP',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            lafarge = tv.get_hist(symbol='LHM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            boa = tv.get_hist(symbol='BOA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            taqa = tv.get_hist(symbol='TQM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            ciment= tv.get_hist(symbol='CMA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

            #Middle Cap
            total = tv.get_hist(symbol='TMA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            addouha = tv.get_hist(symbol='ADH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            tgcc = tv.get_hist(symbol='TGC',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            cdm = tv.get_hist(symbol='CDM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            atlanta = tv.get_hist(symbol='ATL',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            bmci =  tv.get_hist(symbol='BCI',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            akdital =  tv.get_hist(symbol='AKT',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            sanlam =  tv.get_hist(symbol='SAH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

            #Low Cap
            cfg = tv.get_hist(symbol='CFG',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            aradei = tv.get_hist(symbol='ARD',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            aliance = tv.get_hist(symbol='ADI',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            disty = tv.get_hist(symbol='DYT',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            auto =  tv.get_hist(symbol='ATH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            saada = tv.get_hist(symbol='RDS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            delta = tv.get_hist(symbol='DHO',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            fenie =  tv.get_hist(symbol='FBR',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

            ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM","CMA","TMA","ADH","TGC","CDM","ATL","BCI","AKT","SAH","CFG","ARD","ADI","DYT","ATH","RDS","DHO","FBR"]
            dataframes = [masi,attijari,iam,bcp,lafarge,boa,taqa,ciment,total,addouha,tgcc,cdm,atlanta,bmci,akdital,sanlam,cfg,aradei,aliance,disty,auto,saada,delta,fenie]

            for df in dataframes:
                if df is None:
                    st.write("Retry")
        
            # Save each DataFrame to disk
            for i, df in zip(ticker, dataframes):
                df.to_pickle(f'dataframe_{i}.pkl')
        
        st.success('Data updated!')
        st.write(f"We successfully created and updated {len(dataframes)} dataframes")

