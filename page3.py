from Functions.functions import *
from Functions.mylibraries import *
from Functions.startegies import *


def app():
    st.header("Introduction to the Trading Strategy page")
    st.write("Welcome to the Trading Strategy page. Here, you can define the best trading strategy for each stock.")
    
    dataframes = load_data()
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
                                'n2': range(20, 210, 10),
                                "constraint": lambda p: p.n1<p.n2}
        },
        'SMA Cross Strategy with Stop Loss': {
            'description': 'Simple Moving Average Crossover Strategy combined with a Trailing Stop Loss',
            'entry': 'Buy when short-term SMA crosses above long-term SMA',
            'exit': 'Sell when the Stop Loss is triggered',
            "symbol" : SmaCross_StopLoss,
            "optimize_params": {'n1': range(20, 110, 10),
                                'n2': range(20, 210, 10),
                                "constraint": lambda p: p.n1<p.n2,
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

    if 'high_volatility_df' in st.session_state and 'low_volatility_df' in st.session_state:
        high_volatility_df = st.session_state['high_volatility_df']
        low_volatility_df = st.session_state['low_volatility_df']

    high_volatility_df_stocks = high_volatility_df["Key"].tolist()
    high_volatility_df_stocks.remove("CFG")
    low_volatility_df_stocks = low_volatility_df["Key"].tolist()
    dff = st.session_state['Newdict_df']
    #st.write(dff.keys())

    
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
            #st.write(high_volatility_df_stocks)
            for elem in high_volatility_df_stocks:
                if elem in dataframes:
                    st.write(elem)
                    best_parameters, optim, last_trade = optimize_strategies(dataframes[elem], strategies)
                    st.write(f"Optimized Strategy Parameters for {elem} :white_check_mark: : {best_parameters}")
                    stock_strategy_return_high[elem] = optim
                    trades_high[elem] = last_trade

            df_return_high = pd.DataFrame(stock_strategy_return_high)
            df_return_high = pd.concat([df_return_high.iloc[[-3]], df_return_high.iloc[:-3]])
            df_return_high.to_pickle('performance_high.pkl')
            

            df_trades_high = pd.DataFrame(trades_high)
            df_trades_high.to_pickle('trades_high.pkl')
                    
        elif market == "Marché Baissier" :
            st.write("Stock with a Beta < 1")
            #st.write(low_volatility_df_stocks)
            for elem in low_volatility_df_stocks:
                if elem in dataframes:
                    st.write(elem)
                    best_parameters, optim,last_trade = optimize_strategies(dataframes[elem], strategies)
                    st.write(f"Optimized Strategy Parameters {elem} :white_check_mark: : {best_parameters}")
                    stock_strategy_return_low[elem] = optim
                    trades_low[elem] = last_trade
                

            df_return_low = pd.DataFrame(stock_strategy_return_low)
            df_return_low=pd.concat([df_return_low.iloc[[-3]], df_return_low.iloc[:-3]])
            df_return_low.to_pickle('performance_low.pkl')
            
            df_trades_low = pd.DataFrame(trades_low)
            #st.write(df_trades_low)
            df_trades_low.to_pickle('trades_low.pkl')
            
    # Beta>1
    st.subheader("Corresponding Stocks performance for an **:green[uptrend market]**")
    df_high = pd.read_pickle('performance_high.pkl')
    mod_high,date = modify_big(df_high)
    st.write(f"The backtest begins from from the start date of each stock to {date}")
    st.write(mod_high)

    ######### Defining perf metrics
    st.subheader(":blue[Performance Metrics Definition]")
    metrics = ["Return [%]","Buy & Hold Return [%]","Return (Ann.) [%]","Volatility (Ann.) [%]","Sharpe Ratio","Max. Drawdown [%]","Avg. Drawdown [%]","Win Rate [%]","Avg. Trade[%]","Profit Factor","Expectancy [%]"]
    metrics_def = ["The total percentage gain or loss on an investment over a specified period.  $$ \\text{Return} = \\left( \\frac{V_f - V_i}{V_i} \\right) \\times 100 $$",
                   "The return if the asset was bought at the start and held until the end of the period, without any trading.  $$ \\text{Buy_and_Hold_Return} = \\left( \\frac{P_{end} - P_{start}}{P_{start}} \\right) \\times 100 $$",
                   "The annualized return, representing the geometric average amount of money earned by an investment each year over a given time period.  $$ R_{ann} = \\left( \\frac{V_f}{V_i} \\right)^{\\frac{1}{T}} - 1 $$",
                   "The annualized standard deviation of returns, measuring the dispersion of returns  $$ \\sigma_{ann} = \\sigma_{daily} \\times \\sqrt{252} $$",
                   "A measure of risk-adjusted return, calculated as the ratio of the portfolio's excess return over the risk-free rate to its standard deviation.  $$ SR = \\frac{R_p - R_f}{\\sigma_p} $$",
                   "The maximum observed loss from a peak to a trough of a portfolio before a new peak is attained. $$ DD_{max} = \\max \\left( \\frac{V_{peak} - V_{trough}}{V_{peak}} \\right) \\times 100 $$",
                   "The average of all drawdowns over the specified period.  $$ DD_{avg} = \\frac{1}{N} \\sum_{i=1}^{N} DD_i \\times 100 $$",
                   "The percentage of trades that were profitable.  $$ WR = \\left( \\frac{\\text{Number of Winning Trades}}{\\text{Total Number of Trades}} \\right) \\times 100 $$",
                   "The average return per trade over the specified period.  $$ \\text{Avg. Trade} = \\frac{1}{N} \\sum_{i=1}^{N} \\text{Trade Return}_i \\times 100 $$",
                   "The ratio of gross profit to gross loss.  $$ PF = \\frac{\\text{Gross Profit}}{\\text{Gross Loss}} $$",
                   "The average expected return per trade, calculated as the product of the win probability and the average win minus the product of the loss probability and the average loss.  $$ E = P_w \\times W - P_l \\times L $$"]
    result_dict = dict(zip(metrics, metrics_def))
    mertic_name = st.selectbox("Choose a Performance Metric to Understand its use",metrics,key='met')
    st.write(f"**{result_dict[mertic_name]}**")
    #########
    st.subheader("Last trade for an **:green[uptrend market]**")
    df_trades_high = pd.read_pickle('trades_high.pkl')
    st.write(modify_small(reorganize_trades(df_trades_high)))

    # Beta<1
    st.subheader("Corresponding Stocks performance for a **:red[downtrend market]**")
    df_low = pd.read_pickle('performance_low.pkl')
    mod_low,date = modify_big(df_low)
    st.write(f"The backtest begins from from the start date of each stock to {date}")
    st.write(mod_low)

    st.subheader("Last trade for a **:red[downtrend market]**")
    df_trades_low = pd.read_pickle('trades_low.pkl')
    st.write(modify_small(reorganize_trades(df_trades_low)))
    
    

