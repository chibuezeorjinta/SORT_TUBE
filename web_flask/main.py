from models.user import User
from models.storage import storage

import json
import os

file_path = "client_secret_1088266269277-0nijetd5bla0ukdhehem63jcjs1djjfq.apps.googleusercontent.com.json"
pwd = os.getcwd()
new_fp = os.path.join(pwd, file_path)

try:
    print(os.path.exists(new_fp))
    with open(file_path) as f:
        file: dict = json.load(f)
        client_id: str = file.get('client_id')
        redirect_uri: str = file.get('redirect_uri')
        print(redirect_uri)

except FileExistsError as e:
    print(e)

scopes = ['https://www.googleapis.com/auth/youtube.readonly']

mytry = User("danielorjinta", new_fp, scopes)
mytry.set_storage(storage)
storage = storage.set_userclass(mytry)


mytry.authenticate()
User.credentials()
mytry.login()
mytry.get_subscriptions()
# #
# kunle = User('Engr_kunle', new_fp, scopes)
# kunle.authenticate()
# kunle.login()
# kunle.get_subscriptions()
#Boss = User('Boss', new_fp, scopes)

# new = User("kunle", new_fp, scopes)
#
# new.authenticate()
# new.login()
# new.get_subscriptions()