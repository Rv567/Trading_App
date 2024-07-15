from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *


def app():
    st.header("Introduction to the prediction page and the model")
    st.write("you can view the predicted weekly variation along with trading decisions.")

    st.subheader("Prediction Table")
    st.write("DataFrame showing Week Before Last Variation %, Last Week Variation %, Predicted Next Week Variation %, Median 50% Value, and Decision (Buy/Sell/Hold)")
    
    # Retrieve Data
    Newdict_df = st.session_state['Newdict_df']
    high_volatility_df = st.session_state['high_volatility_df']
    low_volatility_df = st.session_state['low_volatility_df']

    dataframes = load_data_weekly()
    dataframes = {key: reorganize(df) for key, df in dataframes.items()}

    #st.write(dataframes["ATW"])#verify data
    Newdict_df.pop('CFG', None)
    Newdict_df.pop('AKT', None)
    st.write(Newdict_df.keys())
        
    st.header("Model Prediction")
    st.write("We use Machine Learning Model to fit it to our data. Then we use it to predict future Weekly Variation%.")
    st.write("**Weekly Percentage Change Formula** :")
    st.markdown("""
        To understand the weekly variation of a stock, we calculate the percentage change in the closing price from one week to the next.

        $$
        \\text{Percentage Change} = \\left( \\frac{\\text{Close}_{\\text{current week}} - \\text{Close}_{\\text{previous week}}}{\\text{Close}_{\\text{previous week}}} \\right) \\times 100
        $$

        """)
    custom_button_css = """
    <style>
    .stButton > button {
        background-color: yellow;
        color: black;
        font-size: 24px;  /* Increase font size */
        padding: 20px 40px;  /* Increase padding */
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .centered-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    </style>
        """

    # Inject CSS into the Streamlit app
    st.markdown(custom_button_css, unsafe_allow_html=True)
    #st.markdown('<div class="centered-button">', unsafe_allow_html=True)

    if st.button("Predict 🔮"):
        st.markdown("<h3 style='color: orange;'>Model is running...⏳</h3>", unsafe_allow_html=True)
        features_df = {}
        target_df ={}
        df_pred_tomorrow = {} #model.predict()
        
        for key in Newdict_df.keys():
                df_ml= dataframes.copy()
                stock = df_ml[key]
                # Technical Indicators
                test_indicators = [ADX,MACD,RSI,BBANDS,SAR,ATR,AD] 
                for elem in test_indicators:
                        elem(stock)

                # Different periods
                for elem in [2,4,8,16,32,64]:
                        EMA(stock,elem)
                        stock[f'Close_rolling_mean_{elem}'] = stock['Close'].rolling(window=elem).mean()
                        stock[f'Close_rolling_std_{elem}'] = stock['Close'].rolling(window=elem).std()
                        
                # Lagg all features
                for col in stock.columns:
                        for i in range(1,10):
                                stock[f"{col}_Lag{i}"] = stock[col].shift(i)

                for i in range(1,10):
                        stock[f"Close_Lag{i}_ratio"] = stock["Close"] / stock[f"Close_Lag{i}"]



                # Add a new targets
                stock["Variation%"] = np.round((stock['Close'].pct_change())*100,2)
                stock["Log_Variation"] = np.log(stock['Close']).diff() 

                # Shifting the target features for logical prediction
                stock["Variation%"] = stock["Variation%"].shift(-1)
                stock["Log_Variation"] = stock["Log_Variation"].shift(-1)

                df_pred_tomorrow[key] = stock.copy() # Copy to be used to predict tomorrow variation
                stock.dropna(inplace=True)

                # Remove all lagged features to define df_features
                features_df[key] = stock[[col for col in stock.columns if 'Lag' in col ]]#and "Close" not in col

                # Define df_target
                target_df[key] = stock[["Close","Variation%","Log_Variation"]]

        ###########
        df_date = {}
        df_actuals = {}
        df_y_pred = {}
        df_prediction = {}
        df_actualClose = {}
        df_actualCloseYest = {}
        df_threshold = {}
        df_indicator={}
    
        # Progress status
        progress_bar = st.progress(0)
        progress_text = st.empty()
        total_keys = len(Newdict_df.keys())

        for i,key in enumerate(Newdict_df.keys()):

                progress_bar.progress((i + 1) / total_keys)
                progress_text.text(f"Processing {key}... ({i + 1}/{total_keys})")
                X = features_df[key]
                y = target_df[key]["Variation%"]

                # Train/Test the model
                X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.8,test_size=0.2, shuffle=False)
                model = XGBRegressor()
                model.fit(X_train, y_train)

                y_pred_train = model.predict(X_train)
                y_pred_test = model.predict(X_test)
                
                # Y tesy Vs. Pred
                df_date[key] = X_test.index
                df_actuals[key] =y_test.values # Actual
                df_y_pred[key]=y_pred_test


                """rmse_train = mean_squared_error(y_train,y_pred_train, squared=False)
                rmse_test = mean_squared_error(y_test,y_pred_test, squared=False)
                df_train[key] = rmse_train
                df_test[key] = rmse_test"""

                # Prediction tomorrow's close
                X_tomorrow = df_pred_tomorrow[key].tail(1)
                X_tomorrow=X_tomorrow[features_df[key].columns]
                df_prediction[key]= float(model.predict(X_tomorrow)) #Predicting tomorrow close

                #df_predictionYest[key]=y_pred_test[-1]
                df_actualClose[key] = y_test[-1]
                df_actualCloseYest[key] = y_test[-2]

                # Decision Making
                df_threshold[key] = y.median()

                # Best Indicators
                # SHAP values for features importance
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_test)

                # Find the best indicators for each stock, indicator = [momentum, overlap, volatility, volume]
                mean_shap = np.mean(np.abs(shap_values), axis=0)
                sorted_index = np.argsort(mean_shap)[::-1]
                sorted_features = X.columns[sorted_index]

                df_indicator[key] = best_indicators_category(sorted_features)

        progress_text.text("Model prediction complete!")
        st.success("All stocks have been processed.")

        """df_tr = pd.DataFrame(list(df_train.items()), columns=["Key", 'RMSE Train'])
        df_tst = pd.DataFrame(list(df_test.items()), columns=["Key", 'RMSE Test'])
        resultat_baselineModel = pd.merge(df_tr,df_tst) # Display Train -> Test
        #st.write(resultat_baselineModel) # i decided not include the RMSE result table"""
        
        # Create different dataframes
        # Actual this week and the previous one 
        df_actualCloseYest = pd.DataFrame(list(df_actualCloseYest.items()), columns=["Key", 'Week Before Last Variation%'])
        df_actualClose = pd.DataFrame(list(df_actualClose.items()), columns=["Key", 'Last Week Variation%'])

        # Prediction
        df_prediction = pd.DataFrame(list(df_prediction.items()), columns=["Key", 'Prediction Next Week Variation%'])

        # Decision Making
        df_threshold = pd.DataFrame(list(df_threshold.items()), columns=["Key", 'Median50%'])

        # T.Indicators
        df_indicators = pd.DataFrame.from_dict(df_indicator,orient="index",columns=['momentum',"overlap","volatility","volume"])
        df_indicators.to_pickle('df_indicators.pkl')

        final= pd.merge(df_actualCloseYest,df_actualClose)
        final = pd.merge (final,df_prediction)
        final = pd.merge (final,df_threshold)
        final["Decision"] = final.apply(todo,axis=1)
        final.to_pickle('final.pkl')

    final = pd.read_pickle('final.pkl') # Store it in local
    #st.write(final)
    # Sort the final data into high and low volatility stocks
    st.subheader("Model prediction for stocks with Beta>1 :")
    high_volatility_df = pd.merge(final,high_volatility_df)
    st.write(high_volatility_df)
    st.subheader("Model prediction for stocks with Beta<1 :")
    low_volatility_df = pd.merge(final,low_volatility_df)
    st.write(low_volatility_df)


    st.subheader("Model Insights")
    st.write("Display the top 4 Technical Indicators contributing to the predictions.")
    df_indicators = pd.read_pickle('df_indicators.pkl')
    st.write(df_indicators)