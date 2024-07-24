from Functions.functions import *
from Functions.mylibraries import *
from dataDaily import *
from dataWeekly import *


def app():
    st.header("Introduction to the Data page")
    st.write("Welcome to the Data Management page. Here, you update stock dataframes with real-time data.")
    st.subheader("Update Real-Time Data")
    st.write("Initiate the update the stock dataframes with real-time data")

    if st.button('Update Daily Stock Dataframes'):
        with st.spinner('In progress...'):
            time.sleep(1)

            ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
            dataframes = [masi,attijari,iam,bcp,lafarge,boa,taqa,managem,ciment,marsa,cosumar,wafa,afriqia,label,total,cih,addouha,akdital,tgcc,cdm,bmci,sanlam,atlanta,cristal,aradei,cfg,aliance,delta,hps,risma,auto,sonasid,saada,jet,stok]

            for df in dataframes:
                if df is None:
                    st.write("Retry")
        
            # Save each DataFrame to disk
            for i, df in zip(ticker, dataframes):
                df.to_pickle(f'dataframe_{i}.pkl')
        
        st.success('Data updated!')
        st.write(f"We successfully created and updated {len(dataframes)} dataframes")

    ###############################################################

    if st.button('Update Weekly Stock Dataframes'):
        with st.spinner('In progress...'):
            time.sleep(1)
            #Market Index
            masiwk = tv.get_hist(symbol='MASI',exchange='CSEMA',interval=Interval.in_daily,n_bars=70000)

            #High Cap
            attijariwk = tv.get_hist(symbol='ATW',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            iamwk = tv.get_hist(symbol='IAM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            bcpwk = tv.get_hist(symbol='BCP',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            lafargewk = tv.get_hist(symbol='LHM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            boawk = tv.get_hist(symbol='BOA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            taqawk = tv.get_hist(symbol='TQM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            managemwk = tv.get_hist(symbol='MNG',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            cimentwk = tv.get_hist(symbol='CMA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            marsawk = tv.get_hist(symbol='MSA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

            #Middle Cap
            cosumarwk = tv.get_hist(symbol='CSR',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            wafawk = tv.get_hist(symbol='WAA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            afriqiawk = tv.get_hist(symbol='GAZ',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            labelwk = tv.get_hist(symbol='LBV',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            totalwk = tv.get_hist(symbol='TMA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            cihwk = tv.get_hist(symbol='CIH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            addouhawk = tv.get_hist(symbol='ADH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            akditalwk =  tv.get_hist(symbol='AKT',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)

            #Low Cap
            tgccwk = tv.get_hist(symbol='TGC',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            cdmwk = tv.get_hist(symbol='CDM',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            bmciwk =  tv.get_hist(symbol='BCI',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            sanlamwk =  tv.get_hist(symbol='SAH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            atlantawk = tv.get_hist(symbol='ATL',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            cristalwk = tv.get_hist(symbol='LES',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            aradeiwk = tv.get_hist(symbol='ARD',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            cfgwk = tv.get_hist(symbol='CFG',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            aliancewk = tv.get_hist(symbol='ADI',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            deltawk = tv.get_hist(symbol='DHO',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            hpswk = tv.get_hist(symbol='HPS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            rismawk = tv.get_hist(symbol='RIS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            autowk =  tv.get_hist(symbol='ATH',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            sonasidwk = tv.get_hist(symbol='SID',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            saadawk = tv.get_hist(symbol='RDS',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            jetwk = tv.get_hist(symbol='JET',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            stokwk = tv.get_hist(symbol='SNA',exchange='CSEMA',interval=Interval.in_daily,n_bars=60000)
            
            ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
            dataframes = [masiwk,attijariwk,iamwk,bcpwk,lafargewk,boawk,taqawk,managemwk,cimentwk,marsawk,cosumarwk,wafawk,afriqiawk,labelwk,totalwk,cihwk,addouhawk,akditalwk,tgccwk,cdmwk,bmciwk,sanlamwk,atlantawk,cristalwk,aradeiwk,cfgwk,aliancewk,deltawk,hpswk,rismawk,autowk,sonasidwk,saadawk,jetwk,stokwk]

            for df in dataframes:
                if df is None:
                    st.write("Retry")
        
            # Save each DataFrame to disk
            for i, df in zip(ticker, dataframes):
                df.to_pickle(f'dataframe_weekly_{i}.pkl')
        
        st.success('Data updated!')
        st.write(f"We successfully created and updated {len(dataframes)} dataframes")

