from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *


def app():
    st.header("Introduction to the prediction page and the model")
    st.write("Welcome to the Prediction page. Here, you can view the predicted close prices and variation percentages for tomorrow, along with trading decisions.")

    st.subheader("Prediction Table")
    st.write("DataFrame showing Actual close price t-1, Actual close price, Predicted tomorrow variation %, Threshold, Beta value and Decision (Buy/Sell/Hold)")
    Newdict_df = st.session_state['Newdict_df']
    high_volatility_df = st.session_state['high_volatility_df']
    low_volatility_df = st.session_state['low_volatility_df']

    features_df = {}
    target_df ={}

    dataframes = load_data_weekly()
    stock_list = ["MASI","ATW","IAM","BCP","LHM","BOA","TQM","CMA","TMA","ADH","TGC","CDM","ATL","BCI","AKT","SAH","CFG","ARD","ADI","DYT","ATH","RDS","DHO","FBR"]
    dataframes = {key: reorganize(df) for key, df in dataframes.items()}

    for key in Newdict_df.keys():

        df_ml= dataframes.copy()
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
        features_df[key] = stock[[col for col in stock.columns if 'Lag' in col ]]#and "Close" not in col

        # Define df_target
        target_df[key] = stock[["Close","Variation"]]

    df_tomorrow_prediction =df_ml.copy() # features for tomorrow prediction
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

    # Threshold
    threshold_combined = {}

    # Technical Indicators
    df_indicator={}

    # Backtesting
    df_y_pred = {}
    df_actuals = {}

    for key in df_ml.keys():
        #df_ml[key]=df_ml[key].dropna()
        X = features_df[key]
        y = target_df[key]["Variation%"]

        # Train/ Test the model,
        X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, shuffle=False)
        model = XGBRegressor()
        model.fit(X_train, y_train)

        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Backtesting
        df_date[key] = X_test.index
        df_actuals[key] =y_test.values
        df_y_pred[key]=y_pred_test


        rmse_train = mean_squared_error(y_train,y_pred_train, squared=False)
        rmse_test = mean_squared_error(y_test,y_pred_test, squared=False)
        df_train[key] = rmse_train
        df_test[key] = rmse_test

        # Prediction tomorrow's close
        X_tomorrow = df_tomorrow_prediction[key].tail(1)
        X_tomorrow=X_tomorrow.drop(columns=['Open', 'High', 'Low',"Variation","Close"])
        df_prediction[key]= float(model.predict(X_tomorrow)) #Predicting tomorrow close
        
        df_predictionYest[key]=y_pred_test[-1]
        df_actualClose[key] = y_test[-1]
        df_actualCloseYest[key] = y_test[-2]


        #Best threshold that maximizes the combined metric (Accuracy and Number of correct predictions)
        actual_today_close = y_test.values
        predicted_tomorrow_close = y_pred_test

        results = pd.DataFrame({
        'Actual Today Close': actual_today_close,
        'Predicted Tomorrow Close': predicted_tomorrow_close
        })

        results['Actual Difference (%)'] = results['Actual Today Close'].pct_change() * 100
        results['Predicted Difference (%)'] = results['Predicted Tomorrow Close'].pct_change() * 100

        thresholds = np.arange(0, 10, 0.1)
        accuracies = []

        # Loop through different threshold values to find the best one
        for threshold in thresholds:
            # Identify instances where the predicted change is greater than the threshold
            high_change = results['Predicted Difference (%)'].abs() > threshold

            # Calculate the predicted and actual trends
            predicted_trend = np.sign(results['Predicted Difference (%)'])
            actual_trend = np.sign(results['Actual Difference (%)'])

            # Filter out NaN values
            correct_predictions = (predicted_trend == actual_trend).dropna()
            high_change_correct_predictions = correct_predictions[high_change]

            # Calculate the accuracy
            accuracy = high_change_correct_predictions.mean() * 100
            accuracies.append(accuracy)

        max_accuracy = max(accuracies)
        optimal_threshold = thresholds[accuracies.index(max_accuracy)]
        threshold_combined[key] = optimal_threshold

        # SHAP values for features importance
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)

        # Find the best indicators for each stock, indicator = [momentum, overlap, volatility, volume]
        mean_shap = np.mean(np.abs(shap_values), axis=0)
        sorted_index = np.argsort(mean_shap)[::-1]
        sorted_features = X.columns[sorted_index]

        df_indicator[key] = best_indicators_category(sorted_features)

    df_tr = pd.DataFrame(list(df_train.items()), columns=["Key", 'RMSE Train'])
    df_tst = pd.DataFrame(list(df_test.items()), columns=["Key", 'RMSE Test'])

    resultat_baselineModel = pd.merge(df_tr,df_tst)
    #st.write(resultat_baselineModel) # i decided not include the RMSE result table
    

    # Actual
    df_actualCloseYest = pd.DataFrame(list(df_actualCloseYest.items()), columns=["Key", 'Actual Close t_1'])
    df_actualClose = pd.DataFrame(list(df_actualClose.items()), columns=["Key", 'Actual Close'])

    # Prediction
    df_predictionYest = pd.DataFrame(list(df_predictionYest.items()), columns=["Key", 'Prediction close t_1'])
    df_prediction = pd.DataFrame(list(df_prediction.items()), columns=["Key", 'Prediction tomorrow close'])

    # Thresold
    df_threshold = pd.DataFrame(list(threshold_combined.items()), columns=["Key", 'Threshold'])

    # T.Indicators
    df_indicators = pd.DataFrame.from_dict(df_indicator,orient="index",columns=['momentum',"overlap","volatility","volume"])

    # Backtesting
    df_actuals = pd.DataFrame(list(df_actuals.items()), columns=["Key", 'Actual Close'])
    df_y_preds = pd.DataFrame(list(df_y_pred.items()), columns=["Key", 'Predictions'])

    final= pd.merge(df_actualCloseYest,df_actualClose)

    final["Prediction Variation%"] = ((df_prediction["Prediction tomorrow close"] - df_predictionYest["Prediction close t_1"])/ df_predictionYest["Prediction close t_1"]) *100

    # Add Threshold for each stock
    final["Threshold"] = df_threshold["Threshold"]

    # Sort the final data into high and low volatility stocks
    high_volatility_df = pd.merge(final,high_volatility_df)
    low_volatility_df = pd.merge(final,low_volatility_df)

    high_volatility_df["Decision"] = high_volatility_df.apply(todo,axis=1)
    low_volatility_df["Decision"] = low_volatility_df.apply(todo,axis=1)
    
    st.caption("Beta > 1 :")
    st.write(high_volatility_df)
    st.caption("Beta < 1 :")
    st.write(low_volatility_df)

    st.subheader("Model Insights")
    st.write("Display the top 4 technical indicators contributing to the predictions.")
    st.write(df_indicators)