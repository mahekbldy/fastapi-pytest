from typing import List
from app.schemas import User
import json
import os

# Get the path to the JSON data
DATA_FILE = os.path.join(os.path.dirname(__file__), "user_data.json")


def load_users() -> List[User]:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return [User(**user) for user in data]
