import streamlit as st

st.session_state.debug = False

pages = {
    "Your account": [
        st.Page("home.py", title="Info"),
        st.Page("study.py", title="Study"),
        st.Page("timerConfig.py", title="Configure Timer"),
        st.Page("listConfig.py", title="Configure To-Do List"),
    ],
}

pg = st.navigation(pages)
pg.run()