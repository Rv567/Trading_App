from Functions.functions import *
from Functions.mylibraries import *
from Functions.startegies import *


def app():
    st.header("Introduction to the Trading Strategy page")
    st.write("Welcome to the Trading Strategy page. Start by selecting the market trend (uptrend or downtrend). Based on your choice, you'll be presented with stocks having a beta > 1 (for uptrend) or stocks with a beta < 1 (for downtrend). Then, you will get the corresponding trading strategy.")
    #st.subheader("Stock Symbol Selection")
    dataframes = load_data()
    stock_list = ["ATW","IAM","BCP","LHM","BOA","TQM","CMA","TMA","ADH","TGC","CDM","ATL","BCI","AKT","SAH","CFG","ARD","ADI","DYT","ATH","RDS","DHO","FBR"]
    
    dataframes = {key: reorganize(df) for key, df in dataframes.items()}
    for key, df in dataframes.items():
        df.index.name = None
        df.index = pd.to_datetime(df.index)
    

    strategies = {
        'MAcross strategy with Stop Loss': {
            'description': 'Moving Average Crossover Strategy combined with a Trailing Stop Loss',
            'entry': 'Buy when short-term SMA crosses above long-term SMA',
            'exit': 'Sell when the Stop Loss is triggered',
            "symbol" : SmaCross_StopLoss,
            "optimize_params": {'n1': range(20, 110, 10),
                                'n2': range(20, 210, 10),
                                "trailing_stop" : range(1,11,1)}

        },
        'Multi Indicator Strategy': {
            'description': 'Strategy that combines 4 indicators at once RSI, SMA, ATR and AD',
            'entry': 'Buy when 3 out of 4 signals are valid',
            'exit': 'Sell when the Stop Loss is triggered',
            "symbol" : MultiIndicatorStrategy,
            "optimize_params": {"level_rsi" : range(10,45,1),
                                "n_sma" : range(20,110,10),
                                "trailing_stop" : range(1,11,1)}
        },
        'SMA Crossover': {
            'description': 'Simple Moving Average Crossover Strategy',
            'entry': 'Buy when short-term SMA crosses above long-term SMA',
            'exit': 'Sell when short-term SMA crosses below long-term SMA',
            "symbol" : SmaCross,
            "optimize_params": {'n1': range(20, 110, 10),
                                'n2': range(20, 210, 10)}
    }
    }

    strategy_name = st.selectbox("Choose a Trading Strategy to Understand its Function",strategies,key='stat')
    strategy = strategies[strategy_name]

    st.subheader(f"Strategy: {strategy_name}")
    st.write(f"**:orange[Description]:** {strategy['description']}")
    st.write(f"**:green[Entry Condition]:** {strategy['entry']}")
    st.write(f"**:red[Exit Condition]:** {strategy['exit']}")

    st.subheader("Market Trend Selection")
    marche = ["Marché Haussier","Marché Baissier"]
    market = st.selectbox('Select Market Trend', marche,key='mar')
    high_volatility_df = st.session_state['high_volatility_df']
    low_volatility_df = st.session_state['low_volatility_df']
    high_volatility_df_stocks = high_volatility_df["Key"].tolist()
    high_volatility_df_stocks.remove("CFG")
    low_volatility_df_stocks = low_volatility_df["Key"].tolist()
    
    st.markdown("""
    **Key Points:**
    - For an **uptrend market**, stocks with a **beta > 1** are selected.
    - For a **downtrend market**, stocks with a **beta < 1** are selected.
    """)


    st.subheader("Strategy Optimization")
    stock_strategy_return = {}
    if market == "Marché Haussier":
        st.write("Stock with a Beta > 1")
        for elem in high_volatility_df_stocks:
            if elem in dataframes:
                st.write(elem)
                best_parameters, optim = optimize_strategies(dataframes[elem], strategies)
                stock_strategy_return[elem]=optim
                st.write(f"Optimized Strategy Parameters :white_check_mark: : {best_parameters}")
                
    else :
        st.write("Stock with a Beta < 1")
        for elem in low_volatility_df_stocks:
            if elem in dataframes:
                st.write(elem)
                best_parameters, optim = optimize_strategies(dataframes[elem], strategies)
                stock_strategy_return[elem]=optim
                st.write(f"Optimized Strategy Parameters :white_check_mark: : {best_parameters}")

    
    stock_list.remove("CFG")
    stock_symbol = st.selectbox('Choose a Stock to see its performance', stock_list,key='stoc')
    st.write(stock_strategy_return[stock_symbol])

    
    
    
