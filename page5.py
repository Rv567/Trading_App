from Functions.functions import *
from Functions.mylibraries import *


def app():
    st.header("Introduction to the statistical analysis and its importance")
    st.write("Welcome to the Statistical Data Analysis page. Here, we analyze correlations between different stocks to identify pairs with strong relationships.")

    df = st.session_state['Newdict_df']
    Newdict_df_close = {key:value["Close"] for key,value in df.items()}
    #Newdict_df_return = {key:value["Close"].pct_change() for key,value in df.items()}

    df = pd.DataFrame(Newdict_df_close)
    df.index = pd.to_datetime(df.index)
    correlation_matrix = df.corr()
    #Heatmap
    mask = np.zeros_like(correlation_matrix, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    st.header("Correlation Calculation")    
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, mask=mask, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix Heatmap')
    st.pyplot(plt)

    st.markdown("""
    ### Key Points:
    - **Positive Correlation**: When the prices of two stocks move in the same direction.
    - **Negative Correlation**: When the prices of two stocks move in opposite directions.
    - **No Correlation**: When there is no discernible pattern in the price movements of two stocks.
    """)
    st.header("Couples with Strong Correlation")
    st.write("Select the correlation threshold.")
    threshold = st.slider('Threshold :', min_value=80, max_value=100, value=90, step=1)
    st.write("List of stock pairs with high correlation values :")
    threshold = threshold/100
    high_corr_pairs = []

    for i in range(len(correlation_matrix.columns)):
        for j in range(i + 1, len(correlation_matrix.columns)):
            if correlation_matrix.iloc[i, j] > threshold:
                high_corr_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j], correlation_matrix.iloc[i, j]))

    # Print the pairs
    for pair in high_corr_pairs:
        st.write(f"Pair: {pair[0]} and {pair[1]} with correlation {pair[2]}")

    st.header("Time-Series Analysis")
    st.write("Select the two pairs from the high correaltion pairs list.")
    pairs = st.selectbox('Select pairs', high_corr_pairs)
    #plot_scatter_pairs(Newdict_df_close, pairs[0],pairs[1])

    st.write("We plot the historical prices of selected stocks.")

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=Newdict_df_close[pairs[0]].index, y=Newdict_df_close[pairs[0]], name=pairs[0],line=dict(color='#0A53D0'))) #, line=dict(color='blue')
    fig.add_trace(go.Scatter(x=Newdict_df_close[pairs[1]].index, y=Newdict_df_close[pairs[1]], name=pairs[1],line=dict(color='#FBE96D'), yaxis='y2')) #, line=dict(color='red')
    fig.update_layout(
            yaxis2=dict(
                title=pairs[1],
                titlefont=dict(color='#FBE96D'),
                tickfont=dict(color='#FBE96D'),
                overlaying='y',
                side='right'
            )
        )
    fig.update_layout(
        title=f'Close Price for : <span style="color:#0A53D0;">{pairs[0]}</span> and <span style="color:#FBE96D;">{pairs[1]}</span>',
        xaxis_title="Date",
        yaxis_title=pairs[0],
        legend_title="Stocks",
        yaxis=dict(
            title=pairs[0],
            titlefont=dict(color='#0A53D0'),
            tickfont=dict(color='#0A53D0')
        )
    )
    
    st.plotly_chart(fig,use_container_width=True)
    ##################################################
    st.header("Pairs Trading")
    st.write("Pairs trading involves identifying two stocks with a strong historical correlation and exploiting the temporary divergences in their price relationship.")
    st.subheader("Spread Calculation")
    df = pd.merge(Newdict_df_close[pairs[0]],Newdict_df_close[pairs[1]],left_index=True, right_index=True, suffixes=(f'_{pairs[0]}', f'_{pairs[1]}'))
    
    X = df[f"Close_{pairs[1]}"]
    X = sm.add_constant(X)
    model = sm.OLS(df[f"Close_{pairs[0]}"], X).fit()

    df['hedge_ratio'] = model.params[1]

    # Calculate the spread
    df['spread'] = df[f"Close_{pairs[0]}"] - df['hedge_ratio'] * df[f"Close_{pairs[1]}"]

    # Calculate z-score
    df['z_score'] = (df['spread'] - df['spread'].mean()) / df['spread'].std()

    st.write(df['z_score'].tail(20))
    st.title('Z-Score Histogram')

    # Create a histogram plot
    fig, ax = plt.subplots()
    ax.hist(df['z_score'], bins=30, edgecolor='black')
    ax.set_title('Z-Score Distribution')
    ax.set_xlabel('Z-Score')
    ax.set_ylabel('Frequency')

    # Display the histogram in the Streamlit app
    st.pyplot(fig)
    st.write(df.describe())
    st.write(np.percentile(df['z_score'], 95))

    st.subheader("Trading Signals Based on Spread")
    z_score_threshold = 2

    buy_signal = df['z_score'] > z_score_threshold
    sell_signal = df['z_score'] < -z_score_threshold

    df['Buy'] = buy_signal.astype(int)
    df['Sell'] = sell_signal.astype(int)

    st.write("Recent Trading Signals Based on Z-Score")
    st.write(df[['z_score', 'Buy', 'Sell']].tail(20))