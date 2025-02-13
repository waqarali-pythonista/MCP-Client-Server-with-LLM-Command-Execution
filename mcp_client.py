

import streamlit as st
import requests

# Server URL
SERVER_URL = "http://127.0.0.1:8000/query"

# Streamlit UI
st.title("🖥️ MCP Client - LLM Command Executor")
st.write("Enter a command query, and the system will generate and execute it securely.")

# Input for user command
user_input = st.text_input("Enter your command request:")

if st.button("Send Query"):
    if user_input.strip():
        response = requests.post(SERVER_URL, json={"query": user_input.strip()})
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                st.error(f"Server Response: {data['error']}")
            else:
                st.success("✅ Command Executed Successfully!")
                st.code(f"Generated Command: {data['command']}", language="bash")
                st.text_area("Execution Result:", data['result'], height=200)
        else:
            st.error(f"Server Error: {response.status_code}")
