# **Stock Market Prediction & Portfolio Optimization using XGBoost**

## 📌 Project Overview  
This project focuses on **stock market analysis, prediction, and portfolio optimization** using **XGBoost**, technical indicators, fundamental analysis, and Markowitz portfolio theory.  
It provides a **Streamlit dashboard** for:
- **Visualizing stock data**
- **Backtesting trading strategies**
- **Optimizing portfolios**
- **Evaluating financial health**
- **Statistical Analysis & Pairs Trading**

---

## ⚡ Features  

### 📊 **Stock Market Data & Visualization**  
-  Collects **daily & weekly** stock data using **TradingView API** (for Moroccan stocks)
![image](https://github.com/user-attachments/assets/148af0dd-81fa-4753-91e2-410b042a21d7)
-  Displays **historical price trends, liquidity filtering, and beta classification**
![image](https://github.com/user-attachments/assets/674a3471-ee77-46af-b144-947f9c715c87)
-  Compares **individual stock vs. MASI benchmark**  
### 📈 **Trading Strategy Development & Backtesting**  
-  Implements **3 Automated Strategies**:  
    1️. **SMA Crossover**  
    2️. **SMA + Stop Loss**  
    3️. **Multi Indicator Strategy (RSI, ATR, AD, SMA)**
  ![image](https://github.com/user-attachments/assets/a6f269cd-ddbb-4d97-8469-de2c00f406bb)

-  **Optimizes strategy parameters** based on market trends
  ![3](https://github.com/user-attachments/assets/5501c6d4-1d88-4803-9b0b-ddd6bcd2f813)

-  Computes **returns, Sharpe ratio, max drawdown, win rate, and expectancy**  

### 🤖 **Machine Learning Prediction (XGBoost)**  
-  Predicts **next week's stock variation %** using:  **Price ratios, technical indicators, rolling statistics, and lagged features**
  ![image](https://github.com/user-attachments/assets/dc1fcdef-2241-4101-85da-ef006b81cada)
  - **XGBoost regression model with SHAP feature importance analysis**  
-  **Decision Framework**:  
    -  **Buy**  
    -  **Hold**  
    -  **Sell**  (based on median % change) 
![image](https://github.com/user-attachments/assets/484398a2-844e-4c99-b899-f924a1915d88)
### 📊 **Portfolio Optimization using Markowitz Model**  
-  Efficient Frontier Optimization for:  
    -  **Max Sharpe Ratio**  
    -  **Minimize Risk**  
    -  **Target Returns**
 ![image](https://github.com/user-attachments/assets/4e84cc97-9401-435c-abc8-36d94d2b25a4)
-  Computes **Performance Metrics**: Alpha, Beta, Standard Deviation, Cumulative Returns  
-  **Custom Portfolio Builder**: Users can **select stocks** and apply optimization  

### 🔍 **Fundamental Analysis & Stock Screener**  
-  **Financial Ratios**:  
    - P/E  
    - ROE  
    - Net Income Growth  
    - Current Ratio  
    - Debt/Equity
![image](https://github.com/user-attachments/assets/3f82907f-ba77-4022-8816-99ef627b600c)
-  Assigns a **Financial Health Score** to each stock  

### 🔬 **Statistical Analysis & Pairs Trading**  
-  Computes **correlation matrix** for stock relationships  
-  Detects **highly correlated stock pairs** for **pairs trading strategies**  
-  Uses **Z-score analysis** for arbitrage signals  
![image](https://github.com/user-attachments/assets/0ca687e4-0e5c-4f36-8bd5-02c3af4fa356)

