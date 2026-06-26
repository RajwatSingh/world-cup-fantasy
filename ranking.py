import json
import os
import time
import unicodedata
from collections import defaultdict
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

TIMEOUT = 30  # seconds per request

CACHE_DIR = ".cache"


def make_session():
    """A session that reuses connections and retries on dropped/throttled requests."""
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1.0,  # 0s, 1s, 2s, 4s, 8s between attempts
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


SESSION = make_session()

SQUADS_URL = "https://play.fifa.com/json/match_predictor/squads.json"
ROUNDS_URL = "https://play.fifa.com/json/fantasy/rounds.json"
PLAYERS_URL = "https://play.fifa.com/json/fantasy/players.json"
PLAYERS_STATS_URL = "https://play.fifa.com/json/fantasy/player_stats"


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
PENALTY_TAKERS = {
    "Kylian Mbappé",  # France
    "Harry Kane",  # England
    "Lionel Messi",  # Argentina
    "Cristiano Ronaldo",  # Portugal
    "Mohamed Salah",  # Egypt
    "Erling Haaland",  # Norway
    "Kevin De Bruyne",  # Belgium
    "Cody Gakpo",  # Netherlands
    "Kai Havertz",  # Germany
    "Riyad Mahrez",  # Algeria
    "Federico Valverde",  # Uruguay
    "Mikel Oyarzabal",  # Spain
    "Raphinha",  # Brazil       (likely matches knownName, not first+last)
    "Brahim Díaz",  # Morocco
    "Granit Xhaka",  # Switzerland
    "James Rodríguez",  # Colombia
    "Ayase Ueda",  # Japan
    "Sadio Mané",  # Senegal
    "Raúl Jiménez",  # Mexico
    "Christian Pulisic",  # USA
    "Enner Valencia",  # Ecuador
    "Marko Arnautović",  # Austria
    "Mehdi Taremi",  # Iran
    "Ajdin Hrustić",  # Australia
    "Hakan Çalhanoğlu",  # Türkiye
    "Franck Kessié",  # Ivory Coast
    "Viktor Gyökeres",  # Sweden
    "Jonathan David",  # Canada
    "Scott McTominay",  # Scotland
    "Yoane Wissa",  # DR Congo
    "Luka Modrić",  # Croatia
    "Vin\u00edcius J\u00fanior",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().replace("-", " ").replace(".", "").split())


full_player_info = defaultdict(dict)
fixtures = {}
teams = {}
pen_takers = {norm(n) for n in PENALTY_TAKERS}
player_rank = {}


def cached_json(name, fetch):
    """Return a cached JSON response from disk, fetching and storing it on a miss.

    The cache never expires; delete the CACHE_DIR folder to force a refresh.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    data = fetch()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data


def url_to_name(url):
    path = urlparse(url).path.strip("/")
    return path.replace("/", "_") or "index.json"


def get_json(url):
    response = SESSION.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    time.sleep(0.2)  # be polite; avoid bursting the server into closing connections
    return response.json()


def fetch_json(url):
    return cached_json(url_to_name(url), lambda: get_json(url))


def get_stats(id):
    url = f"{PLAYERS_STATS_URL}/{id}.json"
    return cached_json(f"player_stats_{id}.json", lambda: get_json(url))


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
        stats = player["stats"]
        fixture = (
            stats["nextFixtureFromScheduledRound"]
            or stats["nextFixtureFromActiveRound"]
        )
        if fixture is None or fixture not in fixtures:
            continue
        home, away = fixtures[fixture]
        opponent = away if player["squadId"] == home else home
        full_player_info[player_name(player)]["opponent"] = teams[opponent]


def map_player_team(players):
    for player in players:
        squad_id = player["squadId"]
        team = teams[squad_id]
        full_player_info[player_name(player)]["team"] = team


def map_player_penalty(players):
    for player in players:
        name = player_name(player)
        known = player["knownName"]

        full_player_info[name]["penalty_taker"] = norm(name) in pen_takers or (
            known is not None and norm(known) in pen_takers
        )


def map_player_stats(players):
    for player in players:
        name = player_name(player)
        pos = player["position"]
        data = get_stats(player["id"])

        info = full_player_info[name]
        info["selected"] = player["percentSelected"]

        shots = goals = minutes = chances = tackles = 0
        clean_sheets = conceded = saves = 0
        for s in data:
            st = s["stats"]
            shots += st.get("ST", 0)
            goals += st.get("GS", 0)
            minutes += st.get("MP", 0)
            chances += st.get("CC", 0)
            tackles += st.get("T", 0)
            clean_sheets += st.get("CS", 0)
            conceded += st.get("GC", 0)
            saves += st.get("S", 0)

        info["shots"] = shots
        info["goals_scored"] = goals
        info["minutes_played"] = minutes
        if pos == "MID":
            info["chances"] = chances
            info["tackles"] = tackles
        elif pos in ("DEF", "GK"):
            info["clean_sheets"] = clean_sheets
            info["goals_conceded"] = conceded
            if pos == "GK":
                info["saves"] = saves


def rank_players():
    for name, info in full_player_info.items():
        opponent = info.get("opponent")
        if opponent is None:
            continue

        opp_strength = TEAM_STRENGTH.get(opponent)
        team_strength = TEAM_STRENGTH.get(info["team"])
        if opp_strength is None or team_strength is None:
            continue

        score = 0

        # weaker opponent (lower strength) is a more favourable fixture
        score += (1 / opp_strength) * 2

        score += team_strength / 10

        if info.get("penalty_taker"):
            score += 3

        score += info.get("shots", 0) / 2

        if info["position"] == "MID":
            score += (info.get("chances", 0) + info.get("tackles", 0)) / 4

        if info["position"] == "GK":
            score += info.get("saves", 0) / 8

        goals = info.get("goals_scored", 0)
        score += goals

        goals_conceded = info.get("goals_conceded", 0)
        clean_sheets = info.get("clean_sheets", 0)
        score += clean_sheets
        if goals_conceded:
            score += 1 / goals_conceded

        selected = info.get("selected", 0)

        if selected < 5:
            score += 4
        else:
            score += 3 - selected / 100

        if info["minutes_played"] < 100:
            score = 0
        else:
            score += info["minutes_played"] / 100

        player_rank[name] = score


def main():
    map_id_squad()
    map_id_match()

    players = fetch_json(PLAYERS_URL)
    map_player_fixture(players)
    map_player_position(players)
    map_player_team(players)
    map_player_penalty(players)
    map_player_stats(players)

    rank_players()
    final = {}
    items = list(player_rank.items())

    for player, score in items:
        if score == 0:
            player_rank.pop(player)

    final = dict(sorted(player_rank.items(), key=lambda item: item[1], reverse=True))

    print(json.dumps(full_player_info, indent=4, ensure_ascii=False))
    print(json.dumps(final, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
