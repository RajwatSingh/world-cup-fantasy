from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import ranking

app = FastAPI()

# app.add_middleware(
#   CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["GET"]
# )

_cache = {"rows": None}


def _rows():
    if _cache["rows"] is None:
        ranking.main()

        _cache["rows"] = ranking.full_player_info

    return _cache["rows"]


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
    ranks = _rows()
    result = {}

    for p, s in ranks.items():
        if s["position"] == position:
            result[p] = s

    return result
