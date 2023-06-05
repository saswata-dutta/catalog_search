import json
from urllib.parse import urlparse
import hashlib


def parse(url):
    urlPath = urlparse(url).path
    ext = urlPath.split(".")[-1]
    fhash = hashlib.md5(urlPath.encode("ascii")).hexdigest()
    fname = f"{fhash}.{ext}"
    return (urlPath, fname)


with open("lam.json", "r") as f:
    data = json.load(f)
    for i, item in enumerate(data):
        url = item["url"]
        urlPath, fname = parse(url)
        item["url_path"] = urlPath
        item["file"] = fname
        item["i"] = i


with open("lam.json", "w") as f:
    json.dump(data, f)
