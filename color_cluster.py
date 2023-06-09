from PIL import Image
import imagehash
import json

hashfn = lambda img: imagehash.colorhash(img, binbits=3)
hashReader = lambda hash_as_str: imagehash.hex_to_flathash(hash_as_str, hashsize=3)

std_cols = [
    "violet",
    "indigo",
    "blue",
    "green",
    "yellow",
    "orange",
    "red",
    "white",
    "black",
    "cyan",
    "magenta",
    "pink",
    "purple",
    "brown",
    "burlywood",
    "yellowgreen",
    "khaki",
]


def gen_std_hashes():
    hashes = {}
    for c in std_cols:
        img = Image.new("RGB", (300, 300), color=c)
        hashes[c] = hashfn(img)

    return hashes


def load_data():
    with open("lam.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open("lam.json", "w") as f:
        json.dump(data, f)


def get_nearest_hash_col(item, std_hashes):
    item_hash = hashReader(item["img_hash"])
    nearest = min(std_hashes.items(), key=lambda it: it[1] - item_hash)
    return nearest[0]


def assing_std_col(data, std_hashes):
    for item in data:
        if "img_hash" in item:
            item["hash_color"] = get_nearest_hash_col(item, std_hashes)


def main():
    std_hashes = gen_std_hashes()
    data = load_data()
    assing_std_col(data, std_hashes)
    save_data(data)


if __name__ == "__main__":
    main()
