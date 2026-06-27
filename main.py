import json

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


@app.get("/api/players")
def get_players(position: str = ""):
    ranking.main()
    ranks = ranking.full_player_info
    result = {}

    for p, s in ranks.items():
        if s["position"] == position:
            result[p] = s

    print(json.dumps(result, indent=4))
    return result


get_players("FWD")
