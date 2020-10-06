import pyrebase
# import uuid
import os
import json
import requests
from requests.exceptions import HTTPError

try:
    from urllib.parse import urlencode, quote
except Exceptions as e:
    from urllib import quote#, urlencode

progress = {
    "stories": {
        "story_id": 1,
        "stages": {
            "image_url": "www.bestdog.com",
            "stage_id": 1.1,
            "completed": False
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
            "serviceAccount": './key.json'
        }
        app = pyrebase.initialize_app(config)
        self.db = app.database()
        self.storage = app.storage()
        self.auth = app.auth()

    def upload_file(self, filepath, upload_to):
        filename = os.path.basename(filepath)
        self.storage.child(upload_to + filename).put(filepath)
        print(upload_to + filename)
        return self.storage.child(upload_to + filename).get_url(None)

    def get_url(self, filepath):
        return self.storage.child(filepath).get_url(None)

    def create_new_user(self, email, password, username):
        # user = {"username": username, "email": email, "password": password}
        story = {"username": username, "story": []}
        # self.db.child('Users').push(user)
        self.db.child('progress').push(story)
        try:
            self.auth.create_user_with_email_and_password(email, password)
            idToken = self.sign_in_with_email_and_password(email, password)[
                'idToken']
            self.set_display_name(username, idToken)
            return "User created.", 200
        except Exception as e:
            return "The email is already in use", 400

    def set_display_name(self, displayName, idToken):
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={0}".format(
            self.auth.api_key)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"idToken": idToken, "displayName": displayName})
        try:
            request_object = requests.post(
                request_ref, headers=headers, data=data)
            return request_object.json()
        except Exception as e:
            try:
                request_object.raise_for_status()
            except HTTPError as e:
                raise HTTPError(e, request_object.text)

    def sign_in_with_email_and_password(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)

    def send_password_reset_email(self, email):
        return self.auth.send_password_reset_email(email)

    def get_account_info(self, idToken):
        return self.auth.get_account_info(idToken)

    # def get_user(self, username):
    #     data = self.db.child('Users').order_by_child(
    #         "username").equal_to(username).get()
    #     try:
    #         for v in data.val().values():
    #             return v
    #     except:
    #         return None

    def get_story_progress(self, username, storyid):
        progress = self.db.child('progress').order_by_child(
            'username').equal_to(username).get()
        try:
            for v in progress.val().values():
                print(v['stories'][storyid])
                return v['stories'][storyid]
        except Exception as e:
            return None

    def update_story_progress(self, username, storyid, stageid, url, completed):
        try:
            progress = self.db.child('progress').order_by_child(
                'username').equal_to(username).get().val()
            for v in progress.values():
                print(v)
                for stage in v['stories'][storyid]["stages"]:
                    if stage['stage_id'] == stageid:
                        stage['image_url'] == url
                        stage['completed'] = True
                        self.db.child('progress').update(progress)
                        return "Updated stage " + stageid, 200
                # did not find existing stage, add as new save
                new_stage = {
                    "image_url": url,
                    "stage_id": stageid,
                    "completed": completed
                }
                v['stories'][storyid]["stages"].append(new_stage)

            self.db.child('progress').update(progress)
            return "Added new stage " + stageid + " to story " + storyid, 200

        except KeyError:
            print("No value found")
            return "User does not exist", 400
        except Exception as e:
            return "Something went wrong", 400

    def start_new_story(self, username, storyid):
        # Start story
        new_stage = {
            "stages": [
                    {
                        "image_url": "",
                        "stage_id": 1,
                        "completed": False
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

    def create_content(self, content):
        self.db.child('content').push(content)

    def get_content(self, storyid):
        log = self.db.child('content').order_by_child(
            "id").equal_to(storyid).get()
        try:
            for v in log.val().values():
                return v
        except Exception as e:
            return None

    def get_all_content(self):
        result = []
        log = self.db.child('content').get()
        try:
            for v in log.val().values():
                story = {
                    "cover_image": v["cover_image"],
                    "story_title": v["story_title"],
                    "id": v["id"]
                }
                result.append(story)
            return result
        except Exception as e:
            return []


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
