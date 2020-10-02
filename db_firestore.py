
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

users = db.collection(u'progress')
for user in users.stream():
    print(user.id)
