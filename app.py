from Functions.mylibraries import *
import page2,page5,page4,page3,page1,page6

# User authentication configuration
names = ["User"]
usernames = ["Axiom"]
passwords = ["Axiom"]

hashed_passwords = Hasher(passwords).generate()

# Create the authenticator object
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "auth_cookie",
    "my_app",
    30
)
# Authentication widget
name, authentication_status, username = authenticator.login("Login", "main")
st.set_page_config(page_title="Home", layout="wide")
if authentication_status:
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
                    options=["Data",'Stock Market',"Trading Strategy","Prediction" ,'Statistical Data Analysis',"Model"],
                    icons=["database-fill-up",'bank2',"clipboard2-pulse-fill","graph-up-arrow",'bar-chart-fill',"robot"],
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
            elif selected_app == "Model":
                page6.app()

    # Create an instance of the MultiApp class and run the app
    app_instance = MultiApp()
    app_instance.run()

elif authentication_status == False:
    st.error("Username or password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

# Logout button
if st.sidebar.button("Logout"):
    authenticator.logout("Logout", "main")