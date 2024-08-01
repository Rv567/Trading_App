from Functions.functions import *
from Functions.mylibraries import *
from Functions.indicators import *


def app():

    st.header("Portfolio Analysis, Build, and Optimization")
    st.subheaderheader("Calculate Portfolio Metrics")
    st.write("""
    - **Cumulative Return%**
    - **Standard Deviation**
    - **Beta**
    - **Sharpe Ratio**
    """)

    st.write("Choose a metric to apply to your stocks and see the results:")
    metric_choice = st.selectbox("Select Metric", ["Cumulative Return%", "Standard Deviation", "Beta", "Sharpe Ratio"])
    if st.button("Apply Metric"):
        if metric_choice == "Cumulative Return%":
            st.write(f"Results for {metric_choice}:")
    