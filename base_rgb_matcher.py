from colorthief import ColorThief
from pathlib import Path
import json

std_colors = {
    "violet": "#ee82ee",
    "indigo": "#4b0082",
    "blue": "#0000ff",
    "green": "#008000",
    "yellow": "#ffff00",
    "orange": "#ffa500",
    "red": "#ff0000",
    "white": "#ffffff",
    "black": "#000000",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "pink": "#ffc0cb",
    "purple": "#800080",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "yellowgreen": "#9ACD32",
    "khaki": "#f0e68c",
}


def hex_to_rgb(h):
    return tuple(int(h[i : i + 2], 16) for i in (1, 3, 5))


def get_std_rgb():
    std_rgb = {}
    for k, v in std_colors.items():
        std_rgb[k] = hex_to_rgb(v)
    return std_rgb


def dominant_rgb(img_path):
    return ColorThief(img_path).get_color(25)


def image_paths():
    images_dir = Path("./images")
    image_ext = ".jpeg .jpg .png".split()
    return [p for p in images_dir.iterdir() if p.is_file() and p.suffix in image_ext]


def rgb_dist(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    mr = (r1 + r2) / 2
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2

    return (2 + mr / 256) * dr * dr + 4 * dg * dg + (2 + (255 - mr) / 256) * db * db


def get_nearest_std_col(rgb, std_rgb):
    return min(std_rgb.items(), key=lambda it: rgb_dist(it[1], rgb))


def save(data):
    with open("base_col_mapping.json", "w") as f:
        json.dump(data, f)


def process():
    std_rgb = get_std_rgb()
    images = image_paths()
    base_col = {}
    for i, img in enumerate(images):
        try:
            if not img.exists():
                continue
            rgb = dominant_rgb(img.absolute())
            nearest = get_nearest_std_col(rgb, std_rgb)
            k = img.stem
            v = nearest[0]
            base_col[k] = v
            if i % 200 == 0:
                print(f"{i}/{len(images)}")
        except:
            print(img)
    save(base_col)


if __name__ == "__main__":
    process()
