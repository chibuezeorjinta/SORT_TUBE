#!/usr/bin/python3
from typing import List, Any


class Bucket:
    def __init__(self):
        self.BucketList: dict = dict()

    def update_channel_list(self, UserChannelList: dict = None):
        if UserChannelList is None:
            print("Invalid Channel List")
        else:
            self.UserChannelList = UserChannelList

    def create_bucket(self, BucketName: str, CreateList: list = None):
        if BucketName is None:
            return "Enter Bucket Name"
        if CreateList is None:
            self.BucketList[BucketName] = []
        else:
            self.bucket_update(BucketName, CreateList)

    def remove_channel(self, BucketName: str, DeleteList: list = None):
        if BucketName in self.BucketList.keys():
            for sub in self.BucketList[BucketName]:
                if sub in DeleteList:
                    self.BucketList[BucketName].remove(sub)
                    return True

    def bucket_update(self, BucketName, UpdateList):
        for subscription in self.UserChannelList['items']:
            if subscription in UpdateList:
                self.BucketList[BucketName].append(subscription)

    @property
    def get_bucket_list(self) -> dict:
        return self.BucketList

    @property
    def get_existing_buckets(self) -> bool | list[Any]:
        if self.BucketList.keys() is None:
            return False
        else:
            return list(self.BucketList.keys())

    def get_bucket(self, BucketName) -> dict:
        return self.BucketList[BucketName]
