import random
import uuid
from datetime import datetime, timedelta
from google.cloud import bigquery

# Config
PROJECT_ID = "civic-pulse-apac"
DATASET_ID = "civic_pulse_data"
TABLE_ID = "Complaints"

# Sample data
CATEGORIES = ["pothole", "water_leak", "garbage", "streetlight", "other"]
WARDS = ["MG Road", "Jubilee Hills", "Banjara Hills", "Hitech City", 
         "Secunderabad", "Kukatpally", "Madhapur", "Gachibowli", 
         "Begumpet", "Ameerpet"]
DEPARTMENTS = {
    "pothole": "Public Works",
    "water_leak": "Water Utility", 
    "garbage": "Sanitation",
    "streetlight": "Electrical Department",
    "other": "General Services"
}
STATUSES = ["new", "assigned", "in_progress", "resolved"]

def generate_complaints(n=10000):
    rows = []
    now = datetime.utcnow()
    
    for _ in range(n):
        category = random.choice(CATEGORIES)
        severity = random.randint(1, 5)
        anomaly = random.random() < 0.15
        priority_score = min(100, severity * 15 + (25 if anomaly else 0))
        days_ago = random.randint(0, 30)
        timestamp = now - timedelta(days=days_ago, 
                                     hours=random.randint(0, 23),
                                     minutes=random.randint(0, 59))
        
        rows.append({
            "complaint_id": str(uuid.uuid4()),
            "timestamp": timestamp.isoformat(),
            "category": category,
            "ward": random.choice(WARDS),
            "severity": severity,
            "priority_score": priority_score,
            "anomaly": anomaly,
            "department": DEPARTMENTS[category],
            "status": random.choice(STATUSES),
            "summary": f"Citizen reported {category.replace('_', ' ')} issue.",
            "confidence": round(random.uniform(0.7, 1.0), 2),
            "recommended_action": f"Inspect and resolve {category.replace('_', ' ')} issue.",
            "estimated_resolution_days": random.randint(1, 7)
        })
    
    return rows

def main():
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    print("Generating 10,000 synthetic complaints...")
    rows = generate_complaints(10000)
    
    print("Loading to BigQuery...")
    # Use load_table_from_json instead of streaming inserts
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("complaint_id", "STRING"),
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("ward", "STRING"),
            bigquery.SchemaField("severity", "INTEGER"),
            bigquery.SchemaField("priority_score", "INTEGER"),
            bigquery.SchemaField("anomaly", "BOOLEAN"),
            bigquery.SchemaField("department", "STRING"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("summary", "STRING"),
            bigquery.SchemaField("confidence", "FLOAT"),
            bigquery.SchemaField("recommended_action", "STRING"),
            bigquery.SchemaField("estimated_resolution_days", "INTEGER"),
        ],
        write_disposition="WRITE_TRUNCATE",
    )
    
    table = client.get_table(table_ref)
    job = client.load_table_from_json(rows, table, job_config=job_config)
    job.result()
    
    print(f"Successfully loaded {len(rows)} rows into BigQuery!")
    print(f"Table: {table_ref}")

if __name__ == "__main__":
    main()