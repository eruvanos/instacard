import logging
from itertools import chain
from typing import List, Dict

import arrow
from InstagramAPI import InstagramAPI

from instacard.model import Postinfo, Userinfo

logger = logging.getLogger(__name__)


class InstagramAdapter:
    def __init__(self, username, password):
        self.api = InstagramAPI(username, password)
        self.api.login()

    def fixed_mediaInfo(self, api, mediaId):
        import json
        data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token,
                           'media_id': mediaId})
        return api.SendRequest('media/' + str(mediaId) + '/info/', login=api.generateSignature(data))

    @staticmethod
    def extract_postinfo(item: Dict) -> List[Postinfo]:
        posts = []
        if 'image_versions2' in item:
            posts.append(Postinfo(
                media_id=item['pk'],
                code=item['code'],
                taken_at=arrow.get(item['taken_at']),
                image=item['image_versions2']['candidates'][0]['url'],
                caption='',
                location=item.get('location'),
            ))

        # elif 'carousel_media' in item:
        #     for media in item['carousel_media']:
        #         posts.append(Postinfo(
        #             media_id=item['pk'],
        #             code=item['code'],
        #             taken_at=arrow.get(item['taken_at']),
        #             image=media['image_versions2']['candidates'][0]['url'],
        #             caption='',
        #             location=item.get('location'),
        #         ))
        return posts

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
        if self.fixed_mediaInfo(self.api, media_id):
            return self.extract_postinfo(self.api.LastJson['items'][0])[0]
        else:
            return None

    def feed(self, user_id: str) -> List[Postinfo]:
        if self.api.getUserFeed(user_id):
            posts = self.api.LastJson['items']
            return list(chain(*map(self.extract_postinfo, posts)))
        else:
            return []
