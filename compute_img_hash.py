import json
from pathlib import Path

from PIL import Image
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
    return hashfn(img)


def hash_as_array(hash_as_str, hashReader):
    return hashReader(hash_as_str).hash.astype("int").flatten()


def main():
    with open("lam.json", "r") as f:
        data = json.load(f)

    hashfn = lambda img: imagehash.colorhash(img, binbits=3)
    hashReader = lambda hash_as_str: imagehash.hex_to_flathash(hash_as_str, hashsize=3)

    images_dir = Path.cwd().joinpath("images")
    for it in data:
        img_path = images_dir.joinpath(it["file"])
        img_ok = img_path.exists() and img_path.is_file()
        if not img_ok:
            it.pop("file")
            continue
        it["img_hash"] = str(get_hash(img_path, hashfn))

    with open("lam.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
