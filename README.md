# FinTech Fraud Detection REST API 

## Business Context
In the financial sector, transaction authorization systems must evaluate complex business rules in milliseconds to prevent fraud while ensuring a frictionless user experience. This project simulates a core banking authorization engine.

## Architecture & Features
A stateful REST API built with **FastAPI** and **SQLite** that evaluates incoming JSON transaction payloads against a rules engine:

1. **Velocity Check:** Queries historical database records to block accounts attempting more than 3 transactions in a short window.
2. **High-Ticket Threshold:** Automatically rejects transactions exceeding $5,000 USD to flag potential embezzlement.
3. **Geo-Fencing:** Blocks transactions originating from high-risk geographic locations.

## Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** SQLite (Relational persistence)
* **Data Validation:** Pydantic
* **Server:** Uvicorn

## How to Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload


Visit http://127.0.0.1:8000/docs to test the endpoints via the interactive Swagger UI.

