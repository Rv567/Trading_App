from Functions.mylibraries import *


# I-Data Collection and Preparation
tv = TvDatafeed()
#Market Index
#masi = tv.get_hist(symbol='MASI',exchange='CSEMA',interval=Interval.in_daily,n_bars=70000)

#Load Data
def load_data():
    ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
    dataframes = {}
    for ticker_symbol in ticker:
        dataframes[ticker_symbol]=pd.read_pickle(f'dataframe_{ticker_symbol}.pkl')
    return dataframes

def load_data_weekly():
    ticker = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]
    dataframes = {}
    for ticker_symbol in ticker:
        dataframes[ticker_symbol]=pd.read_pickle(f'dataframe_weekly_{ticker_symbol}.pkl')
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

def reorganize2(dataframe,ticker):
    if 'symbol' in dataframe.columns:
        dataframe = dataframe.drop('symbol', axis=1)
        dataframe.index = pd.to_datetime(dataframe.index).date
        dataframe.index = pd.to_datetime(dataframe.index)
    # Rename columns
    return dataframe.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': f'{ticker}',
        'volume': 'Volume'
    }).rename_axis("Date")

def reorganize_trades(df):
    df_transposed = df.transpose()

    # Rename the columns to the first row and then drop the first row
    selected_columns = ['EntryTime',"ExitTime", 'EntryPrice', 'ReturnPct']
    df_transposed = df_transposed[selected_columns]
    df_transposed=df_transposed.rename(columns={"EntryTime":"Entry Time","ExitTime":"Exit Time","EntryPrice":"Entry Price","ReturnPct":"Perf %"})
    df_transposed["Perf %"]=df_transposed["Perf %"]*100
    return df_transposed
    
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
    window=252 # yearly
    total = df["Close"] * df["Volume"]
    volume = total.rolling(window=window).mean()
    average_volume = volume.mean()
    return average_volume

def beta(df, df_marketIndex): #3-Year Beta

    df_stock = df.copy()
    df_stock.index = pd.to_datetime(df_stock.index)
    df_marketIndex.index = pd.to_datetime(df_marketIndex.index)

    df_stock = df_stock.loc["2021-01-01":] # on calcule le beta a partir d'une date
    df_marketIndex = df_marketIndex.loc["2021-01-01":]

    
    df_stock["Variation"] = df_stock["Close"].pct_change()
    df_marketIndex["Variation"] = df_marketIndex["Close"].pct_change() 

    combined = pd.DataFrame({"stock": df_stock["Variation"], "index": df_marketIndex["Variation"]})
    combined = combined.dropna()
    covariance_matrix  = np.cov(combined["stock"], combined["index"])
    covariance = covariance_matrix[0, 1] # covariance(stock,index)
    variance = np.var(combined["index"])
    beta = covariance / variance
    return beta

def newbeta(stock_returns, index_returns):

    combined = pd.DataFrame({"stock": stock_returns, "index": index_returns})
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
    if df["Prediction Next Week Variation%"] > df["Median50%"]:
        return "Buy"
    elif df["Prediction Next Week Variation%"] < - df["Median50%"]:
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
    best_optim = None

    total_strategies = len(strategies)
    progress = 0
    progress_bar = st.progress(0)
    status_text = st.empty()

    for strategy_name, strategy in strategies.items():
        progress += 1
        status_text.text(f"Optimizing strategy: {strategy_name} ({progress}/{total_strategies})")
    
        bt = Backtest(dataframe, strategy["symbol"], cash=1_000_000, commission=0.0088)
        optim = bt.optimize(maximize="Return [%]", **strategy["optimize_params"])

        if optim['Return [%]'] > best_return:
            best_return = optim['Return [%]']
            best_parameters = optim["_strategy"]
            last_trade = optim["_trades"].iloc[-1]
            best_optim = optim

        # Update progress bar
        progress_bar.progress(progress / total_strategies)

    status_text.text("Optimization completed.")
    return best_parameters, best_optim, last_trade
    #return best_strategy, best_parameters

def remove_time(duration):
        return duration.split()[0]

def modify_big(df):
    rows_to_remove = ['Duration', 'Exposure Time [%]', 'Profit Factor', 'Expectancy [%]', 'SQN']
    indices_to_remove = [3,4,5,6,12,13,15,16,17,27]
    df_filtered = df.drop(df.index[indices_to_remove])
    df_rounded = df_filtered.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
    for i in [1,2]:
        df_rounded.iloc[i] = pd.to_datetime(df_rounded.iloc[i], errors='coerce').dt.strftime("%d-%m-%Y")

    store_endDate = df_rounded.iloc[2,1]
    df_rounded = df_rounded.drop(df.index[2])

    i=1
    for i in range(len(df_rounded.columns)):
        df_rounded.iloc[13,i] = str(pd.Timedelta(df_rounded.iloc[13,i]).days) + " days"

        df_rounded.iloc[14,i] = str(pd.Timedelta(df_rounded.iloc[14,i]).days) + " days"

    return df_rounded,store_endDate

def modify_small(df):
    df_rounded = df.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
    df_rounded["Entry Time"] = pd.to_datetime(df_rounded["Entry Time"], errors='coerce').dt.date
    df_rounded["Exit Time"] = pd.to_datetime(df_rounded["Exit Time"], errors='coerce').dt.date

    return df_rounded

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



def trace_pie(df_poids):
    df_poids_filtered = df_poids[df_poids['Poids %'] > 0]

    fig = px.pie(
    df_poids_filtered, 
    values='Poids %', 
    names='Stock', 
    title='Stock Weights in Portfolio',
    color_discrete_sequence=px.colors.sequential.Plasma
    )

    # Update the pie chart layout for better readability and aesthetics
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label'
    )
    fig.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide', 
        title_font_size=18, 
        legend_title_text='Stocks',
        title={
            'text': "Stock Weights in Portfolio",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
            height=650,  # Set the height of the figure
            width=650 
    )

    st.plotly_chart(fig)


