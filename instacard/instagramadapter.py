import logging
from typing import List, Dict

import arrow
from InstagramAPI import InstagramAPI

from instacard.model import Postinfo, Userinfo

logger = logging.getLogger(__name__)


class InstagramAdapter:
    def __init__(self, username, password):
        self.api = InstagramAPI(username, password)
        self.api.login()

    @staticmethod
    def extract_postinfo(item: Dict) -> Postinfo:
        return Postinfo(
            media_id=item['pk'],
            code=item['code'],
            taken_at=arrow.get(item['taken_at']),
            image=item['image_versions2']['candidates'][0]['url'],
            caption='',
            location=item.get('location'),
        )

    def get_user_info(self, username: str) -> Userinfo:
        if not self.api.searchUsername(username):
            logger.warning('Could not find user %s.' % username)
            return None
        user_id = self.api.LastJson['user']['pk']
        fullname = self.api.LastJson['user']['full_name']
        pic = self.api.LastJson['user']['hd_profile_pic_url_info']['url']
        return Userinfo(
            user_id=user_id,
            username=username,
            fullname=fullname,
            image=pic
        )

    def post(self, media_id):
        if self.api.mediaInfo(media_id):
            return self.extract_postinfo(self.api.LastJson['items'][0])
        else:
            return None

    def feed(self, user_id: str) -> List[Postinfo]:
        if self.api.getUserFeed(user_id):
            posts = self.api.LastJson['items']
            return list(map(self.extract_postinfo, posts))
        else:
            return []
