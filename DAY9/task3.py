import streamlit as st

st.title("Form App")

with st.form("registration_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    submitted = st.form_submit_button("Submit")

if submitted:
    if not name.strip():
        st.error("Name cannot be empty")
    elif "@" not in email:
        st.error("Please enter a valid email address")
    elif age <= 0:
        st.error("Age must be greater than 0")
    else:
        st.success(f"Welcome {name}! Registration successful.")
        st.write(f"Email: {email}")
        st.write(f"Age: {age}")