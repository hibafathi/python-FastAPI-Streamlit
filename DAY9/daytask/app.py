import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.session_state.setdefault("page", "login")
st.session_state.setdefault("token", None)
st.session_state.setdefault("email", None)


def login_page():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not email.strip() or not password.strip():
            st.error("Please fill in both email and password")
            return

        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state["token"] = data["access_token"]
                st.session_state["email"] = email
                st.session_state["page"] = "dashboard"
                st.rerun()
            else:
                error_detail = response.json().get("detail", "Login failed")
                st.error(error_detail)

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to server. Make sure backend.py is running.")


def dashboard_page():
    st.title("Dashboard")
    st.success(f"Welcome, {st.session_state['email']}!")
    st.write("This is a placeholder dashboard.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()


if st.session_state["page"] == "login":
    login_page()
elif st.session_state["page"] == "dashboard":
    dashboard_page()