import json
import os

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://play.fifa.com/api/en/fantasy/ranking/league/8578?limit=20"
HEADERS = {
    "Accept": "application/json",
    "Cookie": os.getenv("COOKIE"),
    "User-Agent": "Mozilla/5.0",
    "Baggage": "sentry-environment=production,sentry-release=fifa-fe-1782916743467,sentry-public_key=8e2fa71bc4354a02b2a80d418f24f274,sentry-trace_id=7bac736bf4bc458f94978a582c9bcd63,sentry-sampled=false,sentry-sample_rand=0.8160473035776491,sentry-sample_rate=0.1",
}


def get_people(startId, managers):
    page = 1
    result = {}

    while True:
        url = f"{URL}&page={page}&startId={startId}"
        request = requests.get(url, headers=HEADERS, timeout=10)

        if request.status_code != 200:
            print(f"request failed: status {request.status_code} on page {page}")
            break

        data = request.json()

        ranks = data.get("success", {}).get("ranks", [])
        if not ranks:
            break

        for m in ranks:
            if m.get("userName") in managers:
                result[m["userName"]] = {
                    "overall_points": m.get("overallPoints"),
                    "rank": m.get("overallRank"),
                }
        page += 1

    return result


def collect_progression(managers, num_rounds):
    progression = {m: {"rounds": [], "ranks": [], "points": []} for m in managers}
    people = {}

    for rnd in range(1, num_rounds + 1):
        people = get_people(rnd, managers)

        for manager, stats in people.items():
            entry = progression[manager]
            entry["rounds"].append(rnd)
            entry["ranks"].append(stats["rank"])
            entry["points"].append(stats["overall_points"])

    print(json.dumps(people, indent=4))
    return progression


def plot_progression(progression, path="league_progression.png"):
    fig, (rank_ax, points_ax) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    for manager, entry in progression.items():
        if not entry["rounds"]:
            continue
        rank_ax.plot(entry["rounds"], entry["ranks"], marker="o", label=manager)
        points_ax.plot(entry["rounds"], entry["points"], marker="o", label=manager)

    rank_ax.set_title("League rank progression")
    rank_ax.set_ylabel("Overall rank")
    rank_ax.invert_yaxis()  # rank 1 (best) sits at the top
    rank_ax.grid(True, alpha=0.3)
    rank_ax.legend()

    points_ax.set_title("League points progression")
    points_ax.set_ylabel("Overall points")
    points_ax.set_xlabel("Round")
    points_ax.grid(True, alpha=0.3)
    points_ax.legend()

    # Only whole-numbered rounds make sense on the x-axis.
    all_rounds = sorted({r for e in progression.values() for r in e["rounds"]})
    if all_rounds:
        points_ax.set_xticks(all_rounds)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved progression graph to {path}")


if __name__ == "__main__":
    MANAGERS = {"ramborajwat", "AswinKopite", "CHEKCHY", "Prakshyam"}
    NUM_ROUNDS = 4

    data = collect_progression(MANAGERS, NUM_ROUNDS)
    plot_progression(data)
