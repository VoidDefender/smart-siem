import json
import os

STATE_FILE = "state.json"

def get_last_position():
    if not os.path.exists(STATE_FILE):
        return 0

    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        return data.get("last_position", 0)

def update_position(position):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_position": position}, f)
