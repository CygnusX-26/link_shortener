from models import Link
from string import ascii_letters
from random import randint
from requests import get, exceptions
from typing import Any
from bcrypt import checkpw



def gen_path() -> str:
    paths = Link.query.all()
    path = __gen_chars()
    while path in paths or path == "all":
        path = __gen_chars()
    return path

def __gen_chars() -> str:
    r = ""
    values = ascii_letters + "0123456789_"
    for _ in range(3):
        r += values[randint(0, len(values) - 1)]
    return r

def test_valid(url: str) -> bool:
    try:
        return get(url, allow_redirects=True).status_code != 404
    except exceptions.ConnectionError:
        return False
    
def statusify(data: Any, success: bool) -> dict:
    return {"success": success, "data": data}

def check_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password.encode(), hashed_password)
        