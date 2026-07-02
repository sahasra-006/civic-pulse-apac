import sys
import os

# Add root_agent directory to path so sub_agents can be found
sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from sub_agents.intake_agent.agent import intake_agent
from sub_agents.anomaly_agent.agent import anomaly_agent
from sub_agents.priority_agent.agent import priority_agent
from sub_agents.qa_agent.agent import qa_agent

complaint_pipeline = SequentialAgent(
    name="complaint_pipeline",
    description="Processes a civic complaint through intake, anomaly detection, and priority routing in sequence.",
    sub_agents=[intake_agent, anomaly_agent, priority_agent],
)

root_agent = Agent(
    name="civic_root_agent",
    model="gemini-2.5-flash",
    description="Orchestrates civic complaint triage system.",
    instruction="""You are the orchestrator of a civic complaint triage system for smart cities.

    You handle two types of requests:

    1. NEW COMPLAINT: When someone describes a civic problem (pothole, water leak,
    garbage, broken streetlight, etc.):
       - Transfer to complaint_pipeline which will automatically run intake, anomaly, and priority agents in sequence

    2. DATA QUESTION: When someone asks about complaint trends, statistics, or data:
       - Transfer to qa_agent directly

    Always transfer to sub-agents. Never answer yourself.""",
    sub_agents=[complaint_pipeline, qa_agent],
)
