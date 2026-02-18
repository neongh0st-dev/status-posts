import os
import sys
import json
import requests

# quick and dirty release ping (X)
# expects an app token (bearer) + plain text status
X_API_BASE = os.getenv("X_API_BASE", "https://api.x.com")
X_BEARER = os.getenv("X_BEARER", "")
STATUS = os.getenv("STATUS", "deploy done")
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"

def post_status():
    if not X_BEARER:
        print("no X_BEARER, abort")
        return 2

    payload = {"text": STATUS}

    if DRY_RUN:
        print("[dry-run] would POST:", json.dumps(payload))
        return 0

    url = f"{X_API_BASE}/2/tweets"
    r = requests.post(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {X_BEARER}",
            "Content-Type": "application/json",
        },
        timeout=10,
    )

    print(r.status_code, r.text[:300])
    return 0 if r.ok else 1

if __name__ == "__main__":
    sys.exit(post_status())
