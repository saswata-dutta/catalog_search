import json
from pathlib import Path

from PIL import Image
from annoy import AnnoyIndex
import imagehash


def remove_alpha(img):
    if img.mode != "RGBA":
        return img
    canvas = Image.new("RGBA", img.size, (255, 255, 255, 255))
    canvas.paste(img, mask=img)
    return canvas.convert("RGB")


def load_img(img_path):
    return remove_alpha(Image.open(img_path))


def get_hash(img_path, hashfn):
    img = load_img(img_path)
    return hashfn(img).hash.astype("int").flatten()


def load_img_index():
    vector_length = 42
    img_index = AnnoyIndex(vector_length, "hamming")

    num_trees = 200
    fname = f"lam_{num_trees}.ann"
    img_index.load(fname)

    return img_index


def load_data():
    count = 22013
    with open("lam.json", "r") as f:
        data = json.load(f)
    return (count, data)


def knn(img_index, query_vec, n, search_k, threshold):
    locs, dists = img_index.get_nns_by_vector(
        query_vec, n, search_k, include_distances=True
    )
    matches = [(i, d) for i, d in zip(locs, dists) if d < threshold]
    matches.sort(key=lambda it: it[1])
    return [i for i, _ in matches]


def main():
    count, data = load_data()
    img_index = load_img_index()

    query_dir = Path.cwd().joinpath("query")
    hashfn = lambda img: imagehash.colorhash(img, binbits=3)
    search_k = -1
    threshold = 13

    def search(query_fname, n):
        query_path = query_dir.joinpath(query_fname)
        query_ok = query_path.exists() and query_path.is_file()
        if not query_ok:
            print(f"missing file {query_path}")
            return []
        query_vec = get_hash(query_path, hashfn)
        matches = knn(img_index, query_vec, n, search_k, threshold)
        return [data[i]["url"] for i in matches]

    return search


if __name__ == "__main__":
    search = main()
