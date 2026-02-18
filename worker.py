import requests
import time
import os

CENTRAL = "http://75.135.168.98:25565/api/submit"

REGION = os.getenv("REGION")
STAT   = os.getenv("STAT")

MAX_PAGES = 700

for page in range(1, MAX_PAGES+1):
    url = f"https://gtacnr.net/api/leaderboards/{REGION}/{STAT}/{page}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()["records"]

        payload = []
        for p in data:
            payload.append({
                "player_id": p["accountId"],
                "player_name": p["accountName"],
                "region": REGION,
                "stat_name": STAT,
                "value": p["value"]
            })

        if payload:
            requests.post(CENTRAL, json=payload)

        print(f"{REGION} {STAT} page {page}")
        time.sleep(3)

    except Exception as e:
        print("error", e)
        time.sleep(5)
