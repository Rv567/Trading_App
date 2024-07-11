from Functions.functions import *
from Functions.mylibraries import *
from Functions.startegies import *


def app():
    st.header("Introduction to the Trading Strategy page")
    st.write("Welcome to the Trading Strategy page. Here, you can define the best trading strategy for each stock.")
    #st.subheader("Stock Symbol Selection")
    dataframes = load_data()
    stock_list = ["ATW","IAM","BCP","LHM","BOA","TQM","CMA","TMA","ADH","TGC","CDM","ATL","BCI","AKT","SAH","CFG","ARD","ADI","DYT","ATH","RDS","DHO","FBR"]
    
    dataframes = {key: reorganize(df) for key, df in dataframes.items()}
    for key, df in dataframes.items():
        df.index.name = None
        df.index = pd.to_datetime(df.index)
    

    strategies = {
        'SMA Cross Strategy': {
            'description': 'Simple Moving Average Crossover Strategy',
            'entry': 'Buy when short-term SMA crosses above long-term SMA',
            'exit': 'Sell when short-term SMA crosses below long-term SMA',
            "symbol" : SmaCross,
            "optimize_params": {'n1': range(20, 110, 10),
                                'n2': range(20, 210, 10)}
        },
        'SMA Cross Strategy with Stop Loss': {
            'description': 'Simple Moving Average Crossover Strategy combined with a Trailing Stop Loss',
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
    ### Key Points:
    - For an **uptrend market**, stocks with a **Beta > 1** are selected.
    - For a **downtrend market**, stocks with a **Beta < 1** are selected.
    """)

    if 'stock_strategy_return_high' not in st.session_state:
        st.session_state['stock_strategy_return_high'] = {}

    if 'stock_strategy_return_low' not in st.session_state:
        st.session_state['stock_strategy_return_low'] = {}

    st.subheader("Strategy Optimization")
    if st.button("Optimize"):
        if market == "Marché Haussier":
            
            st.write("Stock with a Beta > 1")
            for elem in high_volatility_df_stocks:
                if elem in dataframes:
                    st.write(elem)
                    best_parameters, optim = optimize_strategies(dataframes[elem], strategies)
                    st.write(f"Optimized Strategy Parameters :white_check_mark: : {best_parameters}")
                    st.session_state['stock_strategy_return_high'][elem] = optim
                    stock_strategy_return_high = st.session_state['stock_strategy_return_high']
            df_return_high = pd.DataFrame(stock_strategy_return_high)
            df_return_high = pd.concat([df_return_high.iloc[[-3]], df_return_high.iloc[:-3]])
            st.write(df_return_high)

                    
        else :
            st.write("Stock with a Beta < 1")
            for elem in low_volatility_df_stocks:
                if elem in dataframes:
                    st.write(elem)
                    best_parameters, optim = optimize_strategies(dataframes[elem], strategies)
                    st.write(f"Optimized Strategy Parameters :white_check_mark: : {best_parameters}")
                    st.session_state['stock_strategy_return_low'][elem] = optim
                    stock_strategy_return_low = st.session_state['stock_strategy_return_low']
            df_return_low = pd.DataFrame(stock_strategy_return_low)
            df_return_low=pd.concat([df_return_low.iloc[[-3]], df_return_low.iloc[:-3]])
            st.write(df_return_low)
        
    """#Beta > 1
    stock_strategy_return_high = st.session_state['stock_strategy_return_high']
    df_return_high = pd.DataFrame(stock_strategy_return_high)
    df_return_high = pd.concat([df_return_high.iloc[[-3]], df_return_high.iloc[:-3]]) #move _strategy to the top
    df_return_high.to_pickle('performance_high.pkl')
    #Beta < 1
    stock_strategy_return_low = st.session_state['stock_strategy_return_low']
    df_return_low = pd.DataFrame(stock_strategy_return_low)
    df_return_low=pd.concat([df_return_low.iloc[[-3]], df_return_low.iloc[:-3]])
    df_return_low.to_pickle('performance_low.pkl')

    if market == "Marché Haussier":
        st.write(pd.read_pickle('performance_high.pkl'))
    else:
        st.write(pd.read_pickle('performance_low.pkl'))"""
    




    """stock_list.remove("CFG")
    stock_symbol = st.selectbox('Choose a Stock to see its performance', stock_list,key='stoc')
    st.write(df[stock_symbol])"""

    
    
    
