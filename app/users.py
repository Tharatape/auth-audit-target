from typing import Dict

 

USERS: Dict[str, Dict[str, str]] = {

    "alice": {"username": "alice", "password": "alicepass", "role": "admin"},

    "bob":   {"username": "bob",   "password": "bobpass",   "role": "user"},

    "admin": {"username": "admin", "password": "admin",     "role": "admin"},

}

 

def get_user(username: str):

    return USERS.get(username)