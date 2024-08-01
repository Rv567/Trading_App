from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *


def app():

    st.header("Portfolio Analysis, Build, and Optimization")
    st.subheader("Meet the Finantial Tools 🔭")
    st.write("""
    - **Cumulative Return%** : total return of an investment over a set period.
    - **Standard Deviation** : measures the amount of variation of a set of values.
    - **Alpha** : measures excess returns relative to benchmark MASI.
    - **Beta** : quantifies an asset's volatility compared to the market.
    - **Sharpe Ratio** : evaluates risk-adjusted performance.
    """)

    #### df definition
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
  
    st.write("Choose a metric to apply to your stocks and see the results:")
    metric_choice = st.selectbox("Select Metric", ["Cumulative Return%", "Standard Deviation","Alpha","Beta", "Sharpe Ratio"])

    if st.button("Apply Metric"):
        if metric_choice == "Cumulative Return%":
            
            cum_returns = {}
            for elem in df.columns:
                individual_cumsum = ((1+df[elem]).cumprod()-1)*100
                cum_returns[elem] = individual_cumsum[-1]
            df_cum_returns = pd.DataFrame(list(cum_returns.items()), columns=['Stock', 'Cumulative Return%']).set_index('Stock')
            st.write(df_cum_returns.sort_values(by="Cumulative Return%", ascending=False))
    

        elif metric_choice == "Standard Deviation" :

            std = {}
            for elem in df.columns:
                std[elem] = round(df[elem].std(), 3)
            df_std = pd.DataFrame(list(std.items()), columns=['Stock', 'Standard Deviation']).set_index('Stock')
            st.write(df_std.sort_values(by="Standard Deviation", ascending=True))

        elif metric_choice == "Alpha":

            alpha = {}
            for elem in df.columns:
                 if elem != "MASI":
                 
                    X = df["MASI"].values.reshape(-1, 1)
                    y = df[elem].values.reshape(-1, 1)
                    model = LinearRegression()
                    linreg = model.fit(X,y)
                    alpha[elem] = np.round(linreg.intercept_,4)

            df_alpha = pd.DataFrame(list(alpha.items()), columns=['Stock', 'Alpha']).set_index('Stock')
            st.write(df_alpha.sort_values(by="Alpha", ascending=False))

        elif metric_choice == "Beta":
            
            beta = {}
            for elem in df.columns:
                if elem != "MASI":
                    beta[elem] = newbeta(df[elem], df["MASI"])

            df_beta = pd.DataFrame(list(beta.items()), columns=['Stock', 'Beta']).set_index('Stock')
            st.write(df_beta.sort_values(by="Beta", ascending=False))
        
        elif metric_choice == "Sharpe Ratio":
            
            risk_free_rate = 0.01 / 252 # 1% en daily devient ceci en annually
            shap = {}
            for elem in df.columns:
                if elem != "MASI":
                    shap[elem] = qs.stats.sharpe(df[elem], rf=risk_free_rate)

            df_shap = pd.DataFrame(list(shap.items()), columns=['Stock', 'Sharpe_Ratio']).set_index('Stock')
            st.write(df_shap.sort_values(by="Sharpe_Ratio", ascending=False))


    # Markowitz Optimization
    st.header("Portfolio Markowitz Optimization")  

    df_close = pd.concat([dataframes[elem][elem] for elem in ticker],join="outer",axis=1,sort=True)
    df_close.index = pd.to_datetime(df_close.index)
    df_close=df_close.drop(columns=["MASI","SNA","LES","CFG"])
    df_close = df_close[df_close.index >= "2020-12-01"]
    df_close = df_close.fillna(method='ffill')
    df_close = df_close[df_close.index >= "2022-12-15"]


    st.write("Choose an Optimization Objective")
    obj_choice = st.selectbox("Select Objective", ["Maximize the Sharpe Ratio of the portfolio", "Minimize the Volatility of the portfolio","Target Return with Minimum Risk"])

    mu = expected_returns.mean_historical_return(df_close)
    S = risk_models.sample_cov(df_close)
    ################### First objective
    if obj_choice == "Maximize the Sharpe Ratio of the portfolio":
        contra = st.selectbox("Add a contraint fo maximum weight allocation", ["Yes", "No"])
        if contra == "Yes":
            choice = st.slider('Choose a maximum weight allocation', min_value=10, max_value=50, value=50, step=10)
            
            ef = EfficientFrontier(mu,S)
            ef.add_constraint(lambda w: w <= choice/100)

            weights = ef.max_sharpe()

            clean_weights = ef.clean_weights()

            df_poids_contr_sharp = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids_contr_sharp["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids_contr_sharp.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids_contr_sharp)
        

        elif contra == "No" :
            ef = EfficientFrontier(mu,S)

            weights = ef.max_sharpe()

            clean_weights = ef.clean_weights()

            df_poids_sharp = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids_sharp["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids_sharp.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids_sharp)

    ################## Second objective
    elif obj_choice == "Minimize the Volatility of the portfolio":
        contra = st.selectbox("Add a contraint fo maximum weight allocation", ["Yes", "No"])
        if contra == "Yes":
            choice = st.slider('Choose a maximum weight allocation', min_value=10, max_value=50, value=50, step=10)
            
            ef = EfficientFrontier(mu,S)
            ef.add_constraint(lambda w: w <= choice/100)

            weights = ef.min_volatility()

            clean_weights = ef.clean_weights()

            df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids)
        

        elif contra == "No" :
            ef = EfficientFrontier(mu,S)

            weights = ef.min_volatility()

            clean_weights = ef.clean_weights()

            df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids)

    ##################### Third objective
    elif obj_choice == "Target Return with Minimum Risk" :
        contra = st.selectbox("Add a contraint fo maximum weight allocation", ["Yes", "No"])
        if contra == "Yes":
            target = st.slider(
                                'Choose a target return',
                                min_value=0.2, 
                                max_value=2.0, 
                                value=0.7, 
                                step=0.1
                            )
            choice = st.slider('Choose a maximum weight allocation', min_value=10, max_value=50, value=50, step=10)
            
            ef = EfficientFrontier(mu,S)
            ef.add_constraint(lambda w: w <= 20/100)
            ef.efficient_return(target_return=target)

            clean_weights = ef.clean_weights()

            df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids)
        

        elif contra == "No" :
            target = st.slider(
                                'Choose a target return',
                                min_value=0.2, 
                                max_value=2.0, 
                                value=0.7, 
                                step=0.1
                            )
            ef = EfficientFrontier(mu,S)

            ef.efficient_return(target_return=target)

            clean_weights = ef.clean_weights()

            df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids)

    st.write(df_poids_sharp)