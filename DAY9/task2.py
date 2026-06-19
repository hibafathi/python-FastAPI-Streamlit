import streamlit as st

st.title("Counter App")

st.session_state.setdefault("count", 0)

col1, col2 = st.columns(2)

with col1:
    if st.button("Increment"):
        st.session_state["count"] += 1

with col2:
    if st.button("Reset"):
        st.session_state["count"] = 0

st.metric("Total Clicks", st.session_state["count"])