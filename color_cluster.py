# note didnt work too well as light and dark colors are clubbed in hash quant

from PIL import Image
import imagehash
import json

hashfn = lambda img: imagehash.colorhash(img, binbits=3)
hashReader = lambda hash_as_str: imagehash.hex_to_flathash(hash_as_str, hashsize=3)

std_cols = [
    "aliceblue",
    "antiquewhite",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgreen",
    "darkgrey",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "green",
    "greenyellow",
    "grey",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgreen",
    "lightgrey",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "purple",
    "rebeccapurple",
    "red",
    "rosybrown",
    "royalblue",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "silver",
    "skyblue",
    "slateblue",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "whitesmoke",
    "yellow",
    "yellowgreen",
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


def get_nearest_col(item, std_hashes):
    item_hash = hashReader(item["img_hash"])
    nearest = min(std_hashes.items(), key=lambda it: it[1] - item_hash)
    print(str(item_hash), nearest[0], str(nearest[1]), nearest[1] - item_hash)
    print(item["url"])

    return nearest[0]


def assing_std_col(data, std_hashes):
    for item in data:
        item["base_color"] = get_nearest_col(item, std_hashes)


def main():
    std_hashes = gen_std_hashes()
    data = load_data()
    assing_std_col(data[:20], std_hashes)
    # save_data(data)


if __name__ == "__main__":
    main()
