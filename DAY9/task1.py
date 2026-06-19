import streamlit as st

st.title("Greeting App")

st.session_state.setdefault("name", "")
st.session_state.setdefault("greeting", "")

name_input = st.text_input("Enter your name", value=st.session_state["name"])

if st.button("Say Hello"):
    st.session_state["name"] = name_input
    st.session_state["greeting"] = f"Hello, {name_input}!"

if st.session_state["greeting"]:
    st.write(st.session_state["greeting"])