import pyrebase
from temp import stories
import uuid
import os

try:
    from urllib.parse import urlencode, quote
except:
    from urllib import urlencode, quote

progress = {
    "stories": {
        "story_id": 1,
        "stages": {
            "image_url": "www.bestdog.com",
            "stage_id": 1.1,
            "status": "incomplete"
        }
    }
}

progress = {
    "stories": {
        "1": {
            "asd": 1
        },
        "2": {
            "asd": 2
        }
    }
}


class FirebaseHelper:

    def __init__(self):
        config = {
            "apiKey": "AIzaSyDOXwnuSlP36o_tB3xiYELds0XOohJaxA4",
            "authDomain": "doodleup-f1847.firebaseapp.com",
            "databaseURL": "https://doodleup-f1847.firebaseio.com/",
            "storageBucket": "doodleup-f1847.appspot.com",
            "serviceAccount": './doodleup-f1847-firebase-adminsdk-x4yoc-66b445712b.json'
        }
        app = pyrebase.initialize_app(config)
        self.db = app.database()
        self.storage = app.storage()
        self.auth = app.auth()

    def upload_file(self, filepath, upload_to):
        filename = os.path.basename(filepath)
        self.storage.child(upload_to+filename).put(filepath)
        print(upload_to+filename)
        return self.storage.child(upload_to+filename).get_url(None)

    def get_file(self, filepath):
        return

    def get_all_users(self):
        return self.db.child('Users').get()

    def create_new_user(self, username, email, password):
        user = {"username": username, "email": email, "password": password}
        story = {"username": username, "story": []}
        self.auth.create_user_with_email_and_password(email, password)
        self.db.child('Users').push(user)
        self.db.child('progress').push(story)

    def sign_in_with_email_and_password(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)

    def send_password_reset_email(self, email):
        return self.auth.send_password_reset_email(email)

    def get_account_info(self, idToken):
        return self.auth.get_account_info(idToken)

    def get_user(self, username):
        data = self.db.child('Users').order_by_child(
            "username").equal_to(username).get()
        try:
            for v in data.val().values():
                return v
        except:
            return None

    def get_story_progress(self, username, storyid):
        progress = self.db.child('progress').order_by_child(
            'username').equal_to(username).get()
        try:
            for v in progress.val().values():
                print(v['stories'][storyid])
                return v['stories'][storyid]
        except:
            return None

    def update_story_progress(self, username, storyid, content):
        try:
            progress = self.db.child('progress').order_by_child(
                'username').equal_to(username).get().val()
        except:
            print("No value found")
            return None
        for v in progress.values():
            for stage in v['stories'][storyid]["stages"]:
                if stage["stage_id"] == content["stage_id"]:
                    stage["image_url"] = content["image_url"]
                    stage["status"] = content["status"]
                    self.db.child('progress').update(progress)
        # did not find existing stage, create new stage instead
        self.start_new_stage(username, storyid, content["stage_id"])

    def start_new_story(self, username, storyid):
        # Start story
        new_stage = {
            "stages": [
                    {
                        "image_url": "",
                        "stage_id": 1.1,
                        "status": "incomplete"
                    }]
        }
        log = self.db.child('progress').order_by_child(
            'username').equal_to(username).get().val()
        for k, v in log.items():
            if "stories" not in v:
                v["stories"] = {storyid: new_stage}
            else:
                stories = v["stories"]
                stories[storyid] = new_stage
        self.db.child('progress').update(log)
        return v["stories"][storyid]

    def start_new_stage(self, username, storyid, stageid):
        new_stage = {
            "image_url": "",
            "stage_id": stageid,
            "status": "incomplete"
        }
        try:
            progress = self.db.child('progress').order_by_child(
                'username').equal_to(username).get().val()
        except:
            return None
        for v in progress.values():
            stages = v['stories'][storyid]["stages"]
            stages.append(new_stage)
            self.db.child('progress').update(progress)

    def create_content(self, content):
        storyid = content['id']
        self.db.child('content').push(content)

    def get_content(self, storyid):
        log = self.db.child('content').order_by_child(
            "id").equal_to(storyid).get()
        try:
            for v in log.val().values():
                return v
        except:
            return None

# print(fb.get_user_progress(1).val())
# print(users.val())

# pyrebase has some compatability issues with url, this is a workaround


pyrebase.pyrebase.quote = lambda s, safe=None: s

# Monkey patch pyrebase: replace quote function in pyrebase to workaround a bug.
# See https://github.com/thisbejim/Pyrebase/issues/294.

# Monkey patch pyrebase: the Storage.get_url method does need quoting :|


def get_url(self, token=None):
    path = self.path
    self.path = None
    if path.startswith('/'):
        path = path[1:]
    if token:
        return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), token)
    return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))


pyrebase.pyrebase.Storage.get_url = lambda self, token=None: \
    get_url(self, token)
