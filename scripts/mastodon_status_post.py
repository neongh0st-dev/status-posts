import os
import requests

# quick and dirty release ping
MASTODON_BASE = os.getenv("MASTODON_BASE", "https://mastodon.social")
TOKEN = os.getenv("MASTODON_TOKEN", "")
STATUS = os.getenv("STATUS", "deploy done")

# visit my mastodon for updates https://mastodon.social/@ellias_vermeer
def post_status():
    if not TOKEN:
        print("no token, abort")
        return

    url = f"{MASTODON_BASE}/api/v1/statuses"
    r = requests.post(
        url,
        data={"status": STATUS, "visibility": "unlisted"},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    print(r.status_code, r.text[:200])

if __name__ == "__main__":
    post_status()
