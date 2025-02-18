# MCP Client-Server with LLM Command Execution

## 📌 Overview
This project implements an MCP (Model Context Protocol) Client-Server system that integrates with an LLM (Groq or Ollama) to dynamically generate and execute system commands securely.

## 🏗️ Features
- **FastAPI-based Server**: Handles command generation and execution securely.
- **LLM Integration**: Uses Ollama to generate appropriate system commands from natural language queries.
- **Client Application**: Allows users to send queries and receive execution results.
- **Security Measures**: Blocks dangerous commands to prevent unintended execution.
- **Cross-Platform Compatibility**: Converts Linux commands to Windows equivalents where necessary.
- **Logging**: Records queries, generated commands, and execution results.

---

## 🚀 Setup Instructions
### 1️⃣ Install Dependencies
Ensure you have Python (3.8+) installed, then run:
```bash
pip install fastapi uvicorn requests langchain_ollama
```

### 2️⃣ Start the Server
Run the FastAPI server:
```bash
python mcp_server.py
```
This will start the API at `http://127.0.0.1:8000`

### 3️⃣ Run the Client
Execute the client script to interact with the server:
```bash
python mcp_client.py
```
Or, use the Streamlit web app for a frontend experience:
```bash
streamlit run mcp_app.py
```

---

## 🛠️ Usage Guide
1. Start the FastAPI server.
2. Open the client (CLI or Streamlit UI).
3. Enter a command request (e.g., *List all files in the directory*).
4. The LLM generates a command, which is executed securely.
5. View the execution result.

---

## 🔐 Security Considerations
- **Blocked Commands**: Dangerous commands (e.g., `rm`, `shutdown`, `del`) are restricted.
- **Input Validation**: Ensures only safe commands are executed.
- **Error Handling**: Prevents execution failures from crashing the application.

---

## 📝 Troubleshooting
| Issue | Solution |
|--------|---------|
| Server not starting | Ensure FastAPI & dependencies are installed correctly. Try `pip install -r requirements.txt`. |
| LLM not generating commands | Check if Ollama is running properly and accessible. |
| Windows/Linux command mismatch | The system automatically converts commands (e.g., `ls` → `dir`). |
| Connection refused | Ensure the server is running before starting the client. |

---

## 📜 Contribution
Feel free to contribute by forking the repository and submitting pull requests!

📌 **GitHub Repository**: [MCP Client-Server with LLM](https://github.com/waqarali-pythonista/MCP-Client-Server-with-LLM-Command-Execution)

