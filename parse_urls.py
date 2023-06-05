import json
from urllib.parse import urlparse


def parse(url):
    r = urlparse(url)
    parts = r.path.split("/")
    fname = parts[2]
    ext = parts[-1].split(".")[-1]
    return f"{fname}.{ext}"


file_names = {}
with open("lam.json", "r") as f:
    data = json.load(f)
    for item in data:
        url = item["offerImageUrl_1"].strip().split("?")[0]
        file = parse(url)
        item["file"] = file

with open("lam.json", "w") as f:
    json.dump(data, f)
