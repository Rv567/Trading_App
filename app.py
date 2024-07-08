import streamlit as st
from streamlit_option_menu import option_menu
import page1,page2,page3,page4,page5,page6


st.set_page_config(page_title="Home", layout="wide")

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            selected_app = option_menu(
                menu_title=None,
                options=['Stock Market', 'Statistical Data Analysis',"Prediction","Trading Strategy","Data","Model"],
                icons=['bank2', 'bar-chart-fill',"graph-up-arrow","clipboard2-pulse-fill","database-fill-up","robot"],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "20px"}, 
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#1e90ff"}
                }
            )

        # Executing the selected app in the main page context
        if selected_app == "Stock Market":
            page1.app()
        elif selected_app == "Statistical Data Analysis":
            page2.app()
        elif selected_app == "Prediction":
            page3.app()
        elif selected_app == "Trading Strategy":
            page4.app()  
        elif selected_app == "Data":
            page5.app()
        elif selected_app == "Model":
            page6.app()

# Create an instance of the MultiApp class and run the app
app_instance = MultiApp()
app_instance.run()