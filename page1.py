from Functions.functions import *
from Functions.mylibraries import *


def app():

    st.header("Introduction to the Data page")
    st.write("Welcome to the Data Management page. Here, you update stock dataframes with real-time data.")
    st.subheader("Update Real-Time Data")
    st.write("Initiate the update the stock dataframes with real-time data.")


    # stock tickers
    market_index = ["MASI"]
    high_cap = ["ATW", "IAM", "BCP", "LHM", "BOA", "TQM", "MNG", "CMA", "MSA"]
    mid_cap = ["CSR", "WAA", "GAZ", "LBV", "TMA", "CIH", "ADH", "AKT"]
    low_cap = ["TGC", "CDM", "BCI", "SAH", "ATL", "LES", "ARD", "CFG", "ADI",
               "DHO", "HPS", "RIS", "ATH", "SID", "RDS", "JET", "SNA"]

    all_tickers = market_index + high_cap + mid_cap + low_cap

    ############################################################ Daily
    if st.button('Update Daily Stock Dataframes'):
        with st.spinner('Updating daily stock data...'):
            time.sleep(1)
            
            # Fetch daily data
            daily_data = fetch_stock_data(all_tickers, "CSEMA", Interval.in_daily, 60000)

            # Save data to disk
            for ticker, df in daily_data.items():
                df.to_pickle(f'dataframe_{ticker}.pkl')

        st.success('Daily data updated!')
        st.write(f"We successfully created and updated {len(daily_data)} dataframes")

    ############################################################### Weekly
    if st.button('Update Weekly Stock Dataframes'):
        with st.spinner('Updating weekly stock data...'):
            time.sleep(1)

            # Fetch weekly data
            weekly_data = fetch_stock_data(all_tickers, "CSEMA", Interval.in_weekly, 60000)

            # Save data to disk
            for ticker, df in weekly_data.items():
                df.to_pickle(f'dataframe_weekly_{ticker}.pkl')

        st.success('Weekly data updated!')
        st.write(f"We successfully created and updated {len(weekly_data)} dataframes")