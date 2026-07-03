import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from firestore_service import save_complaint
import json

def write_to_firestore(priority_json: str) -> str:
    """Write the final complaint with priority data to Firestore.
    
    Args:
        priority_json: JSON string with priority_score, department, 
                      recommended_action, estimated_resolution_days
    
    Returns:
        Confirmation message with complaint ID
    """
    try:
        data = json.loads(priority_json)
        complaint_id = save_complaint(data)
        return f"Saved to Firestore with ID: {complaint_id}"
    except Exception as e:
        return f"Firestore save failed: {str(e)}"

firestore_tool = FunctionTool(write_to_firestore)

priority_agent = Agent(
    name="priority_agent",
    model="gemini-2.5-flash",
    description="Computes priority score and routes complaint to correct department.",
    instruction=(
        "You are a civic complaint routing officer. "
        "You will receive a JSON object containing complaint classification and anomaly data. "
        "Based on this, compute: "
        "- priority_score: integer 0-100 (severity * 15, add 25 if anomaly=true, add 10 if water_leak, add 5 if streetlight, cap at 100) "
        "- department: pothole->Public Works, water_leak->Water Utility, garbage->Sanitation, streetlight->Electrical Department, other->General Services "
        "- recommended_action: one clear sentence on what the department should do "
        "- estimated_resolution_days: integer estimate based on priority "
        "Then call write_to_firestore with the complete JSON including all fields from previous agents plus your computed fields. "
        "Finally return only valid JSON with keys: priority_score, department, recommended_action, estimated_resolution_days."
    ),
    tools=[firestore_tool],
)
