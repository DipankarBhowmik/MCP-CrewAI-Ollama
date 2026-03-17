    # crew_with_mcp.py
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

# ✅ Connect to Ollama (SmolLM2 135M)
llm = LLM(
    #model="ollama/smollm2:135m",
    model="ollama/phi3",
    base_url="http://127.0.0.1:11434",  # ✅ must include /v1
    api_key="NA" , # Ollama ignores this but CrewAI requires a value
    timeout=300
)

# 1. Define server parameters to connect to your MCP server
server_params = StdioServerParameters(
    command="python",
    args=["math_mcp_server.py"],  # points to our server file
    env={**os.environ},
)

# 2. Start MCPServerAdapter to load tools
with MCPServerAdapter(server_params) as mcp_tools:
    print("✅ Available tools:", [tool.name for tool in mcp_tools])

    # 3. Define the Agent
    agent = Agent(
        role="Math Solver",
        goal="Solve math problems using MCP tools",
        backstory="A helpful local agent that performs basic arithmetic",
        tools=mcp_tools,
        reasoning=False,
        verbose=True,
        llm=llm,  # 🔑 Use Ollama
    )

    # 4. Define a task
    task = Task(
        description="Use the MCP add tool to add 10 and 15.",
        expected_output="25",
        agent=agent,   # bind the agent
    )

    # 5. Assemble and run the crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process="sequential",
    )

    result = crew.kickoff()
    print("\n🎯 Final Result:", result)
