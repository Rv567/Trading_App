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

    if st.button('Update Weekly Stock Dataframes'):
        with st.spinner('In progress...'):
            time.sleep(1)

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

