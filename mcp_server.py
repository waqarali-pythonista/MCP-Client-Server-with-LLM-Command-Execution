
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import logging
import re
import platform
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# ------------------------- FastAPI Setup ------------------------- #
app = FastAPI()

# ------------------------- Logging Setup ------------------------- #
logging.basicConfig(
    filename="mcp_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ------------------------- Langchain & Ollama Setup ------------------------- #
template = """You are an AI assistant that only outputs shell commands. Do not provide explanations.

User Query: {question}

Shell Command:"""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2:latest")  # ✅ Using LLaMA 3.2

chain = prompt | model

# ------------------------- Security: Block Dangerous Commands ------------------------- #
BLOCKED_COMMANDS = {"rm", "shutdown", "reboot", "poweroff", "del", "format", "mkfs", "dd"}

def is_safe_command(command: str) -> bool:
    """Checks if the command contains any dangerous operations."""
    return not any(re.search(rf"\b{cmd}\b", command, re.IGNORECASE) for cmd in BLOCKED_COMMANDS)

# ------------------------- OS Compatibility Fix ------------------------- #
def fix_command_for_os(command: str) -> str:
    """Converts Linux commands to Windows equivalent if necessary."""
    if platform.system() == "Windows":
        command = command.replace("ls -l", "dir").replace("ls", "dir")
    return command

# ------------------------- Function to Clean Generated Commands ------------------------- #
def clean_generated_command(response: str) -> str:
    """Cleans the LLM-generated command by removing unnecessary formatting like triple backticks."""
    return re.sub(r"```(?:\w+)?", "", response.strip())  # Remove ``` and any optional language specifier

# ------------------------- Command Execution Function ------------------------- #
def execute_command(command: str) -> str:
    """Executes a shell command safely and returns the output."""
    try:
        if not is_safe_command(command):
            logging.warning(f"Blocked Command Attempt: {command}")
            return "Error: Command blocked for security reasons."

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip() if result.stdout else result.stderr.strip()

        if result.returncode != 0:
            logging.error(f"Command execution failed: {output}")
            return f"Error: {output}"

        return output
    except Exception as e:
        logging.error(f"Command execution error: {str(e)}")
        return f"Exception: {str(e)}"

# ------------------------- API Endpoint ------------------------- #
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    """Receives a query, generates a system command using LLM, executes it, and returns the result."""
    try:
        user_query = request.query.strip()
        logging.info(f"Received Query: {user_query}")

        # Generate system command using LLM
        raw_response = chain.invoke({"question": user_query})
        generated_command = clean_generated_command(raw_response)

        # ✅ Fix for Windows/Linux compatibility
        generated_command = fix_command_for_os(generated_command)

        logging.info(f"Generated Command: {generated_command}")

        # Execute the generated command
        execution_result = execute_command(generated_command)
        logging.info(f"Execution Result: {execution_result}")

        return {"command": generated_command, "result": execution_result}
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
