import json
from pathlib import Path
import requests

with open("tools/token.json") as f:
    token = json.load(f)["token"]

vids = ["OUkuc46XzU0", "gX4nCYgFc-w", "YwbmLbJzJiY", "yEBLoLZJZAE", "ejo6urjRllM", 
        "oUWk27df3OU", "8sH1a1HbB4E", "DHk8MYo038I", "1Q91IwPWl0U", "-HNjsNSx4tg", "hMz3okrct30"]

headers = {"Authorization": f"Bearer {token}"}
v_str = ",".join(vids)
resp = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={v_str}&part=snippet", headers=headers)
items = resp.json().get("items", [])
for item in items:
    vid = item["id"]
    title = item["snippet"]["title"][:30]
    thumbs = item["snippet"].get("thumbnails", {})
    maxres = thumbs.get("maxres") or thumbs.get("standard") or thumbs.get("high") or thumbs.get("default")
    thumb_url = maxres.get("url") if maxres else "None"
    print(f"{vid}: {title}... -> thumb: {thumb_url}")
