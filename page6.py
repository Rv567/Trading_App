from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *


def app():

    st.header("Portfolio Analysis, Build, and Optimization")
    st.subheader("Calculate Portfolio Metrics")
    st.write("""
    - **Cumulative Return%**
    - **Standard Deviation**
    - **Beta**
    - **Sharpe Ratio**
    """)

    st.write("Choose a metric to apply to your stocks and see the results:")
    metric_choice = st.selectbox("Select Metric", ["Cumulative Return%", "Standard Deviation", "Beta", "Sharpe Ratio"])
    
    #We load our entire data from pickle files
    dataframes = load_data()
    ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
    dataframes = {key: reorganize2(df, ticker[idx]) for idx, (key, df) in enumerate(dataframes.items())}

    df = pd.concat([dataframes[elem][elem] for elem in ticker],join="outer",axis=1,sort=True)
    # Remove NA
    df = df[df.index >"2022-12-08"]
    df = df.fillna(method='ffill')
    df = df[df.index >= "2022-12-14"] # AKT is the recent stock

    for elem in df.columns:
        df[elem] = df[elem].pct_change()

    df.dropna(inplace=True)
    st.write(df)

    if st.button("Apply Metric"):
        if metric_choice == "Cumulative Return%":
            st.write(f"Results for {metric_choice}:")
    