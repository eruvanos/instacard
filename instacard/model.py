from collections import namedtuple
from dataclasses import dataclass

Userinfo = namedtuple('Userinfo', [
    'user_id',
    'username',
    'fullname',
    'image',
])
Address = namedtuple('Address', [
    'name',
    'streetno',
    'city',
    'state',
    'zip',
    'country'
])

@dataclass
class Postinfo:
    media_id: str
    code: str
    taken_at: str
    image: str
    caption: str
    location: str
    carousel_index: int = 0
