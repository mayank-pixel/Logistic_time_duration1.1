import streamlit as st

def get_or_init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]
