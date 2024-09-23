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
    ty = list(Newdict_df.keys())
    st.write(f"Stocks : {ty}")
    st.header("Beta Classification")
    st.write("We split the selected stocks into High/Low volatility stocks.")
    list_df = high_low_volat(Newdict_df,dataframes["MASI"])

    st.subheader('Stocks with Beta > 1')
    st.dataframe(list_df[0])
    st.session_state['high_volatility_df'] = list_df[0] # store it for page2
    st.subheader('Stocks with Beta < 1')
    st.session_state['low_volatility_df'] = list_df[1]
    st.dataframe(list_df[1])

    st.markdown("""
    #### Key Points:
    **Beta measures how much a stock's price moves compared to the overall market. It's calculated on 3-Year.**
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
    st.write("Filter and identify stocks based on various fundamental criteria Net Income, Current Ratio, D/E, AT, P/E ...")
    st.write("modif")
    morocco_url = 'https://scanner.tradingview.com/morocco/scan'

    # Create a query for the Moroccan stock exchange
    query = (Query()
            .select('name', 'close', "Change %","Net Income (Annual YoY Growth)", "Return on Equity (TTM)","current_ratio", "debt_to_equity","asset_turnover_current","Price to Earnings Ratio (TTM)",'dividends_yield',
                "Perf.YTD","industry")
            .order_by('market_cap_basic', ascending=False))  # Sort by market cap in descending order
    query.url = morocco_url
    count, df = query.get_scanner_data()

    df.drop(columns=["ticker"],inplace=True)
    df = df.rename(columns={"name":"Name","close":"Close","change":"Change %","price_earnings_ttm":"P/E","dividends_yield":"Div Yield %","net_income_yoy_growth_fy":"Net Income Growth %","Perf.YTD":"Perf %","return_on_equity":"ROE %","current_ratio":"Current Ratio","debt_to_equity":"Debt/equity","asset_turnover_current":"Asset Turnover","industry":"Industry"})
    df = df.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

    def sector(f):
        if f == "Regional Banks" or f == "Major Banks":
            return "Banques"
        elif f == "Wireless Telecommunications":
            return "Télécommunications"
        elif f == "Construction Materials":
            return "Bâtiment et Matériaux de Construction"
        elif f == "Other Metals/Minerals":
            return "Mines"
        elif f == "Electric Utilities":
            return "Electricité"
        elif f == "Multi-Line Insurance":
            return "Assurances"
        elif f == "Real Estate Development":
            return "Participation et promotion immobilières"
        elif f == "Hospital/Nursing Management":
            return "Santé"
        elif f == "Beverages: Alcoholic" or f == "Beverages: Non-Alcoholic":
            return "Boissons"
        elif f == "Specialty Stores":
            return "Pétrole et Gaz"
        elif f == "Other Transportation":
            return "Transport"
        elif f == "Wholesale Distributors":
            return "Pétrole et Gaz"
        elif f == "Engineering & Construction":
            return "Bâtiment et Matériaux de Construction"
        elif f == "Food Retail":
            return "Distributeurs"
        elif f == "Food: Specialty/Candy":
            return "Distributeurs"
        elif f == "Hotels/Resorts/Cruise lines":
            return "Loisirs et Hôtels"
        elif f == "Finance/Rental/Leasing":
            return "Sociétés de financement et Autres Activités Financières"
        elif f == "Steel":
            return "Bâtiment et Matériaux de Construction"
        elif f == "Pharmaceuticals: Major":
            return "Industrie Pharmaceutique"
        elif f == "Chemicals: Major Diversified":
            return "Chimie"
        else:
            return f
        
    df['Industry'] = df['Industry'].apply(sector)





    """df["Sector"] = ["Banques",  # ATW
            "",  # IAM
            "Banques",  # BCP
            "Bâtiment et Matériaux de Construction",  # LHM
            "Banques",  # BOA
            "Mines",  # MNG
            "Electricité",  # TQM
            "Transport",  # MSA
            "Bâtiment et Matériaux de Construction",  # CMA
            "Agroalimentaire et Production",  # CSR
            "Assurances",  # WAA
            "Pétrole et Gaz",  # GAZ
            "Santé",  # AKT
            "Distributeurs",  # LBV
            "Pétrole et Gaz",  # TMA
            "Banques",  # CIH
            "Participation et promotion immobilières",  # ADH
            "Bâtiment et Matériaux de Construction",  # TGC
            "Banques",  # BCI
            "Assurances",  # SAH
            "Assurances",  # ATL
            "Agroalimentaire et Production",  # LES
            "Boissons",  # SBM
            "Industrie Pharmaceutique",  # SOT
            "Banques",  # CFG
            "Sociétés de placement immobilier",  # ARD
            "Participation et promotion immobilières",  # ADI
            "Holding",  # DHO
            "Matériels, Logiciels et Services Informatiques",  # HPS
            "Mines",  # SMI
            "Distributeurs",  # ATH
            "Loisirs et Hôtels",  # RIS
            "Bâtiment et Matériaux de Construction",  # SID
            "Mines",  # CMT
            "Boissons",  # OUL
            "Distributeurs",  # MUT
            "Participation et promotion immobilières",  # RDS
            "Distributeurs",  # NKL
            "Bâtiment et Matériaux de Construction",  # JET
            "Sociétés de financement et Autres Activités Financières",  # EQD
            "Sociétés de financement et Autres Activités Financières",  # SLF
            "Sociétés de financement et Autres Activités Financières",  # MAB
            "Matériels, Logiciels et Services Informatiques",  # DWY
            "Assurances",  # AFM
            "Chimie",  # SNP
            "Sociétés de financement et Autres Activités Financières",  # MLE
            "Industrie Pharmaceutique",  # PRO
            "Matériels, Logiciels et Services Informatiques",  # MIC
            "Agroalimentaire et Production",  # DRI
            "Bâtiment et Matériaux de Construction" #COL
 
        ]"""
    #          
    st.write(df.drop(columns=["Close","Change %","Perf %"]))

    st.header("Fundamental Analysis ⚙️")
    st.write("""
        We assess the financial health of a stock based on five key categories: 
        Profitability, Liquidity, Solvency, Efficiency, and Valuation.
        """)
    key = ["Profitability","Liquidity","Solvency","Efficiency","Valuation"]
    explaination = ["Higher margins and returns generally indicate a more profitable and efficient business.","A higher ratio suggests that the company has enough liquidity to cover its near-term liabilities.","Measures a company's ability to meet its long-term debt obligations.","Measures how effectively a company manages its assets to generate sales.","Lower ratios may indicate that the stock is undervalued, while higher ratios may suggest that it is overvalued."]
    dico = dict(zip(key,explaination))
    st.write(pd.DataFrame(dico, index=["Interpretation"]).transpose())

    #Stock Selection
    st.subheader("Stock Selection")
    st.write("First choose a Stock to see it Financial Health Assessment.")
    
    #stock_symbol = st.selectbox('Select Stock Symbol', ["ATW","IAM","BCP","LHM","BOA","TQM",'MNG',"CMA",'MSA','CSR','WAA','GAZ','LBV',"TMA",'CIH',"ADH","AKT","TGC","CDM","BCI","SAH","ATL",'LES',"ARD","CFG","ADI","DHO",'HPS','RIS',"ATH","SID","RDS","JET","SNA"])
    stock_symbol = st.selectbox('Select Stock Symbol', df["Name"].tolist())
    
    ################################Profitability
    st.subheader("Profitability:")
    #Net Income Growth%
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,"Net Income Growth %")

    trace_fundamental(df_sec,industry,"Net Income Growth %")
    score=0
    if company_value < industry_value:
        st.markdown(
            f"<div style='color:red; font-size: 18px;'>"
            f"❌ {stock_symbol} is underperforming in terms of Net Income Growth: "
            f"<strong>{company_value}%</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}%</strong>."
            f"</div>",
            unsafe_allow_html=True
        )
    elif company_value >= industry_value and not np.isnan(company_value):
        score += 1
        st.markdown(
            f"<div style='color:green; font-size: 18px;'>"
            f"✅ {stock_symbol} is outperforming in terms of Net Income Growth: "
            f"<strong>{company_value}%</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}%</strong>."
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )
    #ROE
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,"ROE %")
    trace_gauge("ROE %",company_value,industry_value)

    if company_value < industry_value:
        st.markdown(
            f"<div style='color:red; font-size: 18px;'>"
            f"❌ {stock_symbol} has a lower Return on Equity (ROE) of <strong>{company_value}%</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}%</strong>. "
            f"This suggests that {stock_symbol} is less efficient in generating profits from its equity compared to other companies in the sector."
            f"</div>",
            unsafe_allow_html=True
        )
    elif company_value >= industry_value and not np.isnan(company_value):
        score += 1
        st.markdown(
            f"<div style='color:green; font-size: 18px;'>"
            f"✅ {stock_symbol} has a higher Return on Equity (ROE) of <strong>{company_value}%</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}%</strong>. "
            f"This indicates that {stock_symbol} is more efficient in generating profits from its equity, demonstrating a stronger performance relative to its peers in the sector."
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )
    ################################Liquidity
    #Current Ratio
    st.subheader("Liquidity:")
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,"Current Ratio")
    trace_fundamental(df_sec,industry,"Current Ratio")
    if company_value < 1:
        st.markdown(
            f"<div style='color:red; font-size: 18px;'>"
            f"❌ {stock_symbol} has a Current Ratio of <strong>{company_value}</strong>, which is below 1. "
            f"This suggests that {stock_symbol} may struggle to meet its short-term liabilities with its current assets, indicating potential liquidity issues."
            f"</div>",
            unsafe_allow_html=True
        )
    elif company_value >= 1 and not np.isnan(company_value):
        score += 1
        st.markdown(
            f"<div style='color:green; font-size: 18px;'>"
            f"✅ {stock_symbol} has a healthy Current Ratio of <strong>{company_value}</strong> > 1. "
            f"This indicates that {stock_symbol} has more than enough current assets to cover its short-term liabilities, suggesting strong liquidity and financial stability."
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )
    ################################Solvency
    st.subheader("Solvency:")
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,"Debt/equity")
    trace_fundamental(df_sec,industry,"Debt/equity")

    if company_value > industry_value:
        st.markdown(
        f"<div style='color:red; font-size: 18px;'>"
        f"❌ {stock_symbol} has a higher Debt-to-Equity Ratio of <strong>{company_value}</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}</strong>. "
        f"This suggests that {stock_symbol} relies more heavily on debt financing, which could indicate higher financial risk and potential challenges in meeting long-term obligations."
        f"</div>",
        unsafe_allow_html=True
    )
    elif company_value <= industry_value and not np.isnan(company_value):
        score += 1
        st.markdown(
        f"<div style='color:green; font-size: 18px;'>"
        f"✅ {stock_symbol} has a Debt-to-Equity Ratio of <strong>{company_value}</strong>, which is lower to the sector average of <strong>{np.round(industry_value, 2)}</strong>. "
        f"This indicates that {stock_symbol} is managing its debt prudently relative to its equity, suggesting strong solvency and a lower financial risk compared to its peers."
        f"</div>",
        unsafe_allow_html=True
    )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )
    ###############################Efficiency
    st.subheader("Efficiency:")
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,"Asset Turnover")
    trace_fundamental(df_sec,industry,"Asset Turnover")

    if company_value < industry_value:
        st.markdown(
        f"<div style='color:red; font-size: 18px;'>"
        f"❌ {stock_symbol} has an Asset Turnover Ratio of <strong>{company_value}</strong>, which is below the sector average of <strong>{np.round(industry_value, 2)}</strong>. "
        f"This suggests that {stock_symbol} may not be utilizing its assets as effectively as its peers to generate revenue, indicating potential inefficiencies in asset management."
        f"</div>",
        unsafe_allow_html=True
    )
    elif company_value >= industry_value and not np.isnan(company_value):
        score += 1
        st.markdown(
        f"<div style='color:green; font-size: 18px;'>"
        f"✅ {stock_symbol} has an Asset Turnover Ratio of <strong>{company_value}</strong>, which is higher or equal to the sector average of <strong>{np.round(industry_value, 2)}</strong>. "
        f"This indicates that {stock_symbol} is efficiently utilizing its assets to generate revenue, outperforming its peers in terms of asset management."
        f"</div>",
        unsafe_allow_html=True
    )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )

    ###############################Valuation
    #PE
    st.subheader("Valuation")
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,'P/E')
    trace_fundamental(df_sec,industry,'P/E')
    trace_gauge('P/E',company_value,industry_value)
    
    if company_value > industry_value:
        st.markdown(
        f"<div style='color:red; font-size: 18px;'>"
        f"❌ {stock_symbol} has a higher PE Ratio of <strong>{company_value}</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}</strong>. "
        f"This suggests that {stock_symbol} may be overvalued relative to its peers, potentially indicating a less attractive investment at the current price."
        f"</div>",
        unsafe_allow_html=True
    )
    elif company_value <= industry_value and not np.isnan(company_value):
        score +=1
        st.markdown(
        f"<div style='color:green; font-size: 18px;'>"
        f"✅ {stock_symbol} has a PE Ratio of <strong>{company_value}</strong>, which is lower to the sector average of <strong>{np.round(industry_value, 2)}</strong>. "
        f"This suggests that {stock_symbol} may be undervalued relative to its peers, potentially offering a more attractive investment opportunity."
        f"</div>",
        unsafe_allow_html=True
    )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )
    #Dividend Yield
    company_value,industry,industry_value,df_sec = metric_definition(df,stock_symbol,'Div Yield %')
    trace_fundamental(df_sec,industry,'Div Yield %')

    if company_value < industry_value:
        st.markdown(
        f"<div style='color:red; font-size: 18px;'>"
        f"❌ {stock_symbol} has a lower Dividend Yield of <strong>{company_value}%</strong> compared to the sector average of <strong>{np.round(industry_value, 2)}%</strong>. "
        f"This suggests that {stock_symbol} may offer a less attractive dividend return relative to its peers, which could be a disadvantage for income-seeking investors."
        f"</div>",
        unsafe_allow_html=True
    )
    elif company_value >= industry_value and not np.isnan(company_value):
        score +=1
        st.markdown(
        f"<div style='color:green; font-size: 18px;'>"
        f"✅ {stock_symbol} has a Dividend Yield of <strong>{company_value}%</strong>, which is higher or equal to the sector average of <strong>{np.round(industry_value, 2)}%</strong>. "
        f"This suggests that {stock_symbol} offers a more attractive dividend return compared to its peers, potentially making it a better option for income-focused investors."
        f"</div>",
        unsafe_allow_html=True
    )
        st.markdown(
        f"""
        <div style="
            background-color: #e0ffe0; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 3px 3px 15px rgba(0, 128, 0, 0.2); 
            margin: 20px auto; 
            width: 240px;  /* Set the width of the box */
            text-align: center;">
            <h4 style="color: #006400; font-family: 'Arial', sans-serif;">🌟 Score +1 🌟</h4>
        </div>
        """, 
        unsafe_allow_html=True
        )


    #Conclusion
    st.subheader("Financial Health Score")
    if score <= 3:
        st.markdown(
            f"""
            <div style="
                background-color: #ffcccc; 
                padding: 15px; 
                border-radius: 8px; 
                box-shadow: 3px 3px 15px rgba(255, 0, 0, 0.2); 
                margin: 20px auto;  
                text-align: center;">
                <h4 style="color: #b30000; font-family: 'Arial', sans-serif; margin: 0;">🚨 Financial Health Score: {score}/7 (Low) 🚨</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    elif score > 3 and score <= 5:
        st.markdown(
            f"""
            <div style="
                background-color: #fff5cc; 
                padding: 15px; 
                border-radius: 8px; 
                box-shadow: 3px 3px 15px rgba(255, 165, 0, 0.2); 
                margin: 20px auto; 
                text-align: center;">
                <h4 style="color: #e65c00; font-family: 'Arial', sans-serif; margin: 0;">⚠️ Financial Health Score: {score}/7 (Medium) ⚠️</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    elif score > 5:
        st.markdown(
            f"""
            <div style="
                background-color: #ccffcc; 
                padding: 15px; 
                border-radius: 8px; 
                box-shadow: 3px 3px 15px rgba(0, 255, 0, 0.2); 
                margin: 20px auto; 
                text-align: center;">
                <h4 style="color: #006600; font-family: 'Arial', sans-serif; margin: 0;">✅ Financial Health Score: {score}/7 (High) ✅</h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
    #st.write(f"Final Financial Health Score for {stock_symbol} is {score}/7")
