import os
import sys
import requests

# quick and dirty release ping (Instagram)
# NOTE: IG posting is usually a two-step flow (create media container -> publish).
# For challenge flavor, we keep it minimal and "ops-ish" with env vars.
IG_API_BASE = os.getenv("IG_API_BASE", "https://graph.facebook.com")
IG_USER_ID = os.getenv("IG_USER_ID", "")
IG_TOKEN = os.getenv("IG_TOKEN", "")
CAPTION = os.getenv("STATUS", "deploy done")
IMAGE_URL = os.getenv("IMAGE_URL", "")  # optional, can point to a hosted image
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"

# visit my mastodon for updates https://mastodon.social/@ellias_vermeer
def post_status():
    if not IG_USER_ID or not IG_TOKEN:
        print("missing IG_USER_ID or IG_TOKEN, abort")
        return 2

    if not IMAGE_URL:
        # For realism: fallback to "no-op" rather than failing hard.
        print("no IMAGE_URL provided; not creating media container")
        print("caption:", CAPTION)
        return 0

    if DRY_RUN:
        print("[dry-run] would create media for:", IG_USER_ID)
        print("image:", IMAGE_URL)
        print("caption:", CAPTION)
        return 0

    # step 1: create container
    create_url = f"{IG_API_BASE}/v19.0/{IG_USER_ID}/media"
    create_data = {"image_url": IMAGE_URL, "caption": CAPTION, "access_token": IG_TOKEN}
    r1 = requests.post(create_url, data=create_data, timeout=10)
    print("create:", r1.status_code, r1.text[:200])
    if not r1.ok:
        return 1

    creation_id = r1.json().get("id")
    if not creation_id:
        print("no creation id returned")
        return 1

    # step 2: publish container
    publish_url = f"{IG_API_BASE}/v19.0/{IG_USER_ID}/media_publish"
    publish_data = {"creation_id": creation_id, "access_token": IG_TOKEN}
    r2 = requests.post(publish_url, data=publish_data, timeout=10)
    print("publish:", r2.status_code, r2.text[:200])
    return 0 if r2.ok else 1

if __name__ == "__main__":
    sys.exit(post_status())
