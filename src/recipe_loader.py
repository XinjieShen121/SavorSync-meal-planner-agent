import json
from typing import List, Dict, Any


def load_recipes(path: str) -> List[Dict[str, Any]]:
    # open the JSON recipe file
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f) # load the JSON data and convert it into Python objects