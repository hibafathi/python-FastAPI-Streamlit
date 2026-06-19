import streamlit as st
st.title("calculator")
a=st.number_input ( " enter the first number")
b=st.number_input ( "enter the second number")
op=st.selectbox ( "select the operator",["+","-","*","/"])
if st.button("calculate"):
    if op=="+":
        res=a+b
    elif op=="-":
        res=a-b
    elif op=="*":
        res=a*b
    elif op=="/":
        if b!=0:
            res=a/b
        else:
            st.error("division by zero is not allowed")
            res=None
    if res is not None:
        st.success(f"Result = {res}")