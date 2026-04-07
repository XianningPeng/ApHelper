import streamlit as st
from supabase import create_client, Client


url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


st.set_page_config(
    page_title="AP Helper",
    page_icon="📘",
    layout="wide"
)



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("📘 AP Helper")
    st.write("You haven't log in yet. Please log in first.")
    st.session_state.userName = st.text_input("Your Name:")
    if "userName" in st.session_state and st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
input_page = st.Page("input.py", title="Input", icon=":material/edit:")
history_page = st.Page("history.py", title="History", icon=":material/history:")
home_page = st.Page("home.py", title="Introduction", icon = ":material/home:")



if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Home" : [home_page],
            "Main" : [input_page, history_page],
            "Account": [logout_page],
        }
    )
    pg.run()
else:
    pg = st.navigation([login_page])
    pg.run()
