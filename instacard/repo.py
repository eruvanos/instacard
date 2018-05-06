import arrow
from tinydb import TinyDB, Query


def _now():
    return arrow.utcnow().for_json()


class Post:
    def __init__(self, username, media_id, processed, skipped):
        self.username = username
        self.media_id = int(media_id)
        self.skipped = skipped
        self.processed = processed

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Post(
            d['username'],
            d['media_id'],
            d['skipped'],
            d['processed'],
        )


class TinyRepo:
    def __init__(self, db_url):
        self.table = TinyDB(db_url).table('posts')

    def posts(self, username):
        return self.table.search(Query().username == username)

    def processed(self, username, media_id, skipped):
        media_id = int(media_id)

        post = Post(
            username,
            media_id,
            skipped,
            _now()
        )
        self.table.insert(post.to_dict())

    def get_post(self, username, media_id):
        media_id = int(media_id)

        q = Query()
        entry = self.table.get((q.username == username) & (q.media_id == media_id))
        if entry:
            return Post.from_dict(entry)
        else:
            return None

    def usernames(self):
        posts = self.table.all()
        return set(map(lambda p: p['username'], posts))

    def check_done(self, username, media_id):
        media_id = int(media_id)

        q = Query()
        return self.table.contains((q.username == username) & (q.media_id == media_id))
