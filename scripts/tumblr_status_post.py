import os
import sys
import requests

# quick and dirty release ping (Tumblr)
# uses OAuth token + blog identifier, posts a short text update
TUMBLR_API_BASE = os.getenv("TUMBLR_API_BASE", "https://api.tumblr.com")
TUMBLR_OAUTH = os.getenv("TUMBLR_OAUTH", "")
TUMBLR_BLOG_ID = os.getenv("TUMBLR_BLOG_ID", "")  # e.g. "myblog.tumblr.com"
STATUS = os.getenv("STATUS", "deploy done")
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"

def post_status():
    if not TUMBLR_OAUTH or not TUMBLR_BLOG_ID:
        print("missing TUMBLR_OAUTH or TUMBLR_BLOG_ID, abort")
        return 2

    if DRY_RUN:
        print("[dry-run] would post text to blog:", TUMBLR_BLOG_ID)
        print(STATUS)
        return 0

    url = f"{TUMBLR_API_BASE}/v2/blog/{TUMBLR_BLOG_ID}/post"
    data = {
        "type": "text",
        "state": "published",
        "title": "ops ping",
        "body": STATUS,
    }

    r = requests.post(
        url,
        data=data,
        headers={"Authorization": f"Bearer {TUMBLR_OAUTH}"},
        timeout=10,
    )

    print(r.status_code, r.text[:300])
    return 0 if r.ok else 1

if __name__ == "__main__":
    sys.exit(post_status())