def trace_perf(portfolio,benchmark):

    # Calculate necessary metrics
    portfolio_volatility = qs.stats.volatility(portfolio, periods=252) * 100
    benchmark_volatility = qs.stats.volatility(benchmark, periods=252) * 100
    portfolio_returns = qs.stats.compsum(portfolio)[-1] * 100
    benchmark_returns = qs.stats.compsum(benchmark)[-1] * 100
    portfolio_sharpe = qs.stats.sharpe(portfolio)
    benchmark_sharpe = qs.stats.sharpe(benchmark)

    # Create figure
    fig = go.Figure()

    # Create scatter trace
    scatter_trace = go.Scatter(
        x=[portfolio_volatility, benchmark_volatility],
        y=[portfolio_returns, benchmark_returns],
        mode='markers+text',
        marker=dict(
            size=75,
            color=[portfolio_sharpe, benchmark_sharpe],
            colorscale='Bluered_r',
            colorbar=dict(title='Sharpe Ratio'),
            showscale=True
        ),
        name='Returns',
        text=['Portfolio', 'Benchmark'],
        textposition='middle center',
        textfont=dict(color='white'),
        hovertemplate='%{y:.2f}%<br>Annualized Volatility: %{x:.2f}%<br>Sharpe Ratio: %{marker.color:.2f}',
        showlegend=False
    )

    # Add trace to figure
    fig.add_trace(scatter_trace)

    # Configuring layout
    fig.update_layout(
        title={'text': '<b>Portfolio vs Benchmark</b> : Risk-Return Profils', 'x': 0.5, 'xanchor': 'center','yanchor': 'top'},
        template='plotly_white',
        height=700,
        width=1000,
        hovermode='x unified'
    )

    fig.update_yaxes(title_text='Cumulative Returns (%)')
    fig.update_xaxes(title_text='Annualized Volatility (%)')

    st.plotly_chart(fig)


def metrics(portfolio,masi):
    metrics_masi = {
                "Win Rate%": np.round(qs.stats.win_rate(masi)*100,2),
                "Max Drawdown%": np.round(qs.stats.max_drawdown(masi)*100,2),
                "VaR at 95%": np.round(qs.stats.var(masi) * -100,2)
            }
    
    metrics_portfolio = {
                "Win Rate%": np.round(qs.stats.win_rate(portfolio)*100,2),
                "Max Drawdown%": np.round(qs.stats.max_drawdown(portfolio)*100,2),
                "VaR at 95%": np.round(qs.stats.var(portfolio) * -100,2)
            }
    df = pd.DataFrame(metrics_masi, index=["MASI"])
    df.loc["Portfolio"]=metrics_portfolio

    st.write(df)
    st.write("VaR Interpretation :")
    st.write(f'The Value at Risk (VaR) at 95% confidence level being {df["VaR at 95%"].iloc[1]}% on a daily basis means that, under normal market conditions, there is a 95% probability that the portfolio will not lose more than {df["VaR at 95%"].iloc[1]}% of its value in a single day.')


def generate_random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))

def trace_fundamental(df_sec,industry,metric):
    random_color = generate_random_color()
    fig = go.Figure(data=[
        go.Bar(x=df_sec['Name'], y=df_sec[metric], text=df_sec[metric], textposition='auto',name=f"{metric}",marker=dict(color=random_color))
        ])
    fig.add_trace(go.Scatter(
        x=df_sec['Name'], 
        y=[df_sec[metric].mean()] * len(df_sec['Name']),  # Repeat the mean value
        mode='lines',
        line=dict(color='red', dash='dash'),  # Customize line color and style
        name=f'Mean {metric} = {df_sec[metric].mean():.2f}'
    ))

        # Adding title and labels
    fig.update_layout(
            title=f'{metric} of {industry} stocks',
            xaxis_title='Stock',
            yaxis_title=f'{metric}'
        )

    st.plotly_chart(fig,use_container_width=True)


def trace_gauge(metric,company_value,industry_value):
    # Create the gauge charts as subplots
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
        horizontal_spacing=0.2
    )

    # Add the gauge for the company value
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=company_value,
        title={'text': f"Company {metric}"},
        gauge={
            'axis': {'range': [0, 40], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "lightcyan"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 10], 'color': "red"},
                {'range': [10, 20], 'color': "orange"},
                {'range': [20, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "green"}],
            'threshold': {
                'line': {'color': "lightblue", 'width': 4},
                'thickness': 0.75,
                'value': company_value}}),
        row=1, col=1)

    # Add the gauge for the industry value
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=industry_value,
        title={'text': f"Sector {metric}"},
        gauge={
            'axis': {'range': [0, 40], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "lightcyan"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 10], 'color': "red"},
                {'range': [10, 20], 'color': "orange"},
                {'range': [20, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "green"}],
            'threshold': {
                'line': {'color': "lightblue", 'width': 4},
                'thickness': 0.75,
                'value': industry_value}}),
        row=1, col=2)

    # Update the layout
    fig.update_layout(
        title=f"{metric} - Company vs Sector",
        font={'color': "white", 'family': "Arial"},
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117"
    )

    st.plotly_chart(fig,use_container_width=True)

def metric_definition(df,stock_symbol,metric):

        company_value = df.set_index("Name").loc[stock_symbol][metric]
        industry = df.set_index("Name").loc[stock_symbol]["Industry"] # get the sector automaticly
        industry_value = df[df["Industry"]==industry][metric].mean()
        df_sec = df[df["Industry"]==industry]

        return company_value,industry,industry_value,df_sec
