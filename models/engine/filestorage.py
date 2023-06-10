#!/usr/bin/python3
"""Class to handle storage of jsons"""
import json
from models.user import User
from google.oauth2.credentials import Credentials


class CredentialsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Credentials):
            return obj.to_json()
        return super().default(obj)


class FileStorage:
    """File storage:
    Args:
        location: str"""

    __Cred_File_Location: str = 'Full_Credentials.json'

    def __init__(self, location, userclass=None):
        """Initialization
        """
        assert isinstance(location, str)
        self.location = location

    def set_userclass(self, userclass):
        self.User = userclass

    def all(self):
        """Print all available jsons for all users"""
        credlist: dict = self.User.credentials()
        key: str
        file: list = []
        for key in credlist.keys():
            filename: str = self.location + key + '.' + credlist[key][0] + '.json'
            print(filename)
            with open(filename) as fp:
                file = json.load(fp)
        print(file)

    def savecred(self):
        """save the credentials class variable"""
        Cred = self.User.credentials
        with open(FileStorage.__Cred_File_Location, 'a', encoding='utf-8') as fp:
            json.dump(Cred, fp, cls=CredentialsEncoder)

    @staticmethod
    def loadcred():
        """Load Full_Credentials file"""
        try:
            with open(FileStorage.__Cred_File_Location) as fp:
                read = fp.read()
                if read:
                    return json.load(fp)
                else:
                    return {}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(e)