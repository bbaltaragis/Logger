from typing import Optional
from fastapi import FastAPI
from controller_functions import *
from fastapi.middleware.cors import CORSMiddleware
from models import *
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    create_db()
    return{"Status": "Database Created"}

@app.get("/dashboard")
def read_anomalies():
    return select_dashboard()

@app.get("/anomaly/{id}")
def read_anomaly(id: int):
    return select_anomaly_reference_and_historical_anomalies(id)


@app.get("/seed") #just used to populate db with test data, and create database if a fresh install
def seed_database():
    if check_db_exists():
        seed_goodlogs()
        fill_anomalyreference()
        fill_historicalanomalies()
    else:
        create_db()
        seed_goodlogs()
        fill_anomalyreference()
        fill_historicalanomalies()
    return {"Status": "Database seeded"}

#@app.post will automatically get the data from the request based on the function parameters(e.g. {"anomaly_id": 7} will get the data from the request body)
@app.post("/insertGoodLogs")
def insert_goodLogs(hash: str, name: str, pattern: str, plaintext: str):
    insert_goodlogs(hash, name, pattern, plaintext)
    return {"Status": "Good Logs Inserted"}


@app.post("/insertAnomalyReference")
def insert_anomalyReference(name: str, hash: str, pattern: str, last_occured: str, plaintext: str, root_cause: str, resolution_steps: str):
    insert_anomalyreference(name, hash, pattern, last_occured, plaintext, root_cause, resolution_steps)
    return {"Status": "Anomaly Reference inserted"}

@app.post("/anomaly/{id}/comment")
def create_comment(comment: Comment):
    try:
        insert_anomalycomments(comment.anomaly_id, comment.comment, comment.username)
    except sqlite3.Error as e:
        return {"error": e}
    return {"Status": "Comment added"}

@app.patch("/anomaly/{id}/updateRootCause")
def update_root_cause(root_cause: RootCause):
    try:
        update_rootcause(root_cause.id, root_cause.root_cause)
    except sqlite3.Error as e:
        return {"error": e}
    return {"Status": "Root cause updated"}

@app.patch("/anomaly/{id}/updateResolutionSteps")
def update_resolution_steps(resolution_steps: ResolutionSteps):
    try:
        update_resolutionsteps(resolution_steps.id, resolution_steps.resolution_steps)
    except sqlite3.Error as e:
        return {"error": e}
    return {"Status": "Resolution steps updated", "resolution_steps": resolution_steps}

if os.path.isfile('Logger.db'):
    print("Logger.db exists")
else:
    create_db()
