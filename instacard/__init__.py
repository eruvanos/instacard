import logging

from flask import Flask, render_template, redirect, url_for

import settings
from instacard import lobadapter
from instacard.instagramadapter import InstagramAdapter
from instacard.repo import TinyRepo

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    insta = InstagramAdapter(settings.USERNAME, settings.PASSWORD)
    repo = TinyRepo(settings.DB_URL)
    lobadapter.init(settings.LOB_API_KEY)

    @app.route('/')
    def index():
        usernames = repo.usernames()
        return render_template('index.html', usernames=usernames)

    @app.route('/<username>')
    def posts(username):
        userinfo = insta.get_user_info(username)
        posts = []

        for p in insta.feed(userinfo.user_id):
            if not repo.check_done(username, p.media_id):
                posts.append(p)
        return render_template('posts.html', userinfo=userinfo, posts=posts)

    @app.route('/<username>/<media_id>/skip')
    def skip(username, media_id):
        if not repo.check_done(username, media_id):
            logger.info(f'skip {username}, {media_id}')
            repo.processed(username, media_id, True)
        else:
            logger.warning(f'already processed {username}, {media_id}')
        return redirect(url_for('posts', username=username))

    @app.route('/<username>/<media_id>/send_postcard')
    def send_postcard(username, media_id):
        if not repo.check_done(username, media_id):
            userinfo = insta.get_user_info(username)
            postinfo = insta.post(media_id)
            lobadapter.send_postcard(userinfo, postinfo, settings.default_address)
            logger.info(f'send_postcard {username}, {media_id}')
            repo.processed(username, postinfo.media_id, False)
        else:
            logger.warning(f'already processed {username}, {media_id}')
        return redirect(url_for('posts', username=username))

    return app
