import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('serviceAccount.key')
firebase_admin.initialize_app(cred)

db = firestore.client()

for doc in db.collection('users').stream():
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

