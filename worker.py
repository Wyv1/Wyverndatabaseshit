import os
import time
import requests
import logging

# Setup logging to stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(handler)

REGION = os.getenv("REGION", "UNKNOWN")
STAT = os.getenv("STAT", "UNKNOWN")
CENTRAL = "http://75.135.168.98:25565/api/submit"
API_KEY = "c2VjdXJlX3JlYWxseV9sb25nX2Jhc2U2NF9rZXlfZm9yX2FwaV9pbg=="
MAX_PAGES = 700

logger.info(f"Worker started for REGION={REGION}, STAT={STAT}")

for page in range(1, MAX_PAGES + 1):
    logger.info(f"Scraping page {page}")
    try:
        r = requests.get(f"https://gtacnr.net/api/leaderboards/{REGION}/{STAT}/{page}", timeout=10)
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
            resp = requests.post(CENTRAL, json=payload, headers={"X-KEY": API_KEY}, timeout=30)
            logger.info(f"Page {page}: sent {len(payload)} players, status={resp.status_code}")

        else:
            logger.info(f"Page {page}: no data to send")

        time.sleep(3)

    except Exception as e:
        logger.error(f"Error on page {page}: {e}")
        time.sleep(5)
