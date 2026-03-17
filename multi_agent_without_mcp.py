from crewai import Agent, Task, Crew, LLM
from tool import add, multiply

# ✅ Connect to Ollama
llm = LLM(
    model="ollama/phi3",
    base_url="http://127.0.0.1:11434",
    api_key="NA",
    timeout=1200
)

# Agent A
agent_add = Agent(
    role="Addition Expert",
    goal="Solve addition problems",
    backstory="Expert in arithmetic",
    llm=llm,
    verbose=True
)

# Agent B
agent_multiply = Agent(
    role="Multiplication Expert",
    goal="Solve multiplication problems",
    backstory="Expert in multiplication",
    llm=llm,
    verbose=True
)

# Tasks
task1 = Task(
    description="Add 10 and 15",
    expected_output="The result of 10 + 15",
    agent=agent_add
)

task2 = Task(
    description="Multiply 6 and 7",
    expected_output="The result of 6 × 7",
    agent=agent_multiply
)

crew = Crew(
    agents=[agent_add, agent_multiply],
    tasks=[task1, task2],
    verbose=True
)

crew.kickoff()

# Direct tool usage
print("Agent A result:", add(10, 15))
print("Agent B result:", multiply(6, 7))