import os
from dotenv import load_dotenv
from smolagents import LiteLLMModel, ToolCollection, CodeAgent
from mcp import StdioServerParameters

load_dotenv()

# Initialize Gemini API
gemini_api_key = os.environ.get("GEMINI_API_KEY")
model = LiteLLMModel(
    model_id="gemini/gemini-2.5-flash-lite",
    api_key=gemini_api_key,
)

# THE WORKAROUND: Run the server directly via standard Python
server_parameters = StdioServerParameters(
    command="python",
    args=["-m", "mcp_server_fetch"],
    env={**os.environ}, # Pass current environment variables
)

# Connect the server and run the agent
with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model, add_base_tools=True)
    
    agent.run("Please use the fetch tool to read 'https://huggingface.co/learn/agents-course/unit2/smolagents/tools' and summarize what this page is about.")