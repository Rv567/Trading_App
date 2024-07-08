from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *


def app():

    #Initialization
    Newdict_df = st.session_state['Newdict_df']
    df_ml= Newdict_df.copy()

    st.header("Introduction to the Model page")
    st.write("Welcome to the Model Management page. Here, you can view and manage the machine learning model used for predicting stock prices")

    st.subheader("Model Overview")
    st.write("Brief description of the XGBoost model and its purpose")

    st.subheader("Train Model")
    st.write("We train our Model on the selected stock dataframes")
    if st.button('Train Model'):
        with st.spinner('In progress...'):

            time.sleep(1)
            for key in Newdict_df.keys():

                stock = df_ml[key]

                test_indicators = [ADX,MACD,RSI,BBANDS,SAR,ATR,AD] #Different indicators
                for elem in test_indicators:
                        elem(stock)

                for elem in [2,4,8,16,32,64]:
                    EMA(stock,elem) #Exp moving average
                    SMA(stock,elem) #Simple moving average
                    stock[f'Close_rolling_mean_{elem}'] = stock['Close'].rolling(window=elem).mean() #Mean
                    stock[f'Close_rolling_std_{elem}'] = stock['Close'].rolling(window=elem).std() #Std

                for col in stock.columns: #Lagegd features
                    for i in range(1,10):
                        stock[f"{col}_Lag{i}"] = stock[col].shift(i)

                stock["Variation"] = stock['Close'].pct_change() * 100
                stock["Variation"] = stock["Variation"].shift(-1)

                stock["Close"] = stock["Close"].shift(-1)

                # Remove all lagged features to define df_features
                features_df = stock[[col for col in stock.columns if 'Lag' in col ]]#and "Close" not in col

                # Define df_target
                target_df = stock[["Close","Variation"]]

            # Date
            df_date = {}

            # For RMSE calculation
            df_train = {}
            df_test = {}

            # Actual vs Prediction values
            df_prediction = {}
            df_predictionYest = {}
            df_actualClose = {}
            df_actualCloseYest = {}


            # Backtesting
            df_y_pred = {}
            df_actuals = {}

            for key in df_ml.keys():
                df_ml[key]=df_ml[key].dropna()
                X = df_ml[key].drop(columns=['Open', 'High', 'Low',"Variation","Close"])
                y = df_ml[key]["Close"]

                # Train/ Test the model,
                X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8,test_size=0.2, shuffle=False)
                model = XGBRegressor()
                model.fit(X_train, y_train)

                y_pred_train = model.predict(X_train)
                y_pred_test = model.predict(X_test)
                
                with open(f'model_{key}.pkl', 'wb') as file:
                    pickle.dump(model, file)

                # Backtesting
                df_date[key] = X_test.index
                df_actuals[key] =y_test.values
                df_y_pred[key]=y_pred_test


                rmse_train = mean_squared_error(y_train,y_pred_train, squared=False)
                rmse_test = mean_squared_error(y_test,y_pred_test, squared=False)
                df_train[key] = rmse_train
                df_test[key] = rmse_test
            
            """st.session_state['df_date'] = df_date
            st.session_state['df_actuals'] = df_actuals
            st.session_state['df_y_pred'] = df_y_pred
            st.session_state['df_test'] = df_test"""

        df_tr = pd.DataFrame(list(df_train.items()), columns=["Key", 'RMSE Train'])
        df_tst = pd.DataFrame(list(df_test.items()), columns=["Key", 'RMSE Test'])
        resultat_baselineModel = pd.merge(df_tr,df_tst)
        st.session_state['resultat_baselineModel'] = resultat_baselineModel

        st.success('Model trained!')    
        #st.write(df_train)

    

    st.subheader("Evaluate Model")
    st.write("We use RMSE as evaluation metric")
    if st.button('Display evaluation results'):
        resultat_baselineModel = st.session_state['resultat_baselineModel']
        st.write(resultat_baselineModel)
    
        """df_date = st.session_state['df_date']
        df_actuals = st.session_state['df_actuals']
        df_y_pred = st.session_state['df_y_pred']
        df_test = st.session_state['df_test']
        stock_symbol = st.selectbox('Select Stock Symbol to test the Model with', df_ml.keys(),key='test')
        plot_train_vs_test(df_date[stock_symbol],df_actuals[stock_symbol],df_y_pred[stock_symbol],df_test[stock_symbol])"""
