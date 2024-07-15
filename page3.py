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

    st.header("Market Trend Selection")
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


    stock_strategy_return_high = {}
    stock_strategy_return_low = {}
    df_return_high = {}
    df_return_low = {}
    trades_high = {}
    trades_low = {}

    custom_button_css = """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
    """

    # Inject CSS into the Streamlit app
    st.markdown(custom_button_css, unsafe_allow_html=True)

    st.header("Strategy Optimization")
    if st.button("Optimize 🚀"):
        if market == "Marché Haussier":
            #st.write(pd.read_pickle('performance_high.pkl'))
            st.write("Stock with a Beta > 1")
            for elem in high_volatility_df_stocks:
                if elem in dataframes:
                    best_parameters, optim, last_trade = optimize_strategies(dataframes[elem], strategies)
                    st.write(f"Optimized Strategy Parameters :white_check_mark: : {best_parameters}")
                    stock_strategy_return_high[elem] = optim
                    trades_high[elem] = last_trade
                    print(trades_high[elem])

            df_return_high = pd.DataFrame(stock_strategy_return_high)
            df_return_high = pd.concat([df_return_high.iloc[[-3]], df_return_high.iloc[:-3]])
            df_return_high.to_pickle('performance_high.pkl')
            

            df_trades_high = pd.DataFrame(trades_high)
            df_trades_high.to_pickle('trades_high.pkl')
                    
        else :
            st.write("Stock with a Beta < 1")
            for elem in low_volatility_df_stocks:
                if elem in dataframes:
                    best_parameters, optim,last_trade = optimize_strategies(dataframes[elem], strategies)
                    st.write(f"Optimized Strategy Parameters :white_check_mark: : {best_parameters}")
                    stock_strategy_return_low[elem] = optim
                    trades_low[elem] = last_trade
                

            df_return_low = pd.DataFrame(stock_strategy_return_low)
            df_return_low=pd.concat([df_return_low.iloc[[-3]], df_return_low.iloc[:-3]])
            df_return_low.to_pickle('performance_low.pkl')
            
            df_trades_low = pd.DataFrame(trades_low)
            df_trades_low.to_pickle('trades_low.pkl')
            

    st.subheader("Corresponding Stocks performance for an **:green[uptrend market]**")
    df_high = pd.read_pickle('performance_high.pkl')
    st.write(df_high)

    st.subheader("Last trade for an **uptrend market**")
    df_trades_high = pd.read_pickle('trades_high.pkl')
    st.write(reorganize_trades(df_trades_high))


    st.subheader("Corresponding Stocks performance for a **:red[downtrend market]**")
    df_low = pd.read_pickle('performance_low.pkl')
    st.write(df_low)

    st.subheader("Last trade for an **downtrend market**")
    df_trades_low = pd.read_pickle('trades_low.pkl')
    st.write(reorganize_trades(df_trades_low))
    

