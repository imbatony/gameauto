import collections
import os
from pathlib import Path


ASSET_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
IMAGE_DIR = Path(ASSET_DIR, "images")
MAP_IMAGE_DIR = Path(IMAGE_DIR, "maps")
ICON_IMAGE_DIR = Path(IMAGE_DIR, "icons")

ASSET = collections.namedtuple("ASSET", ["name", "type"])


def get_asset_path(asset: ASSET) -> str:
    if asset.type == "map":
        return str(Path(MAP_IMAGE_DIR, asset.name))
    elif asset.type == "icon":
        return str(Path(ICON_IMAGE_DIR, asset.name))

    return None


RELATIVE_POS = collections.namedtuple("RELATIVE_POS", ["x_ratio", "y_ratio"])
