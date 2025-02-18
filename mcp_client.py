

# import streamlit as st
# import requests

# # Server URL
# SERVER_URL = "http://127.0.0.1:8000/query"

# # Streamlit UI
# st.title("🖥️ MCP Client - LLM Command Executor")
# st.write("Enter a command query, and the system will generate and execute it securely.")

# # Input for user command
# user_input = st.text_input("Enter your command request:")

# if st.button("Send Query"):
#     if user_input.strip():
#         response = requests.post(SERVER_URL, json={"query": user_input.strip()})
        
#         if response.status_code == 200:
#             data = response.json()
            
#             if "error" in data:
#                 st.error(f"Server Response: {data['error']}")
#             else:
#                 st.success("✅ Command Executed Successfully!")
#                 st.code(f"Generated Command: {data['command']}", language="bash")
#                 st.text_area("Execution Result:", data['result'], height=200)
#         else:
#             st.error(f"Server Error: {response.status_code}")

# import streamlit as st
# import requests
# import uuid

# # Server URL
# SERVER_URL = "http://127.0.0.1:8000/mcp/query"

# # Streamlit UI
# st.title("🖥️ MCP Client - LLM Command Executor")
# st.write("Enter a command query, and the system will generate and execute it securely.")

# # Input for user command
# user_input = st.text_input("Enter your command request:")

# if st.button("Send Query"):
#     if user_input.strip():
#         session_id = str(uuid.uuid4())  # Generate unique session ID
#         payload = {
#             "protocol": "MCP",
#             "version": "1.0",
#             "session_id": session_id,
#             "message_type": "query",
#             "payload": {"query": user_input.strip()},
#         }
        
#         response = requests.post(SERVER_URL, json=payload)
        
#         if response.status_code == 200:
#             data = response.json()
            
#             if data["status"] == "error":
#                 st.error(f"Server Response: {data['payload']['error']}")
#             else:
#                 st.success("✅ Command Executed Successfully!")
#                 st.code(f"Generated Command: {data['payload']['command']}", language="bash")
#                 st.text_area("Execution Result:", data['payload']['result'], height=200)
#         else:
#             st.error(f"Server Error: {response.status_code}")


import streamlit as st
import requests
import uuid

# Server URL
SERVER_URL = "http://127.0.0.1:8000/mcp/query"

# Streamlit UI
st.title("🖥️ MCP Client - LLM Command Executor")
st.write("Enter a command query, and the system will generate and execute it securely.")

# Input for user command
user_input = st.text_input("Enter your command request:")

if st.button("Send Query"):
    if user_input.strip():
        session_id = str(uuid.uuid4())  # Generate unique session ID
        payload = {
            "protocol": "MCP",
            "version": "1.0",
            "session_id": session_id,
            "message_type": "query",
            "payload": {"query": user_input.strip()},
        }
        
        response = requests.post(SERVER_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            if "mcpServers" in data and "error" in data["mcpServers"]:
                st.error(f"Server Response: {data['mcpServers']['error']['message']}")
            elif "mcpServers" in data and "commandExecution" in data["mcpServers"]:
                command_data = data["mcpServers"]["commandExecution"]
                st.success("✅ Command Executed Successfully!")
                st.code(f"Generated Command: {command_data['command']} {' '.join(command_data['args'])}", language="bash")
                st.text_area("Execution Result:", command_data['output'], height=200)
            else:
                st.error("Unexpected server response format.")
        else:
            st.error(f"Server Error: {response.status_code}")