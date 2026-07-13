import os
import uuid
from datetime import datetime
from google.cloud import firestore

def save_complaint(complaint_data: dict) -> str:
    """Save a processed complaint to Firestore."""
    try:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        db = firestore.Client(project=project_id)
        complaint_id = str(uuid.uuid4())
        
        doc_data = {
            "complaint_id": complaint_id,
            "timestamp": datetime.utcnow().isoformat(),
            "category": complaint_data.get("category", "other"),
            "ward": complaint_data.get("ward", "unknown"),
            "severity": complaint_data.get("severity", 1),
            "priority_score": complaint_data.get("priority_score", 0),
            "anomaly": complaint_data.get("anomaly", False),
            "department": complaint_data.get("department", "General Services"),
            "status": "new",
            "summary": complaint_data.get("summary", ""),
            "recommended_action": complaint_data.get("recommended_action", ""),
            "estimated_resolution_days": complaint_data.get("estimated_resolution_days", 3),
        }
        
        db.collection("live_complaints").document(complaint_id).set(doc_data)
        return complaint_id
    except Exception as e:
        print(f"Firestore error: {e}")
        return "error" 
