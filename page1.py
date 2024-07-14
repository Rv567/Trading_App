from Functions.functions import *
from Functions.mylibraries import *
from data_daily import *


def app():
    st.header("Introduction to the Data page")
    st.write("Welcome to the Data Management page. Here, you update stock dataframes with real-time data.")
    st.subheader("Update Real-Time Data")
    st.write("Initiate the update the stock dataframes with real-time data")

    if st.button('Update stock dataframes ..'):
        with st.spinner('In progress...'):
            time.sleep(1)

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

