from Functions.functions import *
from Functions.mylibraries import *
from Functions.startegies import *


def app():
    st.header("Introduction to the Trading Strategy page")
    st.write("Welcome to the Trading Strategy page. Here, you can select a stock symbol, choose a trading strategy, and backtest it to see how it performs")
    st.subheader("Stock Symbol Selection")
    dataframes = load_data()
    stock_list = ["ATW","IAM","BCP","LHM","BOA","TQM","CMA","TMA","ADH","TGC","CDM","ATL","BCI","AKT","SAH","CFG","ARD","ADI","DYT","ATH","RDS","DHO","FBR"]
    marche = ["Marché Haussier","Marché Baissier"]
    dataframes = {key: reorganize(df) for key, df in dataframes.items()}
    for key, df in dataframes.items():
        df.index.name = None
        df.index = pd.to_datetime(df.index)

    stock_symbol = st.selectbox('Select Stock Symbol', stock_list,key='st')

    st.subheader("Strategy Selection")
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
                                'n2': range(20, 210, 10),
                                'constraint': lambda p: 20 < p.n2 - p.n1}
    }
    }

    marche = ["Marché Haussier","Marché Baissier"]
    market = st.selectbox('Select market trend', marche,key='mar')
    high_volatility_df = st.session_state['high_volatility_df']
    low_volatility_df = st.session_state['low_volatility_df']
    high_volatility_df_stocks = high_volatility_df["Key"].tolist()
    high_volatility_df_stocks.remove("CFG")
    low_volatility_df_stocks = low_volatility_df["Key"].tolist()
    
    if market == "Marché Haussier":
        for elem in high_volatility_df_stocks:
            if elem in dataframes:
                #optimize_strategies(dataframes[elem], strategies)
                st.write(elem)
                bt = Backtest(dataframes[elem], SmaCross, cash=1_000_000, commission=0.0044)
                stats = bt.run()
                st.write(stats)
    else :
        for elem in low_volatility_df_stocks:
            if elem in dataframes:
                st.write(elem)
                bt = Backtest(dataframes[elem], SmaCross, cash=1_000_000, commission=0.0044)
                stats = bt.run()
                st.write(stats)

    strategy_name = st.selectbox('Choose a strategy', strategies,key='stat')
    strategy = strategies[strategy_name]

    st.subheader(f"Strategy: {strategy_name}")
    st.write(f"**:orange[Description]:** {strategy['description']}")
    st.write(f"**:green[Entry Condition]:** {strategy['entry']}")
    st.write(f"**:red[Exit Condition]:** {strategy['exit']}")

    bt = Backtest(dataframes[stock_symbol], strategy["symbol"], cash=1_000_000, commission=0.0044)
    
    if st.button("Backtest Strategy"):
        stats = bt.run()
        st.write("Backtest Results")
        st.write(stats)
        

    st.subheader("Strategy Optimization")
    if st.button("Optimize Strategy"):
        with st.spinner('In progress...'):
            optim = bt.optimize(maximize="Return [%]",
                            **strategy["optimize_params"])
            st.write(optim)
            #bt.plot()
        st.divider()
        st.subheader(f"Optimized Strategy Parameters :white_check_mark: : {optim['_strategy']}")

    
    
    
