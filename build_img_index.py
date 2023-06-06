import json
from annoy import AnnoyIndex
import imagehash


hashReader = lambda hash_as_str: imagehash.hex_to_flathash(hash_as_str, hashsize=3)


def hash_as_array(hash_as_str):
    return hashReader(hash_as_str).hash.astype("int").flatten()


def prep_data():
    with open("lam.json", "r") as f:
        data = json.load(f)
    inf = len(data) * 2
    data.sort(key=lambda it: it["i"] if "img_hash" in it else inf)
    count = 0
    for i, it in enumerate(data):
        if "img_hash" in it:
            count += 1
        it["i"] = i

    with open("lam.json", "w") as f:
        json.dump(data, f)

    return (count, data)


def prep_image_index(vector_length, data, count):
    t = AnnoyIndex(vector_length, "hamming")
    for it in data[:count]:
        i = it["i"]
        v = hash_as_array(it["img_hash"])
        t.add_item(i, v)

    num_trees = 200
    t.build(num_trees)
    t.save(f"lam_{num_trees}.ann")


def main():
    # count, data = prep_data()
    count = 22013
    with open("lam.json", "r") as f:
        data = json.load(f)
    prep_image_index(42, data, count)


if __name__ == "__main__":
    main()
