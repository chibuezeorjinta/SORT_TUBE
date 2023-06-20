#!/usr/bin/python3
"""user class used to login and authenticate youtube account"""
# import requests
# from google.oauth2 import google_auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import json
import os
import uuid
from models.bucket import Bucket


class User:
    CREDENTIALS = {}
    Instances = []

    def __init__(self, username="", secret_path="", scope=[], storage=None):
        """
        :type username: str
        :type secret_path: str
        :type scope: list
        """
        if secret_path == "":
            raise SyntaxError("USAGE=> username : str, secret_path : str, scope : []")
        if type(secret_path) is not str:
            raise TypeError("path is needed")
        else:
            self.client_secrets_path = secret_path
        if type(scope) is not list:
            raise TypeError("scope list is needed")
        if scope is []:
            raise SyntaxError("USAGE=> username : str, secret_path : str, scope : []")
        else:
            self.scopes = scope
        if type(username) is not str:
            raise TypeError("username string is needed")
        if username is None:
            raise SyntaxError("USAGE=> username : str, secret_path : str, scope : []")
        else:
            self.username = username

        self.id: str = ""

        self.storage = storage


        self.credentials: object = None
        self.youtube: build = None

        self.ID_LIST: list = []
        self.Buckets: object = Bucket()
        self.SubscriptionList: dict = {}


    @classmethod
    def get_instance(cls, args: str) -> object:
        for existing in User.Instances:
            if existing.username == args:
                return existing
        return False
        #for args in User.__CREDENTIALS.keys():

    # def append_instance(self):
    #     User.Instances.append(self)

    def set_storage(self, storage):
        self.storage = storage
        User.CREDENTIALS = self.storage.loadcred()

    def authenticate(self):
        if self.credentials is None or not self.credentials.valid:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_path, self.scopes)
            self.credentials = flow.run_local_server(port=5665, open_browser=True)
            if self.credentials is None or not self.credentials.valid:
                return False
            else:
                #self.login()
                self.ID_LIST = [self.id, self.credentials]
                if User.CREDENTIALS is None:
                    User.CREDENTIALS = {}
                if self.username not in User.CREDENTIALS.keys():
                    User.CREDENTIALS[self.username] = self.ID_LIST
                print(User.CREDENTIALS)
                #.self.storage.savecred()

        # else:
        #     self.login()

    def login(self):
        if self.credentials is None:
            print("Authentication is required. Please authenticate first using the 'authenticate' method.")
            return

        self.youtube: build = build('youtube', 'v3', credentials=self.credentials)
        user_info_service = build('oauth2', 'v2', credentials=self.credentials)
        user_info = user_info_service.userinfo().get().execute()
        print(user_info)

        self.username = user_info['name']
        self.UserId = self.username + '.' + self.id
        self.dump_file = "json/" + self.UserId + ".json"
        self.get_subscriptions()
        return True

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

            # if 'items' in subscriptions:
            #     for subscription in subscriptions['items']:
            #         print(subscription['snippet']['title'])

            if 'items' in sublist:
                for sub in subscriptions['items']:
                    sublist['items'].append(sub)

            if not subscriptions.get('nextPageToken'):
                break

        with open(self.dump_file, "w", encoding="utf-8") as deep:
            json.dump(sublist, deep)

        self.SubscriptionList = sublist
        self.get_sublist()

    def user_buckets(self):
        return self.Buckets.get_existing_buckets

    def get_sublist(self) -> list:
        try:
            with open(self.dump_file, "r", encoding="utf-8") as fp:
                self.SubscriptionList: dict = json.load(fp)
            self.Buckets.update_channel_list(self.SubscriptionList)
            # if 'items' in self.SubscriptionList:
            #     newlist = []
            #     for sub in self.SubscriptionList['items']:
            #         newlist.append(sub['snippet']['title'])
            if type(self.SubscriptionList) is dict:
                return self.SubscriptionList
        except FileNotFoundError:
            self.get_subscriptions()

    @staticmethod
    def credentials(cls) -> dict:
        """
        return class variable
            type: object
        """
        print(User.CREDENTIALS)
        return User.CREDENTIALS

    def get_recent_videos(self, channel_id):
        try:
            # Get the current time and the time 24 hours ago
            now = datetime.datetime.now()
            twenty_four_hours_ago = now - datetime.timedelta(hours=24)

            # Make the API request to retrieve the videos
            response = self.youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,  # Adjust the number of results as needed
                publishedAfter=twenty_four_hours_ago.isoformat() + 'Z',  # ISO 8601 format
                type='video'
            ).execute()

            # Extract the video details from the response
            videos = response['items']
            #video_ids = [video['id']['videoId'] for video in videos]

            # Return the list of video IDs
            return videos
        except HttpError as e:
            print('An error occurred:', e)
            return []

    def get_recent_videos_by_channel_name(self, channel_name):
        try:
            # Get the current time and the time 24 hours ago
            now = datetime.datetime.now()
            twenty_four_hours_ago = now - datetime.timedelta(hours=24)

            # Make the API request to retrieve the videos
            response = self.youtube.search().list(
                part='snippet',
                q=channel_name,
                maxResults=50,  # Adjust the number of results as needed
                publishedAfter=twenty_four_hours_ago.isoformat() + 'Z',  # ISO 8601 format
                type='video'
            ).execute()

            # Extract the video details from the response
            videos = response['items']
            video_ids = [video['id']['videoId'] for video in videos]

            # Return the list of video IDs
            return video_ids
        except HttpError as e:
            print('An error occurred:', e)
            return []

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
