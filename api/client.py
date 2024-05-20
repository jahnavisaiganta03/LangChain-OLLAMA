import requests
import streamlit as st

def get_openai_response(input_text):
    response=requests.post("http://localhost:8000/openai/invoke",
    json={'input':{'topic':input_text}})

    return response.json()['output']['content']

def get_llama2_response(input_text):
    response=requests.post(
    "http://localhost:8000/llama2/invoke",
    json={'input':{'topic':input_text}})

    return response.json()['output']

def get_llama3_response(input_text):
    response=requests.post(
    "http://localhost:8000/llama3/invoke",
    json={'input':{'topic':input_text}})

    return response.json()['output']

    ## streamlit framework

st.title('Langchain Routes test')
input_text=st.text_input("OPENAI")
input_text1=st.text_input("LLAMA2")
input_text2=st.text_input("LLAMA3")
if input_text:
    st.write(get_openai_response(input_text))

if input_text1:
    st.write(get_llama2_response(input_text1))

if input_text2:
    st.write(get_llama2_response(input_text2))