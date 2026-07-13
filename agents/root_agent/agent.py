import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import FunctionTool
from sub_agents.intake_agent.agent import intake_agent
from sub_agents.anomaly_agent.agent import anomaly_agent
from sub_agents.priority_agent.agent import priority_agent
from sub_agents.qa_agent.agent import qa_agent
from firestore_service import save_complaint

def save_to_firestore(complaint_json: str) -> str:
    """Save processed complaint data to Firestore for live tracking.
    
    Args:
        complaint_json: JSON string containing the processed complaint data
    
    Returns:
        complaint_id of the saved document
    """
    try:
        data = json.loads(complaint_json)
        complaint_id = save_complaint(data)
        return f"Complaint saved to Firestore with ID: {complaint_id}"
    except Exception as e:
        return f"Error saving to Firestore: {str(e)}"

firestore_tool = FunctionTool(save_to_firestore)

complaint_pipeline = SequentialAgent(
    name="complaint_pipeline",
    description="Processes a civic complaint through intake, anomaly detection, and priority routing in sequence.",
    sub_agents=[intake_agent, anomaly_agent, priority_agent],
)

root_agent = Agent(
    name="civic_root_agent",
    model="gemini-3.5-flash",
    description="Orchestrates civic complaint triage system.",
    instruction=(
        "You are the orchestrator of a civic complaint triage system for smart cities. "
        "You handle two types of requests: "
        "1. NEW COMPLAINT: When someone describes a civic problem (pothole, water leak, "
        "garbage, broken streetlight, etc.), transfer to complaint_pipeline which will "
        "automatically run intake, anomaly, and priority agents in sequence. "
        "After complaint_pipeline completes, call save_to_firestore with the combined JSON results. "
        "Return the complete results to the user. "
        "2. DATA QUESTION: When someone asks about complaint trends, statistics, or data, "
        "transfer to qa_agent directly. "
        "Always transfer to sub-agents. Never answer yourself."
    ),
    sub_agents=[complaint_pipeline, qa_agent],
    tools=[firestore_tool],
)