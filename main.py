from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/api/teams")
def get_teams():
    return [
        {"name": "France", "strength": 10.0},
        {"name": "Japan", "strength": 6.9},
        {"name": "Haiti", "strength": 2.4},
    ]
