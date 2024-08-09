from Functions.functions import *
from Functions.mylibraries import *


def app():
    st.header('Brief introduction to the page and its functionalities')
    st.write("Welcome to the Stock Market Visualization page. Here, you can explore recent close prices, filter stocks by liquidity, and classify them based on their beta values.")

    st.header("Stock Ticker Selection")
    #We load our entire data from pickle files
    dataframes = load_data()
    stock_list = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"]

    dataframes = {key: reorganize(df) for key, df in dataframes.items()}

    stock_color = {symbol: "#{:02x}{:02x}{:02x}".format(random.randint(0, 255),
                                                    random.randint(0, 255),
                                                    random.randint(0, 255))
                for symbol in stock_list}

    #st.write(dataframes["ATW"]["Close"].iloc[-1]) #check last price
    stock_symbol = st.selectbox('Select Stock Symbol', stock_list,key='stock1')
    
    #st.write(dataframes[stock_symbol].tail(10))

    st.subheader(f'Historical Closing Prices for {stock_symbol}')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=dataframes[stock_symbol].index,
    y=dataframes[stock_symbol]["Close"],
    mode='lines',
    line=dict(color=stock_color[stock_symbol])
    ))


    fig.update_layout(
        title={
        'text': f"Close Prices for {stock_symbol}",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        xaxis_title="Time",
        yaxis_title="Close Price",
        margin=dict(l=40, r=40, t=40, b=40),
        width=800,
        height=400
    )

    last_close_price = dataframes[stock_symbol]["Close"].iloc[-1]

    fig.add_annotation(
    x=dataframes[stock_symbol].index[-1],
    y=last_close_price,
    text=f'Last Close: {last_close_price:.2f}',
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(
        size=13,
        color=stock_color[stock_symbol]
    ),
    align="center",
    arrowcolor="grey",
    arrowsize=1,
    arrowwidth=2,
    bordercolor="grey",
    borderwidth=2
    )
    st.plotly_chart(fig)

    """st.write("Time series decompostion into (trend, seasonal, and residual)")
    decompose(dataframes[stock_symbol])"""

    #We separate our selected data into high/ low volatility stocks
    st.header('Liquidity Filtering')
    st.write("We filter our list of stocks by liquidity.")
    st.write("Select the Volume Threshold :")
    threshold = st.slider('Volume', min_value=100000, max_value=30000000, value=2000000, step=100000)
    fst = filter_stocks(dataframes, 0.7, threshold)
    Newdict_df = {key:value for key,value in dataframes.items() if key in fst}# our working df came for liquidity threshold
    st.session_state['Newdict_df'] = Newdict_df # store it for page2
    st.markdown("""
        **Volume Calculation:**
        - The formula for volume is given by:
        $$
        \\text{Volume} = \\text{Quantity} \\times \\text{Close Price}
        $$
        - The average volume of a stock is calculated using a 252-day rolling mean (dynamic average of previous 252 days).
        """)

    st.subheader("Stocks meeting the liquidity criteria")
    st.write(Newdict_df.keys())
    st.header("Beta Classification")
    st.write("We split the selected stocks into High/Low volatility stocks")
    list_df = high_low_volat(Newdict_df,dataframes["MASI"])

    st.subheader('Stocks with Beta > 1')
    st.dataframe(list_df[0])
    st.session_state['high_volatility_df'] = list_df[0] # store it for page2
    st.subheader('Stocks with Beta < 1')
    st.session_state['low_volatility_df'] = list_df[1]
    st.dataframe(list_df[1])

    st.markdown("""
    #### Key Points:
    **Beta measures how much a stock's price moves compared to the overall market. It's calculated based on 3 Years data.**
    - **Beta = 1**: The stock moves exactly in line with the market.
    - **Beta > 1**: The stock is more volatile than the market.
    - **Beta < 1**: The stock is less volatile than the market.
    """)
    st.header('Stock Risk-Return Profile')

    #Plot2
    #st.write('Comparison of Cumulative Returns vs. Annualized Volatility')

    individual_cumsum = pd.DataFrame()
    annualized_volatility = pd.Series(dtype=float)
    sharp_ratio = pd.Series(dtype=float)

    # Populate example data (replace with your actual calculations)
    for symbol in Newdict_df.keys():
        individual_returns = Newdict_df[symbol]["Close"].pct_change()
        individual_cumsum[symbol] = ((1+individual_returns).cumprod()-1)*100
        annualized_volatility[symbol] = (individual_returns.std()*np.sqrt(252) )*100
        individual_ex_returns = individual_returns - 0.01 / 252
        sharp_ratio[symbol] = individual_ex_returns.mean()*252/ (individual_returns.std()*np.sqrt(252))

    fig = go.Figure()
    sharp_min = min(sharp_ratio)
    sharp_max = max(sharp_ratio)

    
    sharp_color = [sharp_ratio[symbol] for symbol in Newdict_df.keys()]
    text = [f"{symbol} : {sharp_ratio:.2f}" for symbol, sharp_ratio in zip(Newdict_df.keys(), sharp_ratio)]
    # Add traces for each stock symbol
    fig.add_trace(go.Scatter(
            x=annualized_volatility.tolist(),
            y=individual_cumsum.iloc[-1].tolist(),
            mode='markers+text',
            marker=dict(
                size=75,
                color=sharp_color,  # Use actual Sharpe ratio for color
                colorscale='Bluered_r',
                cmin=sharp_min,  # Set min for colorscale
                cmax=sharp_max,  # Set max for colorscale
                colorbar=dict(title='Sharpe Ratio'),
                showscale=True
            ),
            text=text,
            textfont=dict(color='white',size=16),
            hovertemplate='%{y:.2f}%<br>Annualized Volatility: %{x:.2f}%<br>Sharpe Ratio: %{marker.color:.2f}',
            name=symbol,  # Legend label
            showlegend=False,
            textposition="middle center"
        ))

    # Update layout of the figure
    fig.update_layout(
        title='Risk-Return Profile',
        xaxis_title='Annualized Volatility (%)',
        yaxis_title='Cumulative Returns (%)',
        hovermode='closest'
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    st.header('Asset vs. Benchmark')
    stock_list.remove("MASI")
    stock_symbol = st.selectbox('Select an Asset', stock_list,key='st1')

    #Asset
    individual_returns_portfolio = dataframes[stock_symbol]["Close"].pct_change()
    individual_cumsum_portfolio= ((1+individual_returns_portfolio).cumprod()-1)*100
    annualized_volatility_portfolio = (individual_returns_portfolio.std()*np.sqrt(252) )*100
    individual_ex_returns_portfolio = individual_returns_portfolio-0.01 / 252
    sharp_portfolio = (individual_ex_returns_portfolio.mean()/ (individual_returns_portfolio.std()*np.sqrt(252)) ).round(2)
    
    #Benchmark
    individual_returns_bench = dataframes["MASI"]["Close"].pct_change()
    individual_cumsum_bench = ((1+individual_returns_bench).cumprod()-1)*100
    annualized_volatility_bench = (individual_returns_bench.std()*np.sqrt(252) )*100
    individual_ex_returns_bench = individual_returns_bench-0.01 / 252
    sharp_bench = (individual_ex_returns_bench.mean()/ (individual_returns_bench.std()*np.sqrt(252)) ).round(2)


    fig3 = go.Figure()

    # Add the portfolio trace
    fig3.add_trace(go.Scatter(x=individual_cumsum_portfolio.index, 
                            y=individual_cumsum_portfolio,
                            mode='lines', name=f'{stock_symbol}', showlegend=True,
                            hovertemplate='%{y:.2f}%'))

    # Add the benchmark trace
    fig3.add_trace(go.Scatter(x=individual_cumsum_bench.index, 
                            y=individual_cumsum_bench,
                            mode='lines', name='MASI', showlegend=True,
                            hovertemplate='%{y:.2f}%',line=dict(color='green')))

    # Update the layout
    fig3.update_layout(
        title=f'Cumulative Returns Over Time for : <span style="color:lightblue;">{stock_symbol}</span> vs. <span style="color:green;">MASI</span>',
        xaxis_title='Date',
        yaxis_title='Cumulative Returns (%)',
        hovermode='x'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig3,use_container_width=True)

    st.header("Stock Screener")
    st.subheader("Fundamental Analysis Tool")
    st.write("Filter and identify stocks based on various fundamental criteria")

    morocco_url = 'https://scanner.tradingview.com/morocco/scan'

    # Create a query for the Moroccan stock exchange
    query = (Query()
            .select('name', 'close', "Change %", "beta_1_year", "Price to Earnings Ratio (TTM)", 'Price to Book (FY)','dividends_yield',
                    "Net Income (Annual YoY Growth)", "Perf.YTD", 'volume', 'Recommend.All')
            .order_by('market_cap_basic', ascending=False))  # Sort by market cap in descending order
    query.url = morocco_url
    count, df = query.get_scanner_data()
    # apply the formatting function to the column
    #df['Rating'] = df['Recommend.All'].apply(format_technical_rating)

    df.drop(columns=["ticker",'Recommend.All'],inplace=True)
    df = df.rename(columns={"name":"Name","close":"Close","change":"Change %","beta_1_year":"Beta 1Y","price_earnings_ttm":"P/E","price_book_ratio":"P/B","dividends_yield":"Div Yield %","net_income_yoy_growth_fy":"Net Income Growth %","Perf.YTD":"Perf %","volume":"Volume"})
    df = df.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
    df["Sector"] = ["Bank","Telecom","Bank","Materials","Bank","Materials","Utilities","Transportation","Materials","Food,Beverage","Insurance","Energy","Consumer Retailing","Healthcare","Energy","Bank","Real Estate","Capital Goods","Bank","Bank","Insurance","Insurance","Food,Beverage","Food,Beverage","Pharmaceuticals","Bank","Real Estate","Real Estate","Capital Goods","Diversified Financials","Materials","Consumer Services","Retail","Materials","Food,Beverage","Materials","Food,Beverage","Real Estate","Retail","Diversified Financials","Capital Goods","Diversified Financials","Real Estate","Tech","Insurance","Insurance","Materials","Tech","Food,Beverage","Pharmaceuticals"]
    st.write(df)


    st.subheader("PE Valuation")
    sector = st.selectbox('Select a Sector', ["Bank","Capital Goods","Consumer Retailing","Diversified Financials","Energy","Food,Beverage","Healthcare","Insurance","Materials","Pharmaceuticals","Real Estate","Retail","Transportation","Tech","Telecom","Utilities",])
    df_sec = df[df["Sector"]==sector]

    random_color = generate_random_color()
    fig = go.Figure(data=[
    go.Bar(x=df_sec['Name'], y=df_sec['P/E'], text=df_sec['P/E'], textposition='auto',name='P/E Ratios',marker=dict(color=random_color))
    ])
    fig.add_trace(go.Scatter(
    x=df_sec['Name'], 
    y=[df_sec["P/E"].mean()] * len(df_sec['Name']),  # Repeat the mean value
    mode='lines',
    line=dict(color='red', dash='dash'),  # Customize line color and style
    name=f'Mean P/E = {df_sec["P/E"].mean():.2f}'
))

    # Adding title and labels
    fig.update_layout(
        title=f'P/E Ratio of {sector}',
        xaxis_title='Stock',
        yaxis_title='P/E Ratio'
    )

    st.plotly_chart(fig,use_container_width=True)

    ######## Gauge
    # Define the values for the gauges
    company_value = df_sec.set_index("Name").loc["ATW"]["P/E"]
    industry_value = df_sec["P/E"].mean()

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
        title={'text': "Company ROE"},
        gauge={
            'axis': {'range': [0, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "lightblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 10], 'color': "red"},
                {'range': [10, 20], 'color': "orange"},
                {'range': [20, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "green"}],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': company_value}}),
        row=1, col=1)

    # Add the gauge for the industry value
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=industry_value,
        title={'text': "Industry ROE"},
        gauge={
            'axis': {'range': [0, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "lightblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 10], 'color': "red"},
                {'range': [10, 20], 'color': "orange"},
                {'range': [20, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "green"}],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': industry_value}}),
        row=1, col=2)

    # Update the layout
    fig.update_layout(
        title="ROE - Company vs Industry",
        font={'color': "darkblue", 'family': "Arial"},
        paper_bgcolor="white",
        plot_bgcolor="black"
    )

    st.plotly_chart(fig,use_container_width=True)
