from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import todos, github, jira, calendar, gmail, google_auth
import time
from sqlalchemy.exc import OperationalError

# Retry logic for DB connection
def create_tables():
    retries = 5
    while retries > 0:
        try:
            models.Base.metadata.create_all(bind=engine)
            print("Database tables created successfully")
            break
        except OperationalError:
            retries -= 1
            print(f"Database not ready, retrying in 2 seconds... ({retries} left)")
            time.sleep(2)

create_tables()

app = FastAPI(title="AIN Dashboard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For minimal friction in local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router)
app.include_router(github.router)
app.include_router(jira.router)
app.include_router(calendar.router)
app.include_router(gmail.router)
app.include_router(google_auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AIN Dashboard API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
