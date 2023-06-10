#!/usr/bin/python3
class Bucket:
    def __init__(self, UserChannelList: dict = None):
        if UserChannelList is None:
            print("Invalid Channel List")
        else:
            self.UserChannelList = UserChannelList
        self.BucketList = {}

    def create_bucket(self, BucketName: str, createlist: list = None):
        if BucketName is None:
            return "Enter Bucket Name"
        if createlist is None:
            self.BucketList[BucketName] = []
        else:
            self.bucket_update(BucketName, createlist)

    def remove_channel(self, deletelist: list = None):
        if deletelist is None:
            return
        else:
            for item in deletelist:
                for subscription in self.BucketList:
                    if item in subscription['snippet']['title']:
                        del subscription
                        break

    def bucket_update(self, BucketName, UpdateList):
        for subscription in self.UserChannelList['items']:
            if subscription['snippet']['title'] in UpdateList:
                self.BucketList[BucketName].append(subscription)

    @property
    def get_bucket_list(self) -> dict:
        return self.BucketList

    @property
    def get_existing_buckets(self) -> list:
        return list(self.BucketList.keys())

    def get_bucket(self, bucketname) -> dict:
        return self.BucketList[bucketname]
