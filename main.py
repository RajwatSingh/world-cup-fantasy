from fastapi import FastAPI

import ranking

app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/api/teams")
def get_teams(min_strength: float = 0):
    teams = ranking.TEAM_STRENGTH
    result = {}

    for t, s in teams.items():
        if s >= min_strength:
            result[t] = s

    return result
