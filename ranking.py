import json
from collections import defaultdict

import requests

TEAM_STRENGTH = {
    "France": 10.0,
    "Spain": 9.7,
    "Argentina": 9.6,
    "England": 9.2,
    "Brazil": 9.1,
    "Portugal": 9.0,
    "Netherlands": 8.4,
    "Germany": 8.3,
    "Belgium": 8.0,
    "Morocco": 7.8,
    "Croatia": 7.7,
    "Colombia": 7.2,
    "Uruguay": 7.1,
    "Japan": 6.9,
    "Switzerland": 6.8,
    "Senegal": 6.7,
    "Mexico": 6.4,
    "United States": 6.2,
    "South Korea": 6.0,
    "Ecuador": 5.9,
    "Austria": 5.8,
    "Iran": 5.6,
    "Norway": 5.6,
    "Australia": 5.3,
    "Egypt": 5.2,
    "Türkiye": 5.1,
    "Ivory Coast": 5.0,
    "Sweden": 5.0,
    "Canada": 4.9,
    "Scotland": 4.7,
    "Algeria": 4.6,
    "Qatar": 4.4,
    "Czechia": 4.4,
    "Paraguay": 4.2,
    "Tunisia": 4.1,
    "Bosnia & Herzegovina": 4.0,
    "Ghana": 3.9,
    "DR Congo": 3.7,
    "South Africa": 3.6,
    "Saudi Arabia": 3.5,
    "Panama": 3.4,
    "Iraq": 3.2,
    "Uzbekistan": 3.0,
    "Cape Verde": 2.8,
    "Jordan": 2.7,
    "Haiti": 2.4,
    "New Zealand": 2.3,
    "Curaçao": 2.0,
}

full_player_info = defaultdict(dict)
fixtures = {}
teams = {}


def map_id_squad():
    squad_url = "https://play.fifa.com/json/match_predictor/squads.json"
    squads = requests.get(
        squad_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )
    data = squads.json()

    for m in data:
        id = m["id"]
        country = m["name"]

        teams[id] = country


def map_id_match():
    round_url = "https://play.fifa.com/json/fantasy/rounds.json"
    rounds = requests.get(
        round_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )
    rounds_data = rounds.json()
    for rnd in rounds_data:
        for m in rnd.get("tournaments", []):
            if (
                m.get("status") == "scheduled"
                and m.get("homeSquadId")
                and m.get("awaySquadId")
            ):
                fixtures[m["id"]] = [m["homeSquadId"], m["awaySquadId"]]


def map_player_position():
    players_url = "https://play.fifa.com/json/fantasy/players.json"
    players = requests.get(
        players_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    )
    data = players.json()

    for p in data:
        name = f"{p['firstName']} {p['lastName']}"
        position = p["position"]
        full_player_info[name]["position"] = position


def map_player_fixture(data):
    for r in data:
        p = r["stats"]
        name = f"{r['firstName']} {r['lastName']}"
        fixture = p["nextFixtureFromScheduledRound"]
        team = r["squadId"]

        if team == fixtures[fixture][0]:
            full_player_info[name]["opponent"] = fixtures[fixture][1]
        else:
            full_player_info[name]["opponent"] = fixtures[fixture][0]


players_url = "https://play.fifa.com/json/fantasy/players.json"
players = requests.get(
    players_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
)
map_id_match()
map_id_squad()
data = players.json()

map_player_fixture(data)
map_player_position()
print(json.dumps(full_player_info, indent=4))
