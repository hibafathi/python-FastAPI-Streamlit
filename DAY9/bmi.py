import streamlit as st

st.title("BMI Calculator")

weight = st.number_input("Weight (kg)")
height = st.number_input("Height (m)")

if st.button("Calculate"):

    bmi = weight / (height ** 2)

    st.success(f"BMI = {bmi:.2f}")