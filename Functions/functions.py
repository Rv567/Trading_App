from Functions.mylibraries import *


# I-Data Collection and Preparation
tv = TvDatafeed()
#Market Index
#masi = tv.get_hist(symbol='MASI',exchange='CSEMA',interval=Interval.in_daily,n_bars=70000)

#Load Data
def load_data():
    ticker = ["MASI","ATW", "IAM", "BCP", "LHM", "BOA", "TQM", "CMA", "TMA", "ADH", "TGC", "CDM", "ATL", "BCI", "AKT", "SAH", "CFG", "ARD", "ADI", "DYT", "ATH", "RDS", "DHO", "FBR"]
    dataframes = {}
    for ticker_symbol in ticker:
        df = pd.read_pickle(f'dataframe_{ticker_symbol}.pkl')
        dataframes[ticker_symbol]=df
    return dataframes

#Reoragnize the dataframe with proper names for the columns 
def reorganize(dataframe):
    if 'symbol' in dataframe.columns:
        dataframe = dataframe.drop('symbol', axis=1)
        dataframe.index = pd.to_datetime(dataframe.index).date
    
    # Rename columns
    return dataframe.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }).rename_axis("Date")

#Time series decompostion into (trend, seasonal, and residual)
def decompose(dataframe):
    df_close = dataframe["Close"]

    stl = STL(df_close, period=365)
    result = stl.fit()

    # Create a figure with 3 subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        subplot_titles=('Close Price', 'Trend', 'Seasonal'))

    # Plot original series in the first subplot
    fig.add_trace(go.Scatter(
        x=df_close.index,
        y=df_close,
        mode='lines',
        name='Close',
        line=dict(color='blue', width=2)
    ), row=1, col=1)

    # Plot trend component in the second subplot
    fig.add_trace(go.Scatter(
        x=result.trend.index,
        y=result.trend,
        mode='lines',
        name='Trend',
        line=dict(color='green', width=2)
    ), row=2, col=1)

    # Plot seasonal component in the third subplot
    fig.add_trace(go.Scatter(
        x=result.seasonal.index,
        y=result.seasonal,
        mode='lines',
        name='Seasonal',
        line=dict(color='orange', width=2)
    ), row=3, col=1)

    # Update layout
    fig.update_layout(
        title='Price Decomposition',
        height=900,
        showlegend=False,
        template='plotly_white'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

def max_without_nan(lst):
    filtered_lst = [value for value in lst if not np.isnan(value)]
    
    if not filtered_lst:
        return np.nan
    
    max_val = np.max(filtered_lst)

    return max_val


def best_indicators_category(liste):

    categories = {
    "momentum": ["ADX","MACD" ,"MACD_Hist","MACD_Signal" ,"RSI", "CCI", "STOCH", "ROC", "WR"],
    "overlap": ["lowerband","middleband","upperband","DEMA", "EMA", "MA", "SAR", "SMA"],
    "volatility": ["ATR", "NATR"],
    "volume": ["AD", "ADOSC", "OBV"]}

    # Initialize dictionaries to store the best indicator for each category
    best_indicators = {category: None for category in categories}

    for feature in liste:
        for category, indicators in categories.items():
            # Check if the feature is in the category
            if any(indicator in feature for indicator in indicators):
                # If no best indicator is set for this category
                if best_indicators[category] is None:
                    best_indicators[category] = feature
                    break
    
    return best_indicators

#Liquidity
def measure_liquidity(df):
    window=30
    volume = df["Volume"].rolling(window=window).mean()
    average_volume = volume.mean()
    return average_volume

def beta(df, index_df):

    stock_df = df.copy()
    stock_df.index = pd.to_datetime(stock_df.index)
    stock_df = stock_df.loc["2020-01-01":] # on calcule le beta a partir d'une date
    
    stock_df["Variation"] = stock_df["Close"].pct_change()
    index_df["Variation"] = index_df["Close"].pct_change() 

    combined = pd.DataFrame({"stock": stock_df["Variation"], "index": index_df["Variation"]})
    combined = combined.dropna()
    covariance_matrix  = np.cov(combined["stock"], combined["index"])
    covariance = covariance_matrix[0, 1] # covariance(stock,index)
    variance = np.var(combined["index"])
    beta = covariance / variance
    return beta


def filter_stocks(df, volatility_threshold, liquidity_threshold):
    selected_keys = []
    for key in df.keys():
        #if measure_volatility(df[key]) < volatility_threshold and measure_liquidity(df[key]) > liquidity_threshold:
        if measure_liquidity(df[key]) > liquidity_threshold:
            selected_keys.append(key)
    return selected_keys

#Separate high/low volatility
def high_low_volat(df1,df2):
    list_df=[]
    high_volatility_stocks={}
    low_volatility_stocks={}

    for i,(keys, items) in enumerate(df1.items()):

        if beta(items,df2)>1 :
            high_volatility_stocks[keys]=beta(items, df2)
        else:
            low_volatility_stocks[keys]=beta(items, df2)

    high_volatility_df = pd.DataFrame(list(high_volatility_stocks.items()),columns=["Key",'Beta'])
    list_df.append(high_volatility_df)
    low_volatility_df = pd.DataFrame(list(low_volatility_stocks.items()),columns=["Key",'Beta'])
    list_df.append(low_volatility_df)
    return list_df

def todo(df):
    if df["Prediction Variation%"] > df["Threshold"]:
        return "Buy"
    elif df["Prediction Variation%"] < - df["Threshold"]:
        return "Sell"
    else:
        return "Hold"
    

def plot_scatter_pairs(df, x,y):

    plt.figure(figsize=(8, 6))
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    sns.scatterplot(data=df, x=df[x], y=df[y], color=color)
    plt.title(f'Scatter plot of {x} vs {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    st.pyplot(plt.gcf())

def plot_train_vs_test(df_date,df_actuals,df_y_pred,rmse_test):

    plt.figure(figsize=(10, 6))
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    plt.plot(df_date,df_actuals, label='Actual', color='b')
    plt.plot(df_date,df_y_pred, label='Predicted', color='r')
    plt.title('Actual vs Predicted Test Values')
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.legend()
    plt.text(0.5, 0.9, f'RMSE = {rmse_test}', horizontalalignment='center', verticalalignment='top', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='green', alpha=0.5))

    plt.tight_layout()
    plt.show()
    st.pyplot(plt.gcf())

#Backtest the strategy on the choosen sequence with our list of parameters
def optimize_strategy(data, strategy, param_grid):
    bt = Backtest(data, strategy, cash=1_000_000, commission=0.0044)
    best_score = -np.inf
    best_params = None

    for params in ParameterGrid(param_grid):
        stats = bt.run(**params)
        if stats['Return [%]'] > best_score:
            best_score = stats['Return [%]']
            best_params = params

    return best_params

#Split data into folds
#We optimize on in-sample
#We test on out-sample

def walk_forward_analysis(data, strategy, param_grid, n_splits=5):
    # Split data into segments
    segment_size = len(data) // n_splits
    results = []
    
    for i in range(n_splits):
        in_sample = data[:segment_size * (i+1)]
        out_of_sample = data[segment_size * (i+1):segment_size * (i+2)]

        if len(out_of_sample) == 0:
            break

        # Optimize on in-sample data
        best_params = optimize_strategy(in_sample, strategy, param_grid)

        # Test on out-of-sample data with the best parameters
        bt = Backtest(out_of_sample, strategy, cash=1_000_000, commission=0.0044)
        stats = bt.run(**best_params)
        print(best_params)
        results.append(stats)

    return results
def optimize_strategies(dataframe, strategies):
    
    best_strategy = None
    best_return = float('-inf')
    best_parameters = None

    for strategy_name, strategy in strategies.items():
        bt = Backtest(dataframe, strategy["symbol"], cash=1_000_000, commission=0.0044)
        stats = bt.run()
        optim = bt.optimize(maximize="Return [%]", **strategy["optimize_params"])
        
        
        if optim['Return [%]'] > best_return:
            best_return = optim['Return [%]']
            best_strategy = strategy_name
            best_parameters = optim["_strategy"]

    return best_parameters, optim
    #return best_strategy, best_parameters

def backtest_ML(data):
    
    # Parameters
    initial_cash = 1000000
    cash = initial_cash
    shares = 0
    portfolio_values = []
    position = False

    # Trading simulation
    for index, row in data.iterrows():
        price = row['Actual Close']
        signal = row['Decision']
        
        if signal == 'Buy' and not position:
            shares_to_buy = cash / price
            if shares_to_buy > 0:
                shares += shares_to_buy
                cash -= shares_to_buy * price
                position = True
        
        elif signal == 'Sell' and position:
            cash += shares * price
            shares = 0
            position = False
        
        portfolio_value = cash + shares * price
        portfolio_values.append(portfolio_value)

    data['portfolio_value'] = portfolio_values

    # Performance calculation
    total_return = (data['portfolio_value'].iloc[-1] - initial_cash) / initial_cash
    annualized_return = (1 + total_return) ** (365 / len(data)) - 1

    print(f"Total Return: {total_return:.2%}")
    print(f"Annualized Return: {annualized_return:.2%}")

    # Plotting portfolio value over time
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['portfolio_value'], label='Portfolio Value')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.legend()
    plt.show()
