#!/usr/bin/python3
"""user class used to login and authenticate youtube account"""
# import requests
# from google.oauth2 import google_auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import os
import uuid
from models.bucket import Bucket


class User:
    __CREDENTIALS = {}

    def __init__(self, username, secret_path, scope, storage=None):
        """
        :type username: str
        :type secret_path: str
        :type scope: list
        """
        if secret_path is None:
            raise SyntaxError("USAGE=> username : str, secret_path : str, scope : []")
        if type(secret_path) is not str:
            raise TypeError("path is needed")
        else:
            self.client_secrets_path = secret_path
        if type(scope) is not list:
            raise TypeError("scope list is needed")
        if scope is None:
            raise SyntaxError("USAGE=> username : str, secret_path : str, scope : []")
        else:
            self.scopes = scope
        if type(username) is not str:
            raise TypeError("username string is needed")
        if username is None:
            raise SyntaxError("USAGE=> username : str, secret_path : str, scope : []")
        else:
            self.username = username
        self.id = str(uuid.uuid4())

        self.storage = storage

        self.UserId = self.username + '.' + self.id
        self.dump_file = "json/" + self.UserId + ".json"
        self.credentials: object = None
        self.youtube: build = None

        self.ID_LIST: list = []
        self.Buckets: object = None
        self.SubscriptionList: list = []

    def set_storage(self, storage):
        self.storage = storage
        User.__CREDENTIALS = self.storage.loadcred()
    def authenticate(self):
        if self.credentials is None:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_path, self.scopes)
            self.credentials = flow.run_local_server(port=5665, open_browser=False)
            self.ID_LIST = [self.id, self.credentials]
            if User.__CREDENTIALS is None:
                User.__CREDENTIALS = {}
            User.__CREDENTIALS[self.username] = self.ID_LIST
            print(User.__CREDENTIALS)
            self.storage.savecred()
        else:
            print(User.__CREDENTIALS)

    def login(self):
        if self.credentials is None:
            print("Authentication is required. Please authenticate first using the 'authenticate' method.")
            return

        self.youtube: build = build('youtube', 'v3', credentials=self.credentials)
        print("Logged in successfully.")

    def get_subscriptions(self):
        if self.youtube is None:
            print("You must log in first.")
            return

        subscriptions: dict = self.youtube.subscriptions().list(
            part='snippet',
            mine=True
        ).execute()

        new_page: str = ""
        sublist = subscriptions

        while True:
            # if subscriptions.get('nextPageToken') in subscriptions != 0:

            subscriptions = self.youtube.subscriptions().list(
                part='snippet',
                mine=True,
                pageToken=new_page
            ).execute()
            new_page = subscriptions.get('nextPageToken')
            if not subscriptions.get('nextPageToken'):
                break
            if 'items' in subscriptions:
                for subscription in subscriptions['items']:
                    print(subscription['snippet']['title'])

            if 'items' in sublist:
                sublist['items'].append(subscriptions['items'])

        with open(self.dump_file, "w", encoding="utf-8") as deep:
            json.dump(sublist, deep)

        self.user_buckets()

    def user_buckets(self):
        try:
            with open(self.dump_file) as fp:
                MyChannelList: dict = json.load(fp)
                self.Buckets = Bucket(MyChannelList)
        except FileExistsError:
            print("Subscription List Does Not Exist. Use get_subscription Method")

    @staticmethod
    def credentials() -> dict:
        """
        return class variable
            type: object
        """
        print(User.__CREDENTIALS)
        return User.__CREDENTIALS
#
# class User:
#     def __init__(self, client_id, redirect_uri):
#         self.client_id = client_id
#         self.redirect_uri = redirect_uri
#         self.access_token = None
#
#     def authenticate(self):
#         auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope=email%20profile'
#         print(f"Please visit the following URL and grant access to continue: {auth_url}")
#         authorization_code = input("Enter the authorization code: ")
#
#         # Exchange authorization code for access token
#         token_url = 'https://accounts.google.com/o/oauth2/token'
#         token_payload = {
#             'code': authorization_code,
#             'client_id': self.client_id,
#             'client_secret': '<YOUR_CLIENT_SECRET>',
#             'redirect_uri': self.redirect_uri,
#             'grant_type': 'authorization_code'
#         }
#         response = requests.post(token_url, data=token_payload)
#         response_json = response.json()
#         self.access_token = response_json['access_token']
#
#     def login(self):
#         if self.access_token:
#             # Perform any necessary login actions using the access token
#             print("Logged in successfully.")
#         else:
#             print("Authentication is required. Please authenticate first using the 'authenticate' method.")
#
# from google.oauth2 import google_auth
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
#
# class User:
#     def __init__(self, client_secrets_path, scopes):
#         self.client_secrets_path = client_secrets_path
#         self.scopes = scopes
#         self.credentials = None
#         self.youtube = None


# # Example usage
# client_secrets_path = 'client_secrets.json'
# scopes = ['https://www.googleapis.com/auth/youtube.readonly']
#
# user = User(client_secrets_path, scopes)
# user.authenticate()
# user.login()
# user.get_subscriptions()
