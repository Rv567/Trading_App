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
    dataframes.pop('CFG', None)
    ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
    dataframes = {key: reorganize2(df, ticker[idx]) for idx, (key, df) in enumerate(dataframes.items())}

    df = pd.concat([dataframes[elem][elem] for elem in ticker],join="outer",axis=1,sort=True)
    # Remove NA
    df = df[df.index >"2022-12-08"]
    df = df.fillna(method='ffill')
    df = df[df.index >= "2022-12-14"] # AKT is the recent stock

    for elem in df.columns:
        df[elem] = df[elem].pct_change()

    df.dropna(inplace=True)

    #cum return
    cum_returns = {}
    for elem in df.columns:
        individual_cumsum = ((1+df[elem]).cumprod()-1)*100
        cum_returns[elem] = individual_cumsum[-1]
    df_cum_returns = pd.DataFrame(list(cum_returns.items()), columns=['Stock', 'Cumulative Return%']).set_index('Stock')
    
    st.write("Choose a metric to apply to your stocks and see the results:")
    metric_choice = st.selectbox("Select Metric", ["Cumulative Return%", "Standard Deviation","Alpha","Beta", "Sharpe Ratio"])

    if st.button("Apply Metric"):
        if metric_choice == "Cumulative Return%":

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
                #if elem != "MASI":
                    shap[elem] = qs.stats.sharpe(df[elem], rf=risk_free_rate)

            df_shap = pd.DataFrame(list(shap.items()), columns=['Stock', 'Sharpe_Ratio']).set_index('Stock')
            st.write(df_shap.sort_values(by="Sharpe_Ratio", ascending=False))


    # Markowitz Optimization
    st.header("Portfolio Markowitz Optimization")  

    df_close = pd.concat([dataframes[elem][elem] for elem in ticker],join="outer",axis=1,sort=True)
    df_close.index = pd.to_datetime(df_close.index)
    df_close=df_close.drop(columns=["MASI","SNA","LES"])
    df_close = df_close[df_close.index >= "2020-12-01"]
    df_close = df_close.fillna(method='ffill')
    df_close = df_close[df_close.index >= "2022-12-15"]


    st.subheader("Optimization Objectives Descriptive")
    st.markdown("""
        ##### Minimize Volatility
        The objective of minimizing volatility is to find the portfolio with the lowest possible risk (volatility) for a given set of assets. This approach focuses solely on reducing the portfolio's risk without explicitly considering returns.

        - **Goal:** Achieve the lowest possible portfolio volatility.

        ##### Maximize Sharpe Ratio
        Maximizing the Sharpe ratio aims to achieve the highest risk-adjusted return. This objective balances the trade-off between return and risk, aiming to optimize the overall performance of the portfolio.

        - **Goal:** Maximize the portfolio's Sharpe ratio, balancing returns and risk.

        ##### Target Return
        The efficient return objective seeks to achieve a specific target return with the least amount of risk. This approach is useful for investors with specific return goals.

        - **Goal:** Minimize risk for a specified target return.""")

    st.subheader("Optimized Portfolio Management")
    obj_choice = st.selectbox("Select Objective", ["Maximize the Sharpe Ratio of the portfolio", "Minimize the Volatility of the portfolio","Target Return with Minimum Risk"])

    mu = expected_returns.mean_historical_return(df_close)
    S = risk_models.sample_cov(df_close)
    ################### First objective
    if obj_choice == "Maximize the Sharpe Ratio of the portfolio":
        contra = st.selectbox("Add a contraint for maximum weight allocation", ["Yes", "No"])
        if contra == "Yes":
            choice = st.slider('Choose a maximum weight allocation', min_value=10, max_value=50, value=50, step=10)
            
            ef = EfficientFrontier(mu,S)
            ef.add_constraint(lambda w: w <= choice/100)

            weights = ef.max_sharpe()

            clean_weights = ef.clean_weights()

            df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids)
        
            st.subheader("Optimized Portfolio Performance")
            # Portfolio Construction
            df_poids_opt = df_poids.set_index("Stock")
            optimized_portfolio=0
            exclude_columns = ["MASI", "SNA","LES"]
            for elem in df.columns:
                if elem not in  exclude_columns:
                    poids = df_poids_opt.loc[elem].values
                    optimized_portfolio += poids/100 * df[elem]

            #Plot
            trace_perf(optimized_portfolio,df["MASI"])

            #Addictional metrics
            st.write("Additional Metrics :")
            metrics(optimized_portfolio,df["MASI"])

        elif contra == "No" :
            ef = EfficientFrontier(mu,S)

            weights = ef.max_sharpe()

            clean_weights = ef.clean_weights()

            df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
            df_poids["Poids %"] *= 100
            st.subheader("Optimized Portfolio Weights")
            st.write(df_poids.sort_values(by="Poids %", ascending=False))
            st.subheader("Optimized Portfolio Allocation")
            trace_pie(df_poids)

            st.subheader("Optimized Portfolio Performance")
            # Portfolio Construction
            df_poids_opt = df_poids.set_index("Stock")
            optimized_portfolio=0
            exclude_columns = ["MASI", "SNA","LES"]
            for elem in df.columns:
                if elem not in  exclude_columns:
                    poids = df_poids_opt.loc[elem].values
                    optimized_portfolio += poids/100 * df[elem]

            #Plot
            trace_perf(optimized_portfolio,df["MASI"])

            #Addictional metrics
            st.write("Additional Metrics :")
            metrics(optimized_portfolio,df["MASI"])

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

            st.subheader("Optimized Portfolio Performance")
            # Portfolio Construction
            df_poids_opt = df_poids.set_index("Stock")
            optimized_portfolio=0
            exclude_columns = ["MASI", "SNA","LES"]
            for elem in df.columns:
                if elem not in  exclude_columns:
                    poids = df_poids_opt.loc[elem].values
                    optimized_portfolio += poids/100 * df[elem]

            #Plot
            trace_perf(optimized_portfolio,df["MASI"])

            #Addictional metrics
            st.write("Additional Metrics :")
            metrics(optimized_portfolio,df["MASI"])

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

            st.subheader("Optimized Portfolio Performance")
            # Portfolio Construction
            df_poids_opt = df_poids.set_index("Stock")
            optimized_portfolio=0
            exclude_columns = ["MASI", "SNA","LES"]
            for elem in df.columns:
                if elem not in  exclude_columns:
                    poids = df_poids_opt.loc[elem].values
                    optimized_portfolio += poids/100 * df[elem]

            #Plot
            trace_perf(optimized_portfolio,df["MASI"])

            #Addictional metrics
            st.write("Additional Metrics :")
            metrics(optimized_portfolio,df["MASI"])
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

            st.subheader("Optimized Portfolio Performance")
            # Portfolio Construction
            df_poids_opt = df_poids.set_index("Stock")
            optimized_portfolio=0
            exclude_columns = ["MASI", "SNA","LES"]
            for elem in df.columns:
                if elem not in  exclude_columns:
                    poids = df_poids_opt.loc[elem].values
                    optimized_portfolio += poids/100 * df[elem]

            #Plot
            trace_perf(optimized_portfolio,df["MASI"])
            
            #Addictional metrics
            st.write("Additional Metrics :")
            metrics(optimized_portfolio,df["MASI"])

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

            st.subheader("Optimized Portfolio Performance")
            # Portfolio Construction
            df_poids_opt = df_poids.set_index("Stock")
            optimized_portfolio=0
            exclude_columns = ["MASI", "SNA","LES"]
            for elem in df.columns:
                if elem not in  exclude_columns:
                    poids = df_poids_opt.loc[elem].values
                    optimized_portfolio += poids/100 * df[elem]

            #Plot
            trace_perf(optimized_portfolio,df["MASI"])

            #Addictional metrics
            st.write("Additional Metrics :")
            metrics(optimized_portfolio,df["MASI"])

    st.header("Own Portfolio Optimization") 
    if "favorite" not in st.session_state:
        st.session_state["favorite"] = [False] * len(df_close.columns)

    stock_data = {
        "Stock": df_close.columns.tolist(),
    }
    data_df = pd.DataFrame(stock_data)
    data_df["Choice"] = st.session_state["favorite"]

    # Display the data editor
    edited_df = st.data_editor(
        data_df,
        column_config={
            "Choice": st.column_config.CheckboxColumn(
                "Choice",
                help="Select your Stocks",
                default=False,
            )
        },
        disabled=["Stock"],
        hide_index=True,
    )

    # Update session state 
    st.session_state["favorite"] = edited_df["Choice"].tolist()
    #Selected Stocks
    favorite_stocks = edited_df[edited_df["Choice"]]["Stock"].tolist()
    df_own = df_close[favorite_stocks]

    #Portfolio Optimization
    mu = expected_returns.mean_historical_return(df_own)
    S = risk_models.sample_cov(df_own)

    contra = st.selectbox("Add a contraint for maximum weight allocation", ["Yes", "No"],key='po')
    if contra == "Yes":
        choice = st.slider('Choose a maximum weight allocation', min_value=10, max_value=50, value=50, step=10,key='poo')
        
        ef = EfficientFrontier(mu,S)
        ef.add_constraint(lambda w: w <= choice/100)

        weights = ef.max_sharpe()

        clean_weights = ef.clean_weights()

        df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
        df_poids["Poids %"] *= 100
        st.subheader("Optimized Portfolio Weights")
        st.write(df_poids.sort_values(by="Poids %", ascending=False))
        st.subheader("Optimized Portfolio Allocation")
        trace_pie(df_poids)
    
        st.subheader("Optimized Portfolio Performance")
        # Portfolio Construction
        df_poids_opt = df_poids.set_index("Stock")
        optimized_portfolio=0
        exclude_columns = ["MASI", "SNA","LES"]
        for elem in df.columns:
            if elem not in  exclude_columns:
                poids = df_poids_opt.loc[elem].values
                optimized_portfolio += poids/100 * df[elem]

        #Plot
        trace_perf(optimized_portfolio,df["MASI"])

        #Addictional metrics
        st.write("Additional Metrics :")
        metrics(optimized_portfolio,df["MASI"])

    elif contra == "No" :
        ef = EfficientFrontier(mu,S)

        weights = ef.max_sharpe()

        clean_weights = ef.clean_weights()

        df_poids = pd.DataFrame(list(clean_weights.items()), columns=['Stock', 'Poids %'])
        df_poids["Poids %"] *= 100
        st.subheader("Optimized Portfolio Weights")
        st.write(df_poids.sort_values(by="Poids %", ascending=False))
        st.subheader("Optimized Portfolio Allocation")
        trace_pie(df_poids)

        st.subheader("Optimized Portfolio Performance")
        # Portfolio Construction
        df_poids_opt = df_poids.set_index("Stock")
        optimized_portfolio=0
        exclude_columns = ["MASI", "SNA","LES"]
        for elem in df.columns:
            if elem not in  exclude_columns:
                poids = df_poids_opt.loc[elem].values
                optimized_portfolio += poids/100 * df[elem]

        #Plot
        trace_perf(optimized_portfolio,df["MASI"])

        #Addictional metrics
        st.write("Additional Metrics :")
        metrics(optimized_portfolio,df["MASI"])