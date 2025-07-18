import streamlit as st
import requests
import os
from requests.exceptions import RequestException

# Get backend URL from environment variable or use default
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.title("🔍 Tech Term Explainer")
st.subheader("Enter a technical term to get a detailed explanation")

term = st.text_input("Enter a technical term:")

if st.button("Explain"):
    if not term:
        st.error("Please enter a term to explain")
    else:
        try:
            with st.spinner("Getting explanation..."):
                res = requests.post(f"{BACKEND_URL}/explain", json={"term": term})
                
                if res.status_code == 200:
                    st.success("Explanation found!")
                    st.write(res.json()['response'])
                else:
                    st.error(f"Error: {res.status_code} - {res.text}")
        except RequestException as e:
            st.error(f"Connection error: {str(e)}. Please check if the backend service is running.")