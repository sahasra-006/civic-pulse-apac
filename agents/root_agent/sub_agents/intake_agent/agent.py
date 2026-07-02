from google.adk.agents import Agent

intake_agent = Agent(
    name="intake_agent",
    model="gemini-2.5-flash",
    description="Classifies civic complaints into categories and severity levels.",
    instruction="""You are a civic complaint intake officer. 
    When given a complaint, extract and return ONLY a JSON object with these exact keys:
    - category: one of [pothole, water_leak, garbage, streetlight, other]
    - severity: integer 1-5 (1=minor, 5=critical)
    - ward: extract location/area name from the complaint, or "unknown" if not mentioned
    - summary: one sentence description of the issue
    - confidence: float 0-1 indicating your confidence in the classification
    
    Return ONLY valid JSON, no extra text, no markdown.""",
) 
