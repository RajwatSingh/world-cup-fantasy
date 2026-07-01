import json

import matplotlib.pyplot as plt
import requests

URL = "https://play.fifa.com/api/en/fantasy/ranking/league/8578?limit=20"
HEADERS = {
    "Accept": "application/json",
    "Cookie": "_abck=79E9EBD910BF5AA4C46C63E793235D16~0~YAAQDBzFFxp4XgqfAQAANE20FhB6CY8Dp9k8vOupuJTHNhg+ArkmJVje+v/vNekf7S5kaRKZVaTMD+z3u2XhgdGxf7OKPCXZT8gy8w6ToAmfZUrE+vKGGmaLpMXSJ0CRh0777v02evOzpWSvLE4dlTQ+Q6e1XoQbef4chxt4gkDuPuLcpRZTHpPQTcW5JKPkx4cgKut0XSFN73pdaSy4PtjwZmPNSuw1LQoLaNfIjLwzOvejUVKwNmcn84PODvB4fYt4C1X7cMjN23F9zVE8lSPB+AGzNyOUN7SPLkhtEtKmqSYcLplH84pRbSyDZr+SfrzUNOoFV8tKjHMeSm+OOMH/+4uk9K6i9miBGvbCG4jS/sZslkVMc91QQohbf76CDaEIbhrvIpwSxAss9VU/RRsQ6qgS8ON4/kYQdqSvcnqLFqU56MJDWQg8uf8Mwh0oIPpAJVq9LakkftT7BSf/uIjX/kKquued9xQyT1aZOHj+1Z3HeBjeg/P/eeaLGX+VuiLovEng+J3eaY/fNqiFdHgrmhZU65hCYrJZCfONqidz/+zXmHJ7jA/3bXGZRQpSOyOhDXVjnSBVJ4okGYJc8PKYMapKf2q38/8sVTm1ve6nVqMEu3utFOQOZDsjJhgL/I4u8hd8CjhkhowOA2ZQITRgqHmWTYoz2Mc=~-1~-1~1782713543~AAQAAAAF%2f%2f%2f%2f%2fy1abPoOvmihatSmjulqpZ+ZJdj1Y32ssvXu5BjsCibFdoi2KNIf%2fFcvRHD%2fGGziydr2HWZo++2+D1%2fkGCeMNTeMB8UTbpsJL2JA~-1; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+30+2026+12%3A32%3A40+GMT%2B0545+(Nepal+Time)&version=202603.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=43eced2b-3b9e-4d8d-8367-0a442832fe0f&interactionCount=1&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&hosts=&genVendors=V12%3A1%2CV6%3A1%2CV8%3A0%2CV15%3A0%2CV14%3A0%2CV4%3A0%2CV22%3A0%2CV16%3A0%2CV17%3A0%2CV9%3A1%2CV10%3A0%2CV21%3A0%2CV20%3A0%2CV13%3A0%2CV18%3A0%2CV25%3A0%2CV3%3A0%2CV19%3A0%2CV24%3A0%2CV7%3A1%2CV26%3A1%2CV11%3A0%2CV5%3A1%2C&intType=1&crTime=1780561526689&geolocation=NP%3B3&AwaitingReconsent=false&isDntEnabled=0; OptanonAlertBoxClosed=2026-06-04T08:25:25.876Z; AMCV_2F2827E253DAF0E10A490D4E%40AdobeOrg=1176715910%7CMCMID%7C85941341052282215104280818240894060536%7CMCAAMLH-1783405794%7C3%7CMCAAMB-1783405794%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1782808194s%7CNONE%7CMCSYNCSOP%7C411-20636%7CvVersion%7C5.4.0%7CMCIDTS%7C20634; _gcl_au=1.1.64202074.1780561528; _scid=1a0c9lOFa-wlL0rgxI1JWLey2Hzxf3KD; _tt_enable_cookie=1; _ttp=01KT8VSH83MVZRYRXPFDBE7RV3_.tt.1; ttcsid_D4JHTCBC77U4IAHDM2D0=1782800999956::42n9uRlwYXH5D7uAfsux.19.1782802039702.1; ttcsid=1782800999957::Sfl3c7sS7awNUb4rWhyQ.9.1782802039701.0::1.279534.286634::1039732.3.699.1634::1039176.9.1019; _twpid=tw.1780561528642.492529127406203722; fs_fliu=true; AMCVS_2F2827E253DAF0E10A490D4E%40AdobeOrg=1; s_cc=true; s_sq=fifaprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dplay%25253Aworldcup%25253Acanadamexicousa2026%25253Agames%25253Afantasy-classic%25253Aleague%25253Atable%2526link%253DLOAD%252520MORE%2526region%253Droot%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dplay%25253Aworldcup%25253Acanadamexicousa2026%25253Agames%25253Afantasy-classic%25253Aleague%25253Atable%2526pidt%253D1%2526oid%253Dfunctionta%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT; __gads=ID=97a28d4d09dfae31:T=1782190659:RT=1782294143:S=ALNI_MaybncLib3gJqwI7QQJVMVjR0n3-w; __gpi=UID=0000147efa183029:T=1782190659:RT=1782294143:S=ALNI_MaWUTJ4EhtaaW-UQWN-j_nWHr7Xmw; __eoi=ID=3daf211b2218367b:T=1782190659:RT=1782294143:S=AA-AfjagYb2VnOs6Vr_6A_vFJzLz; X-SID=86062d6038f76d12c3297ef3_1782709955; bm_sz=19EA68BCD76F92D79D71A8F0E3673D3C~YAAQnP3UF4CpIRafAQAAgJFIFwDeiyi/FH2RUYrBRWZylZzUPNT/6r4Yo1r6sLC4fAlieaRSW4rqSxK0/LqxnDxM2PC2loAw/N1qQUggAKJA3flNeEEXgHDVY5BIIYd+11vj3w4PLPadhN8eddWyD0LuUrbFsHq64eLSmKzEjb+PEBsvQX6W4LumkvmwhmmZlxkboj35RujYwocRat6dCLtyASkXyTTJ0pOOvLSSkbnU1KHMmQo59jO2+bClPrj6NWeojvtJOyuubf97YaaMy1PfZZ8pNE9q+jrERmRFkYNlIaLgxpoUtz8c46SGUg/Zp0ybbVGlZIyMA0shstxJ68mi9d4GkmDP1//dZPUxRzycSac00WQJxBmxcMJ+Fdb6gCQkUohYaaGNv2pJOtNtB3YJby4sHguKZRw/aTqhT4MN6w2mtiZ1ApHzEMmObCLJ9f4oTD5Jx2ke5QCpHkOzNtSU610MSrFF28evJVYERE5BXBVSnRZTLQpTW1B0ydaa63oATXExKzpy+jffPVj444/GVmBy2pZ+Q8Y=~3356469~3293745; ak_bmsc=270774112F0FF728CEF159A54F011EE5~000000000000000000000000000000~YAAQv/3UFzoWBBafAQAAYB0jFwAVgn6mzftqwSqjrafRL5bZoh8kNgvZcC+ie7Bd1fYpYypqW8+AZrQdTNme4umzRembm0/d1k4FIQuZAz9KYB44vNYgPIhVMlpwFN1t1LdWynfL9Sbw5Y4H8XBr7tuhS2V/3Q6KVVhcCPZI3cU7JVr+QuKQmWa1X9aPtD/aFOKQSjInIYhnZEIidbm3WwNqjlg/EZXGV7gUPWkl9LXS4B7XbcyVCWnmu5Ie0R8aFxm8rsUvvNWwMT5OrEdgOBmBnGI8ZdMhi4Kkvs2l7BQA7GioIhftVFymErsuvtGYhBpu4EYlJtaoV4tvsecKBqc66IhPJVhm2u+2zQvC1JCzke01vzFyYXQ+rY/HP/VFgv47wVAXOCTGmQ==; bm_sv=3D162049DF1FE3689D7FA33723B45DA1~YAAQnP3UF8ipIRafAQAAPJ9IFwBYGzMiJPpiyoOqkvD1YcB5ZVy1oY+oEg3YfUiJHsP+bmkRjWDnjj927nTuO90RoliXsNFHRz6SflBcVXXbUFeldqbIMRYe2/mBWEx4XqLFOFzNYW9qvay/rPaE/mevCyQk2ZCp+zuAyYY0+75iNtHQJJbQjf2qyNFNbTVPRaC+7pujIRQyELUljTYUQP0radVoHqrYri1p9VFXqgIxyXVpAAFMhGuvRTSX1iU=~1; adobeSessionCookie=82eg74ejf26dafckf0kh1782800997310; _scid_r=7S0c9lOFa-wlL0rgxI1JWLey2Hzxf3KDj3VWtA",
    "User-Agent": "Mozilla/5.0",
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

    for rnd in range(1, num_rounds + 1):
        people = get_people(rnd, managers)

        for manager, stats in people.items():
            entry = progression[manager]
            entry["rounds"].append(rnd)
            entry["ranks"].append(stats["rank"])
            entry["points"].append(stats["overall_points"])

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
