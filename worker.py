import requests
import time
import os

CENTRAL = "http://75.135.168.98:25565/api/submit"

REGION = os.getenv("REGION")
STAT   = os.getenv("STAT")

# This must match SECRET in app.py
API_KEY = "c2VjdXJlX3JlYWxseV9sb25nX2Jhc2U2NF9rZXlfZm9yX2FwaV9pbg=="

MAX_PAGES = 700

for page in range(1, MAX_PAGES+1):
    url = f"https://gtacnr.net/api/leaderboards/{REGION}/{STAT}/{page}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json().get("records", [])

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
            resp = requests.post(
                CENTRAL,
                json=payload,
                headers={"X-KEY": API_KEY},
                timeout=30
            )
            print(f"[SEND] Page {page} -> {resp.status_code} {resp.text}")

        else:
            print(f"[SKIP] Page {page} has no data")

        print(f"{REGION} {STAT} page {page} done")
        time.sleep(3)

    except Exception as e:
        print(f"[ERROR] Page {page}: {e}")
        time.sleep(5)
