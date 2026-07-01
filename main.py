import threading
from typing import Set

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import league_ranking
import ranking

app = FastAPI()
DEFAULT_MANAGERS = {"ramborajwat", "AswinKopite", "CHEKCHY", "Prakshyam"}

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["GET"]
)

_cache = {"rows": None}
_lock = threading.Lock()


def _rows():
    if _cache["rows"] is None:
        with _lock:
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

    if not position:
        return ranks

    result = {}

    for p, s in ranks.items():
        if s["position"] == position:
            result[p] = s

    return result


@app.get("/api/ranks")
def get_ranks(players: str = "", round: int = 4):
    names = {m.strip() for m in players.split(",") if m.strip()} or DEFAULT_MANAGERS
    return league_ranking.collect_progression(names, round)
