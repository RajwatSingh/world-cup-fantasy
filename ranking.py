import json
from collections import defaultdict

import requests

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

SQUADS_URL = "https://play.fifa.com/json/match_predictor/squads.json"
ROUNDS_URL = "https://play.fifa.com/json/fantasy/rounds.json"
PLAYERS_URL = "https://play.fifa.com/json/fantasy/players.json"

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


def fetch_json(url):
    response = requests.get(url, headers=HEADERS)
    return response.json()


def player_name(player):
    return f"{player['firstName']} {player['lastName']}"


def map_id_squad():
    for squad in fetch_json(SQUADS_URL):
        teams[squad["id"]] = squad["name"]


def map_id_match():
    for rnd in fetch_json(ROUNDS_URL):
        for match in rnd.get("tournaments", []):
            if (
                match.get("status") == "scheduled"
                and match.get("homeSquadId")
                and match.get("awaySquadId")
            ):
                fixtures[match["id"]] = [match["homeSquadId"], match["awaySquadId"]]


def map_player_position(players):
    for player in players:
        full_player_info[player_name(player)]["position"] = player["position"]


def map_player_fixture(players):
    for player in players:
        fixture = player["stats"]["nextFixtureFromScheduledRound"]
        home, away = fixtures[fixture]
        opponent = away if player["squadId"] == home else home
        full_player_info[player_name(player)]["opponent"] = opponent


def main():
    map_id_squad()
    map_id_match()

    players = fetch_json(PLAYERS_URL)
    map_player_fixture(players)
    map_player_position(players)

    print(json.dumps(full_player_info, indent=4))


if __name__ == "__main__":
    main()
