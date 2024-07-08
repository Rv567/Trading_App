from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *

Newdict_df = st.session_state['Newdict_df']
high_volatility_df = st.session_state['high_volatility_df']
low_volatility_df = st.session_state['low_volatility_df']

def app():
    st.header("Introduction to the Model page")
    st.write("Welcome to the Model Management page. Here, you can view and manage the machine learning model used for predicting stock prices")

    st.subheader("Model Overview")
    st.write("Brief description of the XGBoost model and its purpose")

    st.subheader("Train/Test Model")
    if st.button('Train Model'):
        for key in Newdict_df.keys():

            df_ml= Newdict_df.copy()
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

            
        st.write(df_train)
