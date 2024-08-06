from Functions.functions import *
import page2,page5,page4,page3,page1,page6


st.set_page_config(
    page_title="Trading App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            selected_app = option_menu(
                menu_title=None,
                options=["Data",'Stock Market',"Trading Strategy","Prediction" ,'Statistical Data Analysis',"Portfolio"],
                icons=["database-fill-up",'bank2',"clipboard2-pulse-fill","graph-up-arrow",'bar-chart-fill',"pie-chart-fill"],
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
        if selected_app == "Data":
            page1.app()
        elif selected_app == "Stock Market":
            page2.app()
        elif selected_app == "Trading Strategy":
            page3.app()
        elif selected_app == "Prediction":
            page4.app()  
        elif selected_app == "Statistical Data Analysis":
            page5.app()
        elif selected_app == "Portfolio":
            page6.app()

# Create an instance of the MultiApp class and run the app
app_instance = MultiApp()
app_instance.run()