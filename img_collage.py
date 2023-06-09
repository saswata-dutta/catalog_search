import math
import json
import pathlib
from PIL import Image

img_dir = pathlib.Path("images")
out_dir = pathlib.Path("collage")
W = 20
color_field = "dom_color"  # "hash_color"


def get_data():
    with open("lam.json", "r") as f:
        data = json.load(f)
        return data


def get_color_groups(data):
    color_groups = {}  # color -> list(img file names)
    for it in data:
        if it.get(color_field) and it.get("file"):
            color_groups.setdefault(it.get(color_field), []).append(it.get("file"))
    return color_groups


def sample_img(path):
    img = Image.open(path)
    img.thumbnail((W, W))
    return img


def dump_img(color, smalls):
    n = math.ceil(math.sqrt(len(smalls)))
    new_im = Image.new("RGB", (n * W, n * W))

    i = 0
    j = 0
    for small in smalls:
        new_im.paste(small, (i, j))
        j += W
        if j > n * W:
            j = 0
            i += W

    new_im.save(out_dir.joinpath(f"{color}.png"))


def process(color_groups):
    for k, vals in color_groups.items():
        paths = [img_dir.joinpath(name) for name in vals]
        smalls = [sample_img(p) for p in paths if p.exists()]
        dump_img(k, smalls)


def main():
    data = get_data()
    color_groups = get_color_groups(data)
    process(color_groups)


if __name__ == "__main__":
    main()
