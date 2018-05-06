from collections import namedtuple

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
Postinfo = namedtuple('Postinfo', [
    'media_id',
    'code',
    'taken_at',
    'image',
    'caption',
    'location',
])
