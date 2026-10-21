import json
import os


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        text = f.read()
    return json.loads(text) if text.strip() else {}


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
