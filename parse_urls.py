import json
from urllib.parse import urlparse
import re


PAT = re.compile(r"""[\/:"'*?<>|~\s$#%^&+=@!;:,^]+""")


def parse(url):
    r = urlparse(url)
    parts = r.path.split("/")
    fname = PAT.sub("__", r.path)
    return fname


with open("lam.json", "r") as f:
    data = json.load(f)
    for i, item in enumerate(data):
        url = item["offerImageUrl_1"].strip().split("?")[0]
        file = parse(url)
        item["url"] = url
        item["file"] = file
        item["i"] = i
        item.pop("offerImageUrl_1")

with open("lam.json", "w") as f:
    json.dump(data, f)
