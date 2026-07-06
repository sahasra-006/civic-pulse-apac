# CivicPulse — Community Infrastructure Intelligence

AI-powered civic complaint triage system that automatically classifies, detects anomalies, and routes citizen complaints to the correct municipal department.

## Live Demo
- **Frontend:** https://civic-pulse-frontend-19402659073.us-central1.run.app
- **Backend API:** https://civic-pulse-agent-19402659073.us-central1.run.app
- **Analytics Dashboard:** https://datastudio.google.com/s/qCMmHEHpWKs

## Problem Statement
Cities receive thousands of civic complaints daily — potholes, water leaks, garbage, broken streetlights. Manual triage is slow, inconsistent, and misses emerging patterns. CivicPulse automates the entire workflow using AI agents.

## Solution
A multi-agent AI system built on Google Cloud ADK that:
- Classifies complaints by category and severity using Gemini
- Detects anomaly spikes (e.g. 12 pothole complaints in one ward vs baseline of 5)
- Computes priority scores and routes to the correct department
- Saves every complaint to Firestore for live tracking
- Provides natural language analytics over 10,000+ historical complaints in BigQuery

## Architecture
- **Root Agent** (Orchestrator) — receives complaints, delegates to sub-agents
- **Intake Agent** — classifies category, severity, ward using Gemini multimodal
- **Anomaly Agent** — detects complaint spikes vs historical baseline
- **Priority Agent** — computes priority score, routes to department, saves to Firestore
- **Q&A Agent** — answers natural language queries against BigQuery data

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Agent Framework | Google ADK 2.3.0 |
| AI Model | Gemini 2.5 Flash (Vertex AI) |
| Deployment | Google Cloud Run |
| Live State | Google Cloud Firestore |
| Historical Data | Google BigQuery (10,000 records) |
| Analytics | Looker Studio |
| Frontend | HTML/CSS/JS served on Cloud Run |

## Setup
```bash
# Clone the repo
git clone https://github.com/sahasra-006/civic-pulse-apac.git
cd civic-pulse-apac

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your GCP project details

# Run locally
adk web agents/
```


